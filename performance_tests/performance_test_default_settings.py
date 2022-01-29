"""Performance test for searching the triangle in which given points are."""

import time
import point_generator

from point_generator import import_mesh

performance_test_file = 'middle_points.txt'
#performance_test_file = 'random_points.txt'
#performance_test_file = 'random_points_random_triangles.txt'

# ToDo Create points here before
#  to make performance testing a two step piece and not a 3 piece

nodes = []
triangles = []
random_points = []

threshhold = 1e-2
amount_of_random_generated_points = 0


def main():
    print(str(threshhold))
    print('Generating points. n = ' + str(amount_of_random_generated_points))
    point_generator.generate_points(amount_of_random_generated_points)
    print('Reading data files.')
    start_up()
    test()
    clean_up()


def start_up():
    """Reading the needed data structures from files"""
    global nodes, triangles, random_points

    nodes, triangles = import_mesh()
    random_points = read_random_points()


def read_random_points(path='random_points/' + performance_test_file):
    """Function to read files with random points"""

    print('Point file: ' + performance_test_file)

    points = []
    with open(path, "r") as f:
        while True:
            split_line = f.readline().split("\t")

            # if end of file is reached
            if len(split_line) < 2:
                break

            points.append((float(split_line[0]), float(split_line[1])))

    return points


def test():
    point_triangle_mapping = []
    # TODO save tris in list not set

    print('Test Starting')
    start_time = int(time.time() * 1000)

    for i in range(len(random_points)):
        #point_triangle_mapping.append(find_triangle(random_points[i]))
        point_triangle_mapping.append(find_triangle_square_check(random_points[i]))
        if (i + 1) % (int(len(random_points) / 10)) == 0:
            print('Found point ' + str(i + 1) + ' of ' + str(len(random_points)))

    end_time = int(time.time() * 1000)
    print('Test finished')
    print(str(end_time - start_time) + ' ms')
    print(str((end_time - start_time) / 1000) + ' s')


def find_triangle(point):
    for current_tri_number in range(len(triangles)):

        # get points a, b and c
        a = nodes[triangles[current_tri_number][0]]
        b = nodes[triangles[current_tri_number][1]]
        c = nodes[triangles[current_tri_number][2]]

        area = calculate_triangle_area(a, b, c)

        # calculate 3 areas of tri with middle point and add them
        area1 = calculate_triangle_area(a, b, point)
        area2 = calculate_triangle_area(a, point, c)
        area3 = calculate_triangle_area(point, b, c)

        area_sum = area1 + area2 + area3

        # see if area equals
        if abs(area_sum - area) < threshhold:
            return current_tri_number

    print('Error: Could find a fitting triangle for point P(' + str(point[0]) + ',' + str(point[1]) + ').')
    return -1


def find_triangle_square_check(point):
    for current_tri_number in range(len(triangles)):

        # get points a, b and c
        a = nodes[triangles[current_tri_number][0]]
        b = nodes[triangles[current_tri_number][1]]
        c = nodes[triangles[current_tri_number][2]]

        minx = min(a[0], b[0], c[0])
        maxx = max(a[0], b[0], c[0])
        miny = min(a[1], b[1], c[1])
        maxy = max(a[1], b[1], c[1])

        if point[0] < minx or point[0] > maxx or point[1] < miny or point[1] > maxy:
            continue

        area = calculate_triangle_area(a, b, c)

        # calculate 3 areas of tri with middle point and add them
        area1 = calculate_triangle_area(a, b, point)
        area2 = calculate_triangle_area(a, point, c)
        area3 = calculate_triangle_area(point, b, c)

        area_sum = area1 + area2 + area3

        # see if area equals
        if abs(area_sum - area) < threshhold:
            return current_tri_number

    print('Error: Could find a fitting triangle for point P(' + str(point[0]) + ',' + str(point[1]) + ').')
    return -1


def calculate_triangle_area(a, b, c):
    """Calculates the performance optimized area of a triangle with given points a, b and c. Points need to be
    a two tuple with x and y coordinates."""
    ab = (b[0] - a[0], b[1] - a[1])
    ac = (c[0] - a[0], c[1] - a[1])
    # Cross product
    area = (ab[0] * ac[1]) - (ac[0] * ab[1])

    return abs(area)


def clean_up():
    pass


if __name__ == "__main__":
    main()

