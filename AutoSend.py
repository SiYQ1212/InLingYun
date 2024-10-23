# -*- coding: utf-8 -*-
#!/usr/bin/python3
import os.path
import smtplib
import threading
from email.mime.text import MIMEText
from email.header import Header
import json
import schedule
import time
from Configure import *
from Function import *
from solvePdf import *


@findError
def readTimetable(jsonFile):
    """
    获取课表json数据
    :param jsonFile: str json文件名
    :return: dict 课表信息
    """
    filePath = os.path.join(os.getcwd(), CoursePDF, jsonFile + ".json")
    with open(filePath, "r", encoding="utf-8") as f:
        courseInformation = json.load(f)
    return courseInformation


@findError
def getTomorrowWeek(day):
    """
    获取明天是第几周
    :param day: datetime.date
    :return: int
    """
    return (day + datetime.timedelta(days=1) - DATA).days // 7 + 1


@findError
def getTomorrowAllCourse(courseInfomation):
    """
    获取明日总课表信息
    :param courseInfomation: dict{str: list}
    :return: list[str, str, dict]
    """
    today = (datetime.datetime.now() + datetime.timedelta(days=0)).strftime('%A')
    days = list(courseInfomation.keys())
    tomorrow_index = (days.index(today) + 1) % len(days)
    tomorrow = days[tomorrow_index]
    return courseInfomation[tomorrow]


@findError
def checkCourse(courseInformation, tomorrowWeek):
    """
    根据明日位于第几周判断明日总课表是否上
    :param courseInformation: str 哪些周上课
    :param tomorrowWeek: int
    :return: bool
    """
    haveWeek = set()
    solveDate = courseInformation.split(',')
    for week in solveDate:
        if '-' in week:
            if '单' in week:
                s, e = map(int, week[:-4].split('-'))
                for i in range(s, e + 1, 2):
                    haveWeek.add(i)
            elif '双' in week:
                s, e = map(int, week[:-4].split('-'))
                for i in range(s, e + 1, 2):
                    haveWeek.add(i)
            else:
                s, e = map(int, week[:-1].split('-'))
                for i in range(s, e + 1):
                    haveWeek.add(i)
        else:
            haveWeek.add(int(week[:-1]))
    return tomorrowWeek in haveWeek


@findError
def modifyMessage(tomorrowAllCourse, tomorrowWeek):
    """
    筛选出明日确定课表
    :param tomorrowAllCourse: list[str, str, dict]
    :param tomorrowWeek: int
    :return: list[str]
    """
    sendInformation = []
    for course in tomorrowAllCourse:
        if checkCourse(course[2]['周数'], tomorrowWeek):
            sendInformation.append(course)
    return ["%s\n%s\n%s\n%s" % (TIME[speak[0]], speak[2]['地点'], speak[2]['教师'], speak[1]) for speak in sendInformation]


@findError
def dealInformation(name):
    """
    整合上述所有信息处理函数
    :param name: str
    :return: list[str]
    """
    allCourse = readTimetable(name)  # 获取课表信息
    tomorrowWeek = getTomorrowWeek(datetime.date.today())  # 获取明天周数
    tomorrowCourse = getTomorrowAllCourse(allCourse)  # 获取明日课表
    if not tomorrowCourse:
        return []
    messages = modifyMessage(tomorrowCourse, tomorrowWeek)  # 筛选明日要上的课
    if not messages:
        return []
    return messages


@findError
def sendProcess(sendMessage, receiver):
    """
    发送邮件功能
    :param sendMessage: str
    :param receiver: str
    :return:
    """
    message = MIMEText(sendMessage, 'plain', 'utf-8')
    message['From'] = Header("SIYU<%s>" % SENDER)  # 发送者
    message['To'] = Header("Receiver<%s>" % receiver)  # 接收者
    subject = '明日课程'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(SENDER, auth_code)
        server.sendmail(SENDER, receiver, message.as_string())
        server.close()
        logSend(f"Send Successfully to {receiver}")
        return True
    except smtplib.SMTPException as e:
        logSend(f"Fail to Send {receiver} and Error:{e}")
        return False


def sendTask():
    Receiver = getReceiver()
    # print(Receiver)
    for name in Receiver.keys():
        try:
            filePath = os.path.join(os.getcwd(), CoursePDF, name + ".json")
            with open(filePath, "r", encoding="utf-8") as f:
                ...
        except:
            pdfToText(name)

    for name in Receiver.keys():
        massage = dealInformation(name)
        if massage:
            # 单开一个线程进行邮件发送
            threading.Thread(target=sendProcess, args=("\n\n\n".join(massage), Receiver[name])).start()


def startEmail():
    # sendTask()
    while 1:
        try:
            schedule.every().day.at(NoticeTime).do(sendTask)
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except Exception as e:
            logError(f"{e}")
            continue


if __name__ == "__main__":
    ...
