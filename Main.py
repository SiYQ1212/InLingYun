from AutoSend import *
from Server import *
from solvePdf import *
import multiprocessing


if __name__ == '__main__':
    startEmail()
    # multiprocessing.Process(target=startServer, args=()).start()
    # multiprocessing.Process(target=startEmail, args=()).start()
    # sendTask()
