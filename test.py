import tkinter as tk
import pygimli as pg
import pygimli.meshtools as mt

window_width = "1150"


def line_delete_test():
    point_size = 20
    x = 200
    y = 400
    world = tk.Tk()
    world.geometry("800x600")
    canvas = tk.Canvas(world, width=800, height=600, bg='white')

    l1 = canvas.create_line(50, 50, 100, 100, fill='black')
    l2 = canvas.create_line(200, 200, 300, 400, fill='black')
    l3 = canvas.create_line(111, 50, 222, 50, fill='black')

    c1 = canvas.create_oval([x - (point_size / 2), y - (point_size / 2),
                             x + (point_size / 2), y + (point_size / 2)],
                            outline='black', fill='red')
    canvas.pack()

    print(c1)

    canvas.delete(l1)
    canvas.delete(c1)
    world.mainloop()


def exporting():
    w = mt.createWorld(start=[-5, -5], end=[5, 5], area=1)
    l1 = mt.createLine(start=[2, 2], end=[1, 2], leftDirection=False)
    # l2 = mt.createLine(start=[2, 2], end=[2, 2], leftDirection=False)

    p1 = mt.createPolygon([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]], isClosed=True, marker=3)

    mesh = mt.createMesh([w, l1, p1, ])
    print(str(mesh))
    # mt.poly()

    # for cell in mesh.cells():
    #    print(cell)

    print(str(mesh.cells()))

    ax, _ = pg.show(mesh)
    # ax, _ = pg.show([w, l1, p1, ], ax=ax, fillRegion=False)

    # not openable
    # mt.exportFenicsHDF5Mesh(w, "exports/new_test.txt")

    mesh.exportAsTetgenPolyFile(mesh, "tetgen_test")
    mt.exportPLC(mesh, "exports/new_test.plc")
    #mesh.exportAsTetgenPolyFile("polyFile")

    # mt.exportSTL(w, "test.stl")


    pg.wait()


def string_test():
    a = "cooler Test"
    b = "\taber Hallo"

    a += b
    print(a)


def touple_type_test():
    a = 1
    b = (1 , 2)
    print(type(a))
    print(type(b))


def list_index_test():
    lst = []

    lst[0] = '0'
    lst[1] = '1'
    lst[2] = '2'
    lst[4] = '4'

    for thing in lst:
        print(thing)

if __name__ == "__main__":
    list_index_test()
