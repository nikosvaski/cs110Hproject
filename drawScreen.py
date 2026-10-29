# Imports the pythonGraph Module
import pythonGraph as pg
import time

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
CANVAS_SIZE = 480
HOZ_BOUND = SCREEN_WIDTH - CANVAS_SIZE
VERT_BOUND = SCREEN_HEIGHT - CANVAS_SIZE



# Setup the Drawing Window
pg.open_window(SCREEN_WIDTH, SCREEN_HEIGHT)
pg.set_window_title("Animation Template")

class Button():
    def __init__(self, x, y, height, width, color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        pg.draw_rectangle(x,y,x+width,y+height,color,True)

    def click_signal(self, mouse_x, mouse_y):
        if (mouse_x in range(self.x,self.x+self.width)) and (mouse_y in range(self.y,self.y+self.height)) and pg.mouse_button_pressed("LEFT"):
            print("I was clicked!")


def mouse_pos():
    return pg.get_mouse_x(), pg.get_mouse_y()




def drawing_loop():
    brush_on = 1
    width = 10
    pRef = [[0,0]]
    classify = Button(0,0,100,100, "Red")

    while pg.window_not_closed():
        if pg.mouse_button_down("LEFT"):
            x,y = mouse_pos()
            classify.click_signal(x,y)
            if pg.mouse_button_pressed("LEFT") and x > HOZ_BOUND and y > VERT_BOUND :
                pRef = [mouse_pos()]
            if x > HOZ_BOUND and y > VERT_BOUND:
                pRef.append((x,y))
                pg.draw_circle(pRef[0][0],pRef[0][1],width/2.5,"Black",True)
                pg.draw_line(pRef[0][0], pRef[0][1], pRef[1][0], pRef[1][1], "Black", width=width)
                pg.draw_circle(pRef[1][0],pRef[1][1],width/2.5,"Black",True)
                pRef.pop(0)
        pg.update_window()
            


if __name__ == "__main__":
    panel_tone = pg.create_color(0, 10, 56)
    pg.draw_rectangle(HOZ_BOUND,0,SCREEN_WIDTH,VERT_BOUND,panel_tone,filled=True)
    pg.draw_rectangle(0,VERT_BOUND,HOZ_BOUND,SCREEN_HEIGHT,panel_tone,filled=True)
    drawing_loop()
    