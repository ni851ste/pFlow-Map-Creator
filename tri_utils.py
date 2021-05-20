import pygimli as pg
import pygimli.meshtools as mt

granularity_old = 100     # for fine grain 0.01
segment_gran = int(1 / (granularity_old * 10))


def main():
    w = mt.createWorld(start=[-5, -5], end=[5, 5], area=granularity_old)
    # TODO what does "leftDirection" mean?
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

    mt.exportPLC(mesh, "test.plc")
    mesh.exportAsTetgenPolyFile("polyFile")

    # mt.exportSTL(w, "test.stl")
    # mt.exportFenicsHDF5Mesh(w, "test.hdf5")

    pg.wait()


if __name__ == "__main__":
    main()


def calculate_mesh(granularity, x_max, y_max, points, holes):

    w = mt.createWorld(start=[0, 0], end=[x_max, y_max], area=int(granularity))

    # Corner Points get drawn as a hole to only generate mesh over the custom polygon
    graph_corner_points = [(0, 0), (0, y_max), (x_max, y_max), (x_max, 0)]
    drawn_graph_corners = mt.createPolygon(graph_corner_points, isClosed=True, isHole=True)

    drawn_walls = draw_polygon_by_polygon(points, y_max, int(granularity))

    to_be_meshed = [w, drawn_graph_corners, drawn_walls]

    for hole in holes:
        drawn_hole = draw_polygon_by_polygon(hole, y_max, int(granularity), hole=True)
        to_be_meshed.append(drawn_hole)

    mesh = mt.createMesh(to_be_meshed)
    ax, _ = pg.show(mesh)
    pg.wait()


def draw_polygon_by_polygon(points, y_max, granularity, hole=False):

    corrected_points = []
    # Points are getting corrected since the graphs origin is one time
    # at top left and needs to be adjusted to bottom left
    for point in points:
        corrected_points.append((point[0], y_max - point[1]))

    # TODO tweak area parameter if needed
    p1 = mt.createPolygon(corrected_points, isClosed=True, isHole=hole, area=float(granularity))

    return p1


def draw_polygon_by_lines(points, y_max):
    # Function to draw lines between all of the points given
    drawn_lines = []

    for i in range(0, len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]

        line = draw_line(p1, p2, y_max)
        drawn_lines.append(line)

    p1 = points[-1]
    p2 = points[0]

    line = draw_line(p1, p2, y_max)
    drawn_lines.append(line)

    return drawn_lines


def draw_line(p1, p2, y_max):
    # Y-Coords have to be calculated with "y_max" because
    # origin on canvas is top left
    # and origin on mesh window is bottom left
    line = mt.createLine(start=[p1[0], y_max - p1[1]], end=[p2[0], y_max - p2[1]], leftDirection=False)
    return line



