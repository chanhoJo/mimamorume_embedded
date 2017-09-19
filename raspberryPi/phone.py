#transmit
from paramiko import SSHClient
from scp import SCPClient
import paramiko
#camera
from picamera import PiCamera
from time import sleep
#socket
import socket
#count
import os
import select
 
camera = PiCamera()
HOST = ''
PORT = 5227

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

#file count
def fileCount():
    imageCount = 0
    for root, dirs, files in os.walk('/root/Documents/image'):
        if files is not None:
            for file in files:
                imageCount += 1
    return imageCount

#image send
def sendImageToAWS(imageCount):
    ipAddress = '133.130.99.167'
    name = 'root'
    pw = 'mimamo123'

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ipAddress, username=name, password=pw)

    scp = SCPClient(ssh.get_transport())

    scp.put('/root/Documents/image/1-2-%s.jpg' %imageCount , '/root/gohtml/mimamo/public/images/monitor/snapShot')        
  

#shooting image    
try :
    while True:

        while 1:
            newClient,_,_ = select.select([s],[],[], 60)
            imageNum = fileCount()
            conn, addr = s.accept()
            
            readable,_,_ = select.select([conn],[],[],60)
            if (readable):
                data = conn.recv(1024)
                
                if data == "123\n":
                    camera.capture('/root/Documents/image/1-2-%s.jpg' %imageNum)
                    sendImageToAWS(imageNum)
                    os.system('python php.py')
except KeyboardInterrupt:
    pass