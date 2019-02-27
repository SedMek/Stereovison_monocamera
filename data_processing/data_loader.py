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

    def crop_im(self, image, pos: tuple, res: int):
        """Crops a square of the image given the position of the upper left corner and the resolution"""
        raise NotImplementedError

    def save_cropped(self, scenario_id: int, index: int, cropped_array: np.ndarray, pos: tuple, res: int, boxes_list: list):
        """Saves the cropped image given the scenario id, the index, the position of the upper left corner and the resolution"""
        raise NotImplementedError

    def parse_identif(self,line: str) -> list:
        """Returns a list of boxes corresponding to the line of the identif.txt file"""
        boxes_list = line.split("colis.")
        boxes_list = boxes_list[1:]
        if len(boxes_list)>=1 :
            for i in range(len(boxes_list)) :
                boxes_list[i] = boxes_list[i][boxes_list[i].find("[")+1:boxes_list[i].find("]")].split(",")
                boxes_list[i] = [int(txt) for txt in boxes_list[i]]
        return boxes_list

    def check_identif(self,boxes_list: list, pos: tuple, res: int) -> bool :
        """Checks if the box given with pos and res intersect with one of the boxes in boxes_list"""
        for box in boxes_list :
            if pos[0]<=box[2] and pos[1]<=box[3] and pos[0]+res >= box[0] and pos[1]+res >= box[1] :
                return True
        return False


    def crop_unique(self, scenario_id : int, index : int, res : int):
        """Crops a unique frame given its scenario id, its index and the resolution of each cell and saves the cropped images"""

        with open(os.path.join(self._input_directory,"scenario_{}".format(scenario_id),"identif.txt"),mode="r") as identif_file:
            identif = identif_file.readlines()
        boxes_list = self.parse_identif(identif[index])

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
                self.save_cropped(scenario_id,index,cropped,(res*i,res*j),res, boxes_list)
            # Saving last cell of the row (shifting it to the left in order not to overpass the limit)
            cropped = self.crop_im(im,(res*i,im_width-res),res)
            self.save_cropped(scenario_id,index,cropped, (res*i,im_width-res), res, boxes_list)

        # Saving last row (shifting it to the top in order not to overpass the limit)
        for j in range(int(im_width / res)):
            cropped = self.crop_im(im, (im_height-res,res*j), res)
            self.save_cropped(scenario_id,index,cropped, (im_height-res,res*j), res, boxes_list)

        # Saving last cell in the bottom right corner (shifting it to the left and the top)
        cropped = self.crop_im(im, (im_height - res, im_width-res), res)
        self.save_cropped(scenario_id,index,cropped, (im_height - res, im_width-res), res, boxes_list)

    def crop_scenario_npy(self, scenario_id : int, res : int, nb_frames: int):
        """Crops all images from one scenario given a grid size"""
        for i in tqdm(range(nb_frames)) :
            self.crop_unique(scenario_id, i ,res)


class DataDepthMapLoader(DataLoader):
    """Class for handling npy data extraction and preprocessing (inherits from DataLoader)"""

    def __init__(self,input_directory: str, output_directory: str):
        DataLoader.__init__(self,input_directory,output_directory)

    def load_im(self, scenario_id : int, index : int):
        """Loads npy file given its scenario_id and its frame index"""
        npy = np.load(os.path.join(self._input_directory,
                                    "scenario_{}".format(scenario_id),
                                    "npy", "Image" + str(index).zfill(4) + ".npy"))
        return np.clip(npy,a_min = 0, a_max = npy[0,0])

    def save_cropped(self, scenario_id: int, index: int, cropped_array: np.ndarray, pos: tuple, res: int, boxes_list: list):
        if self.check_identif(boxes_list, pos, res) :
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

    def load_im(self, scenario_id : int, index : int):
        """Loads npy file given its scenario_id and its frame index"""
        return cv2.imread(os.path.join(self._input_directory,
                                       "scenario_{}".format(scenario_id),
                                       str(index).zfill(4) + ".jpg"))

    def save_cropped(self, scenario_id: int, index: int, cropped_array: np.ndarray, pos: tuple, res: int, boxes_list: list):
        if self.check_identif(boxes_list, pos, res) :
            cv2.imwrite(os.path.join(self._output_directory, "scenario_" + str(scenario_id) + "_" + str(res),
                                 str(index).zfill(4) + "_" + str(pos[1]) + "_" + str(pos[0])+".jpg"), cropped_array)

    def crop_im(self, image_array: np.ndarray, pos: tuple, res: int):
        """Crops a square of the image given the position of the upper left corner and the resolution"""
        return image_array[pos[0]:pos[0] + res, pos[1]:pos[1] + res,:]



data_loader_npy = DataDepthMapLoader(os.path.join("..","..","stereo-tracking"),os.path.join("..","..","cropped","npy"))
data_loader_jpg = DataImageLoader(os.path.join("..","..","stereo-tracking"),os.path.join("..","..","cropped","jpg"))
# data_loader_jpg.crop_scenario_npy(0,64,22)
data_loader_jpg.crop_scenario_npy(0,128,50)







