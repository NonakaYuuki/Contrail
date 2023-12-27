from typing import List
import numpy as np
import xarray as xr
import xesmf as xe
from scipy import interpolate


class ClimCORE:
    def __init__(self,
                year: int,
                month: int,
                day: int,
                hour: int,
                lat_list: List[float],
                lon_list: List[float],
                alt_list: List[float]
                ):
        if month < 10:
            month = f'0{month}'
        if day < 10:
            day = f'0{day}'
        if hour < 10:
            hour = f'0{hour}00'
        else:
            hour = f'{hour}00'
        self.date = str(year) + str(month) + str(day) + str(hour)
        self.lat_list: List[float] = sorted(lat_list)
        self.lon_list: List[float] = sorted(lon_list)
        self.alt_list: List[float] = sorted([alt for alt in alt_list])
        self.alt_list_orig: List[float] = sorted(alt_list)

        # モデル格子の緯度、経度、地面高度の読み込み
        ds_lat = xr.open_dataset('./data/ClimCORE/const/FLAT.nc')
        ds_lon = xr.open_dataset('./data/ClimCORE/const/FLON.nc')
        ds_z = xr.open_dataset('./data/ClimCORE/const/ZS.nc')
        flat = ds_lat['FLAT'] # 緯度     [degN]
        flon = ds_lon['FLON'] # 経度     [degE]
        zs  = ds_z['ZS']   # 地面高度 [m]

        # モデル面(フルレベル)高度に関する定数の読み込み
        #  [モデル面高度 = zz + ff * 地面高度]
        f = open('./data/ClimCORE/const/model_height.full_level.txt')
        lines = f.readlines()
        zz,ff = [], []
        for l in lines[3:]:
            data = l.split()
            zz.append(float(data[1]))
            ff.append(float(data[2]))

        # Regrid用dataset(入力モデル格子)
        ds_in = xr.Dataset(coords = dict(lon = (["x","y"], flon.data),
                                         lat = (["x","y"], flat.data)))

        # Regrid用dataset(抽出する緯度経度)
        self.size = (len(self.lat_list), len(self.lon_list))
        ds_out = xr.Dataset(coords = dict(lon = (["x","y"], np.tile(self.lon_list, len(self.lat_list)).reshape(self.size)),
                                          lat = (["x","y"], np.repeat(self.lat_list, len(self.lon_list)).reshape(self.size))))
        # print(np.tile(self.lon_list, len(self.lat_list)).reshape(self.size))
        # print(np.repeat(self.lat_list, len(self.lon_list)).reshape(self.size))

        # 水平補間
        self.regridder = xe.Regridder(ds_in, ds_out, "bilinear")
        # zs_regrid = self.regridder(zs.data)

        # 鉛直補間
        # self.alt_matrix = []
        # for i in range(self.size[0]):
        #     alt_row = []
        #     for j in range(self.size[1]):
        #         alt = [zz_ + ff_ * zs_regrid[i][j] for zz_, ff_ in zip(zz, ff)] # モデル面高度 [m] (海抜)
        #         alt_row.append(alt)
        #     self.alt_matrix.append(alt_row)
        
        #気圧高度への変換（feet）
        ds = xr.open_dataset('./data/ClimCORE/fcst_mdl.Ges/P/{0}/P.{1}.nc'.format(self.date[:-6], self.date))
        ds_pressure_alt = 4.43308*10**4 * (1 - (ds/1013.25)**0.190263) / 0.3048
        pressure_alt_regrid = self.regridder(ds_pressure_alt['P'].data)
        self.alt_matrix = []
        for i in range(self.size[0]):
            alt_row = []
            for j in range(self.size[1]):
                alt = pressure_alt_regrid[0][:,i,j] 
                alt_row.append(alt)
                # print(alt)
            self.alt_matrix.append(alt_row)
        # print(self.alt_matrix)
    
    def Pressure(self):
        # モデル面物理量
        ds = xr.open_dataset('./data/ClimCORE/fcst_mdl.Ges/P/{0}/P.{1}.nc'.format(self.date[:-6], self.date))
        # print(ds['P'].data[0][0][0])
        P_regrid = self.regridder(ds['P'].data)

        data_array = []
        for i in range(self.size[0]):
            data_list_by_changing_lon = []
            for j in range(self.size[1]):
                data_list_by_changing_alt = []
                z = self.alt_matrix[self.size[0] - i - 1][j]
                P = P_regrid[0][:,self.size[0] - i - 1,j]
                fit = interpolate.interp1d(z, P, kind='cubic') # 3次スプラインフィッティング
                for alt in self.alt_list:
                    data_out = fit(alt) # 抽出データ
                    data_list_by_changing_alt.append(data_out)
                data_list_by_changing_lon.append(data_list_by_changing_alt)
            data_array.append(data_list_by_changing_lon)
        result = xr.DataArray(data_array, coords={"lat" : sorted(self.lat_list, reverse=True),
                                                  "lon" : self.lon_list,
                                                  "alt" : self.alt_list_orig})
        return result
    
    def convert_Q_to_RHw(self, Q, P, T):
        eps = 0.622
        T0 = 273.15
        ew = 6.1094 * np.e**(17.625 * (T - T0)/(273.71 + T - T0))
        e = P / eps * 1 / (1/Q + (1-eps)/eps)
        RHw = e / ew
        return RHw
    
    def convert_RHw_to_RHi(self, RHw, T):
        T0 = 273.15
        ew = 6.1094 * np.e**(17.625 * (T - T0)/(273.71 + T - T0))
        ei = 6.1128 * np.e**(22.571 * (T - T0)/(273.71 + T - T0)) 
        return RHw * ew / ei
    
    def RHw(self):
        # モデル面物理量
        ds_QVa = xr.open_dataset('./data/ClimCORE/fcst_mdl.Ges/QVa/{0}/QVa.{1}.nc'.format(self.date[:-6], self.date))
        ds_P = xr.open_dataset('./data/ClimCORE/fcst_mdl.Ges/P/{0}/P.{1}.nc'.format(self.date[:-6], self.date))
        ds_T = xr.open_dataset('./data/ClimCORE/fcst_mdl.Ges/T/{0}/T.{1}.nc'.format(self.date[:-6], self.date))
        QVa_regrid = self.regridder(ds_QVa['QVa'].data)
        P_regrid = self.regridder(ds_P['P'].data)
        T_regrid = self.regridder(ds_T['T'].data)

        data_array = []
        for i in range(self.size[0]):
            data_list_by_changing_lon = []
            for j in range(self.size[1]):
                data_list_by_changing_alt = []
                z = self.alt_matrix[self.size[0] - i - 1][j]
                QVa = QVa_regrid[0][:,self.size[0] - i - 1,j]
                P = P_regrid[0][:,self.size[0] - i - 1,j]
                T = T_regrid[0][:,self.size[0] - i - 1,j]
                fit_QVa = interpolate.interp1d(z, QVa, kind='cubic') # 3次スプラインフィッティング
                fit_P = interpolate.interp1d(z, P, kind='cubic') # 3次スプラインフィッティング
                fit_T = interpolate.interp1d(z, T, kind='cubic') # 3次スプラインフィッティング
                for alt in self.alt_list:
                    data_out_QVa = fit_QVa(alt) # 抽出データ
                    data_out_P = fit_P(alt) # 抽出データ
                    data_out_T = fit_T(alt) # 抽出データ
                    data_out = self.convert_Q_to_RHw(data_out_QVa, data_out_P, data_out_T)
                    data_list_by_changing_alt.append(data_out * 100)
                data_list_by_changing_lon.append(data_list_by_changing_alt)
            data_array.append(data_list_by_changing_lon)
        result = xr.DataArray(data_array, coords={"lat" : sorted(self.lat_list, reverse=True),
                                                  "lon" : self.lon_list,
                                                  "alt" : self.alt_list_orig})
        return result
    
    def RHi(self):
        # モデル面物理量
        ds_QVa = xr.open_dataset('./data/ClimCORE/fcst_mdl.Ges/QVa/{0}/QVa.{1}.nc'.format(self.date[:-6], self.date))
        ds_P = xr.open_dataset('./data/ClimCORE/fcst_mdl.Ges/P/{0}/P.{1}.nc'.format(self.date[:-6], self.date))
        ds_T = xr.open_dataset('./data/ClimCORE/fcst_mdl.Ges/T/{0}/T.{1}.nc'.format(self.date[:-6], self.date))
        QVa_regrid = self.regridder(ds_QVa['QVa'].data)
        P_regrid = self.regridder(ds_P['P'].data)
        T_regrid = self.regridder(ds_T['T'].data)

        data_array = []
        for i in range(self.size[0]):
            data_list_by_changing_lon = []
            for j in range(self.size[1]):
                data_list_by_changing_alt = []
                z = self.alt_matrix[self.size[0] - i - 1][j]
                QVa = QVa_regrid[0][:,self.size[0] - i - 1,j]
                P = P_regrid[0][:,self.size[0] - i - 1,j]
                T = T_regrid[0][:,self.size[0] - i - 1,j]
                fit_QVa = interpolate.interp1d(z, QVa, kind='cubic') # 3次スプラインフィッティング
                fit_P = interpolate.interp1d(z, P, kind='cubic') # 3次スプラインフィッティング
                fit_T = interpolate.interp1d(z, T, kind='cubic') # 3次スプラインフィッティング
                for alt in self.alt_list:
                    data_out_QVa = fit_QVa(alt) # 抽出データ
                    data_out_P = fit_P(alt) # 抽出データ
                    data_out_T = fit_T(alt) # 抽出データ
                    data_out_RHw = self.convert_Q_to_RHw(data_out_QVa, data_out_P, data_out_T)
                    data_out = self.convert_RHw_to_RHi(data_out_RHw, data_out_T)
                    data_list_by_changing_alt.append(data_out * 100)
                data_list_by_changing_lon.append(data_list_by_changing_alt)
            data_array.append(data_list_by_changing_lon)
        result = xr.DataArray(data_array, coords={"lat" : sorted(self.lat_list, reverse=True),
                                                  "lon" : self.lon_list,
                                                  "alt" : self.alt_list_orig})
        return result
    
    def Temperature(self):
        # モデル面物理量
        ds = xr.open_dataset('./data/ClimCORE/fcst_mdl.Ges/T/{0}/T.{1}.nc'.format(self.date[:-6], self.date))
        T_regrid = self.regridder(ds['T'].data)

        data_array = []
        for i in range(self.size[0]):
            data_list_by_changing_lon = []
            for j in range(self.size[1]):
                data_list_by_changing_alt = []
                z = self.alt_matrix[self.size[0] - i - 1][j]
                T = T_regrid[0][:,self.size[0] - i - 1,j]
                fit = interpolate.interp1d(z, T, kind='cubic') # 3次スプラインフィッティング
                for alt in self.alt_list:
                    data_out = fit(alt) # 抽出データ
                    data_list_by_changing_alt.append(data_out)
                data_list_by_changing_lon.append(data_list_by_changing_alt)
            data_array.append(data_list_by_changing_lon)
        result = xr.DataArray(data_array, coords={"lat" : sorted(self.lat_list, reverse=True),
                                                  "lon" : self.lon_list,
                                                  "alt" : self.alt_list_orig})
        return result
    
    def U_Wind(self):
        # モデル面物理量
        ds = xr.open_dataset('./data/ClimCORE/fcst_mdl.Ges/UMET/{0}/UMET.{1}.nc'.format(self.date[:-6], self.date))
        UMET_regrid = self.regridder(ds['UMET'].data)

        data_array = []
        for i in range(self.size[0]):
            data_list_by_changing_lon = []
            for j in range(self.size[1]):
                data_list_by_changing_alt = []
                z = self.alt_matrix[self.size[0] - i - 1][j]
                UMET = UMET_regrid[0][:,self.size[0] - i - 1,j]
                fit = interpolate.interp1d(z, UMET, kind='cubic') # 3次スプラインフィッティング
                for alt in self.alt_list:
                    data_out = fit(alt) # 抽出データ
                    data_list_by_changing_alt.append(data_out)
                data_list_by_changing_lon.append(data_list_by_changing_alt)
            data_array.append(data_list_by_changing_lon)
        result = xr.DataArray(data_array, coords={"lat" : sorted(self.lat_list, reverse=True),
                                                  "lon" : self.lon_list,
                                                  "alt" : self.alt_list_orig})
        return result
    
    def V_Wind(self):
        # モデル面物理量
        ds = xr.open_dataset('./data/ClimCORE/fcst_mdl.Ges/VMET/{0}/VMET.{1}.nc'.format(self.date[:-6], self.date))
        VMET_regrid = self.regridder(ds['VMET'].data)

        data_array = []
        for i in range(self.size[0]):
            data_list_by_changing_lon = []
            for j in range(self.size[1]):
                data_list_by_changing_alt = []
                z = self.alt_matrix[self.size[0] - i - 1][j]
                VMET = VMET_regrid[0][:,self.size[0] - i - 1,j]
                fit = interpolate.interp1d(z, VMET, kind='cubic') # 3次スプラインフィッティング
                for alt in self.alt_list:
                    data_out = fit(alt) # 抽出データ
                    data_list_by_changing_alt.append(data_out)
                data_list_by_changing_lon.append(data_list_by_changing_alt)
            data_array.append(data_list_by_changing_lon)
        result = xr.DataArray(data_array, coords={"lat" : sorted(self.lat_list, reverse=True),
                                                  "lon" : self.lon_list,
                                                  "alt" : self.alt_list_orig})
        return result

if __name__ == '__main__':
    clim = ClimCORE(2018,
                    7,
                    1,
                    0,
                    [25,40],
                    [130,135,140,145],
                    [100,30000])
    print(clim.RHi().data)