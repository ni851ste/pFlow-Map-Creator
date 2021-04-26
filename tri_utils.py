import pygimli as pg
import pygimli.meshtools as mt

granularity = 100     # for fine grain 0.01
segment_gran = int(1 / (granularity * 10))


def main():
    w = mt.createWorld(start=[-5, -5], end=[5, 5], area=granularity)
    # TODO what does "leftDirection" mean?
    l1 = mt.createLine(start=[2, 2], end=[1, 2], leftDirection=False)
    # l2 = mt.createLine(start=[2, 2], end=[2, 2], leftDirection=False)

    # TODO create room as polygon and not single lines??
    p1 = mt.createPolygon([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]], isClosed=True, marker=3)

    mesh = mt.createMesh([w, l1, p1, ])
    print(str(mesh))
    # mt.poly()


    #for cell in mesh.cells():
    #    print(cell)

    print(str(mesh.cells()))

    ax, _ = pg.show(mesh)
    #ax, _ = pg.show([w, l1, p1, ], ax=ax, fillRegion=False)

    mt.exportPLC(mesh, "test.plc")
    mesh.exportAsTetgenPolyFile("polyFile")

    #mt.exportSTL(w, "test.stl")
    #mt.exportFenicsHDF5Mesh(w, "test.hdf5")

    pg.wait()


if __name__ == "__main__":
    main()


def calculate_mesh(x_max, y_max, points, obstacles):

    drawn_lines = []
    w = mt.createWorld(start=[0, 0], end=[x_max, y_max], area=granularity)

    for i in range(0, len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]

        # TODO duplicate Code here
        line = mt.createLine(start=[p1[0], p1[1]], end=[p2[0], p2[1]], leftDirection=False)
        drawn_lines.append(line)

    p1 = points[-1]
    p2 = points[0]
    line = mt.createLine(start=[p1[0], p1[1]], end=[p2[0], p2[1]], leftDirection=False)
    drawn_lines.append(line)

    to_do_draw = [w]
    to_do_draw = to_do_draw + drawn_lines


    mesh = mt.createMesh(to_do_draw)
    ax, _ = pg.show(mesh)
    pg.wait()
