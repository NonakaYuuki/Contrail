'''
Created on 2022/02/03

@author: workstation1
'''


import numpy as np
from scipy import signal, interpolate
import pandas as pd
import binascii
import struct
import pygrib

class GetMSMSurf:

       
    def __init__(self, rf,ido0 ,ido1 ,kdo0 ,kdo1):

        self.rf = rf
        self.lat0 = ido0
        self.lat1 = ido1 
        self.lon0 = kdo0
        self.lon1 = kdo1
        self.lonlists = []
        self.latlists = []
        for lat in  [i / 10000 for i in range(int(self.lat0*10000),(int(self.lat1)*10000+1),500*2)]:
            self.latlists.append('{:.2f}'.format(lat))
        for lon in  [i / 10000 for i in range(int(self.lon0*10000),int((self.lon1)*10000+1),625*2)]:
            self.lonlists.append('{:.4f}'.format(lon))        
        self.latlists.reverse()

    def getMSM_surf_u_wind_table_create(self,tm):

        grbs = pygrib.open(self.rf)
        #print(grbs.select(parameterName='u-component of wind', forecastTime=3))
        prmsl_fc0 = grbs.select(parameterName='u-component of wind', forecastTime=tm)[0]
        values, lats, lons = prmsl_fc0.data(self.lat0, self.lat1+0.05*2, self.lon0, self.lon1)
        self.df = pd.DataFrame(values,index=self.latlists,columns=self.lonlists)      
        grbs.close()

    def getMSM_surf_u_wind(self,wf):
        self.wf = wf
        self.df.to_csv(self.wf)

    def getMSM_surf_v_wind_table_create(self,tm):
      
        grbs = pygrib.open(self.rf)
        prmsl_fc0 = grbs.select(parameterName='v-component of wind', forecastTime=tm)[0]
        values, lats, lons = prmsl_fc0.data(self.lat0, self.lat1+0.05*2, self.lon0, self.lon1)
        self.df= pd.DataFrame(values,index=self.latlists,columns=self.lonlists)
        grbs.close()    

    def getMSM_surf_v_wind(self,wf): 
        self.wf = wf
        self.df.to_csv(self.wf)     
        
    def getMSM_surf_kelvin_table_create(self,tm): 
        grbs = pygrib.open(self.rf)
        prmsl_fc0 = grbs.select(parameterName='Temperature', forecastTime=tm)[0]
        values, lats, lons = prmsl_fc0.data(self.lat0, self.lat1+0.05*2, self.lon0, self.lon1)
        self.df = pd.DataFrame(values,index=self.latlists,columns=self.lonlists)
        grbs.close()

    def getMSM_surf_kelvin(self,wf):     
        self.wf = wf
        self.df.to_csv(self.wf)
       
    
    def pointGetMSM_surf_kelvin(self,ido,kdo): 
          
        # self.df = pd.read_csv(self.wf,index_col=0)        
        t = self.df.at[str('{:.2f}'.format(ido)),str('{:.4f}'.format(kdo))]
        return t
   
   

    def pointGetMSM_surf_v_wind(self,ido,kdo): 
    
        # self.df = pd.read_csv(self.wf,index_col=0)    
        v = self.df.at[str('{:.2f}'.format(ido)),str('{:.4f}'.format(kdo))]
        return v

    def pointGetMSM_surf_u_wind(self,ido,kdo):     
             
        # self.df = pd.read_csv(self.wf,index_col=0)       
        u = self.df.at[str('{:.2f}'.format(ido)),str('{:.4f}'.format(kdo))]
        return u

    ##############class GetMSMSurf          END #######################################################################################################
    ################################################


