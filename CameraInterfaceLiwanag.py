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
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

    Categories = ['Anger', 'AngrilyDisgusted', 'AngrilySurprised', 'Disgust', 
            'DisgustedlySurprised', 'Fear', 'FearfullyAngry', 'FearfullySurprised',
              'HappilyDisgusted', 'HappilySurprised', 'Happiness', 'Neutral',
              'SadlyAngry', 'SadlyDisgusted', 'SadlyFearful', 'SadlySurprised',
              'Sadness', 'Surprise']

    desc = LocalBinaryPatterns(24, 8)
    model = pickle.load(open('trained_model.p','rb'))

    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        self.image = Image()
        layout.add_widget(self.image)
        layout.add_widget(MDRaisedButton(
            text="CLICK HERE",
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(None, None))
        )
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.load_video, 1.0/33.0)
        return layout

    def load_video(self, *args):
        ret, frame = self.capture.read()
        # Unsure about this vvvvv
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray,
                                                scaleFactor=1.1,
                                                minNeighbors=5,
                                                minSize=(60, 60),
                                                flags=cv2.CASCADE_SCALE_IMAGE)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h),(0,255,0), 2)
            faceROI = gray[y:y+h,x:x+w]

            resized_img = resize(faceROI, (128,64))
            fd, hog_image = hog(resized_img, orientations=9, pixels_per_cell=(8, 8),cells_per_block=(2, 2), visualize=True, multichannel=False)
            hist = self.desc.describe(resized_img)
            feat = np.hstack([fd,hist])
            l = [feat]
            #probability = self.model.predict_proba(l)
            #for ind,val in enumerate(self.Categories):
            #    print(f'{val} = {probability[0][ind]*100}%')
            print("The predicted image is : "+self.Categories[self.model.predict(l)[0]])

        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

if __name__ == "__main__":
    MainApp().run()
