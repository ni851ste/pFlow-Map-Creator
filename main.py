import tkinter as tk
import random

window_width = "1000"
window_height = "600"


drawingSpace2=0


def drag_start(event):
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y


def drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x, y=y)


def init_window():
    global drawingSpace2
    window = tk.Tk()
    window.config(background="#CCCCCC")
    window.geometry("{0}x{1}".format(window_width, window_height))

    # Left frame
    leftFrame = tk.Frame(window, width=200, height=600)
    leftFrame.grid(row=0, column=0, padx=2, pady=2)

    drawingSpace = tk.Canvas(leftFrame, width=800, height=600, bg='white')
    drawingSpace.grid(row=0, column=0)
    drawingSpace2 = drawingSpace

    #tk.Label(leftFrame, text="Instructions:").grid(row=0, column=0, padx=10, pady=2)
    #Instruct = tk.Label(leftFrame, text="1\n2\n2\n3\n4\n5\n6\n7\n8\n9\n")
    #Instruct.grid(row=1, column=0, padx=10, pady=2)



    rightFrame = tk.Frame(window, width=200, height=600)
    rightFrame.grid(row=0, column=1, padx=2, pady=2)

    tk.Label(rightFrame, text="Instructions:")\
        .grid(row=0, column=0, padx=10, pady=2)

    Instruct = tk.Label(rightFrame, text="1\n2\n2\n3\n4\n5\n6\n7\n8\n9\n")
    Instruct.grid(row=1, column=0, padx=10, pady=2)


    go = tk.Button(rightFrame, text='Add Square', command=add_label)
    go.grid(row=0, column=1)

    add_label(drawingSpace, "red")
    add_label(drawingSpace, "purple")


    return window


def add_label(window=drawingSpace2, color="grey", width=10, height=5):
    label = tk.Label(window, bg=color, width=width, height=height)
    label.place(x=random.randint(0, 600), y=random.randint(0, 400))

    label.bind("<Button-1>", drag_start)
    label.bind("<B1-Motion>", drag_motion)

    return label


def main():

    labels = []

    window = init_window()



    #label = tkinter.Label(window, bg="red", width=10, height=5)
    #label.place(x=0, y=0)

    #label2 = tkinter.Label(window, bg="blue", width=10, height=5)
    #label2.place(x=100, y=100)


    window.mainloop()



if __name__ == "__main__":
    main()