class GetMSMPall:

       
    def __init__(self, rf,ido0 ,ido1 ,kdo0 ,kdo1,alt0,alt1):

        self.rf = rf
        self.lat0 = ido0
        self.lat1 = ido1 
        self.lon0 = kdo0
        self.lon1 = kdo1
       
        self.alt0= alt0
        self.alt1= alt1
        self.lonlists = []
        self.latlists = []
        self.altlists = []

        for lat in  [i / 10 for i in range(int(self.lat0*10),int((self.lat1)*10+1),1)]:
            self.latlists.append(lat)
        for lon in  [i / 1000 for i in range(int(self.lon0*1000),int((self.lon1)*1000+1),125)]:
            self.lonlists.append(lon)        
        for alt in range(alt0,alt1+1,500):
            self.altlists.append(alt)   
        self.latlists.reverse()

    def MSM_Pall_kelvin_table_create(self,tm):

        grbs = pygrib.open(self.rf)
        rh_1000hPa = grbs.select(parameterName='Temperature', level=1000, forecastTime=tm)[0]
        values1000t, lats, lons = rh_1000hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_925hPa = grbs.select(parameterName='Temperature', level=925, forecastTime=tm)[0]
        values925t, lats, lons = rh_925hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_850hPa = grbs.select(parameterName='Temperature', level=850, forecastTime=tm)[0]
        values850t, lats, lons = rh_850hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_700hPa = grbs.select(parameterName='Temperature', level=700, forecastTime=tm)[0]
        values700t, lats, lons = rh_700hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_600hPa = grbs.select(parameterName='Temperature', level=600, forecastTime=tm)[0]
        values600t, lats, lons = rh_600hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_500hPa = grbs.select(parameterName='Temperature', level=500, forecastTime=tm)[0]
        values500t, lats, lons = rh_500hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_400hPa = grbs.select(parameterName='Temperature', level=400, forecastTime=tm)[0]
        values400t, lats, lons = rh_400hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_300hPa = grbs.select(parameterName='Temperature', level=300, forecastTime=tm)[0]
        values300t, lats, lons = rh_300hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_250hPa = grbs.select(parameterName='Temperature', level=250, forecastTime=tm)[0]
        values250t, lats, lons = rh_250hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_200hPa = grbs.select(parameterName='Temperature', level=200, forecastTime=tm)[0]
        values200t, lats, lons = rh_200hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_150hPa = grbs.select(parameterName='Temperature', level=150, forecastTime=tm)[0]
        values150t, lats, lons = rh_150hPa.data(self.lat0-0.1, self.lat1,self.lon0, self.lon1)
        rh_100hPa = grbs.select(parameterName='Temperature', level=100, forecastTime=tm)[0]
        values100t, lats, lons = rh_100hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)

        self.kelvin = np.concatenate([[values1000t],[values925t],[values850t],[values700t],[values600t],[values500t],[values400t],[values300t],[values250t],[values200t],[values150t],[values100t]], axis=0)
      
    
        rh_1000hPa = grbs.select(parameterName='Geopotential height', level=1000, forecastTime=tm)[0]
        values1000g, lats, lons = rh_1000hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values1000g.fill(4.43308*10**4 * (1 - (1000/1013.25)**0.190263) / 0.3048)
        rh_925hPa = grbs.select(parameterName='Geopotential height', level=925, forecastTime=tm)[0]
        values925g, lats, lons = rh_925hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values925g.fill(4.43308*10**4 * (1 - (925/1013.25)**0.190263) / 0.3048)
        rh_850hPa = grbs.select(parameterName='Geopotential height', level=850, forecastTime=tm)[0]
        values850g, lats, lons = rh_850hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values850g.fill(4.43308*10**4 * (1 - (850/1013.25)**0.190263) / 0.3048)
        rh_700hPa = grbs.select(parameterName='Geopotential height', level=700, forecastTime=tm)[0]
        values700g, lats, lons = rh_700hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values700g.fill(4.43308*10**4 * (1 - (700/1013.25)**0.190263) / 0.3048)
        rh_600hPa = grbs.select(parameterName='Geopotential height', level=600, forecastTime=tm)[0]
        values600g, lats, lons = rh_600hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values600g.fill(4.43308*10**4 * (1 - (600/1013.25)**0.190263) / 0.3048)
        rh_500hPa = grbs.select(parameterName='Geopotential height', level=500, forecastTime=tm)[0]
        values500g, lats, lons = rh_500hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values500g.fill(4.43308*10**4 * (1 - (500/1013.25)**0.190263) / 0.3048)
        rh_400hPa = grbs.select(parameterName='Geopotential height', level=400, forecastTime=tm)[0]
        values400g, lats, lons = rh_400hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values400g.fill(4.43308*10**4 * (1 - (400/1013.25)**0.190263) / 0.3048)
        rh_300hPa = grbs.select(parameterName='Geopotential height', level=300, forecastTime=tm)[0]
        values300g, lats, lons = rh_300hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values300g.fill(4.43308*10**4 * (1 - (300/1013.25)**0.190263) / 0.3048)
        rh_250hPa = grbs.select(parameterName='Geopotential height', level=250, forecastTime=tm)[0]
        values250g, lats, lons = rh_250hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values250g.fill(4.43308*10**4 * (1 - (250/1013.25)**0.190263) / 0.3048)
        rh_200hPa = grbs.select(parameterName='Geopotential height', level=200, forecastTime=tm)[0]
        values200g, lats, lons = rh_200hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values200g.fill(4.43308*10**4 * (1 - (200/1013.25)**0.190263) / 0.3048)
        rh_150hPa = grbs.select(parameterName='Geopotential height', level=150, forecastTime=tm)[0]
        values150g, lats, lons = rh_150hPa.data(self.lat0-0.1, self.lat1, self.lon0,self. lon1)
        values150g.fill(4.43308*10**4 * (1 - (150/1013.25)**0.190263) / 0.3048)
        rh_100hPa = grbs.select(parameterName='Geopotential height', level=100, forecastTime=tm)[0]
        values100g, lats, lons = rh_100hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values100g.fill(4.43308*10**4 * (1 - (100/1013.25)**0.190263) / 0.3048)


        self.Geopotential = np.concatenate([[values1000g],[values925g],[values850g],[values700g],[values600g],[values500g],[values400g],[values300g],[values250g],[values200t],[values150g],[values100g]], axis=0)
        
        self.table  = []   
        self.colname = ['Lat','Lon']
        for h in range(self.alt0,self.alt1+ 1,500):  
            self.colname.append(str(h))        
        for i in range(0,self.kelvin.shape[1]):
            for k in range(0,self.kelvin.shape[2]):
             
                row = []
                row.append(self.latlists[i])
                row.append(self.lonlists[k])
                for h in  self.altlists:
                    t = hokan_kelvin(self,h, i, k)
                    row.append("{0:10.6f}".format(t))
                self.table.append(row)
        self.df = pd.DataFrame(self.table,columns =  self.colname)
        grbs.close()
        return self.df

    def MSM_Pall_windtable_create(self,tm):
        grbs = pygrib.open(self.rf)
        rh_1000hPa = grbs.select(parameterName='u-component of wind', level=1000, forecastTime=tm)[0]
        values1000, lats, lons = rh_1000hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_925hPa = grbs.select(parameterName='u-component of wind', level=925, forecastTime=tm)[0]
        values925, lats, lons = rh_925hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_850hPa = grbs.select(parameterName='u-component of wind', level=850, forecastTime=tm)[0]
        values850, lats, lons = rh_850hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_700hPa = grbs.select(parameterName='u-component of wind', level=700, forecastTime=tm)[0]
        values700, lats, lons = rh_700hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_600hPa = grbs.select(parameterName='u-component of wind', level=600, forecastTime=tm)[0]
        values600, lats, lons = rh_600hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_500hPa = grbs.select(parameterName='u-component of wind', level=500, forecastTime=tm)[0]
        values500, lats, lons = rh_500hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_400hPa = grbs.select(parameterName='u-component of wind', level=400, forecastTime=tm)[0]
        values400, lats, lons = rh_400hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_300hPa = grbs.select(parameterName='u-component of wind', level=300, forecastTime=tm)[0]
        values300, lats, lons = rh_300hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_250hPa = grbs.select(parameterName='u-component of wind',level=250, forecastTime=tm)[0]
        values250, lats, lons = rh_250hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_200hPa = grbs.select(parameterName='u-component of wind', level=200, forecastTime=tm)[0]
        values200, lats, lons = rh_200hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_150hPa = grbs.select(parameterName='u-component of wind', level=150, forecastTime=tm)[0]
        values150, lats, lons = rh_150hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_100hPa = grbs.select(parameterName='u-component of wind', level=100, forecastTime=tm)[0]
        values100, lats, lons = rh_100hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)

        self.wind0 = np.concatenate([[values1000],[values925],[values850],[values700],[values600],[values500],[values400],[values300],[values250],[values200],[values150],[values100]], axis=0)
        
        rh_1000hPa = grbs.select(parameterName='v-component of wind', level=1000, forecastTime=tm)[0]
        values1000, lats, lons = rh_1000hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_925hPa = grbs.select(parameterName='v-component of wind', level=925, forecastTime=tm)[0]
        values925, lats, lons = rh_925hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_850hPa = grbs.select(parameterName='v-component of wind', level=850, forecastTime=tm)[0]
        values850, lats, lons = rh_850hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_700hPa = grbs.select(parameterName='v-component of wind', level=700, forecastTime=tm)[0]
        values700, lats, lons = rh_700hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_600hPa = grbs.select(parameterName='v-component of wind', level=600, forecastTime=tm)[0]
        values600, lats, lons = rh_600hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_500hPa = grbs.select(parameterName='v-component of wind', level=500, forecastTime=tm)[0]
        values500, lats, lons = rh_500hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_400hPa = grbs.select(parameterName='v-component of wind', level=400, forecastTime=tm)[0]
        values400, lats, lons = rh_400hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_300hPa = grbs.select(parameterName='v-component of wind', level=300, forecastTime=tm)[0]
        values300, lats, lons = rh_300hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_250hPa = grbs.select(parameterName='v-component of wind', level=250, forecastTime=tm)[0]
        values250, lats, lons = rh_250hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_200hPa = grbs.select(parameterName='v-component of wind', level=200, forecastTime=tm)[0]
        values200, lats, lons = rh_200hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_150hPa = grbs.select(parameterName='v-component of wind', level=150, forecastTime=tm)[0]
        values150, lats, lons = rh_150hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_100hPa = grbs.select(parameterName='v-component of wind', level=100, forecastTime=tm)[0]
        values100, lats, lons = rh_100hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)

        self.wind1 = np.concatenate([[values1000],[values925],[values850],[values700],[values600],[values500],[values400],[values300],[values250],[values200],[values150],[values100]], axis=0)
       
    
        rh_1000hPa = grbs.select(parameterName='Geopotential height', level=1000, forecastTime=tm)[0]
        values1000g, lats, lons = rh_1000hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_925hPa = grbs.select(parameterName='Geopotential height', level=925, forecastTime=tm)[0]
        values925g, lats, lons = rh_925hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_850hPa = grbs.select(parameterName='Geopotential height', level=850, forecastTime=tm)[0]
        values850g, lats, lons = rh_850hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_700hPa = grbs.select(parameterName='Geopotential height', level=700, forecastTime=tm)[0]
        values700g, lats, lons = rh_700hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_600hPa = grbs.select(parameterName='Geopotential height', level=600, forecastTime=tm)[0]
        values600g, lats, lons = rh_600hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_500hPa = grbs.select(parameterName='Geopotential height', level=500, forecastTime=tm)[0]
        values500g, lats, lons = rh_500hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_400hPa = grbs.select(parameterName='Geopotential height', level=400, forecastTime=tm)[0]
        values400g, lats, lons = rh_400hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_300hPa = grbs.select(parameterName='Geopotential height', level=300, forecastTime=tm)[0]
        values300g, lats, lons = rh_300hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_250hPa = grbs.select(parameterName='Geopotential height', level=250, forecastTime=tm)[0]
        values250g, lats, lons = rh_250hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_200hPa = grbs.select(parameterName='Geopotential height', level=200, forecastTime=tm)[0]
        values200g, lats, lons = rh_200hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_150hPa = grbs.select(parameterName='Geopotential height', level=150, forecastTime=tm)[0]
        values150g, lats, lons = rh_150hPa.data(self.lat0-0.1, self.lat1, self.lon0,self. lon1)
        rh_100hPa = grbs.select(parameterName='Geopotential height', level=100, forecastTime=tm)[0]
        values100g, lats, lons = rh_100hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)


        self.Geopotential = np.concatenate([[values1000g],[values925g],[values850g],[values700g],[values600g],[values500g],[values400g],[values300g],[values250g],[values200g],[values150g],[values100g]], axis=0)
       
        self.table  = []   
        self.colname = ['Lat','Lon']
        for h in range(self.alt0,self.alt1+ 1,500):  
            self.colname.append(str(h) + "u")  
            self.colname.append(str(h) + "v")  
             
        for i in range(0,self.wind0.shape[1]):
            for k in range(0,self.wind0.shape[2]):
                row = []
                row.append(self.latlists[i])
                row.append(self.lonlists[k])
                for h in  self.altlists:
                    u,v = hokan_wind(self,h, i, k)
                    row.append("{0:10.6f}".format(u))
                    row.append("{0:10.6f}".format(v))
                self.table.append(row)
                  
        self.df = pd.DataFrame(self.table,columns =  self.colname)
        grbs.close()

    def MSM_Pall_humidity_table_create(self,tm):

        grbs = pygrib.open(self.rf)
        rh_1000hPa = grbs.select(parameterName='Relative humidity', level=1000, forecastTime=tm)[0]
        values1000t, lats, lons = rh_1000hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_925hPa = grbs.select(parameterName='Relative humidity', level=925, forecastTime=tm)[0]
        values925t, lats, lons = rh_925hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_850hPa = grbs.select(parameterName='Relative humidity', level=850, forecastTime=tm)[0]
        values850t, lats, lons = rh_850hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_700hPa = grbs.select(parameterName='Relative humidity', level=700, forecastTime=tm)[0]
        values700t, lats, lons = rh_700hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_600hPa = grbs.select(parameterName='Relative humidity', level=600, forecastTime=tm)[0]
        values600t, lats, lons = rh_600hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_500hPa = grbs.select(parameterName='Relative humidity', level=500, forecastTime=tm)[0]
        values500t, lats, lons = rh_500hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_400hPa = grbs.select(parameterName='Relative humidity', level=400, forecastTime=tm)[0]
        values400t, lats, lons = rh_400hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        rh_300hPa = grbs.select(parameterName='Relative humidity', level=300, forecastTime=tm)[0]
        values300t, lats, lons = rh_300hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)

        self.humidity = np.concatenate([[values1000t],[values925t],[values850t],[values700t],[values600t],[values500t],[values400t],[values300t]], axis=0)
      
    
        rh_1000hPa = grbs.select(parameterName='Geopotential height', level=1000, forecastTime=tm)[0]
        values1000g, lats, lons = rh_1000hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values1000g.fill(4.43308*10**4 * (1 - (1000/1013.25)**0.190263) / 0.3048)
        rh_925hPa = grbs.select(parameterName='Geopotential height', level=925, forecastTime=tm)[0]
        values925g, lats, lons = rh_925hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values925g.fill(4.43308*10**4 * (1 - (925/1013.25)**0.190263) / 0.3048)
        rh_850hPa = grbs.select(parameterName='Geopotential height', level=850, forecastTime=tm)[0]
        values850g, lats, lons = rh_850hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values850g.fill(4.43308*10**4 * (1 - (850/1013.25)**0.190263) / 0.3048)
        rh_700hPa = grbs.select(parameterName='Geopotential height', level=700, forecastTime=tm)[0]
        values700g, lats, lons = rh_700hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values700g.fill(4.43308*10**4 * (1 - (700/1013.25)**0.190263) / 0.3048)
        rh_600hPa = grbs.select(parameterName='Geopotential height', level=600, forecastTime=tm)[0]
        values600g, lats, lons = rh_600hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values600g.fill(4.43308*10**4 * (1 - (600/1013.25)**0.190263) / 0.3048)
        rh_500hPa = grbs.select(parameterName='Geopotential height', level=500, forecastTime=tm)[0]
        values500g, lats, lons = rh_500hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values500g.fill(4.43308*10**4 * (1 - (500/1013.25)**0.190263) / 0.3048)
        rh_400hPa = grbs.select(parameterName='Geopotential height', level=400, forecastTime=tm)[0]
        values400g, lats, lons = rh_400hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values400g.fill(4.43308*10**4 * (1 - (400/1013.25)**0.190263) / 0.3048)
        rh_300hPa = grbs.select(parameterName='Geopotential height', level=300, forecastTime=tm)[0]
        values300g, lats, lons = rh_300hPa.data(self.lat0-0.1, self.lat1, self.lon0, self.lon1)
        values300g.fill(4.43308*10**4 * (1 - (300/1013.25)**0.190263) / 0.3048)


        self.Geopotential = np.concatenate([[values1000g],[values925g],[values850g],[values700g],[values600g],[values500g],[values400g],[values300g]], axis=0)
        
        self.table  = []   
        self.colname = ['Lat','Lon']
        for h in range(self.alt0,self.alt1+ 1,500):  
            self.colname.append(str(h))        
        for i in range(0,self.humidity.shape[1]):
            for k in range(0,self.humidity.shape[2]):
             
                row = []
                row.append(self.latlists[i])
                row.append(self.lonlists[k])
                for h in  self.altlists:
                    t = hokan_humidity(self,h, i, k)
                    row.append("{0:10.6f}".format(t))
                self.table.append(row)
        self.df = pd.DataFrame(self.table,columns =  self.colname)
        grbs.close()
        return self.df


    def getMSM_Pall_wind(self,wf):
      
        self.wf = wf
        self.df.to_csv(self.wf,index=None)  
  
  
    def  getMSM_Pall_kelvin(self,wf):

        self.wf = wf 
        self.df.to_csv(self.wf,index=None)  
 
    def pointGetMSM_Pall_kelvin(self,ido,kdo,alt): 
             
        df_point = self.df[(self.df["Lat"] == ido) & (self.df['Lon'] == kdo)] 
        t = df_point.at[df_point.index[0],str(alt)]
        return t
      
    def pointGetMSM_Pall_wind(self,ido,kdo,alt): 
      
        df_point = self.df[(self.df["Lat"] == ido) & (self.df['Lon'] == kdo)]    
        u = df_point.at[df_point.index[0],str(alt) + "u"]
        v = df_point.at[df_point.index[0],str(alt) + "v"]
        return u,v
    
    def pointGetMSM_Pall_humidity(self,ido,kdo,alt): 
             
        df_point = self.df[(self.df["Lat"] == ido) & (self.df['Lon'] == kdo)] 
        t = df_point.at[df_point.index[0],str(alt)]
        return t

  ################################################



