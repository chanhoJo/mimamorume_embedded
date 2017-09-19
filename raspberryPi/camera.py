from paramiko import SSHClient
from scp import SCPClient
import paramiko
from picamera import PiCamera
from time import sleep
import os

camera = PiCamera()

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
    ssh.connect(ipAddress, username=name, password=pw)

    scp = SCPClient(ssh.get_transport())

    scp.put('/home/pi/Documents/camera/images/3-1-%s.jpg' %imageCount, '/root/gohtml/mimamo/public/images/monitor/snapShot')


def cameraCaptureTime():
    imageNum = fileCount()
    camera.capture('/home/pi/Documents/camera/images/3-1-%s.jpg' %imageNum)
    sendImageToAWS(imageNum)

while True:
    cameraCaptureTime()
    os.system('python php.py')
    sleep(180)
