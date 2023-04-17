# 计算90%分位数
import os
import xarray as xr
import pandas as pd
import numpy as np
from netCDF4 import Dataset
import netCDF4 as nc
import glob
from datetime import timedelta
import datetime


def get_base_percentile(folder, folder_1984, percen_nc_file, percen):
    # 打开文件夹内个月nc数据，按照时间维度拼接
    # 日最高温
    combinenc = xr.open_mfdataset(folder + '\max_historical_0.25_*.nc', combine='by_coords')
    # 日最低温
    # combinenc = xr.open_mfdataset(folder + '\\min_historical_0.25_*.nc', combine='by_coords')
    # 计算基期百分位数各月时间节点
    time_arr = []
    percen_filelist = []
    time_month_list = []
    startIndex = 0
    data_list = glob.glob(folder_1984 + '\*.nc')
    # 遍历1984年各月数据，获取时间、月日数和存储路径
    for i in range(0, len(data_list)):  # len(data_list)
        # 获取文件路径
        file_name = data_list[i]
        print(file_name)
        # 打开数据，获取时间维度数据
        T_hour_file = Dataset(file_name)
        timeInt = T_hour_file.variables['time'][:]
        # 存储到时间数组，31，60，91...366
        time_month_list.append(timeInt)
        day = timeInt.shape[0]
        endIndex = startIndex + day
        time_arr.append(endIndex)
        startIndex = endIndex
        print(time_arr)
        # 解析存储路径
        print(file_name)
        file_name0 = os.path.basename(file_name).split('_')[0] + '_'
        precen_name = 'pencen' + str(percen) + "_"
        month_name = os.path.basename(file_name).split('_')[-1][-5:]
        print(file_name0, precen_name, month_name)
        percen_filelist.append(file_name0 + precen_name + month_name)
        print(percen_filelist)
        # 遍历读文件，拼接各月时间数组
        tm_1984 = combinenc.isel(time=(combinenc.time.dt.year == 1984))
    # 获取时间纬度数据
    timelist = combinenc.variables['time']
    tas = combinenc.variables['tasmax']
    # 获取经纬度数据
    lat0 = combinenc.variables['lat'][:]
    lon0 = combinenc.variables['lon'][:]
    # 计算三个维度，时间、经度、纬度*************
    timeNum = tm_1984.tasmax.shape[0]
    latNum = combinenc.tasmax.shape[1]
    lonNum = combinenc.tasmax.shape[2]
    # 遍历每一个时间T（1天数据）计算周围五个时间窗口的百分位数
    # 遍历年时间数组
    index = 0
    # 取到1984年日期，计算5天时间窗
    timern = tm_1984.variables['time']
    # 定义基期百分位数计算结果数组，计算每个像元每层366天时间维度的百分位结果
    baseperoid_percen = np.zeros((time_arr[0], latNum, lonNum), dtype='float32')
    # 获取每天时间，计算时间窗时间范围
    for i in range(0, timern.shape[0]):  # timern.shape[0]
        if i >= 31:
            baseperiod_index = i - time_arr[index]
        else:
            baseperiod_index = i
        # 获取某一天
        basetime = timern[i]
        #         print('basetime某天')
        #         print(basetime)
        # 将datetime64[ns]转换为datetime日期类型
        basetime_tm = basetime.values.astype('datetime64[s]').tolist()
        #         print('basetime_tm转换')
        #         print(basetime_tm)
        # 定义时间窗数组
        timewindow_5day = []
        # 计算前两天日期，并添加到时间窗
        for deltapsub in range(1, 3):
            timewindow_5day.append(basetime_tm - timedelta(days=deltapsub))
        # 将当天日期添加到时间窗
        timewindow_5day.append(basetime_tm)
        # 计算后三天日期，并添加到时间窗
        for deltapplus in range(1, 3):
            timewindow_5day.append(basetime_tm + timedelta(days=deltapplus))
        print('timewindow_5day5天时间窗')
        print(timewindow_5day)
        tas_window_values = np.zeros((0, latNum, lonNum), dtype='float32')
        # 遍历时间窗时间，取出月、日
        for j in range(0, 5):
            # 获取月、日
            month = timewindow_5day[j].month
            day = timewindow_5day[j].day
            print('month,day')
            print(month, day)
            # 取到基期年份中时间窗5天数据
            tas_month = combinenc.isel(time=(combinenc.time.dt.month == month))
            tas_timewindow = tas_month.isel(time=(tas_month.time.dt.day == day))
            # 将所有天数据拼接
            if j == 0:
                tas_window_values = tas_timewindow.tasmax
            else:
                tas_window_values = xr.concat([tas_window_values, tas_timewindow.tasmax], dim="time")
        print('tas_window_values')
        # print(tas_window_values[:, 120, 379].values)
        # 计算百分位数
        baseperoid_percen[baseperiod_index] = np.nanpercentile(tas_window_values[:][:], percen, axis=0)
        print('baseperoid_percen')
        # print(baseperoid_percen[:, 120, 379])
        print('time_arr')
        print(time_arr)
        # 如果是一年的最后一天，将计算的基期百分位结果数组写入新的nc文件
        if i + 1 in time_arr:
            # 计算某一个月的总天数
            index = time_arr.index(i + 1)
            print('index')
            print(index)
            #         print(index,month_day[index],month_day[index-1])
            # 拼接新nc文件的名称：H:\percen10_maxtem_198201.nc
            percen_nc_file2 = percen_nc_file + '_' + percen_filelist[index]
            print('percen_nc_file2')
            print(percen_nc_file2)
            T_lastMonthNum = 0
            if index >= 1:
                T_lastMonthNum = time_arr[index - 1]
                T_MonthNum = time_arr[index] - T_lastMonthNum
            else:
                T_MonthNum = time_arr[index]
            print('T_MonthNum,T_lastMonthNum')
            print(T_MonthNum, T_lastMonthNum)
            print(percen_nc_file2, T_MonthNum, latNum, lonNum,
                  time_month_list[index],
                  lat0, lon0, baseperoid_percen)
            write_nc(percen_nc_file2, T_MonthNum, latNum, lonNum,
                     time_month_list[index],
                     lat0, lon0, baseperoid_percen)
            # 写日最低温nc文件
            N_MonthNum = time_arr[index + 1] - time_arr[index]
            # 定义基期百分位数计算结果数组，计算每个像元每层时间维度的百分位结果
            baseperoid_percen = np.zeros((N_MonthNum, latNum, lonNum), dtype='float32')


