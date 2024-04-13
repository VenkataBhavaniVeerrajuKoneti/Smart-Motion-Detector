#Motion_Detector.py
# Python program to implement  
# Webcam Motion Detector 
import cv2

from datetime import datetime 

r_frame = None

motion_list = [ None, None ] 

time = []

video = cv2.VideoCapture(0)

frame_width = int(video.get(3))

frame_height = int(video.get(4))

c=1

while True:
    check, frame = video.read()
    
    motion = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

    gray = cv2.GaussianBlur(gray, (21, 21), 0)  

    if r_frame is None: 
        r_frame = gray 
        continue

    diff_frame = cv2.absdiff(r_frame, gray) 
 
    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
    
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) 

    cnts,_ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
  
    for contour in cnts: 
        if cv2.contourArea(contour) < 10000: 
            continue
        motion = 1
  
        (x, y, w, h) = cv2.boundingRect(contour) 

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
  
    motion_list.append(motion)

    if motion_list[-1] == 1 and motion_list[-2] == 0: 
        time.append(datetime.now())
        
        video_object = cv2.VideoWriter('Data/Video%d.avi'%(c),cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))
        
    if motion:
        video_object.write(frame)
        
    if motion_list[-1] == 0 and motion_list[-2] == 1: 
        time.append(datetime.now())
        
        video_object.release()
        
        c = c+1
    
 
    cv2.imshow("Gray Frame", gray) 

    cv2.imshow("Difference Frame", diff_frame) 
 
    cv2.imshow("Threshold Frame", thresh_frame) 
 
    cv2.imshow("Color Frame", frame) 
  
    key = cv2.waitKey(1) 
 
    if key == ord('q'): 
        if motion == 1: 
            time.append(datetime.now())
            video_object.release()
        break
video.release()

f=open("Data.txt","w")
f.write("\tStart Time\t\tEnd Time\n")
for i in range(0, len(time), 2):
    f.write(str(time[i])[:19]+"\t\t"+str(time[i + 1])[:19]+"\n")
f.close()
cv2.destroyAllWindows() 
