import xarray as xr
import numpy as np

nc = xr.open_dataset(
    r'CMIP/Data/csdiETCCDI_yr_ACCESS-CM2_ssp126_r1i1p1f1_b1961-1990_v20191108_2015-2100.nc')
v = nc['csdiETCCDI']
latlon = v.loc[:, 15:60, 70:140]  # 最小纬度:最大纬度,最小经度:最大经度
ds = xr.Dataset({'CsdiETCCDI': latlon})
ds.to_netcdf('CMIP/Data/CSDI_China_SSP1-2.6.nc')  # 输出路径
print('success')

# from cdo import *
#
# cdo = Cdo() file = 'CMIP/Data/csdiETCCDI_yr_ACCESS-CM2_ssp126_r1i1p1f1_b1961-1990_v20191108_2015-2100_v2-0.nc' outfile =
# 'CMIP/Data/csdiETCCDI_yr_ACCESS-CM2_ssp126_r1i1p1f1_b1961-1990_v20191108_2015-2100.nc' cdo.remapbil('r1440x720', input=file,
# output=outfile) # cdo remapbic,r1440x720 wsdiETCCDI_yr_ACCESS-CM2_ssp126_r1i1p1f1_b1961-1990_v20191108_2015-2100_v2-0.nc
# wsdiETCCDI_yr_ACCESS-CM2_ssp126_r1i1p1f1_b1961-1990_v20191108_2015-2100.nc
