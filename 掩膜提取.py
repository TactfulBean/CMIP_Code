from osgeo import gdal

vName = 'CSDI'
SSP = 'SSP1-2.6'
# 掩膜
input_shape = r"D:\WorkSpace\LocalServerFile\China\4326China.shp"

for year in range(2021, 2051):
    for mon in range(1, 13):
        # 输入栅格
        input_raster = r'TIF/'+vName+'_'+SSP+'/CSDI_'+SSP+'_' + str(year) + str(mon) + '.tif'
        input_raster = gdal.Open(input_raster)
        # 输出路径
        output_raster = r'TIF/'+vName+'_China_'+SSP+'/'+vName+'_China_'+SSP+'_' + str(year) + str(mon) + '.tif'

        ds = gdal.Warp(output_raster,
                       input_raster,
                       format='GTiff',
                       cutlineDSName=input_shape,  # or any other file format
                       # optionally you can filter your cutline (shapefile) based on attribute values
                       cutlineWhere="FIELD = 'whatever'",
                       dstNodata=-9999)  # select the no data value you like
        ds = None
