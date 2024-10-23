# -*- coding: utf-8 -*-
import json
import socket
import threading
import os
import time

from Function import *

IP = "127.0.0.1"
PORT = 12312

CoursePDF = "coursePdf"


def handleClient(conn, addr):
    logServer(f"Connect from: {addr}")

    # 接收字符串pdfName
    pdfNameLength = int(conn.recv(10).decode())
    pdfName = conn.recv(pdfNameLength).decode()

    # 接收字符串email
    emailLength = int(conn.recv(10).decode())
    email = conn.recv(emailLength).decode()

    Receiver = getReceiver()
    Receiver[pdfName] = email
    with open("nameEmail.json", "w", encoding="utf-8") as f:
        json.dump(Receiver, f, ensure_ascii=False, indent=4)

    # 接收PDF文件
    pdf_length = int(conn.recv(10).decode())
    received_data = b''

    while len(received_data) < pdf_length:
        data = conn.recv(1024)
        if not data:
            break
        received_data += data

    if received_data[:4] == b'%PDF':
        currentPath = os.getcwd()
        filePath = os.path.join(currentPath, CoursePDF, pdfName + '.pdf')
        with open(filePath, 'wb') as f:
            f.write(received_data)
        logServer(f"From {email} received {pdfName}.pdf")
    else:
        logServer(f"Failed to receive PDF from {email}\n\n")

    conn.close()


def startServer():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    logServer("Server Startup...\n\n")
    try:
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handleClient, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        logError("Server Shutting Down")
    finally:
        server_socket.close()
        print("Server socket closed")



if __name__ == "__main__":
    startServer()
