#!/usr/bin/env python3
from collections import defaultdict
from collections import Counter

vertices = [] # a list of (x, y, z) tuples
faces = [] # a list of faces, each element being a list of vertex indices

# a list of face indices, keyed by a frozenset of vertex indices
# the zeroth face index in the list is considered the normative face index
# and subsequent face indices are duplicates
unique_face_dict = defaultdict(list) 

face_index_dict = {} # a mapping from non-unique to unique face indices

cells = [] # a list of cells, each element being a list of face indices
owner = []
neighbour = []

def uniquify_face_index(faceI):
    return unique_face_dict[frozenset(faces[faceI])][0]

def reindex_face(old_faceI):
    return face_index_dict[old_faceI]

with open("points.dat") as points_file:
    for vertex_str in points_file.readlines():
        vertices.append(tuple([float(v) for v in vertex_str.split()]))

with open("faces.dat") as faces_file:
    for faceI, face_str in enumerate(faces_file.readlines()):
        face = [int(f) for f in face_str.split()]
        faces.append(face)
        unique_face_dict[frozenset(face)].append(faceI)

with open("cells.dat") as cells_file:
    for cell_str in cells_file.readlines():
        cells.append([int(c) for c in cell_str.split()])

cells = [list(map(uniquify_face_index, cell)) for cell in cells]

faces = []
for new_faceI, item in enumerate(unique_face_dict.items()):
    faces.append(item[0])
    for old_faceI in item[1]:
        face_index_dict[old_faceI] = new_faceI

cells = [map(reindex_face, cell) for cell in cells]

adjacency = [[] for _ in range(len(faces))]

for cellI, cell in enumerate(cells):
    for faceI in cell:
        adjacency[faceI].append(cellI)

# TODO: internal faces need to go first, external faces last
# TODO: presumably all faces, internal or boundary have an owner, but only internal faces have a neighbour?
# TODO: figure out boundary faces
internal_faces = [faces[faceI] for faceI, cells in enumerate(adjacency) if len(cells) > 1]
owner = [cells[0] for cells in adjacency if len(cells) > 1]
neighbour = [cells[1] for cells in adjacency if len(cells) > 1]

def format_list(l):
    return "(" + " ".join([str(x) for x in l]) + ")"

def format_file(name, l, formatter, clazz):
    with open("constant/polyMesh/" + name, "w") as f:
        print("""FoamFile
{{
    version     2.0;
    format      ascii;
    class       {clazz};
    location    "constant/polyMesh";
    object      {name};
}}""".format(name=name, clazz=clazz), file=f)
        print(len(l), file=f)
        print("(", file=f)
        for x in l:
            print(formatter(x), file=f)
        print(")", file=f)

format_file("points", vertices, format_list, "vectorField")
format_file("faces", internal_faces, format_list, "faceList")
format_file("owner", owner, str, "labelList")
format_file("neighbour", neighbour, str, "labelList")
