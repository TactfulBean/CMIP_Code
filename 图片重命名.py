import os

# path = 'F:\image\MC'
path = "G:\海绵宝宝\海绵宝宝 第02季"
# filetype = '.jpg'
season = "SE02_"
filetype = '.mp4'
filelist = os.listdir(path)
# num = 1

for file in filelist:
    Olddir = os.path.join(path, file)
    filename = os.path.splitext(file)[0].split(' ')[1].split("第")[1].split("集")[0]
    if int(filename) < 10:
        Newdir = os.path.join(path, season + "00" + str(filename) + filetype)
    elif int(filename) >= 100:
        Newdir = os.path.join(path, season + str(filename) + filetype)
    else:
        Newdir = os.path.join(path, season + "0" + str(filename) + filetype)
    print(Newdir)
    # print(filename)
    # print("")
    os.rename(Olddir, Newdir)
    # num += 1
