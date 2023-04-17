import os

# 解决日期编号排序问题
path = 'TIF\R20'
filetype = '.tif'

filelist = os.listdir(path)
year = 2021
mon = 1
for file in filelist:
    Olddir = os.path.join(path, file)
    filename = os.path.splitext(file)[0]
    x = filename.split("_")
    print(Olddir)

    if int(x[2]) < 10:
        Newdir = os.path.join(path, "R20_" + str(year) + '_0' + x[2] + filetype)
    else:
        Newdir = os.path.join(path, "R20_" + str(year) + "_" + x[2] + filetype)
    print(Newdir)

    os.rename(Olddir, Newdir)
    print("重命名完毕")
    print("")
    mon += 1
    if mon == 13:
        mon = 1
        year += 1


