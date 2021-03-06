from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from math import *
import random

class UselessBall(Widget):
    vx = NumericProperty(1)
    vy = NumericProperty(1)
    color = [1, 0, 0, 1]
    is_x = False
    is_y = False

    def velo(self,xx,yy):
        self.vx = xx
        self.vy = yy

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def update_color(self):
        cc = lambda : random.randint(0, 100)/100.0
        self.color = [cc(), cc(), cc(), 1]
        self.canvas.children[0].rgba = self.color

class UselessJoy(Widget):
    rad = NumericProperty(0)
    dis = NumericProperty(0)

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True
    
    def on_touch_move(self,touch):
        nx = self.parent.width/10
        ny = 70
        
        if touch.grab_current is self:    
            self.center_x = touch.x
            self.center_y = touch.y
            way = sqrt((self.center_x-nx) ** 2 + (self.center_y-ny) ** 2)
            theta = 270 * 0.0174532925
            if self.center_x-nx != 0:
                theta = atan2((self.center_y-ny),(self.center_x-nx))
            elif self.center_y-ny > 0:
                theta = 90 * 0.0174532925
            if way > 30:
                way = 30
                self.center_x = nx+30*cos(theta)
                self.center_y = ny+30*sin(theta)
            self.rad = theta
            self.dis = way/30.0
            print("Rad = " + str(theta) + " Distance = " + str(self.dis))

    def on_touch_up(self,touch):
        if touch.grab_current is self:
            print("OK")
            touch.ungrab(self)
            self.begin()
            return True
    
    def begin(self):
        self.center_x = self.parent.width / 10
        self.center_y = 70
        self.rad = 0
        self.dis = 0

class UselessGame(Widget):
    ball = ObjectProperty(None)
    joy = ObjectProperty(None)
    
    def update(self,dt):
        #print(self.ball.size)
        self.bounce_ball(self.ball)
    
    def bounce_ball(self,ball):
        ball.center_x += self.joy.dis*10*cos(self.joy.rad)
        ball.center_y += self.joy.dis*10*sin(self.joy.rad)
        if ball.y < 0:
            ball.y = 0
            if not ball.is_y:
                ball.update_color()
            ball.is_y = True
        elif ball.y > self.height-ball.height:
            ball.y = self.height-ball.height
            if not ball.is_y:
                ball.update_color()
            ball.is_y = True
        else:
            ball.is_y = False
        if ball.x < 0:
            ball.x = 0
            if not ball.is_x:
                ball.update_color()
            ball.is_x = True
        elif ball.x > self.width-ball.width:
            ball.x = self.width-ball.width
            if not ball.is_x:
                ball.update_color()
            ball.is_x = True
        else:
            ball.is_x = False

class UselessApp(App):
    def build(self):
        game = UselessGame()
        Clock.schedule_interval(game.update , 1.0/120)
        return game

if __name__ == '__main__':
    UselessApp().run()
