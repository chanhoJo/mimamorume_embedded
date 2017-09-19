from paramiko import SSHClient
from scp import SCPClient
import paramiko
from picamera import PiCamera
from time import sleep
import serial
import os

camera = PiCamera()
ser = serial.Serial('/dev/ttyACM0', 9600)

def fileCount():
    imageCount = 0
    for root, dirs, files in os.walk('/home/pi/Documents/camera/images'):
        if files is not None:
            for file in files:
                imageCount += 1
    return imageCount

def sendImageToAWS(imageCount):
    ipAddress = '133.130.99.167'
    name = 'root'
    pw = 'mimamo123'

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ipAddress, username = name, password = pw)

    scp = SCPClient(ssh.get_transport())
    scp.put('/home/pi/Documents/camera/images/2-3-%s.jpg' %imageCount, '/root/gohtml/mimamo/public/images/monitor/snapShot')
    
    scp.close()

def cameraCaptureSensing():
    imageNum = fileCount()
    camera.capture('/home/pi/Documents/camera/images/2-3-%s.jpg' %imageNum)
    sendImageToAWS(imageNum)
    
#shooting


while True:
    try:
        sensorValue = int(ser.readline(), base=10)
        
        #camera.start_preview()
        if sensorValue == 1:
            cameraCaptureSensing()
            os.system('python php.py')
            print "yes"
        else:
            print "no"
    except serial.serialutil.SerialException:
        continue
    except paramiko.ssh_exception:
        continue

    
    
