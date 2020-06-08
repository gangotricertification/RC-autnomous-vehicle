import cv2
import numpy as np
import matplotlib.pyplot as plt

def prepro(frame):
    frame = cv2.resize(frame,(640,420),interpolation = cv2.INTER_AREA)

    frame1=frame.copy()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(3,3),0)
    canny=cv2.Canny(blur,50,150)

    mask=np.zeros_like(canny)
    polygons=np.array([[(0,420),(0,130),(640,130),(640,420)]])
    mask=cv2.fillPoly(mask,polygons,255)
    masked_image=cv2.bitwise_and(canny,mask)
    imagem=cv2.bitwise_not(masked_image)

    lines = cv2.HoughLinesP(masked_image,1,np.pi/180,100,minLineLength=100,maxLineGap=50)
    try:
        left_line=[]
        right_line=[]
        for i in range(0,lines.shape[0]):
            x1,y1,x2,y2=lines[i][0]
            try:
                parameters=np.polyfit((x1,x2),(y1,y2),1)
                slope=parameters[0]
                intercept=parameters[1]
                if slope<0:
                    left_line.append((slope,intercept))
                else:
                    right_line.append((slope,intercept))
            except:
                continue
        
        l = False
        r = False
        if len(left_line) == 0:
            l = True
        else:
            left_avg=np.average(left_line,axis=0)
            left_x1=int((420-left_avg[1])/left_avg[0])
            left_x2=int((130-left_avg[1])/left_avg[0])
            #print("l",left_avg)
        if len(right_line) == 0:
            r = True
        else:
            right_avg=np.average(right_line,axis=0)
            right_x1=int((420-right_avg[1])/right_avg[0])
            right_x2=int((130-right_avg[1])/right_avg[0])
            #print("r",right_avg)

        if l == False and r == False:
            x11 = int((left_x1+right_x1)/2)
            x22 = int((left_x2+right_x2)/2)

            
            #cv2.line(frame,(x11,420),(x22,130),(123,234,231),5)
            #cv2.line(frame,(320,420),(320,130),(0,255,255),10)
            final_m = np.polyfit((x11,x22),(420,130),1)

            #cv2.line(frame,(left_x1,420),(left_x2,130),(120,255,255),10)
            #cv2.line(frame,(right_x1,420),(right_x2,130),(0,255,255),10)
        ret = []
        if l == False and r == False:
            #cv2.imshow("Fd",frame)
        
            if final_m[0]>0:
                ret.append('left')
                angle_with_y = 90-np.degrees(np.arctan(final_m[0]))
                ret.append(angle_with_y)
                #cv2.imshow("fds",frame)
                return ret
            else:
                ret.append('right')
                angle_with_y = 90-(-1*np.degrees(np.arctan(final_m[0])))
                ret.append(angle_with_y)
                #cv2.imshow("fds",frame)
                return ret
        elif l == True:
##            x2 = 320
##            y1 = 130
##            y2 = 420
##            sl = -1
##            x1 = ((y2-y1)/sl) + x2
##            cv2.line(frame,(int(x1),y1),(x2,y2),(120,255,255),10)
##            print("SDF")
            #cv2.imshow("Fd",frame)
            ret.append('left')
            angle_with_y = 35
            ret.append(angle_with_y)
            return ret
            
        else:
##            x2 = 320
##            y1 = 130
##            y2 = 0
##            sl = 1
##            x1 = ((y2-y1)/sl) + x2
##            cv2.line(frame,(int(x1),y1),(x2,y2),(120,255,255),10)
            #cv2.imshow("Fd",frame)
            ret.append('right')
            angle_with_y = 35
            ret.append(angle_with_y)
            return ret
    except:
        pass

#frame = cv2.imread(r"C:\Users\ashum\Desktop\lane.png")
##print("sdf")
##cap = cv2.VideoCapture(0)
##while(True):
##    ret,frame = cap.read()
##    a = prepro(frame)
##    print(a)
