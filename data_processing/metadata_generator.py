import argparse
from tqdm import tqdm
import json
import os

def files_in_folder(folder):
    output = set()
    file_info = dict()
    # Filename has this format "sc1_0023_64_128.jpg or .npy"
    for filename in tqdm(os.listdir(folder)):
        if filename.endswith('jpg') and filename.replace('jpg','npy') in os.listdir(folder): # Checks that both jpg and npy are available
            
            filename_parts = filename.split('_')
            temp = filename_parts[-1].split('.')
            del filename_parts[-1]

            filename_parts.extend(temp)
            filename_parts[1] = filename_parts[1].replace('Image','') # removes "Image" from the beginning of the name if it exists
            # filename_parts example: ["sc1","0023","64","128"]

            sc_img = filename_parts[0]+"_"+filename_parts[1] # example "sc1_0023"

            if sc_img in file_info.keys():
                file_info[sc_img].add((filename_parts[3],filename_parts[2]))
            else:
                file_info[sc_img] = set()
                file_info[sc_img].add((filename_parts[3],filename_parts[2]))
    
    for sc_img in file_info.keys():
        file_info[sc_img]= list(file_info[sc_img])
    
    return file_info

def meta_generator(folder):
    file_info = files_in_folder(folder)

    meta_scenes = []
    for sc_img in file_info.keys():
        
        scenario_name, base_name = sc_img.split('_') # example "sc1_0023" --> "sc1" and "0023"
        
        for pos in file_info[sc_img]:
            scene_available = True
            for i in range(10):
                try:
                    if pos not in file_info[scenario_name + "_" + str(int(base_name)+i).zfill(4)] :
                        scene_available = False
                        break
                    else:
                        file_info[scenario_name+ "_" + str(int(base_name)+i).zfill(4)].remove(pos) # this is to not include the same picture in another scenario, maybe change it to do data augmentation
                except KeyError:
                    # there are no more images, so we are not able to form a scenario of 10 pictures
                    scene_available = False
                    break
            
            if scene_available:
                scene = {}
                scene["depth"]=[scenario_name + "_" + str(int(base_name)+i).zfill(4)+"_"+pos[1]+"_"+pos[0]+".npy" for i in range(10)]
                scene["time_step"]= 0.125 # TODO check if its expressed in seconds (8 Hertz => 0.125 s)
                scene["speed"]= [-0.8*50, 0, 0] # *50 to scale to 0 à 100 m # TODO check if the speed should be expressed in meters and if it is expressed in 3D starting with x.
                scene["length"]=  10
                scene["imgs"]=[scenario_name + "_" + str(int(base_name)+i).zfill(4)+"_"+pos[1]+"_"+pos[0]+".jpg" for i in range(10)]
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