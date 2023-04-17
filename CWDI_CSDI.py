import glob
import os

import netCDF4 as nc
import numpy as np
import xarray as xr
from osgeo import gdal, osr


def NC_to_TIFF(u_arr, data_path, out_tif_name):
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
    out_tif = driver.Create(out_tif_name, N_Lon, N_Lat, 1, gdal.GDT_Float32)
    # 设置影像的显示范围
    geotransform = (LonMin, Lon_Res, 0, LatMax, 0, -Lat_Res)
    out_tif.SetGeoTransform(geotransform)
    # 获取地理坐标系统信息，用于选取需要的地理坐标系统
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)  # 定义输出的坐标系为"WGS 84"，AUTHORITY["EPSG","4326"]
    out_tif.SetProjection(srs.ExportToWkt())  # 给新建图层赋予投影信息
    out_tif.GetRasterBand(1).WriteArray(u_arr)
    out_tif.GetRasterBand(1).SetNoDataValue(-99)
    out_tif.FlushCache()  # 将数据写入硬盘
    del out_tif  # 注意必须关闭tif文件


def getTxn(flag, temp, percen_arr, vName):
    # 日最高气温的极高值、极低值
    def get_Txxn(atype):
        # 获取气温数值
        if vName == "tasmax":
            temp_arr = np.array(temp.tasmax)
        elif vName == "tasmin":
            temp_arr = np.array(temp.tasmin)
        # 计算天数、行列数、生成结果数组
        rownum = int(temp_arr.shape[0])
        colnum = int(temp_arr.shape[1])
        tempper_sum = np.zeros((rownum, colnum))
        # TXx 日最高气温的极高值
        if atype == 'max':
            tempper_Value = np.nanmax(temp_arr, axis=0) - 273.15
        # TNn 日最高气温的极低值
        elif atype == 'min':
            tempper_Value = np.nanmin(temp_arr, axis=0) - 273.15
        # 背景值设置为-1
        tempper_Value[np.isnan(temp_arr[0])] = -99
        # 数组行逆序 0-399
        tempper_Value = tempper_Value[::-1]
        return tempper_Value
        # 暖持续日数

    def get_Txnp(percen, percen_arr):
        # 获取气温数值
        if vName == "tasmax":
            temp_arr = np.array(temp.tasmax)
        elif vName == "tasmin":
            temp_arr = np.array(temp.tasmin)
        # 计算分位数数值
        temp_per = percen_arr.temp
        # 计算天数、行列数、生成结果数组
        timenum = temp_arr.shape[0]
        rownum = int(temp_per.shape[1])
        colnum = int(temp_per.shape[2])
        temp_per_rel = np.zeros((timenum, rownum, colnum))
        tempper_sum = np.zeros((rownum, colnum))
        # 遍历每天数据
        for i in range(0, temp_arr.shape[0]):
            if percen == 10:
                # 比较气温和百分位数，满足1，不满足0
                temp_percen = np.where(temp_arr[i][:, :] < temp_per[i][:, :], 1, 0)
                temp_per_rel[i] = temp_percen
            elif percen == 90:
                temp_percen = np.where(temp_arr[i][:, :] > temp_per[i][:, :], 1, 0)
                temp_per_rel[i] = temp_percen
        # 计算满足分位数条件的总日数
        tempper_sum = np.sum(temp_per_rel, axis=0)
        # 背景值设置为-1
        tempper_sum[np.isnan(temp_arr[0])] = -1
        # 数组行逆序 0-399
        tempper_sum = tempper_sum[::-1]
        return tempper_sum

    def get_WSDI(percen):
        # 获取气温数值
        if vName == "tasmax":
            temp_arr = np.array(temp.tasmax)
        elif vName == "tasmin":
            temp_arr = np.array(temp.tasmin)
        # 计算分位数数值
        temp_per = percen_arr.temp
        # 计算天数、行列数、生成结果数组
        timenum = temp_arr.shape[0]
        rownum = int(temp_per.shape[1])
        colnum = int(temp_per.shape[2])
        temp_per_rel = np.zeros((timenum, rownum, colnum))
        tempper_sum = np.zeros((rownum, colnum))
        # 气温数据与百分位数数据比较大小，大于赋值1，小于赋值0
        for i in range(0, temp_arr.shape[0]):  # temp_arr.shape[0]
            if percen == 10:
                # 比较气温和百分位数，满足1，不满足0
                temp_percen = np.where(temp_arr[i][:, :] < temp_per[i][:, :], 1, 0)
                temp_per_rel[i] = temp_percen
            elif percen == 90:
                temp_percen = np.where(temp_arr[i][:, :] > temp_per[i][:, :], 1, 0)
                temp_per_rel[i] = temp_percen
        # print(temp_per_rel)
        # 遍历逐行逐列
        # print(rownum, colnum)
        for latIndex in range(0, rownum):
            for lonIndex in range(0, colnum):
                # 获取该像元月降水量数据
                try:
                    temp_value = temp_per_rel[:, latIndex, lonIndex]
                except:
                    print(latIndex, lonIndex)  # 不要注释
                if np.isnan(temp_value).any():
                    continue
                else:
                    # 筛选降水>=1mm的日期,
                    tempday_shape = temp_value.shape
                    tmp = np.zeros(tempday_shape)
                    # 后一位加上前一位，记录是数字1的位置
                    # 原数组是[0，0，0，0，0，0，1，1，1，1，1，1，1,0,0,0]
                    # 错位相加[0，0，0，0，0，1，2，2，2，2，2，2，1,0,0,0]
                    # 记录1的索引[5,12],12-5=7
                    tmp = np.array(temp_value[1:]) + np.array(temp_value[:-1])
                    if temp_value[0] == 0:
                        tmp = np.insert(tmp, 0, 0)
                    else:
                        tmp = np.insert(tmp, 0, 1)
                    loc = np.arange(len(temp_value))  # tempday_shape[0]
                    loc = loc[tmp == 1]
                    if temp_value[-2] + temp_value[-1] == 2:
                        loc = np.append(loc, len(temp_value))
                    elif temp_value[-1] == 1:
                        loc[-1] = len(temp_value)
                        loc = np.append(loc, len(temp_value))
                    locnum = loc.shape[0]
                    temp_cons = np.zeros(len(temp_value))  # tempday_shape[0]
                    # 以2为步长，遍历计算每天的连续日数
                    # 假设loc=[4,10，14，16],索引4-10=7-1，索引14-16=3-1
                    for loci in range(0, locnum, 2):
                        if loc[loci] == loc[loci + 1]:
                            temp_cons[loc[loci] - 1] = 1
                        else:
                            for con_days in range(loc[loci], loc[loci + 1]):
                                temp_cons[con_days] = loc[loci + 1] - con_days
                    all_days = (temp_cons >= 6).sum()
                    tempper_sum[180 - latIndex][lonIndex] = all_days
        return tempper_sum

    if flag == 11:
        output = get_Txnp(10, percen_arr)
    elif flag == 12:
        output = get_Txnp(90, percen_arr)
    elif flag == 21:
        output = get_Txxn('max')
    elif flag == 22:
        output = get_Txxn('min')
    elif flag == 31:
        output = get_WSDI(90)
    elif flag == 32:
        output = get_WSDI(10)
    return output


