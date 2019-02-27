import numpy as np
import cv2
import os
from tqdm import tqdm


class DataLoader :
    """Abstract class for handling data extraction and preprocessing"""

    def __init__(self,input_directory : str, output_directory : str):
        """Specifies the input directory to find the data and the output directory """
        self._input_directory = input_directory
        self._output_directory = output_directory

    def load_im(self, scenario_id : int, index : int):
        raise NotImplementedError

    def load_pair_images_openCV(self,scenario_id : int, index : int):
        left_img = cv2.imread(self.get_img_path(scenario_id, index-1))
        right_img = cv2.imread(self.get_img_path(scenario_id, index-1))
        npy = np.load(self.get_npy_path(scenario_id,index))
        return [left_img,right_img,npy]

    def crop_im(self, image, pos: tuple, res: int):
        """Crops a square of the image given the position of the upper left corner and the resolution"""
        raise NotImplementedError

    def save_cropped(self, scenario_id: int, index: int, cropped_array: np.ndarray, pos: tuple, res: int):
        """Saves the cropped image given the scenario id, the index, the position of the upper left corner and the resolution"""
        raise NotImplementedError

    def crop_unique(self, scenario_id : int, index : int, res : int):
        """Crops a unique frame given its scenario id, its index and the resolution of each cell and saves the cropped images"""

        im = self.load_im(scenario_id,index)
        im_width = np.shape(im)[1]
        im_height = np.shape(im)[0]

        # Creating directory if not existing
        if not os.path.exists(os.path.join(self._output_directory, "scenario_" + str(scenario_id) + "_" + str(res))):
            os.makedirs(os.path.join(self._output_directory, "scenario_" + str(scenario_id) + "_" + str(res)))

        # Cropping and saving all cells
        for i in range(int(im_height/res)) :
            for j in range(int(im_width / res)):
                cropped = self.crop_im(im,(res*i,res*j),res)
                self.save_cropped(scenario_id,index,cropped,(res*i,res*j),res)
            # Saving last cell of the row (shifting it to the left in order not to overpass the limit)
            cropped = self.crop_im(im,(res*i,im_width-res),res)
            self.save_cropped(scenario_id,index,cropped, (res*i,im_width-res), res)

        # Saving last row (shifting it to the top in order not to overpass the limit)
        for j in range(int(im_width / res)):
            cropped = self.crop_im(im, (im_height-res,res*j), res)
            self.save_cropped(scenario_id,index,cropped, (im_height-res,res*j), res)

        # Saving last cell in the bottom right corner (shifting it to the left and the top)
        cropped = self.crop_im(im, (im_height - res, im_width-res), res)
        self.save_cropped(scenario_id,index,cropped, (im_height - res, im_width-res), res)

    def crop_scenario_npy(self, scenario_id : int, res : int):
        """Crops all images from one scenario given a grid size"""
        for i in tqdm(range(500)) :
            self.crop_unique(scenario_id, i ,res)


class DataDepthMapLoader(DataLoader):
    """Class for handling npy data extraction and preprocessing (inherits from DataLoader)"""

    def __init__(self,input_directory: str, output_directory: str):
        DataLoader.__init__(self,input_directory,output_directory)

    def get_path(self, scenario_id : int, index : int):
        """Returns the path to find a npy file given its scenario_id and its frame index"""
        return os.path.join(self._input_directory, "scenario_{}".format(scenario_id), "npy", "Image" + str(index).zfill(4) + ".npy")

    def save_cropped(self, scenario_id: int, index: int, cropped_array: np.ndarray, pos: tuple, res: int):
        np.save(os.path.join(self._output_directory, "scenario_" + str(scenario_id) + "_" + str(res),
                             str(index).zfill(4) + "_" + str(pos[1]) + "_" + str(pos[0])), cropped_array)

    def crop_im(self, image_array: np.ndarray, pos: tuple, res: int):
        """Crops a square of the image given the position of the upper left corner and the resolution"""
        return image_array[pos[0]:pos[0] + res, pos[1]:pos[1] + res]


class DataImageLoader(DataLoader) :
    """Class for handling jpeg data extraction and preprocessing (inherits from DataLoader)"""

    def __init__(self,input_directory: str, output_directory: str):
        DataLoader.__init__(self,input_directory,output_directory)

    def get_path(self, scenario_id : int, index : int):
        """Returns the path to find an image file given its scenario_id and its frame index"""
        return os.path.join(self._input_directory, "scenario_{}".format(scenario_id), str(index).zfill(4) + ".jpg")


data_loader = DataDepthMapLoader(os.path.join("..","..","stereo-tracking"),os.path.join("..","..","cropped"))
data_loader.crop_scenario_npy(0,64)
data_loader.crop_scenario_npy(0,128)







