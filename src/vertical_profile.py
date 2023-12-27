import numpy as np
import matplotlib.pyplot as plt
from  MSM import GetMSMPall

def RHw_to_RHi(RHw, T, T0):
        ew = 6.1094 * np.e**(17.625 * (T - T0)/(273.71 + T - T0))
        ei = 6.1128 * np.e**(22.571 * (T - T0)/(273.71 + T - T0)) 
        return RHw * ew / ei

def vis_profile(date, hour, lat, lon):
    if 0<=hour<=9:
        hour='0{0}'.format(hour)
    rf  =  "./data/"+'{0}/'.format(date)+ "Z__C_RJTD_{0}{1}0000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin".format(date,hour)
    msm = GetMSMPall(rf, lat, lat, lon, lon, 0, 30000) 
    df_temperature_list = []
    df_humidity_list = []
    T_list = []
    H_list = []
    alt_list = []
    for alt in range(0, 35000, 5000):
        #温度
        df_temperature_list.append(msm.MSM_Pall_kelvin_table_create(0))
        df_point = df_temperature_list[0][(df_temperature_list[0]["Lat"] == lat) & (df_temperature_list[0]['Lon'] == lon)] 
        T = float(df_point.at[df_point.index[0],str(alt)])

        #湿度
        df_humidity_list.append(msm.MSM_Pall_humidity_table_create(0))
        df_point = df_humidity_list[0][(df_humidity_list[0]["Lat"] == lat) & (df_humidity_list[0]['Lon'] == lon)] 
        RHw = float(df_point.at[df_point.index[0],str(alt)])
        T0 = 273.15
        RHi = RHw_to_RHi(RHw, T, T0)

        T_list.append(T-273.15)
        H_list.append(RHi)
        alt_list.append(alt)

    fig, axes = plt.subplots(nrows=1, ncols=2)
    plt.subplots_adjust(hspace=0.4, left=0.1, right=0.95)
    axes[0].plot(T_list, alt_list, linewidth=3, color='dodgerblue')
    axes[0].axvline(x=-40, color='red')
    axes[0].set_xlabel('Temperature (°C)', fontsize=20, fontweight='bold')
    axes[0].set_ylabel('Altitude (ft)', fontsize=20, fontweight='bold')
    axes[0].grid(which = "both", axis = "y", color = "black", alpha = 0.8, linestyle = "--", linewidth = 1)
    axes[0].tick_params(axis='x', labelsize=20)
    axes[0].tick_params(axis='y', labelsize=20)
    axes[1].plot(H_list, alt_list, linewidth=3, color='dodgerblue')
    axes[1].axvline(x=100, color='red')
    axes[1].set_xlabel('RHi (%)', fontsize=20, fontweight='bold')
    axes[1].grid(which = "both", axis = "y", color = "black", alpha = 0.8, linestyle = "--", linewidth = 1)
    axes[1].tick_params(axis='x', labelsize=20)
    axes[1].tick_params(axis='y', labelsize=20)
    plt.show()

for date in [20220101, 20220201, 20220301, 20220401, 20220501, 20220601, 20220701, 20220801, 20220901, 20221001, 20221101, 20221201]:
    for hh in [3,6,9,12,15,18,21]:
        vis_profile(date, hh, 42.7, 141.5)