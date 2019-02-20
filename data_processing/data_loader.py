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
        """Returns the path to find a specific image file"""
        return os.path.join(self.__input_directory,"scenario_{}".format(scenario_id),str(index).zfill(4)+".jpg")

    def get_npy_path(self, scenario_id : int, index : int):
        """Returns the path to find a specific npy file"""
        return os.path.join(self.__input_directory,"scenario_{}".format(scenario_id),"npy","Image"+str(index).zfill(4)+".npy")

    def load_pair_images_openCV(self,scenario_id : int, index : int):
        left_img = cv2.imread(self.get_img_path(scenario_id, index-1))
        right_img = cv2.imread(self.get_img_path(scenario_id, index-1))
        npy = np.load(self.get_npy_path(scenario_id,index))
        return [left_img,right_img,npy]

    def crop_unique_npy(self, scenario_id : int, index : int, res : int):
        npy = np.load(self.get_npy_path(scenario_id,index))
        height = np.shape(npy)[1]
        width = np.shape(npy)[0]
        if not os.path.exists(os.path.join(self.__output_directory, "scenario_"+str(scenario_id)+"_"+str(res))):
            os.makedirs(os.path.join(self.__output_directory, "scenario_"+str(scenario_id)+"_"+str(res)))
        for i in range(int(width/res)) :
            for j in range(int(height / res)):
                cropped = npy[res * i:res * (i + 1), res * j: res * (j + 1)]
                np.save(os.path.join(self.__output_directory, "scenario_"+str(scenario_id)+"_"+str(res),
                                     str(index).zfill(4)+"_"+str(i*res)+"_"+str(j*res)), cropped)
            #Saving last cell (shifting it to the top in order not to overpass the limit)
            cropped = npy[res * i:res * (i + 1),height-res:height]
            np.save(os.path.join(self.__output_directory, "scenario_" + str(scenario_id) + "_" + str(res),
                                 str(index).zfill(4) + "_" + str(i * res) + "_" + str(height-res)), cropped)

        # Saving last column (shifting it to the left in order not to overpass the limit)
        for j in range(int(height / res)):
            cropped = npy[width-res:width, res*j:res*(j+1)]
            np.save(os.path.join(self.__output_directory, "scenario_" + str(scenario_id) + "_" + str(res),
                             str(index).zfill(4) + "_" + str(width - res) + "_" + str(j * res)), cropped)
        cropped = npy[width - res:width, height - res:height]
        np.save(os.path.join(self.__output_directory, "scenario_" + str(scenario_id) + "_" + str(res),
                             str(index).zfill(4) + "_" + str(width - res) + "_" + str(height - res)), cropped)


    def crop_scenario_npy(self, scenario_id : int, res : int):
        for i in tqdm(range(500)) :
            #print("Cropping frame {}...".format(i))p
            self.crop_unique_npy(scenario_id, i ,res)


data_loader = DataLoader(os.path.join("..","stereo-tracking"),os.path.join("..","cropped"))
data_loader.crop_scenario_npy(0,64)
data_loader.crop_scenario_npy(0,128)







