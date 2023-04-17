import glob
import os
import numpy as np
import xarray as xr
import netCDF4 as nc
from osgeo import gdal, osr, ogr
import threading


# 步骤3
# -----指数计算及TIFF导出-----

def NC_to_TIFF(u_arr, data_path, out_tif_name):
    # print(u_arr)
    # 读nc数据
    nc_data_obj = nc.Dataset(data_path)
    # 读取经纬度数据
    Lon = nc_data_obj.variables['lon'][:]
    Lat = nc_data_obj.variables['lat'][:]
    # 影像的左上角和右下角坐标
    LonMin, LatMax, LonMax, LatMin = [Lon.min(), Lat.max(), Lon.max(), Lat.min()]
    print(Lon.min(), Lat.max(), Lon.max(), Lat.min())
    # 分辨率计算 90 140
    N_Lat = len(Lat)
    N_Lon = len(Lon)
    # 44.5/89=0.5
    Lat_Res = (LatMax - LatMin) / (float(N_Lat) - 1)
    Lon_Res = (LonMax - LonMin) / (float(N_Lon) - 1)

    # 创建.tif文件
    driver = gdal.GetDriverByName('GTiff')
    # out_tif_name = Output_folder + '\\'+ 'Prec1979_CWD'+ '.tif'
    out_tif = driver.Create(out_tif_name, N_Lon, N_Lat, 1, gdal.GDT_Float32)
    # 设置影像的显示范围
    # -Lat_Res一定要是-的
    geotransform = (LonMin, Lon_Res, 0, LatMax, 0, -Lat_Res)
    out_tif.SetGeoTransform(geotransform)
    # 获取地理坐标系统信息，用于选取需要的地理坐标系统
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)  # 定义输出的坐标系为"WGS 84"，AUTHORITY["EPSG","4326"]
    out_tif.SetProjection(srs.ExportToWkt())  # 给新建图层赋予投影信息
    # 去除异常值
    # u_arr[u_arr[:, :]== -32768] = -99
    # 数据写出
    out_tif.GetRasterBand(1).WriteArray(u_arr)
    out_tif.GetRasterBand(1).SetNoDataValue(-99)
    out_tif.FlushCache()  # 将数据写入硬盘
    del out_tif  # 注意必须关闭tif文件


# 获取特定坐标的年降水量数据
def getPreYearVal(latIndex, lonIndex, pre, month):
    pre2 = pre.variables['pr'][:, latIndex, lonIndex]
    pre_month = pre2[pre.time.dt.month == month] * 24 * 3600
    return pre_month


