# Imports the pythonGraph Module numpy and pillow
import pythonGraph as pg
import numpy as np
from PIL import Image as pic
# run pip install pythongraph numpy pillow 
# to get this script to work

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
CANVAS_SIZE = 560
HOZ_BOUND = SCREEN_WIDTH - CANVAS_SIZE
VERT_BOUND = SCREEN_HEIGHT - CANVAS_SIZE
BUTTON_TONE = pg.create_color(139, 194, 239)
PANEL_TONE = pg.create_color(0, 10, 56)
EXIT_TONE = pg.create_color(202, 94, 86)
# class constants that determine window sizing for the drawing panel and ui elements as well as button color


# Setup the Drawing Window
pg.open_window(SCREEN_WIDTH, SCREEN_HEIGHT)
pg.set_window_title("Animation Template")
#the usual stuff

class Button():
    # button class becuase I dont like the way pygraph does rectangles and I have more than 1 button
    # I feel like the actions are all pretty self explanatory
    def __init__(self, x, y, width, height, color, text, font_size):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.text = text
        self.font_size = font_size
        pg.draw_rectangle(x,y,x+width,y+height,color,True)
        pg.draw_text(text, x+10, (y+height//2)-15, "black", font_size)

    def click_signal(self, mouse_x, mouse_y):
        if (mouse_x in range(self.x,self.x+self.width)) and (mouse_y in range(self.y,self.y+self.height)) and pg.mouse_button_pressed("LEFT"):
            return True

    def erase(self):
        pg.draw_rectangle(HOZ_BOUND,VERT_BOUND,SCREEN_WIDTH,SCREEN_HEIGHT,"white",True)

    def exit(self):
        pg.close_window()

    def save(self,buffer):
        save_image(buffer)

# oh god this is where it starts
# pixel buffer is a blank numpy array the size of the drawing canvas

def create_buffer(shape):
    return np.zeros(shape, dtype=np.uint8)

def get_bounds(pixel, r, buffer_dims):
    x, y = pixel
    hoz_min = np.clip(x-r, 0, buffer_dims[1])
    hoz_max = np.clip(x+r+1, 0, buffer_dims[1])
    vert_min = np.clip(y-r, 0, buffer_dims[0])
    vert_max = np.clip(y+r+1, 0, buffer_dims[0])
    return ((hoz_max, hoz_min),(vert_max,vert_min))

# for two points, it draws a smaller "working frame" with opposite corners at the two points plus a small pixel buffer of the brushes thickness

def calculate_projection(a, b, xs, ys):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    x_offset = xs - a[0]
    y_offset = ys - a[1]
    x_dx = x_offset * dx
    y_dy = y_offset * dy
    t = (x_dx + y_dy) / (dx**2 + dy**2)
    t = np.clip(t, 0, 1)
    return t

# use dot products to calculate the shadow that every point in the working frame casts on the line segement between the two points

def calculate_closest_point(a, b, t):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    cx = a[0] + t*dx
    cy = a[1] + t*dy
    return cx, cy

#use the projection from before to get a fraction of the line segment to reference a specific point in the line segment

def calculate_distance(cx, cy, xs, ys):
    dx = xs - cx
    dy = ys - cy
    return np.hypot(dx,dy)

#find the distance of every point in the working frame to its closest point on the line segment

def mask(dist, r):
    m = dist<r
    return m

# if the distance is less than the radius, mark this point as true to be filled with ink

def buffer_draw(buffer, a, b, r):
    buffer_dims = buffer.shape
    ((hoz_max1, hoz_min1),(vert_max1,vert_min1)) = get_bounds(a,r,buffer_dims)
    ((hoz_max2, hoz_min2),(vert_max2,vert_min2)) = get_bounds(b,r,buffer_dims)
    hoz_max = max(hoz_max1,hoz_max2)
    hoz_min = min(hoz_min1,hoz_min2)
    vert_max = max(vert_max1,vert_max2)
    vert_min = min(vert_min1,vert_min2)
    draw_to = buffer[vert_min:vert_max,hoz_min:hoz_max]
    ys, xs = np.ogrid[vert_min:vert_max,hoz_min:hoz_max]
    t = calculate_projection(a, b, xs, ys)
    cx, cy = calculate_closest_point(a, b, t)
    dist = calculate_distance(cx, cy, xs, ys)
    m = mask(dist, r)
    draw_to[m] = 255

#pull it all together, use the above logic to draw white on a black working portion of the buffer and then put it into the buffer

def save_image(buffer):
    img = pic.fromarray(buffer)
    img.save("img.png")

# save the buffer to a png image using PIL


def mouse_pos():
    return pg.get_mouse_x(), pg.get_mouse_y()

def draw_buttons():
    return (Button(10,10,200,100, EXIT_TONE, "EXIT", 100),
            Button(30,150,150,50, BUTTON_TONE, "CLASSIFY", 40),
            Button(30,220,150,50, BUTTON_TONE, "ERASE", 40),
            Button(30,300,150,50, BUTTON_TONE, "SAVE", 40)
    )

# button wrapper function for decomp

def button_listen(exit_button, classify_button, erase_button, save_button, x, y,buffer):
    if classify_button.click_signal(x,y):
        print("I was clicked")
    elif erase_button.click_signal(x,y):
        erase_button.erase()
    elif exit_button.click_signal(x,y):
        exit_button.exit()
    elif save_button.click_signal(x,y):
        save_button.save(buffer)

#handle (most of) the button inputs 

def draw(x, y, width, pRef, buffer):
    #main draw loop
    if pg.mouse_button_down("LEFT"):
            if pg.mouse_button_pressed("LEFT") and x > HOZ_BOUND and y > VERT_BOUND :
                for i in range(len(pRef)): pRef.pop()
                pRef.append(mouse_pos())
                # cover the first time the mouse is pressed as a starting point for that stroke
            if x > HOZ_BOUND and y > VERT_BOUND:
                pRef.append((x,y))
                a = (pRef[0][0]-HOZ_BOUND,pRef[0][1]-VERT_BOUND)
                b = (pRef[1][0]-HOZ_BOUND,pRef[1][1]-VERT_BOUND)
                #  a and b are logic for writing to the buffer but the position reference (pRef) is used for both
                buffer_draw(buffer, a, b, r=width)
                pg.draw_circle(pRef[0][0],pRef[0][1],(2*width)/2.5,"Black",True)
                pg.draw_line(pRef[0][0], pRef[0][1], pRef[1][0], pRef[1][1], "Black", width=2*width)
                pg.draw_circle(pRef[1][0],pRef[1][1],(2*width)/2.5,"Black",True)
                # look at the last position and this position, draw a line between the two and put circles at either end
                pRef.pop(0)

def ui_init():
    pg.draw_rectangle(HOZ_BOUND,0,SCREEN_WIDTH,VERT_BOUND,PANEL_TONE,filled=True)
    pg.draw_rectangle(0,VERT_BOUND,HOZ_BOUND,SCREEN_HEIGHT,PANEL_TONE,filled=True)
    pg.draw_text("DIGIT CLASSIFIER",  HOZ_BOUND+20, (0+VERT_BOUND//2) - 25, "white", 70)
    # some ui rectangles for style points i guess

def main_loop():
    # this is the main loop where everything runs
    buffer = create_buffer((560,560))
    pRef = [(0,0)]
    exit_button, classify_button, erase_button, save_button = draw_buttons()
    while pg.window_not_closed():
        x,y = mouse_pos()
        button_listen(exit_button,classify_button,erase_button, save_button, x, y, buffer)
        if erase_button.click_signal(x,y):
            buffer = create_buffer((CANVAS_SIZE,CANVAS_SIZE))
        draw(x,y,20, pRef, buffer)
        pg.update_window()
            

# all runtime code goes under this
if __name__ == "__main__":
    ui_init()
    main_loop()
    