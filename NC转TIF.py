import numpy as np
import netCDF4 as nc
from osgeo import gdal, osr

for year in range(2021, 2101):
    var = 'wsdiETCCDI'
    data = r'CMIP/WSDI_SSP1-2.6_0.25/WSDI_SSP1-2.6_'+str(year)+'.nc'.format(var)
    f = nc.Dataset(data)
    var_lon = f['lon'][:]
    var_lat = f['lat'][:]
    data = f[var][0, :]
    data_arr = np.asarray(data)
    data_arr = data_arr[::-1]  # 因为我的数据维度是正序排列，需要逆序一下
    # 影像的左上角和右下角坐标
    LonMin, LatMax, LonMax, LatMin = [var_lon.min(), var_lat.max(), var_lon.max(), var_lat.min()]
    # 分辨率计算
    N_Lat = len(var_lat)
    N_Lon = len(var_lon)
    Lon_Res = (LonMax - LonMin) / (float(N_Lon) - 1)
    Lat_Res = (LatMax - LatMin) / (float(N_Lat) - 1)

    # 创建.tif文件
    driver = gdal.GetDriverByName('GTiff')
    out_tif_name = r'CMIP/TIF/WSDI_SSP1-2.6/WSDI_SSP1-2.6_'+str(year)+'.tif'.format(var)
    out_tif = driver.Create(out_tif_name, N_Lon, N_Lat, 1, gdal.GDT_Float32)  # 创建框架

    # 设置影像的显示范围
    # Lat_Res一定要是-的
    geotransform = (LonMin, Lon_Res, 0, LatMax, 0, -Lat_Res)
    out_tif.SetGeoTransform(geotransform)

    # 获取地理坐标系统信息，用于选取需要的地理坐标系统
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)  # 定义输出的坐标系为"WGS 84"，AUTHORITY["EPSG","4326"]
    out_tif.SetProjection(srs.ExportToWkt())  # 给新建图层赋予投影信息

    # 数据写出
    out_tif.GetRasterBand(1).WriteArray(data_arr)  # 将数据写入内存，此时没有写入硬盘
    out_tif.FlushCache()  # 将数据写入硬盘
    out_tif = None  # 注意必须关闭tif文件
