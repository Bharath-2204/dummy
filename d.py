import numpy as np
import cv2
import streamlit as st
from PIL import Image
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration


  
para = cv2.aruco.DetectorParameters_create()
aru_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_100)    #aruco dictionary
def predict(img):
                          Thr=[100,200]
                          image_greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                             #Finding the contours and processing the image
                          image_blur = cv2.GaussianBlur(img,(5,7),0)
                          imagecanny = cv2.Canny(image_blur,Thr[0],Thr[1])
                          kernel = np.ones((2,2)) 
                          imgDial = cv2.dilate(imagecanny,kernel,iterations=3)
                          iThre = cv2.erode(imgDial,kernel,iterations=2)
                          thresh, image_black = cv2.threshold(image_greyscale, 100,100,cv2.THRESH_BINARY)

                          corners, _, _ = cv2.aruco.detectMarkers(img, aru_dict, parameters=para)
                          if corners:
                              int_corners = np.int0(corners)
                              cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
                              contours, _ = cv2.findContours(iThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                              aru_peri = cv2.arcLength(corners[0], True)

                              pix_cm_rat = aru_peri / 20          #Obtaining pixel to cm ratio using the aruco marker
                              for contour in contours:
                                  area = cv2.contourArea(contour)
                                  if area > 2500:                 #The contours/edges of objects will be drawn only if their area is above 2500

                                      rect = cv2.minAreaRect(contour)
                                      (x,y), (w,h), angle = rect



                                      box = cv2.boxPoints(rect)
                                      box = np.int0(box)


                                      wide =h/pix_cm_rat
                                      tall =w/pix_cm_rat
                                      cv2.circle(img,(int(x),int(y)),5,(0,0,255), -1)
                                      cv2.polylines(img,[box],True,(0,255,0),2)
                                      cv2.putText(img,"Width : {}".format(round(wide,2)),(int(x),int(y - 15)), cv2.FONT_HERSHEY_PLAIN,3,(0,0,100),3)
                                      cv2.putText(img,"Height : {}".format(round(tall,2)),(int(x),int(y - 100)), cv2.FONT_HERSHEY_PLAIN,3,(0,0,100),3)

                          return cv2.flip(img, 1)        
class VideoCapture:
      def recv(self, frame):
       
          img = frame.to_ndarray(format="bgr24")

          img = predict(img)

          return av.VideoFrame.from_ndarray(cv2.flip(img,1), format="bgr24")

webrtc_streamer(
    key="TEST",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}),
    media_stream_constraints={"video": True, "audio": False},
    video_processor_factory=VideoCapture,
    async_processing=True,
)


                                                            
                                
                       
                        


        
    
       


  