def hokan_kelvin(self,alt,i,k):

    hgt = float(alt)
    
    for h in range(0,13):
     
        if hgt < self.Geopotential[h,i,k]:
            break
    if h == 13:
        print("Error in hokan()")
        exit
    else:

        hgt = np.float32(hgt)        
        t0 = self.kelvin[h-1,i,k] #np.float64
        t1 = self.kelvin[h,i,k] #np.float64       
        t0 = np.float32(t0)
        t1 = np.float32(t1)
    
        h0 = self.Geopotential[h-1,i,k] #np.float64
        h1 = self.Geopotential[h,i,k] #np.float64
        h0 = np.float32(h0) #np.float32
        h1 = np.float32(h1) #np.float32
     
    
        a  = (hgt - h0) / (h1 - h0) 
        a = np.float32(a)

        t  = t0 + (t1 - t0) * a
    

    return t   

def hokan_wind(self,alt,i,k):
  
    hgt = float(alt) * 0.3048
 
    for h in range(0,13):
        if hgt < self.Geopotential[h,i,k]:
            break
    if h == 13:
        print("Error in hokan()")
        exit
    else:
        hgt = np.float32(hgt)          
        u0 = self.wind0[h-1,i,k] #np.float64
        u1 = self.wind0[h,i,k] #np.float64       
        u0 = np.float32(u0)
        u1 = np.float32(u1)
        v0 = self.wind1[h-1,i,k] #np.float64
        v1 = self.wind1[h,i,k] #np.float64       
        v0 = np.float32(v0) #np.float32
        v1 = np.float32(v1) #np.float32       
        h0 = self.Geopotential[h-1,i,k] #np.float64
        h1 = self.Geopotential[h,i,k] #np.float64
        h0 = np.float32(h0) #np.float32
        h1 = np.float32(h1) #np.float32          
        a  = (hgt - h0) / (h1 - h0) 
        a = np.float32(a)
        u  = u0 + (u1 - u0) * a
        v  = v0 + (v1 - v0) * a

    return u,v             

def hokan_humidity(self,alt,i,k):

    hgt = float(alt)
    
    for h in range(0,8):
     
        if hgt < self.Geopotential[h,i,k]:
            break
    if h == 7:
        # print("Over the alititude existed in the data",self.Geopotential[h,i,k])      
        t1 = self.humidity[h,i,k] #np.float64       
        t1 = np.float32(t1)
        t  = t1

    else:
        hgt = np.float32(hgt)        
        t0 = self.humidity[h-1,i,k] #np.float64
        t1 = self.humidity[h,i,k] #np.float64       
        t0 = np.float32(t0)
        t1 = np.float32(t1)

        h0 = self.Geopotential[h-1,i,k] #np.float64
        h1 = self.Geopotential[h,i,k] #np.float64
        h0 = np.float32(h0) #np.float32
        h1 = np.float32(h1) #np.float32
        

        a  = (hgt - h0) / (h1 - h0) 
        a = np.float32(a)

        t  = t0 + (t1 - t0) * a
    

    return t 