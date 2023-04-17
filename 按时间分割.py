import xarray as xr

vName = "wsdiETCCDI"
# 步骤1
#  -----按时间分割(年)-----
nc = xr.open_dataset(
    r'CMIP/Data/WSDI_China_SSP1-2.6.nc')
v = nc[vName]
print(v)
for year in range(2021, 2101):
    time = v.loc[str(year) + '-01-01 00:00:00':str(year + 1) + '-01-01 00:00:00']
    ds = xr.Dataset({vName: time})
    ds.to_netcdf('CMIP/WSDI_SSP1-2.6_0.25/WSDI_SSP1-2.6_' + str(year) + '.nc')  # 输出路径
    print(str(year) + 'success')

#  -----按时间分割(月)-----
# vName = "tasmin"
# SSP = "SSP5-8.5"
# for year in range(2021, 2051):
#     nc = xr.open_dataset(
#         r'CMIP6_0.25/' + vName + '_China_' + SSP + '_0.25/' + vName + '_China_0.25_' + str(year) + '.nc')
#     v = nc[vName]
#     # print(v)
#     for mon in range(1, 13):
#         if mon == 12:
#             time = v.loc[str(year) + '-' + str(mon) + '-01 00:00:00':str(year + 1) + '-01-01 00:00:00']
#             ds = xr.Dataset({vName: time})
#             ds.to_netcdf(
#                 'CMIP6_0.25/' + vName + '_China_' + SSP + '_0.25_mon/' + vName + '_0.25_' + str(year) + str(mon) + '.nc')  # 输出路径
#             print(vName + "_" + SSP + "_" + str(year) + str(mon) + 'success')
#         elif mon < 9:
#             time = v.loc[str(year) + '-0' + str(mon) + '-01 00:00:00':str(year) + '-0' + str(mon + 1) + '-01 00:00:00']
#             ds = xr.Dataset({vName: time})
#             ds.to_netcdf(
#                 'CMIP6_0.25/' + vName + '_China_' + SSP + '_0.25_mon/' + vName + '_0.25_' + str(year) + '0' + str(mon) + '.nc')  # 输出路径
#             print(vName + "_" + SSP + "_" + str(year) + '0' + str(mon) + 'success')
#         elif mon == 9:
#             time = v.loc[str(year) + '-0' + str(mon) + '-01 00:00:00':str(year) + '-' + str(mon + 1) + '-01 00:00:00']
#             ds = xr.Dataset({vName: time})
#             ds.to_netcdf(
#                 'CMIP6_0.25/' + vName + '_China_' + SSP + '_0.25_mon/' + vName + '_0.25_' + str(year) + '0' + str(mon) + '.nc')  # 输出路径
#             print(vName + "_" + SSP + "_" + str(year) + '0' + str(mon) + 'success')
#         else:
#             time = v.loc[str(year) + '-' + str(mon) + '-01 00:00:00':str(year) + '-' + str(mon + 1) + '-01 00:00:00']
#             ds = xr.Dataset({vName: time})
#             ds.to_netcdf(
#                 'CMIP6_0.25/' + vName + '_China_' + SSP + '_0.25_mon/' + vName + '_0.25_' + str(year) + str(mon) + '.nc')  # 输出路径
#             print(vName + "_" + SSP + "_" + str(year) + str(mon) + 'success')
