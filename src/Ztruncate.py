from plyfile import PlyData, PlyElement
import numpy as np
import sys

def save_ply(path_ply,X,Y, Z, R, G, B):

    with open(path_ply, mode='w') as f:

        line = 'ply\n'
        f.write(line)

        line = 'format ascii 1.0\n'
        f.write(line)

        line = 'element vertex %d\n' % X.shape[0]
        f.write(line)

        line = 'property float x\n'
        f.write(line)

        line = 'property float y\n'
        f.write(line)

        line = 'property float z\n'
        f.write(line)

        line = 'property uchar red\n'
        f.write(line)

        line = 'property uchar green\n'
        f.write(line)

        line = 'property uchar blue\n'
        f.write(line)

        line = 'end_header\n'
        f.write(line)

        for i in range(X.shape[0]):
            line = '%f %f %f %d %d %d\n' % (X[i], Y[i], Z[i], R[i], G[i], B[i])
            f.write(line)

    print('save %s' % path_ply)

argv = sys.argv
argc = len(argv)

print('%s truncates the PLY in the Z-direction' % argv[0])
print('[usage] python %s <ply> [<percent(1-100)>]' % argv[0])

if argc < 2:
    quit()

PERCENT = 5

if argc > 2:
    PERCENT = int(argv[2])

plydata = PlyData.read(argv[1])
X = plydata['vertex']['x']
Y = plydata['vertex']['y']
Z = plydata['vertex']['z']
R = plydata['vertex']['red']
G = plydata['vertex']['green']
B = plydata['vertex']['blue']

maxZ = np.max(Z)
minZ = np.min(Z)
ampZ =  maxZ - minZ
TH = minZ + ampZ * PERCENT / 100

indices = np.where(Z > TH)

X = np.delete(X, indices)
Y = np.delete(Y, indices)
Z = np.delete(Z, indices)
R = np.delete(R, indices)
G = np.delete(G, indices)
B = np.delete(B, indices)

path_ply = 'Ztruncated.ply' 
save_ply(path_ply,X,Y, Z, R, G, B)
