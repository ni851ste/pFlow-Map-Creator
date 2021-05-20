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

hole_poly_number = -1
hole_polys = []
hole_poly_lines = []

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

    current_color = 'red'
    if hole_poly_number >= 0:
        current_color = 'blue'

    point = drawing_canvas.create_oval([x - point_radius, y - point_radius,
                                        x + point_radius, y + point_radius],
                                       outline='black', fill=current_color)

    current_point_list = None

    if hole_poly_number >= 0:
        global hole_polys
        hole_polys[hole_poly_number].append((x, y, point))
        current_point_list = hole_polys[hole_poly_number]
    else:
        global wall_points
        # x = X-Coord
        # y = Y-Coord
        # point is the ID of point in canvas (used to delete and redraw)
        wall_points.append((x, y, point))
        current_point_list = wall_points

    if len(current_point_list) > 1:
        to_be_drawn_points = current_point_list[-2:]
        p1 = to_be_drawn_points[0]
        p2 = to_be_drawn_points[1]

        line = drawing_canvas.create_line([p1[0], p1[1], p2[0], p2[1]], fill='black')
        global lines
        lines.append(line)


def finish_wall_points(triangulate_btn, finish_button):
    if len(wall_points) < 3:
        print('Cant finish, since not enough points have been placed.')
        return

    if hole_poly_number < 0:
        # Draw the last line between first and last given point
        p1 = wall_points[-1]
        p2 = wall_points[0]
        line = drawing_canvas.create_line([p1[0], p1[1], p2[0], p2[1]], fill='black')
        global lines
        lines.append(line)
    else:
        current_wall_points = hole_polys[hole_poly_number]

        p1 = current_wall_points[-1]
        p2 = current_wall_points[0]
        line = drawing_canvas.create_line([p1[0], p1[1], p2[0], p2[1]], fill='black')
        global hole_poly_lines
        hole_poly_lines[hole_poly_number].append(line)

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

    # modulo needed here in case last point in list is clicked and the index (i + 1) overflows
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


def draw_additional_polygons(triangulate_btn, finish_button):
    global drawing_canvas, hole_poly_number

    drawing_canvas.unbind('<Button-1>')
    drawing_canvas.unbind('<B1-Motion>')
    drawing_canvas.unbind('<ButtonRelease-1>')

    drawing_canvas.bind('<Button-1>', draw_wall_points)

    global hole_polys, hole_poly_lines
    hole_poly_number += 1
    hole_polys.append([])
    hole_polys[hole_poly_number] = []

    hole_poly_lines.append([])
    hole_poly_lines[hole_poly_number] = []

    triangulate_btn.config(state='disabled')
    finish_button.config(state='normal')


def start_mesh_config():

    # Make sure there is only one popup open
    global popup_open
    if popup_open:
        return

    popup_open = True

    popup = tk.Toplevel()
    popup.wm_title("Meshing")
    popup.protocol("WM_DELETE_WINDOW", lambda: close_popup(popup))

    selected = tk.IntVar()

    tk.Label(popup, text="Select preferred meshing granularity.").pack()

    r0 = tk.Radiobutton(popup, text="Coarse", value=0, variable=selected)
    r1 = tk.Radiobutton(popup, text="Medium", value=1, variable=selected)
    r2 = tk.Radiobutton(popup, text="Fine", value=2, variable=selected)

    r0.pack(padx=5, pady=5)
    r1.pack(padx=5, pady=5)
    r2.pack(padx=5, pady=5)

    mesh_btn = tk.Button(popup, text="Generate Mesh", command=lambda: triangulate(selected.get(), popup))
    mesh_btn.pack(padx=5, pady=5)


def close_popup(window):
    """Custom close function for mesh config popup"""
    global popup_open
    popup_open = False
    window.destroy()


def triangulate(granularity_level,
                config_popup,
                window_x_max=int(window_width),
                window_y_max=int(window_height)):
    """Function to start the meshing"""

    # Start to calculate the granularity
    # by finding the size of the polygon
    poly_x_max = poly_y_max = 0
    poly_x_min = poly_y_min = sys.maxsize

    for point in wall_points:
        x = point[0]
        y = point[1]

        poly_x_min = min(poly_x_min, x)
        poly_y_min = min(poly_y_min, y)

        poly_x_max = max(poly_x_max, x)
        poly_y_max = max(poly_y_max, y)

    poly_width = poly_x_max - poly_x_min
    poly_height = poly_y_max - poly_y_min

    # Configuration of granularity level
    granularity = 0
    if granularity_level == 0:
        # Coarse
        granularity = ((poly_width / 0.3) + (poly_height / 0.3)) / 2
    elif granularity_level == 1:
        # Normal
        granularity = ((poly_width / 3) + (poly_height / 3)) / 2
    elif granularity_level == 2:
        # Fine
        granularity = ((poly_width / 30) + (poly_height / 30)) / 2

    tri.calculate_mesh(granularity, window_x_max, window_y_max, wall_points, hole_polys)

    close_popup(config_popup)


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

            triangulate_btn = tk.Button(self, text='Calculate Mesh', command=start_mesh_config, state=tk.DISABLED)
            triangulate_btn.grid(row=1, column=1)

            finish_wall_points_btn = tk.Button(self,
                                               text='Finish Points',
                                               command=lambda: finish_wall_points(triangulate_btn,
                                                                                  finish_wall_points_btn))
            finish_wall_points_btn.grid(row=0, column=1)

            add_sqr = tk.Button(self, text='Draw holes', command=lambda: draw_additional_polygons(triangulate_btn,
                                                                                                   finish_wall_points_btn))
            add_sqr.grid(row=2, column=1)


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
