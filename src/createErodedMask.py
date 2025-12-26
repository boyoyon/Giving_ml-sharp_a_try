import cv2, glob, os, sys
import numpy as np

def main():
    
    KERNEL_SIZE = 5

    argv = sys.argv
    argc = len(argv)

    print('%s creates an eroded mask from the area of the specified images where pixel values are (0,0,0).' % argv[0])
    print('[usage] python %s <wildcard for images> [<erode size(default: %d)>]' % (argv[0], KERNEL_SIZE))
    
    if argc < 2:
        quit()

    if argc > 2:
        KERNEL_SIZE = int(argv[2])

    if KERNEL_SIZE % 2 == 0:
        KERNEL_SIZE += 1

    paths = glob.glob(argv[1])

    for path in paths:

        rgb = cv2.imread(path)
        H, W = rgb.shape[:2]
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

        mask = np.zeros((H,W,1), np.uint8)
        mask[np.where(gray != 0)] = 255

        kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)

        base = os.path.basename(path)
        filename = os.path.splitext(base)[0]
        dst_path = '%s_mask_eroded_by_%d.png' % (filename, KERNEL_SIZE)
        cv2.imwrite(dst_path, mask)
        print('save %s' % dst_path)

if __name__ == '__main__':
    main()
