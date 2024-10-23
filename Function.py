#!/usr/bin/python3
import datetime
import inspect
import os.path


def logError(info: str):
    """
    错误日志
    :param info:
    :return:
    """
    with open(os.path.join(os.getcwd(), "logs", "error.log"), "a+", encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now()}: {info} \n")


def logServer(info: str):
    """
    活动日志
    :param info:
    :return:
    """
    with open(os.path.join(os.getcwd(), "logs", "server.log"), "a+", encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now()}: {info} \n")


def logSend(info: str):
    """
    邮件发送日志
    :param info:
    :return:
    """
    with open(os.path.join(os.getcwd(), "logs", "send.log"), "a+", encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now()}: {info} \n")


def getCurrentFileName(file):
    """
    获取当前运行该函数的文件名称
    :param file:
    :return:
    """
    return file.split("\\")[-1].split(".")[0]


def getReceiver():
    """
    获取name 和 email的关系
    :return:
    """
    filePath = os.path.join(os.getcwd(), CoursePDF, "nameEmail.json")
    try:
        with open(filePath, "r", encoding="utf-8") as f:
            receiver = json.load(f)
        return receiver
    except:
        return {}


def findError(func):
    """
    函数报错检测器
    :param func:
    :return:
    """
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            filename = getCurrentFileName(inspect.getsourcefile(func))
            logError(f"<{filename}> [{func.__name__}] Occurred: {e}")
            return False
    return inner



