import numpy as np
import pandas as pd
import netCDF4 as nc
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import dateutil.parser  # 引入这个库来将日期字符串转成统一的datatime时间格式

# plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

nf = nc.Dataset(r'CMIP/Data/WSDI_China_SSP1-2.6.nc', 'r')
# nf2 = nc.Dataset(r'CMIP/Data/csdiETCCDI_yr_ACCESS-CM2_ssp126_r1i1p1f1_b1961-1990_v20191108_2015-2100_v2-0.nc', 'r')
# nf3 = nc.Dataset(r'CMIP/Data/csdiETCCDI_yr_ACCESS-CM2_ssp126_r1i1p1f1_b1961-1990_v20191108_2015-2100.nc', 'r')
# --变量列表--
# print(nf.variables.keys())
# print(nf2.variables.keys())
# print(nf3.variables.keys())
# print(nf2.variables.keys())
# print(nf3.variables.keys())

# print(nf2.variables.items())
# var_data = nf4["csdiETCCDI"][:]
# print(var_data)
# var_data = nf4["csdiETCCDI"][:]
# print(var_data)
# var_data = nf4["csdiETCCDI"][:]
# print(var_data)

# print(nf.variables['lat'][:].data)
print(len(nf.variables['lat'][:].data))
# print(nf.variables['lon'][:].data)
print(len(nf.variables['lon'][:].data))
# print(nf.variables['lon'][:].min(), nf.variables['lat'][:].max(), nf.variables['lon'][:].max(), nf.variables['lat'][:].min())
# print(nf.variables['time'])
# print(nf.variables['lat'][:].data)
# print(nf.variables['lon'][:].data)
# print(nf.variables['lat'][:].max()-nf.variables['lat'][:].min())
# print(nf.variables['lon'][:].max()-nf.variables['lon'][:].min())
# print(nf.variables['lon'][:].max())
# print(nf.variables['ta'])

# --时间列表--
# print(nf.variables['time'])
# time = nc.num2date(nf.variables['time'][:], 'days since 2015-1-1 00:00:00').data
# print(time)
# print(time[0].year)

# --读取数据--
# print(nf.variables['lat'][:].data)
# print(nf.variables['lon'][:].data)
# print(nf.variables['tas'])

# --绘制--
# all_times = nf.variables['time']
# sdt = dateutil.parser.parse("2015-1-1")
# edt = dateutil.parser.parse("2015-2-1")
# st_idx = nc.date2index(sdt, all_times, select='before')
# et_idx = nc.date2index(edt, all_times, select='before')
# print(st_idx)
# print(et_idx)
# precip = nf.variables['pr'][st_idx:et_idx + 1, :].data
# # # 缺失值处理：missing_value: 1e+20
# precip[precip == 1e+20] = 0
# print(precip.shape)
# # print(precip)
#
# lats = nf.variables['lat'][:].data
# lons = nf.variables['lon'][:].data
# # print(lats)
# # 经纬度平均值
# lon_0 = lons.mean()
# lat_0 = lats.mean()
# # m = Basemap(lat_0=lon_0, lon_0=lat_0)
# m = Basemap(llcrnrlon=65, llcrnrlat=15, urcrnrlon=140, urcrnrlat=60)
# lon, lat = np.meshgrid(lons, lats)
# xi, yi = m(lon, lat)
# # 绘制经纬线
# m.drawparallels(np.arange(-90., 91., 20.), labels=[1, 0, 0, 0], fontsize=10)
# m.drawmeridians(np.arange(-180., 180., 40.), labels=[0, 0, 0, 1], fontsize=10)
# # Add Coastlines, States, and Country Boundaries
# m.drawcoastlines()
# m.drawstates()
# m.drawcountries()
# for i in range(1):
#     precip_0 = precip[i:i + 1:, ::, ::]
#     cs = m.pcolor(xi, yi, np.squeeze(precip_0))
#     if i == 0:
#         cbar = m.colorbar(cs, location='bottom', pad="10%")
#         cbar.set_label(nf.variables['pr'].units)
#     plt.title(str(i + 1) + '月')
#     plt.savefig(str(i) + '.jpg', dpi=400)
