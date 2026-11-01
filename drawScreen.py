# Imports the pythonGraph Module
import pythonGraph as pg
import time

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
CANVAS_SIZE = 480
HOZ_BOUND = SCREEN_WIDTH - CANVAS_SIZE
VERT_BOUND = SCREEN_HEIGHT - CANVAS_SIZE
BUTTON_TONE = pg.create_color(139, 194, 239)
PANEL_TONE = pg.create_color(0, 10, 56)
EXIT_TONE = pg.create_color(202, 94, 86)


# Setup the Drawing Window
pg.open_window(SCREEN_WIDTH, SCREEN_HEIGHT)
pg.set_window_title("Animation Template")

class Button():
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


def mouse_pos():
    return pg.get_mouse_x(), pg.get_mouse_y()




def drawing_loop():
    width = 20
    pRef = [[0,0]]
    exit_button = Button(10,10,200,100, EXIT_TONE, "EXIT", 100)
    classify_button = Button(30,130,150,50, BUTTON_TONE, "CLASSIFY", 40)
    erase_button = Button(30,200,150,50, BUTTON_TONE, "ERASE", 40)

    while pg.window_not_closed():
        x,y = mouse_pos()
        if classify_button.click_signal(x,y):
            print("I was clicked")
        elif erase_button.click_signal(x,y):
            erase_button.erase()
        elif exit_button.click_signal(x,y):
            exit_button.exit()
        elif pg.mouse_button_down("LEFT"):
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
    pg.draw_rectangle(HOZ_BOUND,0,SCREEN_WIDTH,VERT_BOUND,PANEL_TONE,filled=True)
    pg.draw_rectangle(0,VERT_BOUND,HOZ_BOUND,SCREEN_HEIGHT,PANEL_TONE,filled=True)
    pg.draw_text("DIGIT CLASSIFIER",  HOZ_BOUND+20, (0+VERT_BOUND//2) - 25, "white", 70)
    drawing_loop()
    