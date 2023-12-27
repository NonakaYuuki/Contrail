import numpy as np
import pandas as pd
from  MSM import GetMSMPall
import plotly.graph_objects as go
from CARATS import CARATS
from airport import Airport_list, Qtedist
from ClimCORE import ClimCORE

class Contrail_in_Japan:
    def __init__(self,
                 date_list,
                 hour_list,
                 min_lat,
                 min_lon,
                 max_lat,
                 max_lon):
        self.date_list = date_list
        self.hour_list = []
        self.min_lat = min_lat
        self.min_lon = min_lon
        self.max_lat = max_lat
        self.max_lon = max_lon
        self.min_altitude = 20000
        self.max_altitude = 40000

        #温度
        for hour in hour_list:
            if 0<=hour<=9:
                self.hour_list.append('0{0}'.format(hour))
            else:
                self.hour_list.append(hour)
        self.df_temperature_list = []
        self.df_humidity_list = []
        self.date_hour_list = []
        for date in self.date_list:
            for hour in self.hour_list:
                self.date_hour_list.append(str(date) + str(hour))
                print(str(date) + str(hour))
                rf  =  "./data/MSM/"+'{0}/'.format(date)+ "Z__C_RJTD_{0}{1}0000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin".format(date, hour)
                msm = GetMSMPall(rf, self.min_lat, self.max_lat, self.min_lon, self.max_lon, self.min_altitude, self.max_altitude) 
                self.df_temperature_list.append(msm.MSM_Pall_kelvin_table_create(0))

                #湿度
                self.df_humidity_list.append(msm.MSM_Pall_humidity_table_create(0))
        
        #ClimCORE
        self.ds_temperature_list = []
        self.ds_humidity_list = []
        for date in self.date_list:
            for hour in self.hour_list:
                Climcore = ClimCORE(int(str(date)[:4]),
                                    int(str(date)[4:6]),
                                    int(str(date)[6:]),
                                    int(hour),
                                    [lat/10 for lat in range(self.min_lat*10, self.max_lat*10 + 1, 1)],
                                    [lon/10 for lon in range(self.min_lon*10, self.max_lon*10 + 1, 1)],
                                    [alt for alt in range(self.min_altitude, self.max_altitude, 1000)])
                #温度
                self.ds_temperature = Climcore.Temperature()
                self.ds_temperature_list.append(self.ds_temperature)
                #湿度
                self.ds_humidity = Climcore.RHi()
                self.ds_humidity_list.append(self.ds_humidity)
    
    def RHw_to_RHi(self, RHw, T):
        # ew = 10**(-7.90298 * (Tst/T - 1) + 5.02808 * np.log10(Tst/T) - 1.3816 * 10**(-7) * (10**(11.34 * (1 - T/Tst)) - 1) + 8.1328 * 10**(-3) * (10**(-3.49149 * (Tst/T - 1)) - 1) + np.log10(1013.246))
        ew = np.exp(
            54.842763
            - 6763.22 / T + 273.15
            - 4.210 * np.log(T + 273.15)
            + 0.000367 * T + 273.15
            + np.tanh(0.0415 * (T + 273.15 - 218.8))
            * (
                53.878
                - 1331.22 / T + 273.15
                - 9.44523 * np.log(T + 273.15)
                + 0.014025 * T + 273.15
            )
        )
        ei = np.exp(
            9.550426
            - 5723.265 / T + 273.15
            + 3.53068 * np.log(T + 273.15)
            - 0.00728332 * T + 273.15
        )
        return RHw * ew / ei
    
    def vis_contrail_MSM(self, altitude):
        lat_list = []
        lon_list = []
        for k in range(len(self.df_temperature_list)):
            for lat in [i / 10 for i in range(int(self.min_lat*10),int((self.max_lat)*10+1),1)]:
                for lon in [i / 1000 for i in range(int(self.min_lon*1000),int((self.max_lon)*1000+1),125)]:
                    df_point = self.df_temperature_list[k][(self.df_temperature_list[k]["Lat"] == lat) & (self.df_temperature_list[k]['Lon'] == lon)] 
                    T = float(df_point.at[df_point.index[0],str(altitude)])
                    df_point = self.df_humidity_list[k][(self.df_humidity_list[k]["Lat"] == lat) & (self.df_humidity_list[k]['Lon'] == lon)] 
                    RHw = float(df_point.at[df_point.index[0],str(altitude)])
                    RHi = self.RHw_to_RHi(RHw, T)

                    if T <= 233.15 and RHi >= 100:
                        lat_list.append(lat)
                        lon_list.append(lon)
            # adding the lines joining the nodes
            fig = go.Figure(go.Scattermapbox(
                name = "contrail",
                mode = "markers",
                opacity=0.4,
                lon = lon_list,
                lat = lat_list,
                marker = {'size': 5, 'color':"blue"}))
            
            # getting center for plots:
            lat_center = np.mean((self.max_lat + self.min_lat) / 2)
            long_center = np.mean((self.max_lon + self.min_lon) / 2)
            # defining the layout using mapbox_style
            fig.update_layout(mapbox_style="open-street-map",
                mapbox_center_lat = 30, mapbox_center_lon=-80)
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                            mapbox = {
                                'center': {'lat': lat_center, 
                                'lon': long_center},
                                'zoom': 4})
            print('vis_contrail_MSM', self.date_hour_list[k])
            fig.show()
            # fig.write_image('./result/{0}_{1}h_{2}ft.png'.format(self.date_list, self.hour_list, altitude))
        
    def vis_contrail_CLimCORE(self, altitude):
        for index, (ds_temperature, ds_humidity) in enumerate(zip(self.ds_temperature_list, self.ds_humidity_list)):
            lat_list = []
            lon_list = []
            for lat in [i / 10 for i in range(int(self.min_lat*10),int((self.max_lat)*10+1),1)]:
                for lon in [i / 10 for i in range(int(self.min_lon*10),int((self.max_lon)*10+1),1)]:
                    
                    T = float(ds_temperature.sel(lat = lat,
                                                    lon = lon,
                                                    alt = altitude))
                
                    RHi = float(ds_humidity.sel(lat = lat,
                                                    lon = lon,
                                                    alt = altitude))

                    if T <= 233.15 and RHi >= 100:
                        lat_list.append(lat)
                        lon_list.append(lon)
            # adding the lines joining the nodes
            fig = go.Figure(go.Scattermapbox(
                name = "contrail",
                mode = "markers",
                opacity=0.4,
                lon = lon_list,
                lat = lat_list,
                marker = {'size': 5, 'color':"blue"}))
            
            # getting center for plots:
            lat_center = np.mean((self.max_lat + self.min_lat) / 2)
            long_center = np.mean((self.max_lon + self.min_lon) / 2)
            # defining the layout using mapbox_style
            fig.update_layout(mapbox_style="open-street-map",
                mapbox_center_lat = 30, mapbox_center_lon=-80)
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                            mapbox = {
                                'center': {'lat': lat_center, 
                                'lon': long_center},
                                'zoom': 4})
            print('vis_contrail_ClimCORE', self.date_hour_list[index])
            fig.show()
            # fig.write_image('./result/{0}_{1}h_{2}ft.png'.format(self.date_list, self.hour_list, altitude))
    
    def fix_latlon(self, lat, lon, alt):
        lat_fix = round(lat, 1)
        
        lon_min = np.floor(lon)
        gap_list = []
        for n in range(5):
            gap = abs(lon_min + 0.25 * n - lon)
            gap_list.append(gap)
        lon_fix = lon_min + 0.25 * np.argmin(gap_list)

        quotient = alt // 500
        if alt % 500 >= 250:
            quotient += 1
        alt_fix = int(500 * quotient)

        return lat_fix, lon_fix, alt_fix
    
    def count_flight(self):
        #飛行経路のウェイポイントを直線で繋ぎ合わせたものを作る
        # f = Flightdata(start_time,
        #                end_time,
        #                airport_list)
        # flightdata_list = f.remk_flightdata()

        #それぞれのフライトについて、飛行機雲発生空域とかぶっているかどうかを確かめる。少しでもかぶっていれば、そのフライトをカウントする。
        airport_list = [airport['name'] for airport in Airport_list]
        columns = airport_list
        index = airport_list
        df_all = pd.DataFrame(index=index, columns=columns)
        df_all.fillna(0, inplace=True)
        for num1, date in enumerate(self.date_list):
            df_oneday = pd.DataFrame(index=index, columns=columns)
            df_oneday.fillna(0, inplace=True)
            exclude_flight_number_list = []
            for num2, hour in enumerate(self.hour_list):
                num = num1 * len(self.hour_list) + num2
                #CARATSの飛行経路のウェイポイントを直線で繋ぎ合わせたものを作る(ここはもう少し計算量減らせると思う)
                Carats = CARATS([date], hour, exclude_flight_number_list)
                flightdata_list = Carats.rmk_flight_data()

                df_hour = pd.DataFrame(index=index, columns=columns)
                df_hour.fillna(0, inplace=True)
                num_flight = 0
                for flightdata in flightdata_list:
                    lat_list = flightdata['lat_list']
                    lon_list = flightdata['lon_list']
                    alt_list = flightdata['alt_list']
                    # print(flightdata)
                    departure_airport = flightdata['departure airport']
                    arrival_airport = flightdata['arrival airport']
                    if departure_airport is None:
                        departure_airport = 'None'
                    if arrival_airport is None:
                        arrival_airport = 'None'
                    #df_allについて
                    if departure_airport not in list(df_all.columns.values):
                        df_all[departure_airport] = 0
                    if arrival_airport not in list(df_all.index.values):
                        df_all.loc[arrival_airport] = 0
                    #df_onedayについて
                    if departure_airport not in list(df_oneday.columns.values):
                        df_oneday[departure_airport] = 0
                    if arrival_airport not in list(df_oneday.index.values):
                        df_oneday.loc[arrival_airport] = 0
                    #df_hourについて
                    if departure_airport not in list(df_hour.columns.values):
                        df_hour[departure_airport] = 0
                    if arrival_airport not in list(df_hour.index.values):
                        df_hour.loc[arrival_airport] = 0

                    for lat, lon, alt in zip(lat_list, lon_list, alt_list):
                        if self.min_lat <= lat <= self.max_lat and self.min_lon <= lon <= self.max_lon and self.min_altitude <= alt <= self.max_altitude:
                            lat_fix, lon_fix, alt_fix = self.fix_latlon(lat, lon, alt)
                            df_point = self.df_temperature_list[num][(self.df_temperature_list[num]["Lat"] == lat_fix) & (self.df_temperature_list[num]['Lon'] == lon_fix)] 
                            T = float(df_point.at[df_point.index[0],str(alt_fix)])
                            df_point = self.df_humidity_list[num][(self.df_humidity_list[num]["Lat"] == lat_fix) & (self.df_humidity_list[num]['Lon'] == lon_fix)] 
                            RHw = float(df_point.at[df_point.index[0],str(alt_fix)])
                            Tst = 372.15
                            T0 = 273.15
                            RHi = self.RHw_to_RHi(RHw, T)

                            if T <= 233.15 and RHi >= 100:
                                # print('条件満たす')
                                df_all.loc[arrival_airport, departure_airport] += 1
                                df_oneday.loc[arrival_airport, departure_airport] += 1
                                df_hour.loc[arrival_airport, departure_airport] += 1
                                num_flight += 1
                                exclude_flight_number_list.append(flightdata['flight_number'])
                                break
                print(date,num_flight)
                
                df_hour.to_csv('./result/num_contrail_flight/CARATS_{0}_{1}h.csv'.format(date,hour))
            df_oneday.to_csv('./result/num_contrail_flight/CARATS_{0}_{1}h.csv'.format(date,self.hour_list))
        df_all.to_csv('./result/num_contrail_flight/CARATS_{0}_{1}h.csv'.format(self.date_list, self.hour_list))


if __name__ == '__main__':
    contrail = Contrail_in_Japan([20180701],
                                 [0,3,6,9,12,15,18,21],
                                 26,
                                 127,
                                 47,
                                 147)
    for alt in [38000]:
        # contrail.vis_contrail_MSM(alt)
        contrail.vis_contrail_CLimCORE(alt)