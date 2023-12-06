import cv2

cap=cv2.VideoCapture(2)
mycascade=cv2.CascadeClassifier('/home/gizemgunes/ros2_ws/src/camera/camera/cascade/haarcascade_frontalface_default.xml')
font1=cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    pencils=mycascade.detectMultiScale(gray,1.3,7)
    for (x,y,w,h) in pencils:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(frame,"FACE",(x,y),font1,1,(255,0,0), cv2.LINE_4)

        if cv2.rectangle:
            print("yüz var")

    cv2.imshow("face",frame)

    if cv2.waitKey(1) & 0xFF==ord("q"):
      break

cap.release()
cv2.destroyAllWindows()