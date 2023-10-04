import numpy as np
import cv2
import random
import geojson
# import matplotlib.pyplot as plt
# from matplotlib.collections import LineCollection
from scipy import interpolate
import random
import os
import json

class ScratchRandomizer:
    """
    """

    def __init__(self, 
                 scratch_mask_width = 15000,
                 scratch_mask_height = 15000,
                 scratch_size_range = {"min": 500, "max": 3000},
                 scratch_line_vertices_range = {"min": 2, "max": 5},
                 scratch_smooth_probability = 0.5,
                 scratch_num_range = {"min": 15, "max": 20},
                 scratch_top_thickness_range = {"min": 5, "max": 10},
                 scratch_bottom_thickness_range = {"min": 1, "max": 3},
                 mask_imgs_save_paths = {"bottom": "C:/Users/user/Documents/project/synthDefect/Assets/DefectMask/defect_bottom_mask.png",
                                        "top": "C:/Users/user/Documents/project/synthDefect/Assets/DefectMask/defect_top_mask.png",
                                        "mix": "C:/Users/user/Documents/project/synthDefect/Assets/DefectMask/defect_mix_mask.png"},
                scratches_global_coords_list_to_json_save_path = "C:/Users/user/Documents/project/synthDefect/SDG/scratches_global_coords_list.json"
                 ):
        self.scratch_mask_width = scratch_mask_width
        self.scratch_mask_height = scratch_mask_height
        self.scratch_size_range = scratch_size_range # 0.5 ~ 3 cm
        self.scratch_line_vertices_range = scratch_line_vertices_range
        self.scratch_smooth_probability = scratch_smooth_probability
        self.scratch_num_range = scratch_num_range
        self.__scratch_num = 0
        self.scratch_top_thickness_range = scratch_top_thickness_range
        self.scratch_bottom_thickness_range = scratch_bottom_thickness_range
        self.__scratches_local_coords_list = list() # [[(L1_p1_x, L1_p1_y), (L1_p2_x, L1_p2_y), ...],[(L2_p1_x, L2_p1_y), (L2_p2_x, L2_p2_y), ...] ...] (float, float)
        self.__scratches_global_location_list = list() # [[L1_x, L1_y], [L2_x, L2_y], ...]
        self.__scratches_global_coords_list = list() # [[[L1_p1_x, L1_p1_y], [L1_p2_x, L1_p2_y], ...],[L2_p1_x, L2_p1_y), [L2_p2_x, L2_p2_y], ...] ...] [float, float]
        self.__defect_top_mask = None
        self.__defect_bottom_mask = None
        self.__defect_shaders_mix_mask = None
        self.__mask_blur_value = 5
        self.mask_imgs_save_paths = mask_imgs_save_paths
        self.scratches_global_coords_list_to_json_save_path = scratches_global_coords_list_to_json_save_path


    def __b_spline_smooth(self, points):
        """
        """
        x=[]
        y=[]
        for point in points:
            x.append(point[0])
            y.append(point[1])

        tck, *rest = interpolate.splprep([x,y],k=2)
        u = np.linspace(0, 1, num=1000)
        smooth = interpolate.splev(u, tck)

        return smooth


    def __generate_one_scratch(self):
        """ 
        """
        # Generate random number of scratch line vertices
        number_vertices = int(random.uniform(self.scratch_line_vertices_range["min"], self.scratch_line_vertices_range["max"]))

        # Generate random number of scratch size    
        scratch_size_x = int(random.uniform(self.scratch_size_range["min"], self.scratch_size_range["max"]))
        scratch_size_y = int(random.uniform(self.scratch_size_range["min"], self.scratch_size_range["max"]))

        # Generate random scratch line
        random_scratch_line = list()
        random_linestring = geojson.utils.generate_random("LineString", numberVertices = number_vertices, boundingBox=[0, 0, scratch_size_x, scratch_size_y])["coordinates"]
        for point in random_linestring:
            random_scratch_line_point = [point[0], scratch_size_y - point[1]]
            random_scratch_line.append(random_scratch_line_point)

        # Scratch line smoothing
        scratch_line_smooth_enable = random.choices([True, False], weights= [self.scratch_smooth_probability, 1 - self.scratch_smooth_probability])[0]

        if scratch_line_smooth_enable and len(random_scratch_line)>2:
            random_scratch_line = self.__b_spline_smooth(random_scratch_line)
            random_scratch_line = list(zip(random_scratch_line[0], random_scratch_line[1]))
            
        return random_scratch_line

    def __generate_random_scratches(self):
        """ 
        """ 
        # Get scratch number need to generate
        self.__scratch_num = int(random.uniform(self.scratch_num_range["min"], self.scratch_num_range["max"]))

        for i in range(self.__scratch_num): 
            random_scratch_line = self.__generate_one_scratch()
            self.__scratches_local_coords_list.append(random_scratch_line)


    def __generate_random_scratches_location(self):
        """ 
        """ 
        for i in range(self.__scratch_num):
            random_scratches_location = [random.randint(0, self.scratch_mask_width), random.randint(0, self.scratch_mask_height)]
            self.__scratches_global_location_list.append(random_scratches_location)


    def __transform_local_coords_to_global(self):
        """ 
        """
        for i in range(self.__scratch_num):

            scratche_local_coords = self.__scratches_local_coords_list[i]
            scratche_global_location = self.__scratches_global_location_list[i]
            scratche_global_coords = list()

            for point in scratche_local_coords:
                transform_point = [point[0] + scratche_global_location[0], point[1] + scratche_global_location[1]]
                scratche_global_coords.append(transform_point)

            if max([transform_point[0] for transform_point in scratche_global_coords]) <= self.scratch_mask_width and \
               max([transform_point[1] for transform_point in scratche_global_coords]) <= self.scratch_mask_height:
                self.__scratches_global_coords_list.append(scratche_global_coords)


    def __generate_scratches_top_and_bottom_mask(self):
        """ 
        """ 
        W = self.scratch_mask_width
        H = self.scratch_mask_height
        defect_top_mask_img = np.zeros((H, W), np.uint8)
        defect_bottom_mask_img = np.zeros((H, W), np.uint8)

        for scratch in self.__scratches_global_coords_list:
            # Convert string List to integer List
            scratch_int = list()
            for point in scratch:
                point_int = [int(point[0]), int(point[1])] # x, y
                scratch_int.append(point_int)
            # Random scratch thickness
            scratch_top_thickness = int(random.uniform(self.scratch_top_thickness_range["min"], self.scratch_top_thickness_range["max"]))
            scratch_bottom_thickness = int(random.uniform(self.scratch_bottom_thickness_range["min"], self.scratch_bottom_thickness_range["max"]))
            # Draw scratch line
            # https://stackoverflow.com/questions/50671524/how-to-draw-lines-between-points-in-opencv
            for point1, point2 in zip(scratch_int, scratch_int[1:]): 
                cv2.line(defect_top_mask_img, point1, point2, [255, 255, 255], scratch_top_thickness)

            for point1, point2 in zip(scratch_int, scratch_int[1:]): 
                cv2.line(defect_bottom_mask_img, point1, point2, [255, 255, 255], scratch_bottom_thickness)            
        
        return defect_top_mask_img, defect_bottom_mask_img

    def __generate_scratches_shaders_mix_mask(self, defect_top_mask_img):
        """ 
        """
        blur_size = self.__mask_blur_value
        scratches_shaders_mix_mask = cv2.GaussianBlur(defect_top_mask_img, (blur_size, blur_size), 0)
        
        return scratches_shaders_mix_mask

      
    def test(self):
        """ 
        """ 
        self.__generate_random_scratches()
        print("self.scratches_local_coords_list")
        print(self.__scratches_local_coords_list)

        self.__generate_random_scratches_location()
        print("self.scratches_global_location_list")
        print(self.__scratches_global_location_list)

        self.__transform_local_coords_to_global()
        print("self.scratches_global_coords_list")
        print(self.__scratches_global_coords_list)

        self.__defect_top_mask, self.__defect_bottom_mask = self.__generate_scratches_top_and_bottom_mask()
        self.__defect_shaders_mix_mask = self.__generate_scratches_shaders_mix_mask(self.__defect_top_mask)

        self.__save_mask_imgs()

        #self.__plot_mask_imgs()

        print("Scratch Randomize COMPLERED !!!")

    def __save_mask_imgs(self):
        """ 
        """
        # Remove exist imgs
        for img_path in self.mask_imgs_save_paths.values():
            if os.path.isfile(img_path):
                os.remove(img_path)

        cv2.imwrite(self.mask_imgs_save_paths["top"], self.__defect_top_mask)
        cv2.imwrite(self.mask_imgs_save_paths["bottom"], self.__defect_bottom_mask)
        cv2.imwrite(self.mask_imgs_save_paths["mix"], self.__defect_shaders_mix_mask)


    def __plot_mask_imgs(self):
        """ 
        """
        # fig = plt.figure(figsize=(15, 5))
        # fig.add_subplot(1, 3, 1).set_title("top_mask")
        # plt.imshow(self.__defect_top_mask,cmap='gray')
        # fig.add_subplot(1, 3, 2).set_title("bottom_mask")
        # plt.imshow(self.__defect_bottom_mask,cmap='gray')
        # fig.add_subplot(1, 3, 3).set_title("mix_mask")
        # plt.imshow(self.__defect_shaders_mix_mask,cmap='gray')
        # plt.show()

    def __save_scratches_global_coords_to_json(self):
        """ 
        """
        with open(self.scratches_global_coords_list_to_json_save_path, 'w') as json_file:
            json.dump(self.__scratches_global_coords_list, json_file)


    def scratch_randomize(self):
        """ 
        """ 
        self.__generate_random_scratches()
        self.__generate_random_scratches_location()
        self.__transform_local_coords_to_global()
        self.__defect_top_mask, self.__defect_bottom_mask = self.__generate_scratches_top_and_bottom_mask()
        self.__defect_shaders_mix_mask = self.__generate_scratches_shaders_mix_mask(self.__defect_top_mask)
        self.__save_mask_imgs()
        self.__save_scratches_global_coords_to_json()
        #self.__plot_mask_imgs()

        print("Scratch Randomize COMPLERED !!!")

if __name__ == '__main__':
    randomizer = ScratchRandomizer()
    randomizer.scratch_randomize()       