from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    '''
    When a widget is defined and uses a Property class, the creation of the property object happens, but the instance 
    doesn’t know anything about its name in the widget class. Hence the id def in the KV file. Might be able to replace with link()
    '''
    velocity = ReferenceListProperty(velocity_x, velocity_y)#tuples the numericProps to be able to edit both at the sametime
    # move function will move the ball one step. This
    #  will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos    # '*' packs the tuple into Vector


class PongGame(Widget):#This will be the root widget that everything is inside of
    ball = ObjectProperty(None)#Will be an object but will be passed later
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:#since x,y default is bottom left(0,0)
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        #player1
        if touch.x < self.width / 3:    #can move paddle within touching a 3rd of the screen
            self.player1.center_y = touch.y     #y is directly tied
        #player2
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):#app class must match kv file minus "app"
    def build(self):#pass the instance of the class to the function so it knows it parent.
        game = PongGame()#define game as a PongGame widget.
        game.serve_ball()# starts moving the ball in rand direction
        Clock.schedule_interval(game.update, 1.0 / 60.0)#updates evey 60th of a second for 60fps
        return game


if __name__ == '__main__':#only autorun the code if the file is being run as main.
    PongApp().run()