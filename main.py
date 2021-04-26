import tkinter as tk
import random
import tri_utils as tri

window_width = "1050"
window_height = "610"
point_size = 9


# TODO -1- Needs work for clean separation into classes
drawing_canvas: tk.Canvas = None

# Labels are obstacles like tables etc
labels = []
wall_points = []


def drag_start(event):
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y


def drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x, y=y)


def left_click_canvas(event):
    x, y = event.x, event.y

    drawing_canvas.create_oval([x - (point_size / 2), y - (point_size / 2),
                                x + (point_size / 2), y + (point_size / 2)],
                               outline='red', fill='red')

    global wall_points
    wall_points.append((x, y))

    if len(wall_points) > 1:
        two_points = wall_points[-2:]
        a = two_points[0]
        b = two_points[1]
        #print(a[0])
        #print(b[0])

        drawing_canvas.create_line([a[0], a[1], b[0], b[1]], fill='black')


def add_label(window=drawing_canvas, color="grey", width: int = 30, height: int = 30):
    # Adding a label (here mostly squares) and to given canvas

    # Squares' size is pixelbased because an empty image is used
    i = tk.PhotoImage()
    label = tk.Label(window, image=i, width=width, height=height, bg=color)

    label.place(x=random.randint(0, 600), y=random.randint(0, 400))

    label.bind('<Button-1>', drag_start)
    label.bind('<B1-Motion>', drag_motion)

    global labels
    labels.append(label)


def triangulate(x_max=int(window_width),
                y_max=int(window_height)):

    tri.calculate_mesh(x_max, y_max, wall_points, [])


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(background="#CCCCCC")
        self.geometry("{0}x{1}".format(window_width, window_height))

        self.leftFrame = OwnFrame(self, True)
        self.rightFrame = OwnFrame(self, False)

        self.mainloop()


class OwnFrame(tk.Frame):
    def __init__(self, parent, left):
        super().__init__(parent, width=200, height=600)
        self.left = left
        self.parent = parent
        self.canvas = None

        # Code to run if Frame is on the left side ...
        if left:
            self.grid(row=0, column=0, padx=2, pady=2)

            self.canvas = OwnCanvas(self)
            self.canvas.bind('<Button-1>', left_click_canvas)

            # TODO -1-
            global drawing_canvas
            drawing_canvas = self.canvas

        # here on the right side
        else:
            self.grid(row=0, column=1, padx=2, pady=2)

            tk.Label(self, text="Instructions:") \
                .grid(row=0, column=0, padx=10, pady=2)

            instructions = tk.Label(self, text="1\n2\n2\n3\n4\n5\n6\n7\n8\n9\n")
            instructions.grid(row=1, column=0, padx=10, pady=2)

            add_sqr = tk.Button(self, text='Add Square', command=add_label)
            add_sqr.grid(row=0, column=1)

            triangulate_btn = tk.Button(self, text='Calculate Mesh', command=triangulate)
            triangulate_btn.grid(row=1, column=1)


class OwnCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=800, height=600, bg='white')
        self.grid(row=0, column=0)

        self.parent = parent
        self.labels = []


def main():
    MainWindow()


if __name__ == "__main__":
    main()
