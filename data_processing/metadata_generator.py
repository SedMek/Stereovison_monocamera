import argparse
from tqdm import tqdm
import json
import os

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
                file_info[filename_parts[0]].add((filename_parts[2],filename_parts[1]))
            else:
                file_info[filename_parts[0]] = set()
                file_info[filename_parts[0]].add((filename_parts[2],filename_parts[1]))
    
    for base_name in file_info.keys():
        file_info[base_name]= list(file_info[base_name])
    
    return file_info

def meta_generator(folder):
    file_info = files_in_folder(folder)

    meta_scenes = []
    for base_name in file_info.keys():
        for pos in file_info[base_name]:
            scene_available = True
            for i in range(10):
                try:
                    if pos not in file_info[str(int(base_name)+i).zfill(4)] :
                        scene_available = False
                        break
                    else:
                        file_info[str(int(base_name)+i).zfill(4)].remove(pos) # this is to not include the same picture in another scenario, maybe change it to do data augmentation
                except KeyError:
                    # there are no more images, so we are not able to form a scenario of 10 pictures
                    scene_available = False
                    break
            
            if scene_available:
                scene = {}
                scene["depth"]=[str(int(base_name)+i).zfill(4)+"_"+pos[1]+"_"+pos[0]+".npy" for i in range(10)]
                scene["time_step"]= 0.125 # TODO check if its expressed in seconds (8 Hertz => 0.125 s)
                scene["speed"]= [-0.8, 0, 0] # TODO check if the speed should be expressed in meters and if it is expressed in 3D starting with x.
                scene["length"]=  10
                scene["imgs"]=[str(int(base_name)+i).zfill(4)+"_"+pos[1]+"_"+pos[0]+".jpg" for i in range(10)]
                meta_scenes.append(scene)

    with open('metadata.json', 'w') as outfile:
        json.dump({"scenes":meta_scenes}, outfile)



if __name__ == "__main__":
    meta_generator(os.path.join("..","..","cropped","jpg","scenario_0_64"))

    # OLD CODE, TO DELETE IF NOT NEEDED

    # ap = argparse.ArgumentParser()
    # ap.add_argument("-s", "--size", required=True, type=int,help="the size of the square cropped image in pixels")
    # ap.add_argument("-b", "--begin", required=True, type=int,help="the first image")
    # ap.add_argument("-e", "--end", required=True, type=int,help="the last image")
    # args = vars(ap.parse_args())



    # suffixes = []
    # x = 0
    # while x < 1296-1296%args['size']:
    #     y = 0
    #     while y < 972-972%args['size']:
    #         suffixes.append('_'+str(x)+'_'+str(y))
    #         y = y + args['size']
    #     x = x + args['size']

    # meta_scenes = []
    # for crop_suffix in suffixes:
    #     for scene_number in range(int(args['begin']), int(args['end'])+1):
    #         scene_number_str = str(scene_number).zfill(3)
    #         scene = {}
    #         scene["depth"]=[scene_number_str+str(image_number)+crop_suffix+".npy" for image_number in range(10)]
    #         scene["time_step"]= 0.125 # TODO check if its expressed in seconds (8 Hertz => 0.125 s)
    #         scene["speed"]= [-0.8, 0, 0] # TODO check if the speed should be expressed in meters and if it is expressed in 3D starting with x.
    #         scene["length"]=  10
    #         scene["imgs"]=[scene_number_str+str(image_number)+crop_suffix+".jpg" for image_number in range(10)]
    #         meta_scenes.append(scene)

    # with open('metadata.json', 'w') as outfile:
    #     json.dump({"scenes":meta_scenes}, outfile)