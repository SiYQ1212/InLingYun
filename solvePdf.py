import os
from Configure import *
from Function import *
import json
import fitz
import re


def pdfToText(pdfName):
    """
    提取PDF文件文本内容
    :param pdfName: str pdf文件名,不包含.pdf
    :return: bool 是否提取成功
    """
    try:
        filePath = os.path.join(os.getcwd(), CoursePDF, pdfName + ".pdf")
        pdf = fitz.open(filePath)
        contents = ""
        for page in pdf:
            contents += page.get_text()

        courseInformation = contents.split('\n')[3:-3]
        courseInformation = courseInformation
        # 暂时存放课程信息
        timetable = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": [],
            "Sunday": []
        }
        PAT = re.compile(r"\d+-\d+")
        Week = CtoE[courseInformation[0]]
        ClassHour = ""

        while len(courseInformation) >= 3:
            week = courseInformation[0]
            # 判断week格式是否为 "星期X"
            if CtoE.get(week) in timetable:
                Week = CtoE[courseInformation.pop(0)]
            classHour = courseInformation[0]
            # 判断classHour格式是否为 "X-X"
            if PAT.match(classHour):
                ClassHour = courseInformation.pop(0)
            courseName, detailedInformation, wasteInfomation = courseInformation.pop(0), courseInformation.pop(0), courseInformation.pop(0)
            if "学分" not in wasteInfomation:
                courseInformation.pop(0)

            newDetailedInformation = {}
            detailedInformation = detailedInformation.split()[:6]
            for key in range(0, len(detailedInformation), 2):
                newDetailedInformation[detailedInformation[key][:-1]] = detailedInformation[key + 1]
            timetable[Week].append([ClassHour, courseName, newDetailedInformation])

        filePath = os.path.join(os.getcwd(), CoursePDF, pdfName + ".json")
        with open(filePath, "w", encoding="utf-8") as f:
            json.dump(timetable, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        logError(e)
        return False


if __name__ == '__main__':
    for name in Receivers.keys():
        try:
            filePath = os.path.join(os.getcwd(), CoursePDF, name + ".json")
            with open(filePath, "r", encoding="utf-8") as f:
                ...
        except:
            pdfToText(name)