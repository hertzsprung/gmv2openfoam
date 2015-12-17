#!/usr/bin/env python3
import numpy as np
from numpy import pi
from collections import Counter
from numpy.linalg import norm

vertices = [] # a list of (x, y, z) tuples
faces = set() # a set of faces, each element being a list of vertex indices

with open("points.dat") as points_file:
    f = points_file.readlines()
    print("Loaded {v} vertices".format(v=len(f)))
    for vertex_str in f:
        vertices.append(tuple([float(v) for v in vertex_str.split()]))

with open("faces.dat") as faces_file:
    faces_file_lines = faces_file.readlines()
    print("Loaded {f} faces".format(f=len(faces_file_lines)))
    for faceI, face_str in enumerate(faces_file_lines):
        faces.add(tuple([int(f) for f in face_str.split()]))
    print("Found {f} unique faces".format(f=len(faces)))

# find front faces (must have all vertices with y=0)
front_faces = []
for f in faces:
    include = True
    for v in f:
        if vertices[v-1][1] > 0:
            include = False

    if include:
        front_faces.append(f)

print("Found {f} unique front faces".format(f=len(front_faces)))

print("Vertices per face stats: ", Counter([len(f) for f in front_faces]))

print("Removing zero-length edges")
def remove_zero_length_edges(f):
    unique_vertices = {}
    for v in f:
        unique_vertices[vertices[v-1]] = v
    return list(unique_vertices.values())

front_faces = [remove_zero_length_edges(f) for f in front_faces]

print("Vertices per face stats: ", Counter([len(f) for f in front_faces]))

print("Correcting orientation")

def centre(face):
    return np.sum(np.array([np.array(vertices[v-1]) for v in face]), axis=0)/len(face)

def edge_vector(centre, v):
    return centre - np.array(vertices[v-1])

def vertex_with_smallest_angle(edge, candidate_edges):
    min_angle_vertexI = -1
    min_angle = 2*pi
    for i, candidate_edge in enumerate(candidate_edges):
        # angle needs to be from 0 -- 2*PI, see http://math.stackexchange.com/q/878785/89878
        dot = np.dot(edge, candidate_edge)
        det = edge[0] * candidate_edge[2] - edge[2] * candidate_edge[0]
        angle = np.arctan2(det, dot)
        if angle < min_angle and angle > 0:
            min_angle = angle
            min_angle_vertexI = i
    return min_angle_vertexI, min_angle

def reorient(face):
    c = centre(face)
    oriented_face = list(face)
    for i, v in enumerate(oriented_face):
        min_angle_vertexI, min_angle = vertex_with_smallest_angle(edge_vector(c, v), [edge_vector(c, v) for v in oriented_face[i+1:]])
        if min_angle_vertexI > -1:
            oriented_face[i+1], oriented_face[i+1+min_angle_vertexI] = oriented_face[i+1+min_angle_vertexI], oriented_face[i+1]

    return oriented_face

front_faces = [reorient(f) for f in front_faces]

with open("surface.obj", "w") as fh:
    for v in vertices:
        print("v {x} {y} {z}".format(x=v[0], y=v[1], z=v[2]), file=fh)
    for f in front_faces:
        print("f " + " ".join([str(v) for v in f]), file=fh)
