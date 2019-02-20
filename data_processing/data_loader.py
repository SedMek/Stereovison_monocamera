import numpy as np
import cv2
import os
from tqdm import tqdm

class DataLoader :
    """Class for handling data extraction and preprocessing"""

    def __init__(self,input_directory : str, output_directory : str):
        """Specifies the input diectory to find the data and the output directory """
        self.__input_directory = input_directory
        self.__output_directory = output_directory

    def get_img_path(self, scenario_id : int, index : int):
        """Returns the path to find an image file given its scenario_id and its frame index"""
        return os.path.join(self.__input_directory,"scenario_{}".format(scenario_id),str(index).zfill(4)+".jpg")

    def get_npy_path(self, scenario_id : int, index : int):
        """Returns the path to find a npy file given its scenario_id and its frame index"""
        return os.path.join(self.__input_directory,"scenario_{}".format(scenario_id),"npy","Image"+str(index).zfill(4)+".npy")

    def load_pair_images_openCV(self,scenario_id : int, index : int):
        left_img = cv2.imread(self.get_img_path(scenario_id, index-1))
        right_img = cv2.imread(self.get_img_path(scenario_id, index-1))
        npy = np.load(self.get_npy_path(scenario_id,index))
        return [left_img,right_img,npy]

    def crop_unique_npy(self, scenario_id : int, index : int, res : int):
        npy = np.load(self.get_npy_path(scenario_id,index))
        image_width = np.shape(npy)[1]
        image_height = np.shape(npy)[0]
        if not os.path.exists(os.path.join(self.__output_directory, "scenario_"+str(scenario_id)+"_"+str(res))):
            os.makedirs(os.path.join(self.__output_directory, "scenario_"+str(scenario_id)+"_"+str(res)))
        for i in range(int(image_height/res)) :
            for j in range(int(image_width / res)):
                cropped = npy[res * i:res * (i + 1), res * j: res * (j + 1)]
                np.save(os.path.join(self.__output_directory, "scenario_"+str(scenario_id)+"_"+str(res),
                                     str(index).zfill(4)+"_"+str(j*res)+"_"+str(i*res)), cropped)
            #Saving last cell (shifting it to the top in order not to overpass the limit)
            cropped = npy[res * i:res * (i + 1),image_width-res:image_width]
            np.save(os.path.join(self.__output_directory, "scenario_" + str(scenario_id) + "_" + str(res),
                                 str(index).zfill(4) + "_" + str(image_width-res))+ "_"+ str(i * res), cropped)

        # Saving last column (shifting it to the left in order not to overpass the limit)
        for j in range(int(image_width / res)):
            cropped = npy[image_height-res:image_height, res*j:res*(j+1)]
            np.save(os.path.join(self.__output_directory, "scenario_" + str(scenario_id) + "_" + str(res),
                             str(index).zfill(4) + "_" + str(j * res))+ "_" + str(image_height - res), cropped)
        cropped = npy[image_height - res:image_height, image_width - res:image_width]
        np.save(os.path.join(self.__output_directory, "scenario_" + str(scenario_id) + "_" + str(res),
                             str(index).zfill(4) + "_" + str(image_width - res)+ "_" + str(image_height - res)), cropped)


    def crop_scenario_npy(self, scenario_id : int, res : int):
        for i in tqdm(range(500)) :
            self.crop_unique_npy(scenario_id, i ,res)


data_loader = DataLoader(os.path.join("..","stereo-tracking"),os.path.join("..","cropped"))
data_loader.crop_scenario_npy(0,64)
data_loader.crop_scenario_npy(0,128)







