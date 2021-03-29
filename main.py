import tkinter as tk
import random

window_width = "1000"
window_height = "600"

# TODO -1- Needs work for clean separation into classes
drawingCanvas = None


def drag_start(event):
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y


def drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x, y=y)


def add_label(window=drawingCanvas, color="grey", width=10, height=5):
    label = tk.Label(window, bg=color, width=width, height=height)
    label.place(x=random.randint(0, 600), y=random.randint(0, 400))

    label.bind("<Button-1>", drag_start)
    label.bind("<B1-Motion>", drag_motion)

    return label






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
            # TODO -1-
            global drawingCanvas
            drawingCanvas = self.canvas

        # here on the right side
        else:
            self.grid(row=0, column=1, padx=2, pady=2)

            tk.Label(self, text="Instructions:") \
                .grid(row=0, column=0, padx=10, pady=2)

            Instruct = tk.Label(self, text="1\n2\n2\n3\n4\n5\n6\n7\n8\n9\n")
            Instruct.grid(row=1, column=0, padx=10, pady=2)

            go = tk.Button(self, text='Add Square', command=add_label)
            go.grid(row=0, column=1)


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



