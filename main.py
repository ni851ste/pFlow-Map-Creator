import tkinter as tk
import random

window_width = "1050"
window_height = "600"

drawing_space = None

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
    print('X:{0} Y:{1}'.format(event.x, event.y))


def init_window():
    global drawing_space
    window = tk.Tk()
    window.config(background="#CCCCCC")
    window.geometry("{0}x{1}".format(window_width, window_height))

    # Left frame
    left_frame = tk.Frame(window, width=200, height=600)
    left_frame.grid(row=0, column=0, padx=2, pady=2)

    drawing_space = tk.Canvas(left_frame, width=800, height=600, bg='white')
    drawing_space.grid(row=0, column=0)

    right_frame = tk.Frame(window, width=200, height=600)
    right_frame.grid(row=0, column=1, padx=2, pady=2)

    tk.Label(right_frame, text="Instructions:") \
        .grid(row=0, column=0, padx=10, pady=2)

    instructions = tk.Label(right_frame, text="1\n2\n2\n3\n4\n5\n6\n7\n8\n9\n")
    instructions.grid(row=1, column=0, padx=10, pady=2)

    go = tk.Button(right_frame, text='Add Square', command=add_label)
    go.grid(row=0, column=1)

    add_label(window=drawing_space, color="red")
    add_label(window=drawing_space, color="purple")

    return window


def add_label(window=drawing_space, color="grey", width: int = 30, height: int = 30):
    # Adding a label (here mostly squares) and to given canvas

    # Squares' size is pixelbased because an empty image is used
    i = tk.PhotoImage()
    label = tk.Label(window, image=i, width=width, height=height, bg=color)

    label.place(x=random.randint(0, 600), y=random.randint(0, 400))

    label.bind("<Button-1>", drag_start)
    label.bind("<B1-Motion>", drag_motion)

    global labels
    labels.append(label)

    return label


def main():

    window = init_window()

    window.mainloop()


if __name__ == "__main__":
    main()
