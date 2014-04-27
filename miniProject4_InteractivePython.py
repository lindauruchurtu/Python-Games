# Mini-project # 4 - Implementation of classic arcade game Pong
#-----------------------------------------
# NB: This is a highly inefficient implementation of the game. I am certain this can be widely improved!
# -------------------------------------------

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
SCORE1 = 0
SCORE2 = 0

ball_pos = [WIDTH / 2, HEIGHT /2]
ball_vel = [0, 0]
paddle1_pos = ([0, (HEIGHT / 2) + HALF_PAD_HEIGHT], [PAD_WIDTH, (HEIGHT / 2) + HALF_PAD_HEIGHT], [PAD_WIDTH, (HEIGHT / 2) - HALF_PAD_HEIGHT], [0, (HEIGHT / 2) - HALF_PAD_HEIGHT])
paddle2_pos = ([WIDTH - PAD_WIDTH, (HEIGHT / 2) + HALF_PAD_HEIGHT], [WIDTH - 1, (HEIGHT / 2) + HALF_PAD_HEIGHT], [WIDTH - 1, (HEIGHT / 2) - HALF_PAD_HEIGHT], [WIDTH - PAD_WIDTH, (HEIGHT / 2) - HALF_PAD_HEIGHT],)
paddle1_vel = 0
paddle2_vel = 0
    

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    #ball_vel = [3, -3]
    
    if direction == RIGHT:
        ball_vel = [random.randrange(2, 4), -random.randrange(1, 3)]
        #print ball_vel
    elif direction == LEFT:
        ball_vel = [-random.randrange(2, 4),-random.randrange(1, 3)]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,ball_pos,ball_vel  # these are numbers
    global SCORE1, SCORE2  # these are ints
    SCORE1 = 0
    SCORE2 = 0
    ball_pos = [WIDTH / 2, HEIGHT /2]
    ball_vel = [0, 0]
    paddle1_pos = ([0, (HEIGHT / 2) + HALF_PAD_HEIGHT], [PAD_WIDTH, (HEIGHT / 2) + HALF_PAD_HEIGHT], [PAD_WIDTH, (HEIGHT / 2) - HALF_PAD_HEIGHT], [0, (HEIGHT / 2) - HALF_PAD_HEIGHT])
    paddle2_pos = ([WIDTH - PAD_WIDTH, (HEIGHT / 2) + HALF_PAD_HEIGHT], [WIDTH - 1, (HEIGHT / 2) + HALF_PAD_HEIGHT], [WIDTH - 1, (HEIGHT / 2) - HALF_PAD_HEIGHT], [WIDTH - PAD_WIDTH, (HEIGHT / 2) - HALF_PAD_HEIGHT],)
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball(RIGHT)

def draw(canvas):
    global SCORE1, SCORE2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Collide and Reflect of bottom side of canvas
    if ball_pos[1] >= (HEIGHT-1) - BALL_RADIUS:
        ball_vel[1]=-ball_vel[1]
        canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    elif ball_pos[1]<= BALL_RADIUS:
        ball_vel[1]=-ball_vel[1]
        canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

    # Ball collides with gutters
    
    if ball_pos[0] >= (WIDTH - PAD_WIDTH -1) - BALL_RADIUS:
        if ball_pos[1] < paddle2_pos[0][1] and ball_pos[1] > paddle2_pos[3][1]:
            #print "ALERT"
            #print ball_vel[0]
            ball_vel[0] = -1.1*ball_vel[0]
            #print ball_vel[0]
            canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
        else:
            SCORE1 = SCORE1 + 1
            #print "Score1 is: ", SCORE1
            ball_pos = [WIDTH / 2, HEIGHT / 2]
            canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
            spawn_ball(LEFT)
    elif ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1]< paddle1_pos[0][1] and ball_pos[1] > paddle1_pos[3][1]:
            #print "ANOTHER ALERT"
            #print ball_vel[0]
            ball_vel[0]= -1.1*ball_vel[0]
            #print ball_vel[0]
            canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
        else:
            SCORE2 = SCORE2 + 1
            #print "Score2 is: ", SCORE2
            ball_pos = [WIDTH / 2, HEIGHT / 2]
            canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
            spawn_ball(RIGHT)
    

           
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # Check paddle position no 1
    if paddle1_pos[3][1] > (HEIGHT - PAD_HEIGHT):
        paddle1_pos[0][1] = HEIGHT - 1
        paddle1_pos[1][1] = HEIGHT - 1
        paddle1_pos[2][1] = (HEIGHT - PAD_HEIGHT)-1
        paddle1_pos[3][1] = (HEIGHT - PAD_HEIGHT)-1
    elif paddle1_pos[3][1] < 0: 
        paddle1_pos[0][1] = PAD_HEIGHT
        paddle1_pos[1][1] = PAD_HEIGHT
        paddle1_pos[2][1] = 0
        paddle1_pos[3][1] = 0
    
    # Check paddle position no 2
    if paddle2_pos[3][1] > (HEIGHT - PAD_HEIGHT):
        paddle2_pos[0][1] = HEIGHT - 1
        paddle2_pos[1][1] = HEIGHT - 1
        paddle2_pos[2][1] = (HEIGHT - PAD_HEIGHT)-1
        paddle2_pos[3][1] = (HEIGHT - PAD_HEIGHT)-1
    elif paddle2_pos[3][1] < 0: 
        paddle2_pos[0][1] = PAD_HEIGHT
        paddle2_pos[1][1] = PAD_HEIGHT
        paddle2_pos[2][1] = 0
        paddle2_pos[3][1] = 0
    
    # update paddle's vertical position, 
    paddle1_pos[0][1] += paddle1_vel
    paddle1_pos[1][1] += paddle1_vel
    paddle1_pos[2][1] += paddle1_vel
    paddle1_pos[3][1] += paddle1_vel
    
    paddle2_pos[0][1] += paddle2_vel
    paddle2_pos[1][1] += paddle2_vel
    paddle2_pos[2][1] += paddle2_vel
    paddle2_pos[3][1] += paddle2_vel
    
    
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 12, 'Yellow', 'Orange')
    canvas.draw_polygon(paddle2_pos, 12, 'Yellow', 'Orange')
    #print paddle1_pos
    # draw scores
    canvas.draw_text("P1" +" "+str(SCORE1) + "/" + "P2" + " " + str(SCORE2),(440,380),30,"Green") 
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 2
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel += - acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel += - acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart",new_game,200)

# start frame
new_game()
frame.start()
