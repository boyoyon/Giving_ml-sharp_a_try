from plyfile import PlyData
import numpy as np
import cv2, glob, os, sys

def save_ply(ply_path, lines, faces):

    with open(ply_path, mode='w') as f:

        line = 'ply\n'
        f.write(line)

        line = 'format ascii 1.0\n'
        f.write(line)

        line = 'element vertex %d\n' % len(lines)
        f.write(line)

        line = 'property float x\n'
        f.write(line)

        line = 'property float y\n'
        f.write(line)

        line = 'property float z\n'
        f.write(line)

        line = 'property float s\n'
        f.write(line)

        line = 'property float t\n'
        f.write(line)

        line = 'element face %d\n' % len(faces)
        f.write(line)

        line = 'property list uchar int vertex_indices\n'
        f.write(line)

        line = 'end_header\n'
        f.write(line)

        for line in lines:
            f.write(line)

        for face in faces:
            f.write(face)

SKIP = 300

argv = sys.argv
argc = len(argv)

print('%s converts 3DGS ply to UV ply' % argv[0])
print('[usage] python %s <wildcard for 3DGS plys> [<skip rate (default: %d)>]' % (argv[0], SKIP))

if argc < 2:
    quit()

paths = glob.glob(argv[1])

if argc > 2:
    SKIP = int(argv[2])


for i, path in enumerate(paths):

    print('processing %d/%d(%s)' % ((i+1), len(paths), path))

    plydata = PlyData.read(path)
    X = plydata['vertex']['x']
    Y = plydata['vertex']['y']
    Z = plydata['vertex']['z']

    intrinsic = plydata['intrinsic']['intrinsic'].reshape(3,3)
    fx = intrinsic[0][0]
    fy = intrinsic[1][1]
    cx = intrinsic[0][2]
    cy = intrinsic[1][2]
    
    image_size = plydata['image_size']['image_size']

    lines = []

    nrPoints = X.shape[0]

    rect = (0, 0, image_size[0], image_size[1])
    point2d = []
    subdiv = cv2.Subdiv2D(rect)

    for i in range(0, nrPoints, SKIP):

        x = X[i]
        y = Y[i]
        z = Z[i]

        xx = fx * x + cx * z
        yy = fy * y + cy * z
    
        u = int(xx / z)
        if u < 0 or u >= image_size[0]:
            continue
    
        v = int(yy / z)
        if v < 0 or v >= image_size[1]:
            continue

        line = '%f %f %f %f %f\n' % (x, y, z, u/image_size[0], 1.0 - v/image_size[1])
        lines.append(line)

        subdiv.insert((u, v))
        point2d.append((u, v))

    triangles = subdiv.getTriangleList()

    faces = []

    for triangle in triangles:
        found = 0
        idx1 = -1
        idx2 = -1
        idx3 = -1

        for i in range(len(point2d)):
            if triangle[0] == point2d[i][0] and triangle[1] == point2d[i][1]:
                idx1 = i                    
                found += 1
            if triangle[2] == point2d[i][0] and triangle[3] == point2d[i][1]:
                idx2 = i                    
                found += 1
            if triangle[4] == point2d[i][0] and triangle[5] == point2d[i][1]:
                idx3 = i                    
                found += 1        

            if found == 3:
                #face = '3 %d %d %d\n' % (idx1, idx2, idx3)
                face = '3 %d %d %d\n' % (idx1, idx3, idx2)
                faces.append(face)
                break

    base = os.path.basename(path)
    filename = os.path.splitext(base)[0]
    dst_path = '%s_3dgs2uv.ply' % filename
    save_ply(dst_path, lines, faces)
    print('save %s' % dst_path)

