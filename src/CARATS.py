import plotly.graph_objects as go
import pandas as pd
import glob
from airport import Airport_list, Qtedist
import numpy as np

class CARATS:
    def __init__(self,
                 date_list,
                 hour,
                 exclude_flight_number_list):
        self.date_list = date_list
        self.hour = int(hour)

        #[{'icao24' : ..., 'departure time' : ..., 'departure airport' : ..., 'arrival airport' : ..., 'lat_list' : [], 'lon_list' : [], 'alt_list' : []}, {}, {}]を作る。flightdataと{}は一対一対応
        self.flight_data_list = []
        for date in self.date_list:
            year = str(date)[:4]
            month = str(date)[4:6]
            day = str(date)[6:]
            flight_data_list_in_a_month = []
            flight_number_list = []
            path = f'/Users/nonakayuuki/university/masters_thesis/CARATS_Open_Data{str(date)[:4] - 1}/{year + month}'
            files = glob.glob(path + f'/*{str(date)}*')
            if files == []:
                raise ValueError('NO CARATS OPEN DATA')
            for file in files:
                df = pd.read_csv(file)
                for index, row in df.iterrows():
                    if row[1] in exclude_flight_number_list:
                        continue
                    if row[1] not in flight_number_list:
                        data = {}
                        data['all_alt_list'] = [row[4]]
                        data['all_lat_list'] = [row[2]]
                        data['all_lon_list'] = [row[3]]
                        data['all_time_list'] = [row[0]]
                        data['flight_number'] = row[1]
                        data['aircraft_type'] = row[5]
                        flight_number_list.append(row[1])
                        if self.hour <= int(row[0][0:2]) < self.hour + 3:
                            data['time_list'] = [row[0]]
                            data['lat_list'] = [row[2]]
                            data['lon_list'] = [row[3]]
                            data['alt_list'] = [row[4]]
                        else:
                            data['time_list'] = []
                            data['lat_list'] = []
                            data['lon_list'] = []
                            data['alt_list'] = []
                        flight_data_list_in_a_month.append(data)
                    
                    else:
                        data = flight_data_list_in_a_month[flight_number_list.index(row[1])]
                        data['all_alt_list'].append(row[4])
                        data['all_lat_list'].append(row[2])
                        data['all_lon_list'].append(row[3])
                        data['all_time_list'].append(row[0])
                        if self.hour <= int(row[0][0:2]) < self.hour + 3:
                            #もし大丈夫なら削除して
                            if data['flight_number'] != row[1]:
                                print('エラー')
                            data['time_list'].append(row[0])
                            data['lat_list'].append(row[2])
                            data['lon_list'].append(row[3])
                            data['alt_list'].append(row[4])

            self.flight_data_list += flight_data_list_in_a_month
        
        #推定したDeparture Airport, Arrival Airportを挿入する（わからないものはNone）
        for flight_data in self.flight_data_list:
            if float(flight_data['all_alt_list'][0]) > 5000:
                # print(flight_data['flight_number'],len(flight_data['all_time_list']),flight_data['all_time_list'][0],flight_data['all_lat_list'][0],flight_data['all_lon_list'][0],flight_data['all_alt_list'][0])
                departure_airport = 'None'
            else:
                lat_departure = float(flight_data['all_lat_list'][0])
                lon_departure = float(flight_data['all_lon_list'][0])
                distance_from_airport = [Qtedist(lat_departure, lon_departure, airport['position'][0], airport['position'][1]) for airport in Airport_list]
                departure_airport = Airport_list[np.argmin(distance_from_airport)]['name']
                if min(distance_from_airport) > 10:
                    departure_airport = 'None'
                    print('Error', min(distance_from_airport))
                    print(lat_departure, lon_departure)
            
            if float(flight_data['all_alt_list'][-1]) > 5000:
                # print(flight_data['flight_number'],len(flight_data['all_time_list']),flight_data['all_time_list'][-1],flight_data['all_lat_list'][-1],flight_data['all_lon_list'][-1],flight_data['all_alt_list'][-1])
                arrival_airport = 'None'
            else:
                lat_arrival = float(flight_data['all_lat_list'][-1])
                lon_arrival = float(flight_data['all_lon_list'][-1])
                distance_from_airport = [Qtedist(lat_arrival, lon_arrival, airport['position'][0], airport['position'][1]) for airport in Airport_list]
                arrival_airport = Airport_list[np.argmin(distance_from_airport)]['name']
                if min(distance_from_airport) > 10:
                    arrival_airport = 'None'
                    print('Error', min(distance_from_airport))
                    print(lat_arrival, lon_arrival)
            
            flight_data['departure airport'] = departure_airport
            flight_data['arrival airport'] = arrival_airport
        # print([len(flight_data['time_list']) for flight_data in self.flight_data_list])
    
    def cover_path(self, lat0, lon0, alt0, time0, lat1, lon1, alt1, time1):
        lat_list = []
        lon_list = []
        alt_list = []
        time_list = []
        a = lat1 - lat0
        b = lon1 - lon0
        c = ((lat0-lat1)**2 + (lon0-lon1)**2)**0.5
        num_devide = int(c / 0.1)
        for n in range(max(0, num_devide - 1)):
            lat = lat0 + a / num_devide * (n + 1)
            lon = lon0 + b / num_devide * (n + 1)
            alt = alt0 + (alt1 - alt0) / num_devide * (n + 1)
            time0_ms = int(time0[0:2]) * (60**3) + int(time0[3:5]) * 60**2 + int(time0[6:8]) * 60 + int(time0[9])
            if int(time0[0:2]) > 18 and int(time1[0:2]) < 6:
                time1_ms = (int(time1[0:2]) + 24) * (60**3) + int(time1[3:5]) * 60**2 + int(time1[6:8]) * 60 + int(time1[9])
            else:
                time1_ms = int(time1[0:2]) * (60**3) + int(time1[3:5]) * 60**2 + int(time1[6:8]) * 60 + int(time1[9])
            time_ms = time0_ms + (time1_ms - time0_ms) / num_devide * (n + 1)
            hour = time_ms // (60**3)
            minute = (time_ms - hour * (60**3)) // (60**2)
            second = (time_ms - hour * (60**3) - minute * (60**2)) // 60
            msecond = time_ms - hour * (60**3) - minute * (60**2) - second * 60
            time = str(f'{int(hour)}:{int(minute)}:{int(second)}.{int(msecond)}')
            lat_list.append(lat)
            lon_list.append(lon)
            alt_list.append(alt)
            time_list.append(time)

        # if len(lat_list):
        #     print(lat_list, lon_list, alt_list, time_list)
        return lat_list, lon_list, alt_list, time_list
    
    def rmk_flight_data(self):
        #[{'icao24' : ..., 'departure time' : ..., 'departure airport' : ..., 'arrival airport' : ..., 'lat_list' : [], 'lon_list' : [], 'alt_list' : []}, {}, {}]を作る。flightdataと{}は一対一対応
        data_list = []
        count=1
        print('FlightData',len(self.flight_data_list))
        for flightdata in self.flight_data_list:
            if not len(flightdata['lat_list']):
                data_list.append(flightdata)
                continue
            data = {}
            lat_list = []
            lon_list = []
            alt_list = []
            time_list = []
            # print('Flightdata',count)
            count+=1
            lat_list_ini, lon_list_ini, alt_list_ini, time_list_ini = flightdata['lat_list'], flightdata['lon_list'], flightdata['alt_list'], flightdata['time_list']
            for n in range(len(lat_list_ini) - 1):
                lat_list.append(lat_list_ini[n])
                lon_list.append(lon_list_ini[n])
                alt_list.append(alt_list_ini[n])
                lat_list_cover, lon_list_cover, alt_list_cover, time_list = self.cover_path(lat_list_ini[n],
                                                                                           lon_list_ini[n],
                                                                                           alt_list_ini[n],
                                                                                           time_list_ini[n],
                                                                                           lat_list_ini[n+1],
                                                                                           lon_list_ini[n+1],
                                                                                           alt_list_ini[n+1],
                                                                                           time_list_ini[n+1])
                lat_list += lat_list_cover
                lon_list += lon_list_cover
                alt_list += alt_list_cover
            lat_list.append(lat_list_ini[-1])
            lon_list.append(lon_list_ini[-1])
            alt_list.append(alt_list_ini[-1])
            
            data['flight_number'] = flightdata['flight_number']
            data['time_list'] = time_list
            data['lat_list'] = lat_list
            data['lon_list'] = lon_list
            data['alt_list'] = alt_list
            data['aircraft_type'] = flightdata['aircraft_type']
            data['departure airport'] = flightdata['departure airport']
            data['arrival airport'] = flightdata['arrival airport']
            data_list.append(data)

        return data_list
    
    def vis_path(self):
        # adding the lines joining the nodes
        fig = go.Figure(go.Scattermapbox(
            name = "center",
            mode = "markers",
            
            lon = [137],
            lat = [36.5],
            marker = {'size': 0, 'color':"red"}))
        
        #add waypoint
        count = 0
        print(len(self.flight_data_list))
        for flightdata in self.flight_data_list:
            print('the number of flight',count)
            count += 1
            lat_list = flightdata['lat_list']
            lon_list = flightdata['lon_list']
            
            fig.add_trace(go.Scattermapbox(
                name = "path",
                mode = "lines",
                opacity=0.1,
                lon = lon_list,
                lat = lat_list,
                marker = {'size': 0, 'color':'dodgerblue'}))
        
        # getting center for plots:
        lat_center = 38.6
        long_center = 137.5
        # defining the layout using mapbox_style
        fig.update_layout(mapbox_style="stamen-terrain",
            mapbox_center_lat = 30, mapbox_center_lon=-80)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        mapbox = {
                            'center': {'lat': lat_center, 
                            'lon': long_center},
                            'zoom': 4.25})   
        
        fig.write_image('./result/flightdata/CARATS_{0}.png'.format(self.date_list))
        fig.show()
                     
                    

if __name__ == '__main__':
    carats = CARATS([202101],0)
    # carats.vis_path()
