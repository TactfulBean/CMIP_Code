import os

# type = "CSDI"
# type = "WSDI"
# type = "TN10P"
# type = "TN90P"
# type = "TX10P"
# type = "TX90P"
# type = "CDD"
type = "CWD"

# SSP = 'SSP1-2.6'
SSP = 'SSP2-4.5'
# SSP = 'SSP5-8.5'

# 结果数据编号转为日期
# path = '../CMIP6/TIF/Origin/'+type+'_'+SSP+'_World'
path = '../CMIP6/TIF/Origin/'+type+'_'+SSP
filetype = '.tif'

filelist = os.listdir(path)
# 文件名按数字部分进行排序
# filelist.sort(key=lambda x: int(x.split(type)[1].split('.tif')[0]))
print(path)
print(filelist)
# 初始赋值年月份
year = 2021
# mon = 1

for file in filelist:
    Olddir = os.path.join(path, file)
    filename = os.path.splitext(file)[0]
    print(filename)
    print(Olddir)
    Newdir = os.path.join(path, type + "_" + SSP + "_" + str(year) + filetype)
    print(Newdir)

    os.rename(Olddir, Newdir)
    print("重命名完毕")
    print("")
    year += 1

# for file in filelist:
#     Olddir = os.path.join(path, file)
#     filename = os.path.splitext(file)[0]
#     print(filename)
#     print(Olddir)
#     if int(mon) < 10:
#         Newdir = os.path.join(path, type + "_" + SSP + "_" + str(year) + '_0' + str(mon) + filetype)
#     else:
#         Newdir = os.path.join(path, type + "_" + SSP + "_" + str(year) + "_" + str(mon) + filetype)
#     print(Newdir)
#
#     os.rename(Olddir, Newdir)
#     print("重命名完毕")
#     print("")
#     mon += 1
#     if mon == 13:
#         mon = 1
#         year += 1



