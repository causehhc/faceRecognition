import numpy as np

if __name__ == '__main__':
    A = np.arange(15).reshape((3, 5))
    print(A)
    B = np.delete(A, 1)  # 先把A给ravel成一维数组，再删除第1个元素。
    C = np.delete(A, 1, axis=0)  # axis=0代表按行操作
    D = np.delete(A, 1, axis=1)  # axis=1代表按列操作
    print(A)  # 并没有改变，delete不会操作原数组。
    print(B)  # 先把A给ravel成一维数组，再删除第1个元素。
    print(C)  # axis=0代表按行操作
    print(D)  # axis=1代表按列操作
