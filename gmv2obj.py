#!/usr/bin/env python3
import numpy as np
from numpy import cross
from collections import Counter
from itertools import permutations

vertices = [] # a list of (x, y, z) tuples
faces = [] # a set of faces, each element being a list of vertex indices

with open("points.dat") as points_file:
    f = points_file.readlines()
    print("Loaded {v} vertices".format(v=len(f)))
    for vertex_str in f:
        vertices.append(tuple([float(v) for v in vertex_str.split()]))
    print("Found {v} unique vertices".format(v=len(vertices)))

with open("faces.dat") as faces_file:
    faces_file_lines = faces_file.readlines()
    print("Loaded {f} faces".format(f=len(faces_file_lines)))
    for faceI, face_str in enumerate(faces_file_lines):
        faces.append(tuple([int(f) for f in face_str.split()]))
    print("Found {f} unique faces".format(f=len(faces)))

front_faces = []
for f in faces:
    include = True
    for v in f:
        if vertices[v-1][1] > 0:
            include = False

    if include:
        front_faces.append(f)

print("Found {f} unique front faces".format(f=len(front_faces)))

#vertex_index_dict = {}
#front_vertices = []

#for old_index, v in enumerate(vertices, start=1):
#    if v[1] > 0:
#        continue
#
#    front_vertices.append(v)
#    vertex_index_dict[old_index] = len(front_vertices)
#
#print("Found {f} front vertices".format(f=len(front_vertices)))

#def reindex_vertex(old_index):
#    return vertex_index_dict[old_index]
#
#front_faces = [list(map(reindex_vertex, f)) for f in front_faces]

print("Vertices per face stats: ", Counter([len(f) for f in faces]))

# check orientation

def edge_vectors(face):
    f = list(face)
    f.append(face[0])
    return [np.array(vertices[vb-1])-np.array(vertices[va-1]) for va, vb in zip(f, f[1:])]

def vertex_ordering_is_sane(face):
    edges = edge_vectors(face)
    for ea, eb in zip(edges, edges[1:]):
        xprod = cross(ea, eb)
        if not (xprod[0] == 0 and xprod[2] == 0 and xprod[1] >= 0):
            return False
    return True

oriented_front_faces = []

for f in front_faces:
    for candidate_f in permutations(f):
        if vertex_ordering_is_sane(candidate_f):
            oriented_front_faces.append(candidate_f)
            break
    else:
        raise RuntimeError("can't find a suitable orientation for face " + '\t'.join([",".join([str(y) for y in vertices[x-1]]) for x in f]))

with open("surface.obj", "w") as fh:
    for v in vertices:
        print("v {x} {y} {z}".format(x=v[0], y=v[1], z=v[2]), file=fh)
    for f in oriented_front_faces:
        print("f " + " ".join([str(v) for v in f]), file=fh)
