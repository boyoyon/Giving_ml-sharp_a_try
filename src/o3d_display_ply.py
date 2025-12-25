import cv2, os, sys
import numpy as np
import open3d as o3d

delta = np.pi / 180
delta2 = 0.005

pcd = None

def key_callback_1(vis, action, mods):

    shift_pressed = (mods & 0x1) != 0

    #if action == 1: # on pressing

    if shift_pressed:
        angle = -delta
    else:
        angle = delta

    rotation = np.array([[np.cos(angle), 0, np.sin(angle), 0],
        [0, 1, 0, 0],
        [-np.sin(angle), 0, np.cos(angle), 0],
        [0, 0, 0, 1]])

    transform = rotation #@ transform
    pcd.transform(transform)

    return True

def key_callback_2(vis, action, mods):

    shift_pressed = (mods & 0x1) != 0

    #if action == 1: # on pressing

    if shift_pressed:
        angle = -delta
    else:
        angle = delta

    rotation = np.array([[1, 0, 0, 0],
        [0, np.cos(angle), -np.sin(angle), 0],
        [0, np.sin(angle), np.cos(angle), 0],
        [0, 0, 0, 1]])

    transform = rotation #@ transform
    pcd.transform(transform)

    return True

def key_callback_3(vis, action, mods):

    shift_pressed = (mods & 0x1) != 0

    #if action == 1: # on pressing

    if shift_pressed:
        angle = -delta
    else:
        angle = delta

    rotation = np.array([[np.cos(angle), -np.sin(angle), 0, 0],
        [np.sin(angle), np.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    transform = rotation #@ transform
    pcd.transform(transform)

    return True

def key_callback_4(vis, action, mods):

    shift_pressed = (mods & 0x1) != 0

    #if action == 1: # on pressing

    if shift_pressed:
        offset = -delta2
    else:
        offset = delta2

    translate = np.array([[1, 0, 0, offset],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    transform = translate
    pcd.transform(transform)

    return True

def key_callback_5(vis, action, mods):

    shift_pressed = (mods & 0x1) != 0

    #if action == 1: # on pressing

    if shift_pressed:
        offset = -delta2
    else:
        offset = delta2

    translate = np.array([[1, 0, 0, 0],
        [0, 1, 0, offset],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])

    transform = translate
    pcd.transform(transform)

    return True

def key_callback_6(vis, action, mods):

    shift_pressed = (mods & 0x1) != 0

    #if action == 1: # on pressing

    if shift_pressed:
        offset = -delta2
    else:
        offset = delta2

    translate = np.array([[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, offset],
        [0, 0, 0, 1]])

    transform = translate
    pcd.transform(transform)

    return True

def main():

    global pcd

    argv = sys.argv
    argc = len(argv)

    print('%s loads ply and visualizes 3d model' % argv[0])
    print('[usage] python %s <ply file> [<zscale>]' % argv[0])

    if argc < 2:
        quit()

    pcd = o3d.io.read_point_cloud(argv[1])

    if argc > 2:
        zscale = float(argv[2])

        # 点の座標をNumPy配列として取得
        # pointsは (N, 3) の配列。列は [x, y, z]
        points = np.asarray(pcd.points)

        # Z座標（インデックス2）をスケーリング
        points[:, 2] *= zscale

        # 加工した配列を点群オブジェクトに戻す
        pcd.points = o3d.utility.Vector3dVector(points)

    center = pcd.get_center()
    pcd.translate(-center)

    # 可視化の設定
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.register_key_action_callback(ord("1"), key_callback_1)
    vis.register_key_action_callback(ord("2"), key_callback_2)
    vis.register_key_action_callback(ord("3"), key_callback_3)
    vis.register_key_action_callback(ord("4"), key_callback_4)
    vis.register_key_action_callback(ord("5"), key_callback_5)
    vis.register_key_action_callback(ord("6"), key_callback_6)

    # 実行
    vis.run()
    vis.destroy_window()

    if argc > 2:
        o3d.io.write_point_cloud('displayed.ply', pcd)
        print('save displayed.ply')

if __name__ == '__main__':
    main()
