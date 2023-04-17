import requests
import json

# 设置GeoServer的用户名和密码
username = 'admin'
password = 'geoserver'

# 设置GeoServer的URL地址和工作空间
geoserver_url = "http://localhost:8080/geoserver"
workspace = "CMIP"

# type = "CSDI"
# type = "WSDI"
# type = "TN10P"
# type = "TN90P"
# type = "TX10P"
# type = "TX90P"
type = "CDD"
# type = "CWD"

SSP = 'SSP1-2.6'
# SSP = 'SSP2-4.5'
# SSP = 'SSP5-8.5'

# 设置数据存储的名称和描述
store_name = type + '_' + SSP + '_MK_SEN'
store_description = ""

# 设置数据存储的URL地址和数据类型
store_url = 'file://D:\WorkSpace\Python_WorkSpace\CMIP_Test\CMIP6\TIF\ME_SEN\China\CDD\CDD_' + SSP + '_MK_SEN.tif'
store_type = "GeoTIFF"

# 创建认证基础验证的请求会话
session = requests.Session()
session.auth = (username, password)

# 定义要发送的JSON数据
json_data = {
    "dataStore": {
        "name": store_name,
        "description": store_description,
        "connectionParameters": {
            "entry": [
                {
                    "@key": "url",
                    "$": store_url
                },
                {
                    "@key": "type",
                    "$": store_type
                }
            ]
        }
    }
}

# 设置请求的URL
store_url = "{}/rest/workspaces/{}/datastores.json".format(geoserver_url, workspace)

# 发送请求并获取响应
response = session.post(store_url, json=json_data)

# 检查响应状态码，如果是201表示成功添加数据存储
if response.status_code == 201:
    print("Data store added successfully")
else:
    print("Error adding data store")
