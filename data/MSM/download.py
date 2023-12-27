import urllib.request
import os

#url='http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2022/01/02/Z__C_RJTD_20220102000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin'
#save_name='./Indata/20220102/Z__C_RJTD_20220102000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin'

#urllib.request.urlretrieve(url, save_name)

def down(year,month,day,hh0):
    if 0<=month<=9:
        month='0{0}'.format(month)
    if 0<=day<=9:
        day='0{0}'.format(day)
    if 0<=hh0<=9:
        hh0='0{0}'.format(hh0)
    if not os.path.isdir('./data/MSM/{0}{1}{2}'.format(year,month,day)):
        os.mkdir('./data/MSM/{0}{1}{2}'.format(year,month,day))
    url='http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/{0}/{1}/{2}/Z__C_RJTD_{0}{1}{2}{3}0000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin'.format(year,month,day,hh0)
    save_name='./data/MSM/{0}{1}{2}/Z__C_RJTD_{0}{1}{2}{3}0000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin'.format(year,month,day,hh0)
    if not os.path.isfile(save_name):
        print('ダウンロード中')
        print(save_name)
        urllib.request.urlretrieve(url, save_name)
        print('ダウンロード完了')

if __name__ == '__main__':
    for hour in [0,3,6,9,12,15,18,21]:
        down(2018,7,1,hour)
