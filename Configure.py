import datetime
import base64
import json


DATA = datetime.date(2024, 8, 26)  # 每学期的第一周的第一天

SENDER = '2194887984@qq.com'  # 后期可以改成邮箱代理池

NoticeTime = "18:00"

auth_code = base64.b64decode("dmhwenhjcWtkbWh0ZGlpaA==".encode('utf-8')).decode('utf-8')

CoursePDF = "coursePdf"  # 存放pdf文件名

CtoE = {
    "星期一": "Monday",
    "星期二": "Tuesday",
    "星期三": "Wednesday",
    "星期四": "Thursday",
    "星期五": "Friday",
    "星期六": "Saturday",
    "星期日": "Sunday"
}

TIME = {
    "1-2": "8:00-9:30",
    "3-4": "9:45-11:15",
    "3-5": "9:45-12:10",
    "6-7": "14:00-15:30",
    "8-9": "15:45-17:15",
    "8-10": "15:45-18:10",
    "11-12": "19:00-20:30",
    "11-13": "19:00-21:25"
}
