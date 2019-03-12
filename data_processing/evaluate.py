import numpy as np
import cv2

if __name__ == '__main__':
	npy_new = np.load('Image0000.npy')
	npy_original = np.load('Image0000_original.npy')
	npy_clipped = np.clip(npy_original,a_min = 0, a_max = npy_original[0,0])
	jpg = cv2.imread('0000.jpg')
	jpg_original = cv2.imread('0000.jpg')

	print(npy_original == npy_new)
	print('---------------------------------')
	print(jpg_original == jpg)