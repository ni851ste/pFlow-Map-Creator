import pygimli as pg
import pygimli.meshtools as mt

granularity = 5     # for fine grain 0.01
segment_gran = int(1 / (granularity * 10))

w = mt.createWorld(start=[-5, -5], end=[5, 5], area=granularity)
l1 = mt.createLine(start=[2, 2], end=[1, 2], leftDirection=False)
# l2 = mt.createLine(start=[2, 2], end=[2, 2], leftDirection=False)

p1 = mt.createPolygon([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]], isClosed=True, marker=3)

mesh = mt.createMesh([w, l1, p1, ])
print(str(mesh))
# mt.poly()

print(str(mesh.nodes()))



ax, _ = pg.show(mesh)
#ax, _ = pg.show([w, l1, p1, ], ax=ax, fillRegion=False)

mt.exportPLC(mesh, "test.plc")
mesh.exportAsTetgenPolyFile("polyFile")

#mt.exportSTL(w, "test.stl")
#mt.exportFenicsHDF5Mesh(w, "test.hdf5")


pg.wait()