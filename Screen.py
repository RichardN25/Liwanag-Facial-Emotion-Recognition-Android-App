from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from plyer import tts, vibrator
import time

class SplashScreen(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.switch_to_home, 5)

    def switch_to_home(self, *args):
        self.manager.current = 'home'

class HomeScreen(Screen):
    id = 1

    def on_enter(self):
        self.start1()

    def start1(self, *args):

        if self.id > 6:
           self.manager.current = 'feedback'
           return

        anim = Animation(opacity=1, duration=1)
        anim += Animation(opacity=1, duration=3)
        anim += Animation(opacity=0, duration=1)
        anim.bind(on_complete=self.start1)
        anim.start(self.ids[f"text{self.id}"])

        if self.id == 1: 
            tts.speak("Hello")
            time.sleep(1)
            self.id +=1
        elif self.id == 2:
            tts.speak("Welcome to Liwanag")
            time.sleep(0.5)
            self.id +=1
        elif self.id == 3:
            tts.speak("We offer 2 feedback features for you to choose from. Please choose an option after hearing the beep sound")
            time.sleep(0.5)
            self.id +=1
        elif self.id == 4:
            tts.speak("Swipe left for text-to-speech feedback")
            time.sleep(0.5)
            self.id +=1
        elif self.id == 5:
            tts.speak("Swipe right for patterned vibrations feedback")
            time.sleep(0.5)
            self.id +=1
        elif self.id == 6:
            tts.speak("Double tap for the tutorial of the pattern vibrations")
            time.sleep(0.5)
            self.id += 1
           

class FeedbackOption(Screen):
    def on_enter(self):
        sound = SoundLoader.load('beep02.wav')
        sound.play()

    def on_touch_move(self, touch):
        if touch.x < touch.ox: # this line checks if a left swipe has been detected
            self.manager.current = 'tts'
         
        elif touch.ox < touch.x: # this line checks if a right swipe has been detected
            self.manager.current = 'vibrate'

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.manager.current = 'demo'
            

class TextToSpeechScreen(Screen):
    def on_touch_move(self, touch):
        if touch.ox < touch.x: # this line checks if a right swipe has been detected
            self.manager.current = 'vibrate'

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.manager.current = 'feedback'

class VibrationPatternScreen(Screen):
    def on_touch_move(self, touch):
        if touch.x < touch.ox: # this line checks if a left swipe has been detected
            self.manager.current = 'tts'

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.manager.current = 'feedback'


