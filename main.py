import math
import sys
import tkinter as tk
import random
import tri_utils as tri

window_width = "1150"
window_height = "610"
point_radius = 5

# TODO -1- Needs work for clean separation into classes
drawing_canvas: tk.Canvas = None

# Labels are obstacles like tables etc
labels = []

wall_points = []
lines = []
to_be_moved_point_index = -1

popup_open = False


def drag_start(event):
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y


def drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x, y=y)


def draw_wall_points(event):
    x, y = event.x, event.y

    point = drawing_canvas.create_oval([x - point_radius, y - point_radius,
                                        x + point_radius, y + point_radius],
                                       outline='black', fill='red')

    global wall_points
    # x = X-Coord
    # y = Y-Coord
    # point is the ID of point in canvas (used to delete and redraw)
    wall_points.append((x, y, point))
    # canvas_points.append(point)

    if len(wall_points) > 1:
        to_be_drawn_points = wall_points[-2:]
        p1 = to_be_drawn_points[0]
        p2 = to_be_drawn_points[1]

        line = drawing_canvas.create_line([p1[0], p1[1], p2[0], p2[1]], fill='black')
        global lines
        lines.append(line)


def finish_wall_points(triangulate_btn, finish_button):
    if len(wall_points) < 3:
        print('Cant finish, since not enough points have been placed.')
        return

    # Draw the last line between first and last given point
    p1 = wall_points[-1]
    p2 = wall_points[0]
    line = drawing_canvas.create_line([p1[0], p1[1], p2[0], p2[1]], fill='black')
    global lines
    lines.append(line)

    # Apply new state to buttons
    triangulate_btn.config(state='normal')
    finish_button.config(state='disabled')

    # Unbind drawing new points
    drawing_canvas.bind('<Button-1>', edit_wall_points)
    drawing_canvas.bind('<B1-Motion>', edit_wall_points_drag_motion)
    drawing_canvas.bind('<ButtonRelease-1>', edit_wall_points_released)


def edit_wall_points(event):
    x, y = event.x, event.y

    current_min_distance = sys.maxsize
    point_index_of_min_distance = 0

    for i in range(len(wall_points)):
        # Find the point nearest to the mouse click
        point_x = wall_points[i][0]
        point_y = wall_points[i][1]

        x_diff = abs(point_x - x)
        y_diff = abs(point_y - y)

        # pythagoras theorem
        current_distance = math.sqrt((x_diff ** 2) + (y_diff ** 2))

        if current_distance < current_min_distance:
            current_min_distance = current_distance
            point_index_of_min_distance = i

    if current_min_distance < 8:
        # if click is in range of a button
        global to_be_moved_point_index
        to_be_moved_point_index = point_index_of_min_distance


def edit_wall_points_drag_motion(event):
    if to_be_moved_point_index == -1:
        # if drag is without the click of a button before, drag does nothing
        return

    global wall_points, lines

    x, y = event.x, event.y

    # define the old point with its lines
    p0 = wall_points[to_be_moved_point_index]
    l0 = lines[to_be_moved_point_index - 1]
    l1 = lines[to_be_moved_point_index]

    # draw new point
    new_p0_id = drawing_canvas.create_oval([x - point_radius, y - point_radius,
                                            x + point_radius, y + point_radius],
                                           outline='black', fill='red')
    # save point as tuple to prepare saving in "wall_points"
    new_p0 = (x, y, new_p0_id)

    point_before_new_p0 = wall_points[to_be_moved_point_index - 1]
    new_l0 = drawing_canvas.create_line([point_before_new_p0[0], point_before_new_p0[1],
                                         new_p0[0], new_p0[1]], fill='black')

    # modulo needed here in case last point in list is clicked and the index overflows
    point_after_new_p0 = wall_points[(to_be_moved_point_index + 1) % len(wall_points)]
    new_l1 = drawing_canvas.create_line([new_p0[0], new_p0[1],
                                        point_after_new_p0[0], point_after_new_p0[1]], fill='black')

    lines[to_be_moved_point_index - 1] = new_l0
    lines[to_be_moved_point_index] = new_l1
    wall_points[to_be_moved_point_index] = new_p0

    # deleting point that has been clicked and its lines
    drawing_canvas.delete(p0[2])
    drawing_canvas.delete(l0)
    drawing_canvas.delete(l1)


def edit_wall_points_released(_):
    # if Button-1 is released the click and drag indicator is set back to a default value
    global to_be_moved_point_index
    to_be_moved_point_index = -1


def add_label(window=drawing_canvas, color="grey", width: int = 30, height: int = 30):
    """ Function is pretty much deprecated """
    # Adding a label (here mostly squares) and to given canvas

    # Squares' size is pixel based because an empty image is used
    i = tk.PhotoImage()
    label = tk.Label(window, image=i, width=width, height=height, bg=color)

    label.place(x=random.randint(0, 600), y=random.randint(0, 400))

    label.bind('<Button-1>', drag_start)
    label.bind('<B1-Motion>', drag_motion)

    global labels
    labels.append(label)


def start_mesh_config():

    global popup_open

    if popup_open:
        return

    popup_open = True

    popup = tk.Toplevel()
    popup.wm_title("Meshing")
    popup.protocol("WM_DELETE_WINDOW", lambda: close_popup(popup))

    selected = tk.StringVar()

    tk.Label(popup, text="Select preferred meshing granularity.").pack()

    r0 = tk.Radiobutton(popup, text="Coarse", value=0, variable=selected)
    r1 = tk.Radiobutton(popup, text="Medium", value=1, variable=selected)
    r2 = tk.Radiobutton(popup, text="Fine", value=2, variable=selected)

    r0.pack(padx=5, pady=5)
    r1.pack(padx=5, pady=5)
    r2.pack(padx=5, pady=5)

    mesh_btn = tk.Button(popup, text="tmp", command=lambda: triangulate(selected.get()))
    mesh_btn.pack(padx=5, pady=5)


def close_popup(window):
    global popup_open
    popup_open = False
    window.destroy()


def triangulate(granularity,
                x_max=int(window_width),
                y_max=int(window_height)):
    tri.calculate_mesh(x_max, y_max, wall_points, [])


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(background="#BBBBBB")
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

        if left:
            # Code to run if Frame is on the left side ...
            self.grid(row=0, column=0, padx=2, pady=2)

            self.canvas = OwnCanvas(self)
            self.canvas.bind('<Button-1>', draw_wall_points)

            # TODO -1-
            global drawing_canvas
            drawing_canvas = self.canvas

        else:
            # here on the right side
            self.grid(row=0, column=1, padx=2, pady=2)

            tk.Label(self, text="Instructions:") \
                .grid(row=0, column=0, padx=10, pady=2)

            instructions = tk.Label(self, text="1\n2\n2\n3\n4\n5\n6\n7\n8\n9\n")
            instructions.grid(row=1, column=0, padx=10, pady=2)

            add_sqr = tk.Button(self, text='Add Square (deprecated)', command=add_label)
            add_sqr.grid(row=0, column=1)

            triangulate_btn = tk.Button(self, text='Calculate Mesh', command=start_mesh_config, state=tk.DISABLED)
            triangulate_btn.grid(row=2, column=1)

            finish_wall_points_btn = tk.Button(self,
                                               text='Finish Points',
                                               command=lambda: finish_wall_points(triangulate_btn,
                                                                                  finish_wall_points_btn))
            finish_wall_points_btn.grid(row=1, column=1)


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
