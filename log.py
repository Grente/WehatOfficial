# coding: utf-8


import time
import os

LOGPATH = "log/"

if not globals().has_key("g_LogFile"):
    g_LogFile = None
    

def OutputLog(file_name, message):
    global g_LogFile
    if not os.path.exists(LOGPATH):
        os.mkdir(LOGPATH)
    
    fp = None
    now = time.time()
    if g_LogFile:
        fp, filepath, day = g_LogFile
        if day != int(now / 3600) or not os.path.exists(filepath):
            fp.close()
            fp = None
    
    if fp is None:
        prefix = time.strftime("%m-%d", time.localtime(now))
        filepath = LOGPATH+"/%s_%s.log"%(prefix, file_name) 
        fp = open(filepath, "a")
        day = now/3600
        g_LogFile = (fp, filepath, day)
    
    fp.write(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime(now)) + message + "\n")
    fp.flush()


RUNNLOG = lambda x:OutputLog("Log", x)
ERRORLOG = lambda x:OutputLog("Error", x)

