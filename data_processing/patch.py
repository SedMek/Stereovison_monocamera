import numpy as np
import cv2
import os
from tqdm import tqdm
import argparse

def files_in_folder(folder):
	output = set()
	file_info = dict()
	for filename in tqdm(os.listdir(folder)):
		if filename.endswith('jpg') or filename.endswith('npy'):
			
			filename_parts = filename.split('_')
			temp = filename_parts[-1].split('.')
			del filename_parts[-1]
			filename_parts.extend(temp)
			filename_parts[0] = filename_parts[0].replace('Image','')
			
			# print(filename_parts)

			if filename_parts[0] in file_info.keys():
				file_info[filename_parts[0]]['y_pos'].add(int(filename_parts[1]))
				file_info[filename_parts[0]]['x_pos'].add(int(filename_parts[2]))
				# file_info[filename_parts[0]]['type'].append(filename_parts[3])
			else:
				file_info[filename_parts[0]] = {'x_pos':set(), 'y_pos':set()}
				file_info[filename_parts[0]]['y_pos'].add(int(filename_parts[1]))
				file_info[filename_parts[0]]['x_pos'].add(int(filename_parts[2]))	
	return file_info

def patch_npy(folder, size):
	
	file_info = files_in_folder(folder)
	for base_name in file_info.keys():
		file_info[base_name]['x_pos'] = list(file_info[base_name]['x_pos'])
		file_info[base_name]['y_pos'] = list(file_info[base_name]['y_pos'])
		
	# Concatenate method:

	# 	# npy patch:
	# 	lines_npy = [np.concatenate([np.load(os.path.join(folder,"Image" + str(base_name) +	'_' + str(file_info[base_name]['x_pos'][i]) + '_' + str(file_info[base_name]['y_pos'][j]) +  ".npy")) for j in range(0,len(file_info[base_name]['y_pos'])) ], axis=1) for i in range(0, len(file_info[base_name]['x_pos']))]
	# 	output_npy = np.concatenate(lines_npy, axis=0)
	# 	np.save('Image'+str(base_name), output_npy)

	# 	# jpg patch:
	# 	lines_jpg = [np.concatenate([cv2.imread(os.path.join(folder, str(base_name) +	'_' + str(file_info[base_name]['x_pos'][i]) + '_' + str(file_info[base_name]['y_pos'][j]) +  ".jpg")) for j in range(0,len(file_info[base_name]['y_pos'])) ], axis=1) for i in range(0, len(file_info[base_name]['x_pos']))]
	# 	output_jpg = np.concatenate(lines_jpg, axis=0)
	# 	cv2.imwrite(str(base_name)+'.jpg', output_jpg)

	# 	print(cv2.imread(os.path.join(folder, str(base_name) + '_' + str(file_info[base_name]['x_pos'][0]) + '_' + str(file_info[base_name]['y_pos'][0]) +  ".jpg")).shape)

	# overwrite method:
		output_npy = np.zeros((972,1296))
		output_jpg = np.zeros((972,1296,3), dtype='uint8')
		print('----------------')
		print('output_npy before', type(output_npy[0,0]))
		print('output_jpg before', type(output_jpg[0,0,0]))


		for i in file_info[base_name]['x_pos']:
			for j in file_info[base_name]['y_pos']:
				output_npy[i:i+size,j:j+size] = np.load(os.path.join(folder,str(base_name) + '_' + str(j) + '_' + str(i) + ".npy"))
				output_jpg[i:i+size,j:j+size] = cv2.imread(os.path.join(folder, str(base_name) + '_' + str(j) + '_' + str(i) + ".jpg"))
					
				print('original_npy', type(np.load(os.path.join(folder,str(base_name) + '_' + str(j) + '_' + str(i) + ".npy"))[0,0]))
		

		np.save('Image'+str(base_name), output_npy)
		cv2.imwrite(str(base_name)+'.jpg', output_jpg)

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-s", "--size", required=True, type=int,help="the size of the square cropped image in pixels")
	args = vars(ap.parse_args())
	

	patch_npy('./temp/', args['size'])