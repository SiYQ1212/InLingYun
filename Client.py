import socket
import re


# IP = "123.56.113.94"
IP = "127.0.0.1"
PORT = 12312

def isValidEmail(email):
    # 定义邮箱正则表达式
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sendInfoToS(pdfName, emailAd, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    # 发送pdfName
    client_socket.sendall(f"{len(pdfName):010d}".encode())  # 发送pdfName的长度
    client_socket.sendall(pdfName.encode())

    # 发送emailAd
    client_socket.sendall(f"{len(emailAd):010d}".encode())  # 发送emailAd的长度
    client_socket.sendall(emailAd.encode())

    # 发送PDF文件
    with open(filename, 'rb') as f:
        data = f.read()
        client_socket.sendall(f"{len(data):010d}".encode())  # 发送PDF文件的长度
        client_socket.sendall(data)

    client_socket.close()

if __name__ == "__main__":
    name, email, pdf = input().split()
    while isValidEmail(email) == False:
        """
        邮箱不正常反馈
        """
        name, email, pdf = input().split()
    sendInfoToS(name, email, pdf)  # 替换为实际数据