class DemoScreen(Screen):
    id = 1

    def on_enter(self):
        print("hello1")
        self.start1()

    def start1(self, *args):
        print(self.id)

        if self.id == 1: 
            self.happyVibrate()
        elif self.id == 2:
            self.neutralVibrate()
        elif self.id == 3:
            self.sadnessVibrate
        elif self.id == 4:
            self.disgustVibrate()
        elif self.id == 5:
            self.fearVibrate()
        elif self.id == 6:
            self.surpriseVibrate()
        elif self.id == 7:
            self.angerVibrate()
        elif self.id == 8:
            self.happilySurprisedVibrate()
        elif self.id == 9:
            self.happilyDisgustedVibrate()
        elif self.id == 10:
            self.sadlyFearfulVibrate()
        elif self.id == 11:
            self.sadlyAngryVibrate()
        elif self.id == 12:
            self.sadlySurprisedVibrate()
        elif self.id == 13:
            self.sadlyDisgustedVibrate()
        elif self.id == 14:
            self.fearAngryVibrate()
        elif self.id == 15:
            self.fearSurprisedVibrate()
        elif self.id == 16:
            self.angrySurprisedVibrate()
        elif self.id == 17:
            self.angryDisgustedVibrate()
        elif self.id == 18:
            self.disgustSurprisedVibrate()

        if self.id > 18:
           print("greater")
           self.manager.current = 'feedback'
           return

        anim = Animation(opacity=1, duration=0.5)
        anim += Animation(opacity=1, duration=8)
        anim += Animation(opacity=0, duration=0.5)
        anim.bind(on_complete=self.start1)
        anim.start(self.ids[f"text{self.id}"]) 
        if self.id <= 18:
            self.id += 1

    def happyVibrate(self):
        time.sleep(1)
        tts.speak("Happiness")
        time.sleep(1)
        #0.3 Seconds
        vibrator.pattern([0,0.3])

    def neutralVibrate(self):
        time.sleep(1)
        tts.speak("Neutral")
        time.sleep(1)
        #1.1 Seconds
        vibrator.pattern([0,0.3,0.5,0.3])

    def sadnessVibrate(self):
        time.sleep(1)
        tts.speak("Sadness")
        time.sleep(1)
        #0.4 Seconds
        vibrator.pattern([0,0.15,0.1,0.15])

    def disgustVibrate(self):
        time.sleep(1)
        tts.speak("Disgust")
        time.sleep(1)
        #1.8 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,1,0.15,0.1,0.15])

    def fearVibrate(self):
        time.sleep(1)
        tts.speak("Fear")
        time.sleep(1)
        #0.65 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,0.1,0.15])

    def surpriseVibrate(self):
        time.sleep(1)
        tts.speak("Surprise")
        time.sleep(1)
        #2.3 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,0.1,0.15,1,0.15,0.1,0.15,0.1,0.15])

    def angerVibrate(self):
        time.sleep(1)
        tts.speak("Anger")
        time.sleep(1)
        #3 Seconds
        vibrator.pattern([0,3])

    #6.6 Seconds
    def happilySurprisedVibrate(self):
        time.sleep(1)
        tts.speak("Happily Surprised")
        time.sleep(1.5)
        #0.3 Seconds
        vibrator.pattern([0,0.3])
        time.sleep(1.8)
        #2.3 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,0.1,0.15,1,0.15,0.1,0.15,0.1,0.15])

    #6.1 Seconds
    def happilyDisgustedVibrate(self):
        time.sleep(1)
        tts.speak("Happily Disgusted")
        time.sleep(1.5)
        #0.3 Seconds
        vibrator.pattern([0,0.3])
        time.sleep(1.8)
        #1.8 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,1,0.15,0.1,0.15])

    #5.35 Seconds
    def sadlyFearfulVibrate(self):
        time.sleep(1)
        tts.speak("Sadly Fearful")
        time.sleep(1.5)
        #0.4 Seconds
        vibrator.pattern([0,0.15,0.1,0.15])
        time.sleep(2.2)
        #0.65 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,0.1,0.15])

    #6.9 Seconds
    def sadlyAngryVibrate(self):
        time.sleep(1)
        tts.speak("Sadly Angry")
        time.sleep(1.5)
        #0.4 Seconds
        vibrator.pattern([0,0.15,0.1,0.15])
        time.sleep(1.4)
        #3 Seconds
        vibrator.pattern([0,3])

    #6.2 Seconds
    def sadlySurprisedVibrate(self):
        time.sleep(1)
        tts.speak("Sadly Surprised")
        time.sleep(1.5)
        #0.4 Seconds
        vibrator.pattern([0,0.15,0.1,0.15])
        time.sleep(1.4)
        #2.3 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,0.1,0.15,1,0.15,0.1,0.15,0.1,0.15])

    #5.7 Seconds
    def sadlyDisgustedVibrate(self):
        time.sleep(1)
        tts.speak("Sadly Disgusted")
        time.sleep(1.5)
        #0.4 Seconds
        vibrator.pattern([0,0.15,0.1,0.15])
        time.sleep(1.4)
        #1.8 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,1,0.15,0.1,0.15])

    #7.5 Seconds
    def fearAngryVibrate(self):
        time.sleep(1)
        tts.speak("Fearfully Angry")
        time.sleep(1.5)
        #0.65 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,0.1,0.15])
        time.sleep(1.65)
        #3 Seconds
        vibrator.pattern([0,3])

    #6.95 Seconds
    def fearSurprisedVibrate(self):
        time.sleep(1)
        tts.speak("Fearfully Surprised")
        time.sleep(1.5)
        #0.65 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,0.1,0.15])
        time.sleep(2.15)
        #2.3 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,0.1,0.15,1,0.15,0.1,0.15,0.1,0.15])

    #8.6 Seconds
    def angrySurprisedVibrate(self):
        time.sleep(1)
        tts.speak("Angrily Surprised")
        time.sleep(1.5)
        #3 Seconds
        vibrator.pattern([0,3])
        time.sleep(3.8)
        #2.3 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,0.1,0.15,1,0.15,0.1,0.15,0.1,0.15])

    #8.3 Seconds
    def angryDisgustedVibrate(self):
        time.sleep(1)
        tts.speak("Angrily Disgusted")
        time.sleep(1.5)
        #3 Seconds
        vibrator.pattern([0,3])
        time.sleep(4)
        #1.8 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,1,0.15,0.1,0.15])

    #8.1 Seconds
    def disgustSurprisedVibrate(self):
        time.sleep(1)
        tts.speak("Disgustedly Surprised")
        time.sleep(1.5)
        #1.8 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,1,0.15,0.1,0.15])
        time.sleep(3.3)
        #2.3 Seconds
        vibrator.pattern([0,0.15,0.1,0.15,0.1,0.15,1,0.15,0.1,0.15,0.1,0.15])

    def on_touch_move(self, touch):
        if touch.x < touch.ox: # this line checks if a left swipe has been detected
            self.manager.current = 'tts'

        elif touch.ox < touch.x: # this line checks if a right swipe has been detected
            self.manager.current = 'vibrate'

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.manager.current = 'feedback'

         
class WindowManager(ScreenManager):
    pass


class AppScreen(MDApp):
    
    def build(self):
        
        kv = Builder.load_file('screen1.kv')

        return kv

if __name__ == '__main__':
    AppScreen().run()