def main():
    # 选择日最高或最低温
    vName = "tasmax"
    SSP = "SSP1-2.6"
    Input_temp_folder = r'CMIP6_0.25/' + vName + '_China_' + SSP + '_0.25_mon'

    # WSDI 最大值90%分位数
    Input_percent_folder = r'CMIP6_0.25/tasmax90%'
    # CSDI 最小值10%分位数
    # Input_percent_folder = r'CMIP6_0.25/tasmin10%'

    # 输出路径
    Output_folder = r'TIF/Temp'

    Output_folder += "\\WSDI_"+SSP
    # Output_folder += "\\CSDI_"+SSP
    # Output_folder += "\\TXx_" + SSP
    # Output_folder += "\\TNn_"+SSP
    # Output_folder += "\\TX90p_"+SSP
    # Output_folder += "\\TX10p_"+SSP

    # 计算极端指数 11-TX10p 12-TX90p 21max-TXx 22min-TNn 31-WSDI 32-CSDI
    # 用tasmax算21和22为TXx和TNx
    # 用tasmin算21和22为TXn和TNn
    type = 31

    data_list = glob.glob(Input_temp_folder + '\*.nc')
    # 遍历日最高/低温中的文件
    print(data_list)
    for i in range(0, len(data_list)):
        Input_folder = data_list[i]
        # 获取文件名
        data_name = os.path.basename(Input_folder)
        # 获取时间
        percen_path = ''
        data_time = data_name.split('_')[-1][-5:]
        print(data_time)
        for file in os.listdir(Input_percent_folder):
            if data_time in file:
                print(file)
                percen_path = os.path.join(Input_percent_folder, file)
                print(percen_path)
        temp = xr.open_dataset(Input_folder)
        percen = xr.open_dataset(percen_path)
        filename = os.path.split(Input_folder)
        time = filename[1].split('_')[-1]
        # print(time)
        # print(Output_folder.split('\\'))
        # print(percen)
        RTxn_arr = getTxn(type, temp, percen, vName)
        # 获取文件名中的年,拼接输出路径
        out_tif_name = Output_folder + '\\ ' + Output_folder.split('\\')[-1] + '_ ' + time.split('.')[0] + '.tif'
        print(out_tif_name)
        # NC转TIFF
        NC_to_TIFF(RTxn_arr, Input_folder, out_tif_name)
        print(out_tif_name + '-----转tif成功')


if __name__ == '__main__':
    main()