def getExtreme(flag, data_path, out_tif_name, pre):
    time = pre.variables['time'][:].data
    # 获取经纬度数据,lat纬度,lon经度
    lat0 = pre.variables['lat'][:].data
    lon0 = pre.variables['lon'][:].data
    # 获取数据变量
    pre2 = pre.variables['pr'][:].data
    # 计算行列数
    latNum = len(lat0)
    lonNum = len(lon0)
    # print(latNum, lonNum)
    # 生成二维数组，存储降雨量数据（用行列号做索引，存储极端气候指数）
    RPre_array = np.zeros((latNum, lonNum))

    def get_R10R20(pr_num):
        if pr_num == 10:
            print("---------------R10中雨日数，降水量>=10mm的总日数---------------------")
        else:
            print("---------------R20中雨日数，降水量>=20mm的总日数---------------------")
        for i in range(1, 13):
            print('第' + str(i) + '月')
            # 获取每个月数据
            pre_month = pre2[pre.time.dt.month == i, :] * 24 * 3600
            # print(pre_month.shape)
            # print(pre_month[:, 120, 375])
            # 计算中雨/大雨日数：pr>=10mm/20mm的总日数
            # 像素数值是空值，赋值-1；非空赋降水量天数
            RPre_array = np.nansum(pre_month >= pr_num, axis=0)
            RPre_array[np.isnan(pre_month[0])] = -1
            # print(RPre_array[120, 375])
            # 数组行逆序 0-399
            RPre_array = RPre_array[::-1]
            # NC转TIFF
            out_tif_name2 = out_tif_name + "_" + str(i) + ".tif"
            NC_to_TIFF(RPre_array, data_path, out_tif_name2)
            print(out_tif_name2 + '-----转tif成功')

    def get_CDWD(typename):
        if typename == 'CDD':
            print("-------CCD-------")
        else:
            print("-------CWD-------")
        for mon in range(1, 13):
            print('第' + str(mon) + '月')
            for latIndex in range(0, latNum):
                for lonIndex in range(0, lonNum):
                    pre_day = getPreYearVal(latIndex, lonIndex, pre, mon)
                    # print(pre_day)
                    # print(latIndex, lonIndex, mon)
                    if np.isnan(pre_day).any():
                        continue
                    else:
                        # print(pre_day)
                        preday_shape = pre_day.shape
                        # print(preday_shape)
                        CDWD_days = np.zeros(preday_shape)
                        if typename == 'CDD':
                            CDWD_days = np.where(pre_day < 1, 1, 0)
                        elif typename == 'CWD':
                            CDWD_days = np.where(pre_day >= 1, 1, 0)
                        # print(CDWD_days)
                        tmp = np.zeros(pre_day.shape)

                        # 后一位减去前一位
                        tmp = CDWD_days[1:] + CDWD_days[:-1]
                        # print(tmp)
                        if CDWD_days[0] == 0:
                            tmp = np.insert(tmp, 0, 0)
                        else:
                            tmp = np.insert(tmp, 0, 1)
                        # print(tmp)
                        loc = np.arange(preday_shape[0])
                        loc = loc[tmp == 1]
                        # print(loc)
                        if tmp[-1] == 2:
                            loc = np.append(loc, preday_shape[0])

                        dif = []
                        locnum = loc.shape[0]
                        if locnum % 2 != 0:
                            locnum = loc.shape[0] - 1
                        for i in range(0, locnum, 2):
                            dif.append(loc[i + 1] - loc[i])
                        # print(dif)
                        if np.any(dif):
                            tmp2 = np.nanmax(dif)
                        else:
                            tmp2 = np.array([-1])
                        # print(tmp2, latIndex, lonIndex)
                        RPre_array[180 - latIndex][lonIndex] = tmp2
            # print(RPre_array)
            # NC转TIFF
            out_tif_name2 = out_tif_name + "_" + str(mon) + ".tif"
            NC_to_TIFF(RPre_array, data_path, out_tif_name2)
            print(out_tif_name2 + '-----转tif成功')

    if flag == 41:
        get_CDWD("CDD")
    elif flag == 42:
        get_CDWD("CWD")
    elif flag == 0:
        get_R10R20(10)
    elif flag == 1:
        get_R10R20(20)


if __name__ == '__main__':
    Input_folder = r'D:\WorkSpace\Python_WorkSpace\CMIP_Test\CMIP6_0.25\pr_China_0.25'
    Output_folder = r'D:\WorkSpace\Python_WorkSpace\CMIP_Test\TIF'
    # 计算极端指数 0-R10 1-R20 2-R95p 3-R99p 41-CDD 42-CWD
    type = 42

    if type == 0:
        # 计算R10
        Output_folder += "\\R10"
    elif type == 1:
        # 计算R20
        Output_folder += "\\R20"
    elif type == 41:
        # 计算CDD
        Output_folder += "\\CDD"
    elif type == 42:
        # 计算CWD
        Output_folder += "\\CWD"

    data_list = glob.glob(Input_folder + '\*.nc')
    print(len(data_list))

    for i in range(0, 5):
        data = data_list[i]
        Input_folder = os.path.join(Input_folder, data)
        data_path = Input_folder
        pre = xr.open_dataset(data_path)
        filename = os.path.split(Input_folder)
        time = filename[1].split('_')[-1]
        print(time)
        out_tif_name = Output_folder + '\\' + Output_folder.split('\\')[-1] + '_' + time.split('.')[0].split('-')[0][0:4]
        getExtreme(type, data_path, out_tif_name, pre)
