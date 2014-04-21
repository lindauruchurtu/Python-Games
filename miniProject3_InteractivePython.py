# Mini-project # 3 - "Stopwatch: The Game"
#-----------------------------------------

import simplegui

# define global variables

stops = 0
success = 0
counter = 0
dec_secs = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(time):
  #  hour = str(time / 3600)
  #  print(hour)
    global dec_secs
    mins = str((time / 600) % 60)
    secs = (time / 10) % 60
    if (secs<10):
        secs = str(0) + str(secs)
    else:
        secs = str(secs)
    dec_secs = time % 10
    new_time = mins + ":" + secs + "." + str(dec_secs)
    return new_time

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button():
    timer.start()

def stop_button():
    global stops, dec_secs, success
    timer.stop()
    stops = stops + 1
    if dec_secs == 0:
        success = success + 1

def reset_button():
    global counter, stops, success
    #timer.stop()
    counter = 0
    stops = 0
    success = 0
    
# timer handler

def timer_handler():
    global counter 
    counter =  counter + 1

# define draw handler - I love red and green

def draw_handler(canvas):
    canvas.draw_text(format(counter),(65,170),70,"Red") 
    canvas.draw_text(str(success) + "/" + str(stops),(220,60),50,"Green") 


# create frame, buttons and draw 

frame = simplegui.create_frame('StopWatch: The Game', 300, 300)


button1 = frame.add_button('Start', start_button, 100)
button2 = frame.add_button('Stop', stop_button, 100)
button3 = frame.add_button('Reset', reset_button, 100)

frame.set_draw_handler(draw_handler)


# Start frame and timer

timer = simplegui.create_timer(100, timer_handler)
frame.start()

