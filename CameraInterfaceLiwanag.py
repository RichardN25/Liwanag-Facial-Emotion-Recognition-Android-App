from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.core.window import Window
from skimage.transform import resize
from skimage.feature import hog
from skimage import feature
import cv2
import os
import numpy as np
import pickle
import threading
import time

Window.size = (300,500)

class LocalBinaryPatterns:
    def __init__(self, numPoints, radius):
        # store the number of points and radius
        self.numPoints = numPoints
        self.radius = radius

    def describe(self, image, eps=1e-7):

        lbp = feature.local_binary_pattern(image, self.numPoints, self.radius, method="uniform")
        (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, self.numPoints + 3), range=(0, self.numPoints + 2))
 
        hist = hist.astype("float")
        hist /= (hist.sum() + eps)
 
        return hist

class MainApp(MDApp):
    # Specify the directory Method 1
    cascPathface = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
    faceCascade = cv2.CascadeClassifier(cascPathface)


    Categories = ['Anger', 'AngrilyDisgusted', 'AngrilySurprised', 'Disgust', 
            'DisgustedlySurprised', 'Fear', 'FearfullyAngry', 'FearfullySurprised',
              'HappilyDisgusted', 'HappilySurprised', 'Happiness', 'Neutral',
              'SadlyAngry', 'SadlyDisgusted', 'SadlyFearful', 'SadlySurprised',
              'Sadness', 'Surprise']

    l=[]
    x = None
    y = None
    w = None
    h = None
    fr = None
    emotion = None
    hist = None
    sec=0
    counter = 0
    frame = None
    with_rectangle = None
  
    desc = LocalBinaryPatterns(24, 8)
    model = pickle.load(open('img_model6_15k_hog_lbp.p','rb'))

    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        self.image = Image()
        layout.add_widget(self.image)
        layout.add_widget(MDRaisedButton(
            text="CLICK HERE",
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(None, None))
        )
        self.capture = cv2.VideoCapture(0)

        Clock.schedule_interval(self.load_video, 0.00001)

        Clock.schedule_interval(self.recognition, 20)


        return layout

    

    def load_video(self, *args):
     
        ret, frame = self.capture.read()
        self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
     

        faces = self.faceCascade.detectMultiScale(self.gray,
                                                scaleFactor=1.2,
                                                minNeighbors=10,
                                                minSize=(64, 64),
                                                flags=cv2.CASCADE_SCALE_IMAGE)

       
        for (x,y,w,h) in faces:
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.with_rectangle = cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h),(0,255,0), 2)
           

        if self.with_rectangle is not None:
            buffer = cv2.flip(self.with_rectangle, 0).tostring()  
            texture = Texture.create(size=(640, 480), colorfmt ='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture
            self.with_rectangle = None
        else:
            buffer = cv2.flip(frame, 0).tostring()  
            texture = Texture.create(size=(640, 480), colorfmt ='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture



    def recognition(self, *args):

        if self.x is not None and self.gray is not None:
            faceROI = self.gray[self.y:self.y+self.h,self.x:self.x+self.w]

            resized_img = resize(faceROI, (128,64))
            fd, hog_image = hog(resized_img, orientations=9, pixels_per_cell=(8, 8),cells_per_block=(2, 2), visualize=True, multichannel=False)
            self.hist = self.desc.describe(resized_img)
            feat = np.hstack([fd,self.hist])
            self.l = [feat]
            print("The pedicted image is: "+self.Categories[self.model.predict(self.l)[0]])
            self.gray = None
            self.x = None
            self.y = None
            self.w = None
            self.h = None
            


if __name__ == "__main__":
    MainApp().run()
