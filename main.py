from tkinter import *
from tkinter import messagebox
import sys
import os
import random


class Coin:
    def __init__(self, p_canvas, width, height, size, tail_coordinates):
        self.x, self.y = tail_coordinates[0]
        while True:
            if [self.x, self.y] in tail_coordinates:
                self.x = random.random() * width // size * size
                self.y = random.random() * height // size * size
            else:
                break
        self.canvas = p_canvas
        self.square_size = size
        self.rect = p_canvas.create_rectangle(self.x, self.y, self.x + size, self.y + size, fill='yellow')

    def remove(self):
        self.canvas.delete(self.rect)


class Snake:
    def __init__(self, p_canvas, x=400, y=200, size=10, length=3, speed=50):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.length = length
        self.vector = (1, 0)
        self.prev_vector = (1, 0)
        self.canvas = p_canvas
        self.tail_coordinates = [[None, None]]
        self.rect = p_canvas.create_rectangle(self.x, self.y, self.x + size, self.y + size, fill='red')
        self.coin = Coin(p_canvas,
                         int(self.canvas["width"]),
                         int(self.canvas["height"]),
                         size, self.tail_coordinates)
        self.has_tail = False
        length -= 1
        if length != 0:
            self.has_tail = True
            self.tail = Tail(p_canvas, length, self.x, self.y, self.size)

    def start(self):
        global gl_score
        global gl_string_score
        self.prev_vector = self.vector
        prev_x, prev_y = self.x, self.y
        dx, dy = self.vector[0] * self.size, self.vector[1] * self.size

        # if snake riches bordersCoin -> teleport it immediately
        dx, dy = get_border_dx_dy(dx, dy, self.x, self.y,
                                  int(self.canvas["width"]),
                                  int(self.canvas["height"]),
                                  self.size)
        self.x, self.y = self.x + dx, self.y + dy
        self.canvas.move(self.rect, dx, dy)

        # if snake has tail -> move it right behind the snake
        if self.has_tail:
            self.tail.tail_move(prev_x, prev_y)
            # get every tail x, y coordinates
            self.tail_coordinates = []
            self.tail.get_coordinates(self.tail_coordinates)

        # if touch coin -> get score, remove coin
        if [self.x, self.y] == [self.coin.x, self.coin.y]:
            self.coin.remove()
            # add new element to snake
            self.add_new_tail()

            # score ++
            gl_score += 1
            gl_string_score.set("Score: {}".format(gl_score))
            self.canvas.itemconfigure(text_score, text=gl_string_score.get())

            # generate new coin
            self.coin = Coin(self.canvas,
                             int(self.canvas["width"]),
                             int(self.canvas["height"]),
                             self.size, self.tail_coordinates)

        # if self coordinates == one of tails coordinates -> fail
        if [self.x, self.y] in self.tail_coordinates:
            messagebox.showinfo('Game over', 'Your score: {}'.format(gl_score))
            window.destroy()
            #restart_program()
        else:
            self.canvas.after(self.speed, self.start)

    def add_new_tail(self):
        last_tail = self.get_last_tail()
        last_tail.has_tail = True
        last_tail.tail = Tail(self.canvas, 1, last_tail.x, last_tail.y, self.size)

    def get_last_tail(self):
        if self.has_tail:
            curr_tail = self.tail
            while curr_tail.has_tail:
                curr_tail = curr_tail.tail
        else:
            return self
        return curr_tail

    def change_vector(self, event):
        if (event.keysym == 'w' or event.keysym == 'W' or
            event.char == 'ц' or event.char == 'Ц' or
            event.keysym == 'Up') and \
                self.prev_vector != (0, 1):
            self.vector = (0, -1)
        if (event.keysym == 's' or event.keysym == 'S' or
            event.char == 'ы' or event.char == 'Ы' or
            event.keysym == 'Down') and \
                self.prev_vector != (0, -1):
            self.vector = (0, 1)
        if (event.keysym == 'a' or event.keysym == 'A' or
            event.char == 'ф' or event.char == 'Ф' or
            event.keysym == 'Left') and \
                self.prev_vector != (1, 0):
            self.vector = (-1, 0)
        if (event.keysym == 'd' or event.keysym == 'D' or
            event.char == 'в' or event.char == 'В' or
            event.keysym == 'Right') and \
                self.prev_vector != (-1, 0):
            self.vector = (1, 0)


class Tail:
    def __init__(self, p_canvas, length, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.length = length
        self.canvas = p_canvas
        self.rect = p_canvas.create_rectangle(self.x, self.y, self.x + size, self.y + size, fill='blue')
        self.has_tail = False
        length -= 1
        if length != 0:
            self.has_tail = True
            self.tail = Tail(p_canvas, length, self.x, self.y, self.size)

    def tail_move(self, x, y):
        prev_x, prev_y = self.x, self.y
        dx, dy = x - self.x, y - self.y
        # if tail riches borders
        dx, dy = get_border_dx_dy(dx, dy, self.x, self.y,
                                  int(self.canvas["width"]),
                                  int(self.canvas["height"]),
                                  self.size)
        self.x, self.y = self.x + dx, self.y + dy
        self.canvas.move(self.rect, dx, dy)
        if self.has_tail:
            self.tail.tail_move(prev_x, prev_y)

    def get_coordinates(self, result_list):
        result_list.append([self.x, self.y])
        if self.has_tail:
            self.tail.get_coordinates(result_list)


def get_border_dx_dy(dx, dy, x, y, width, height, size):
    if x > width - size:
        dx = 0 - width
    if x < 0:
        dx = width
    if y > height - size:
        dy = 0 - height
    if y < 0:
        dy = height
    return dx, dy


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, *sys.argv)


if __name__ == "__main__":
    window_width = 600
    window_height = 600
    square_size = 20

    window = Tk()
    window.title("Snake")

    gl_score = 0
    gl_string_score = StringVar()
    gl_string_score.set("Score: 0")

    canvas = Canvas(window, width=window_width, height=window_height, bg='white', bd='0')
    text_score = canvas.create_text((window_width, 0), width=window_width, anchor='ne', fill='black',
                                    text=gl_string_score.get(), font='Bahnschrift {}'.format(square_size))
    canvas.pack()

    snake = Snake(canvas, length=1, speed=70, size=square_size)
    snake.start()

    window.bind('<KeyPress>', snake.change_vector)
    mainloop()
