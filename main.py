# import the necessary packages
# importing the required libraries

from picamera.array import PiRGBArray
from picamera import PiCamera
import threading
import multiprocessing
import cv2
import numpy
import datetime
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        #self.threadID = threadID
        self.name = name
    def run(self):
        print "Sending " + self.name
        if exitFlag:
         threadName.exit()
        mailvid(self.name)
        print "Exiting " + self.name

#defining the function for mail

def mailvid(proName):
 print "Sending " + proName

 fromaddr = "jee95t@gmail.com"
 toaddr = "jeet181095@gmail.com"
 
 msg = MIMEMultipart()
 
 msg['From'] = fromaddr
 msg['To'] = toaddr
 msg['Subject'] = "SUBJECT OF THE EMAIL"
 
 body = "TEXT YOU WANT TO SEND"
 
 msg.attach(MIMEText(body, 'plain'))

 filename = proName+".avi"
 attachment = open("/home/pi/manjeet/"+filename, "rb")
 
 part = MIMEBase('application', 'octet-stream')
 part.set_payload((attachment).read())
 encoders.encode_base64(part)
 part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
 msg.attach(part)
 
 server = smtplib.SMTP('smtp.gmail.com', 587)
 server.starttls()
 server.login(fromaddr, "manjeet18")
 text = msg.as_string()
 server.sendmail(fromaddr, toaddr, text)
 server.quit()
 print "Exiting " + proName
 return

# defining the function for differential image

def diffimagefuncn(imgpast,imgpresent,imgfuture):
 diff1=cv2.absdiff(imgpast,imgpresent)
 diff2=cv2.absdiff(imgpresent,imgfuture)
 diffimg1=cv2.bitwise_and(diff1,diff2)
 ret,diffimg=cv2.threshold(diffimg1,25,255,cv2.THRESH_BINARY)
 return diffimg

# initialize the camera and grab a reference to the raw camera capture
#cap=cv2.VideoCapture(0)
if __name__ == '__main__':
 camera = PiCamera()
 camera.resolution = (640, 480)
 camera.framerate = 32
 rawCapture = PiRGBArray(camera, size=(640, 480))
 
 # allow the camera to warmup

 time.sleep(0.1)

 # capture(in raspi)/reading frames from camera
 # grab the raw NumPy array representing the image, then initialize the timestamp
 # and occupied/unoccupied text
 for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
  captframe1=frame.array
  break

 # converting frames in grayscale form

 captframe1=cv2.cvtColor(captframe1,cv2.COLOR_BGR2GRAY)
 captframe2=captframe1
 captframe3=captframe1

 # capture frames from the camera
 # calling differential image function in a loop
 # shifting frames after every comparison # type q for quiting the program
 # clear the stream in preparation for the next frame
 
 fourcc=cv2.VideoWriter_fourcc(*'MJPG')
 outgo=0
 jobs = []
 rawCapture.truncate(0)
 while True:
  print str(datetime.datetime.now())+' open1'
  #frame1 = camera.capture(rawCapture, format="bgr", use_video_port=True)
  #camera.capture(rawCapture, format="bgr")
  #frame1=rawCapture.array
  differimage=diffimagefuncn(captframe1,captframe2,captframe3)
  count=cv2.countNonZero(differimage)
  #print count
  if(count>400):
   namevid1='vid'+str(datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S"))
   namevid=namevid1+'.avi'
   out=cv2.VideoWriter(namevid,fourcc,14.0,(640,480))
   cv2.destroyAllWindows()
   print count
   print str(datetime.datetime.now())
   i=0
   rawCapture.truncate(0)
   for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    rimage=frame.array
    out.write(rimage)
    cv2.imshow("realdetect",rimage)
    i=i+1
    key1= cv2.waitKey(10)& 0xFF
    if (key1==ord('q'))or(i==70):
     if key1==ord('q'):
      outgo=1
     break
    rawCapture.truncate(0)
   cv2.destroyAllWindows()
   out.release()
   print str(datetime.datetime.now())
   #ser = multiprocessing.Process(target=mailvid, args=(namevid1))
   ser = myThread(namevid1)
   jobs.append(ser)
   #ser.daemon = True
   ser.start()
   rawCapture.truncate(0)
   for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    captframe2=frame.array
    captframe2=cv2.cvtColor(captframe2,cv2.COLOR_BGR2GRAY)
    captframe3=captframe2
    break
  cv2.imshow("motiondetect",differimage)
  rawCapture.truncate(0)
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   differimage=frame.array
   break
  cv2.imshow("realdetect",differimage)
  captframe1=captframe2
  captframe2=captframe3
  #captframe1=cap.read()[1]
  #captframe2=cap.read()[1]
  #cv2.imshow("realdetect",differimage)
  #captframe1=cv2.cvtColor(captframe1,cv2.COLOR_BGR2GRAY)
  #captframe2=cv2.cvtColor(captframe2,cv2.COLOR_BGR2GRAY)
  captframe3=cv2.cvtColor(differimage,cv2.COLOR_BGR2GRAY)
  key= cv2.waitKey(10)& 0xFF
  rawCapture.truncate(0)                               ##########
  # if the `q` key was pressed, break from the loop
  if (key == ord('q'))or(outgo==1):
   cv2.destroyAllWindows()
   break

 #end of while loop
 #cv2.destroyAllWindows()
 #################jobs[-1].terminate()
 print 'WAITING..'
 for i in jobs:
  i.join()
  #print '%s.exitcode = %s' % (i.name, i.exitcode)
 print "goodbye user"
 
