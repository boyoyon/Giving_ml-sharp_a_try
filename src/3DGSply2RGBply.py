from plyfile import PlyData
import numpy as np
import os, sys

def save_ply(ply_path, lines):

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

        line = 'property float opacity\n'
        f.write(line)

        line = 'property uchar red\n'
        f.write(line)

        line = 'property uchar green\n'
        f.write(line)

        line = 'property uchar blue\n'
        f.write(line)

        line = 'end_header\n'
        f.write(line)

        for line in lines:
            f.write(line)

argv = sys.argv
argc = len(argv)

print('%s converts 3DGS ply to RGB ply' % argv[0])
print('[usage] python %s <ply>' % argv[0])

if argc < 2:
    quit()

plydata = PlyData.read(argv[1])
X = plydata['vertex']['x']
Y = plydata['vertex']['y']
Z = plydata['vertex']['z']

opac = plydata['vertex']['opacity']

f_dc_0 = plydata['vertex']['f_dc_0']
f_dc_1 = plydata['vertex']['f_dc_1']
f_dc_2 = plydata['vertex']['f_dc_2']

lines = []

nrPoints = X.shape[0]
c0 = 1 / (1.77 * 2)

for i in range(nrPoints):

    x = X[i]
    y = Y[i]
    z = Z[i]

    o = 1/(1+np.exp(-opac[i]))

    r = max(0, min(255, int((f_dc_0[i] * c0 + 0.5) * 255)))
    g = max(0, min(255, int((f_dc_1[i] * c0 + 0.5) * 255)))
    b = max(0, min(255, int((f_dc_2[i] * c0 + 0.5) * 255)))

    line = '%f %f %f %f %d %d %d\n' % (x, y, z, o, r, g, b)

    lines.append(line)

base = os.path.basename(argv[1])
filename = os.path.splitext(base)[0]
dst_path = '%s_3dgs2rgb.ply' % filename
save_ply(dst_path, lines)
print('save %s' % dst_path)



