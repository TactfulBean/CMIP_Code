import xarray as xr
import numpy as np

#  -----数据初步处理-----
vName = "csdiETCCDI"
SSP = "SSP5-8.5"

nc = xr.open_dataset(r'CMIP/Data/csdiETCCDI_yr_ACCESS-CM2_ssp126_r1i1p1f1_b1961-1990_v20191108_2015-2100_v2-0.nc')
v = nc[vName]
for year in range(2021, 2101):
    time = v.loc[str(year) + '-01-01 00:00:00':str(year + 1) + '-01-01 00:00:00']
    ds = xr.Dataset({vName: time})
    ds.to_netcdf('CMIP/Temp/'+vName+SSP+'_' + str(year) + '.nc')  # 输出路径
    print(str(year) + 'success')

new_lon = np.arange(65, 145, 0.25)  # 经度范围及目标尺度
new_lat = np.arange(10, 65, 0.25)  # 纬度范围及目标尺度
# 多文件处理可以采用循环
for year in range(2021, 2101):
    # 打开文件
    ori_data = xr.open_dataset('CMIP/Temp/'+vName+SSP+'_' + str(year) + '.nc')
    new_data = ori_data.interp(lat=new_lat, lon=new_lon)  # 线性插值
    print(str(year) + '_0.25_success')
    v = new_data[vName]
    latlon = v.loc[:, 15:60, 70:140]  # 最小纬度:最大纬度,最小经度:最大经度
    ds = xr.Dataset({vName: latlon})
    ds.to_netcdf('CMIP/CSDI_SSP1-2.6_0.25/CSDI_SSP1-2.6_0.25_' + str(year) + '.nc')  # 输出路径
    print(str(year) + '_China_0.25_success')
