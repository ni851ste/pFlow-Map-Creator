import pygimli as pg
import pygimli.meshtools as mt
import os

granularity_old = 100  # for fine grain 0.01
segment_gran = int(1 / (granularity_old * 10))


def main():
    w = mt.createWorld(start=[-5, -5], end=[5, 5], area=granularity_old)
    # TODO what does "leftDirection" mean?
    l1 = mt.createLine(start=[2, 2], end=[1, 2], leftDirection=False)
    # l2 = mt.createLine(start=[2, 2], end=[2, 2], leftDirection=False)

    p1 = mt.createPolygon([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]], isClosed=True, marker=3)

    mesh = mt.createMesh([w, l1, p1, ])
    print(str(mesh))
    # print(str(mesh.cells()))
    # mt.poly()
    # print(mesh.cells())

    #ax, _ = pg.show(mesh)
    #pg.wait()

    # create tmp and .poly export
    path = str(os.getcwd()) + "/tmp"
    if not os.path.exists(path):
        os.mkdir(path)

    mt.exportPLC(mesh, "tmp/tmp_export.poly")

    f = open("tmp/tmp_export.poly", "r")

    first_info_line = f.readline()
    no_of_nodes = int(first_info_line.split("\t")[0])
    print(str(no_of_nodes) + " nodes found.")

    nodes = []

    for i in range(no_of_nodes):
        read_line = f.readline()
        split_line = read_line.split("\t")

        nodes.append((float(split_line[1]), float(split_line[2])))

    second_info_line = f.readline()
    no_of_boundaries = int(second_info_line.split("\t")[0])

    print(str(no_of_boundaries) + " boundaries found")

    boundaries = []
    for i in range(no_of_boundaries):
        read_line = f.readline()
        split_line = read_line.split("\t")

        boundaries.append((int(split_line[1]), int(split_line[2])))

    export(mesh, boundaries)


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


def export(mesh, boundaries):
    # first boundary

    found_triangles = []
    i = 0
    second_loop = False

    while i < len(boundaries) - 2:
        try:
            p0 = boundaries[i][0]
            p1 = boundaries[i][1]
            p2 = None

            node_set = {p0, p1}

            j_range = None
            if second_loop:
                j_range = range(i + 2, len(boundaries) - 1)
            else:
                j_range = range(i + 1, len(boundaries) - 1)

            for j in j_range:
                # find 2nd boundary

                bound = boundaries[j]

                b0 = bound[0]
                b1 = bound[1]

                if b0 in node_set or b1 in node_set:
                    # found 2nd boundary
                    #print("j: " + str(j))

                    if b0 in node_set:
                        p2 = b1
                    elif b1 in node_set:
                        p2 = b0

                    node_set.add(p2)

                    if node_set in found_triangles:
                        # searching for a triangle that has already been found
                        # continue to move second pointer down the list
                        node_set.remove(p2)
                        continue
                    # print(str(p0) + " " + str(p1) + " " + str(p2))

                    for k in range(j + 1, len(boundaries)):
                        # find 3rd boundary
                        last_bound = boundaries[k]
                        lb0 = last_bound[0]
                        lb1 = last_bound[1]

                        if lb0 in node_set and lb1 in node_set:
                            # found 3rd boundary
                            #print("k: " + str(k))
                            if node_set not in found_triangles:
                                found_triangles.append(node_set)
                            raise LoopDone

                    node_set.remove(p2)
                    p2 = None
            #i = i + 1
            second_loop = True
            raise LoopDone
        except LoopDone:
            if second_loop:
                i = i + 1
                #print("i: " + str(i))
                second_loop = False
            else:
                second_loop = True

            #continue



    print(str(len(found_triangles)) + " cells have been found.")
    #ax, _ = pg.show(mesh)
    #pg.wait()


class LoopDone(Exception): pass


if __name__ == "__main__":
    main()
