import cv2 as cv

cap = cv.VideoCapture(0)
tracker = cv.legacy.TrackerMOSSE_create()
isTrue,img = cap.read()
bbox = cv.selectROI("Tracking",img,False)
tracker.init(img,bbox)
def drawBox(img,bbox):
    x,y,w,h =  int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv.rectangle(img , (x,y),(x+w,y+h),(0,0,255),3,1)
    cv.putText(img , str("Tracking") , (75,95),cv.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
while True:
    timer = cv.getTickCount()
    isTrue,img = cap.read()
    isTrue,bbox = tracker.update(img)
    if isTrue:
        drawBox(img,bbox)
    else:
        cv.putText(img , str("Lost") , (75,75),cv.FONT_HERSHEY_COMPLEX,0.7,(255,0,0),2)
    fps = cv.getTickFrequency()/(cv.getTickCount()-timer)
    cv.putText(img , str(int(fps)) , (75,50),cv.FONT_HERSHEY_COMPLEX,0.7,(255,0,0),2)
    cv.imshow("Webcam" , img)
    if cv.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()