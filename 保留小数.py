import json

# 读取json文件并转成字典
with open("D:\WorkSpace\Vue_WorkSpace\cmip_prediction\public\json\Area.json", "r", encoding="utf-8") as f:
    data = json.load(f)


# 遍历字典，对其中数值进行保留小数操作
def floatify(obj):
    if isinstance(obj, dict):
        return {k: floatify(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [floatify(elem) for elem in obj]
    elif isinstance(obj, float):
        return round(obj, 4)
    else:
        return obj


data = floatify(data)

# 将结果输出为json文件
with open("D:\WorkSpace\Vue_WorkSpace\cmip_prediction\public\json\Area2.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
