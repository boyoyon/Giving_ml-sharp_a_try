from plyfile import PlyData, PlyElement
import numpy as np
import cv2, os, sys

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

def main():

    oTH = 0.75

    argv = sys.argv
    argc = len(argv)
    
    print('%s creates RGB ply from 3DGS ply with background removed' % argv[0])
    print('[usage] python %s <3DGS ply> <mask>' % argv[0])
    
    if argc < 3:
        quit()
    
    plydata = PlyData.read(argv[1])
    mask = cv2.imread(argv[2], cv2.IMREAD_UNCHANGED)
    Hmask = mask.shape[0]
    Wmask = mask.shape[1]
    
    X = plydata['vertex']['x']
    Y = plydata['vertex']['y']
    Z = plydata['vertex']['z']
    
    intrinsic = plydata['intrinsic']['intrinsic'].reshape(3,3)
    fx = intrinsic[0][0]
    fy = intrinsic[1][1]
    cx = intrinsic[0][2]
    cy = intrinsic[1][2]
    
    image_size = plydata['image_size']['image_size']
    
    if Wmask != image_size[0] or Hmask != image_size[1]:
        mask = cv2.resize(mask, image_size)

    opac = plydata['vertex']['opacity']

    f_dc_0 = plydata['vertex']['f_dc_0']
    f_dc_1 = plydata['vertex']['f_dc_1']
    f_dc_2 = plydata['vertex']['f_dc_2']

    lines = []

    nrPoints = X.shape[0]
    c0 = 1 / (1.77 * 2)

    opac = plydata['vertex']['opacity']

    f_dc_0 = plydata['vertex']['f_dc_0']
    f_dc_1 = plydata['vertex']['f_dc_1']
    f_dc_2 = plydata['vertex']['f_dc_2']

    lines = []

    nrPoints = X.shape[0]
    c0 = 1 / (1.77 * 2)

    for i in range(nrPoints):

        if i % 100000 == 0:
            print('processing %d/%d' % (i, nrPoints))

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
    
        if mask[v][u] == 0:
            continue

        o = 1/(1+np.exp(-opac[i]))
        if o < oTH:
            continue 

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

if __name__ == '__main__':
    main()

