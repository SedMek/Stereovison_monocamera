import argparse
from tqdm import tqdm
import json


if __name__ == "__main__":

	ap = argparse.ArgumentParser()
	ap.add_argument("-s", "--size", required=True, type=int,help="the size of the square cropped image in pixels")
	args = vars(ap.parse_args())


	suffixes = []
	x = 0
	while x < 1296:
		y = 0
		while y < 972:
			suffixes.append('_'+str(x)+'_'+str(y))
			y = y + args['size']
		x = x + args['size']

	meta_scenes = []
	for crop_suffix in suffixes:
		for scene_number in range(2):
			scene_number_str = str(scene_number)
			if scene_number<10:
				scene_number_str = "0"+scene_number_str
			scene = {}
			scene["depth"]=["00"+scene_number_str+str(image_number)+crop_suffix+".npy" for image_number in range(10)]
			scene["time_step"]= 0.125 # TODO check if its expressed in seconds (8 Hertz => 0.125 s)
			scene["speed"]= [0.8, 0, 0] # TODO check if the speed should be expressed in meters and if it is expressed in 3D starting with x.
			scene["length"]=  10
			scene["imgs"]=["00"+scene_number_str+str(image_number)+crop_suffix+".jpg" for image_number in range(10)]
			meta_scenes.append(scene)

	with open('meta.json', 'w') as outfile:
		json.dump({"scenes":meta_scenes}, outfile)
