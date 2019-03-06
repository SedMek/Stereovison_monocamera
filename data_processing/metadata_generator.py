import argparse
from tqdm import tqdm
import json


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--size", required=True, type=int,help="the size of the square cropped image in pixels")
    ap.add_argument("-b", "--begin", required=True, type=int,help="the first image")
	ap.add_argument("-e", "--end", required=True, type=int,help="the last image")
   	args = vars(ap.parse_args())



    suffixes = []
    x = 0
    while x < 1296-1296%args['size']:
        y = 0
        while y < 972-972%args['size']:
            suffixes.append('_'+str(x)+'_'+str(y))
            y = y + args['size']
        x = x + args['size']

    meta_scenes = []
    for crop_suffix in suffixes:
        for scene_number in range(int(args['begin']), int(args['end'])+1):
            scene_number_str = str(scene_number).zfill(3)
            scene = {}
            scene["depth"]=[scene_number_str+str(image_number)+crop_suffix+".npy" for image_number in range(10)]
            scene["time_step"]= 0.125 # TODO check if its expressed in seconds (8 Hertz => 0.125 s)
            scene["speed"]= [-0.8, 0, 0] # TODO check if the speed should be expressed in meters and if it is expressed in 3D starting with x.
            scene["length"]=  10
            scene["imgs"]=[scene_number_str+str(image_number)+crop_suffix+".jpg" for image_number in range(10)]
            meta_scenes.append(scene)

    with open('metadata.json', 'w') as outfile:
        json.dump({"scenes":meta_scenes}, outfile)