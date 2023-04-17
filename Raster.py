import arcpy
from arcpy.sa import *

# 使用ArcGIS所带的IDLE (Python GUI)运行
SSP = "SSP5-8.5"
Vname = "WDSI"


def rastercal(workspace1, outpath):
    arcpy.CheckOutExtension("spatial")
    arcpy.gp.overwriteOutput = 1
    arcpy.env.workspace = workspace1
    files = arcpy.ListRasters("*", "tif")

    year = 2021
    mon = 1
    sum = 0
    for file in files:
        print(file)
        mon += 1
        sum += Raster(file)
        if mon == 13:
            sum.save(outpath + ''+Vname+'_China_' + SSP + '_' + str(year) + ".tif")
            mon = 1
            sum = 0
            year += 1
            print("---------------")


if __name__ == "__main__":
    # 输入路径
    workspace1 = 'D:\\WorkSpace\\Python_WorkSpace\\CMIP_Test\\TIF\\'+Vname+'_China_' + SSP + '\\'
    # 输出路径
    outpath = 'D:\\WorkSpace\\Python_WorkSpace\\CMIP_Test\\TIF\\'+Vname+'_China_' + SSP + '_year\\'
    rastercal(workspace1, outpath)