def write_nc(new_file_name, days, latnum, lonnum, time, lat, lon, tasmax):
    # 创建一个新的nc
    new_nc = nc.Dataset(new_file_name, 'w', format='NETCDF4')
    # 创建维度，时间、经度、纬度
    new_nc.createDimension('time', days)
    new_nc.createDimension('lat', latnum)
    new_nc.createDimension('lon', lonnum)
    # 创建变量，时间、经度、纬度
    # 时间变量i4对应nc中的int-(32 位有符号整数)
    # 有效的数据类型说明符包括：( 'f4', 'f8', 'i2', 'i2', 'i1', 'i1', 'S1', 'i4', 'i4')
    timevar = new_nc.createVariable('time', 'i4', ("time"))
    # 对应nc数据的units
    timevar.units = "hours since 1900-01-01 00:00:0.0"
    new_nc.createVariable('lat', 'float32', ("lat"))
    new_nc.createVariable('lon', 'float32', ("lon"))
    # 创建温度变量*****************
    new_nc.createVariable('temp', 'float32', ('time', 'lat', 'lon'))
    # 给各维度（时间、经度、纬度）填充数据
    print('填充数据')
    print(time)
    new_nc.variables['time'][:] = time
    print("time is done!")
    new_nc.variables['lat'][:] = lat
    print("lat is done!")
    new_nc.variables['lon'][:] = lon
    print("lon is done!")
    # 给温度变量填充数据
    new_nc.variables['temp'][:] = tasmax
    print("tmp is done!")
    # 关闭文件
    new_nc.close()


if __name__ == '__main__':
    # 时间文件
    folder_1984 = r'CMIP6_0.25/1988'
    # 日最低温数据
    # folder = r'CMIP6_0.25/tasmax_historical_China_mon_0.25'
    # pencen_file_name = r'CMIP6_0.25/tasmax10%'
    # 日最高温数据
    folder = r'CMIP6_0.25/tasmax_historical_China_mon_0.25'
    pencen_file_name = r'CMIP6_0.25/tasmax90%'

    # get_base_percentile(folder, folder_1984, pencen_file_name, 90)
    combinenc = xr.open_mfdataset(folder + '\max_historical_0.25_*.nc', combine='by_coords')
    print(combinenc)