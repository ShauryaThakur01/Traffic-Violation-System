import cv2
import time
import database
from plate import plate_detection
import os

cwd = os.getcwd()
print(cwd)

cascade_src = os.path.join(cwd,'speeding\\cars1.xml')
#line a
ax1=378
ay=115
ax2=793
#line b
bx1=350
by=195
bx2=793
#car num
i = 1
car_cascade = cv2.CascadeClassifier(cascade_src)
def Speed_Cal(time):
    #Here i converted m to Km and second to hour then divison to reach Speed in this form (KM/H) 
    #the 9.144 is distance of free space between two lines # found in https://news.osu.edu/slow-down----those-lines-on-the-road-are-longer-than-you-think/
    #i know that the 9.144 is an standard and my video may not be that but its like guess and its need Field research
    try:
        Speed = (80*3600)/(time*1000)
        return Speed
    except ZeroDivisionError:
        print (5)

def detect(img,start_time,speedviolated):
    #bluring to have exacter detection
    blurred = cv2.blur(img,ksize=(15,15))
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 2)
    
    for (x,y,w,h) in cars:
        while int(ay) == int((y+y+h)/2):
            start_time = time.time()
            break
            
        while int(ay) <= int((y+y+h)/2):
            if int(by) <= int((y+y+h)/2)&int(by+10) >= int((y+y+h)/2):
                cv2.line(img,(bx1,by),(bx2,by),(0,255,0),2)
                Speed = Speed_Cal(time.time() - start_time)
                print("Car Number "+" Speed: "+str(Speed))
                if Speed>20:
                    plate_number = plate_detection.detect(img[y:y+h,x:x+w])
                    if plate_number not in speedviolated and plate_number!=None:
                        speedviolated.append(plate_number)
                        database.insert_data(plate_number,0,0,1,0)
                return speedviolated
                #cv2.putText(img, "Speed: "+str(Speed)+"KM/H", (x,y-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),3);
                break
            else:
                break