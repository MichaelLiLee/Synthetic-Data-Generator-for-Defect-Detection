"""SceneGenerateRandomizer

"""
import bpy
import random
import glob
import os
from mathutils import Euler
import math

class SceneGenerateRandomizer:
    def __init__(self,
                asset_plane_folder_path = "C:/Users/user/Documents/project/synthDefect/Assets/PlaneModel",
                asset_table_folder_path = "C:/Users/user/Documents/project/synthDefect/Assets/TableModel",
                plane_placement_area = {"x_min":-0.2, "x_max": 0.2, "y_min":-0.2, "y_max":0.2}
                ):

        self.asset_table_folder_path = asset_table_folder_path
        self.asset_plane_folder_path = asset_plane_folder_path
        self.plane_placement_area = plane_placement_area
        self.__table_object_collection = bpy.data.collections["TableCollection"]
        self.__plane_object_collection = bpy.data.collections["PlaneCollection"]
        self.__plane_coordinate = [0,0,0.001]
        self.__plane_pose = [0,0,0]

    def __load_object(self, filepath, collection):
        """ Asset Linking
        """
        ## append object from .blend file
        with bpy.data.libraries.load(filepath, link = False,assets_only = True) as (data_from, data_to):
            data_to.objects = data_from.objects
        ## link object to current scene
        for obj in data_to.objects:
            if obj is not None:
                collection.objects.link(obj)

    def __import_table_and_plane_asset(self):
        """ 
        """ 
        ## get table object asset path
        table_object_path_list = glob.glob(os.path.join(self.asset_table_folder_path, "*.blend"))
        ## link table asset to current scene
        table_asset_path = random.sample(table_object_path_list, 1)[0]
        self.__load_object(filepath = table_asset_path, collection = self.__table_object_collection)

        ## get plane object asset path
        plane_object_path_list = glob.glob(os.path.join(self.asset_plane_folder_path, "*.blend"))
        ## link plane asset to current scene
        plane_asset_path =  random.sample(plane_object_path_list, 1)[0]
        self.__load_object(filepath = plane_asset_path, collection = self.__plane_object_collection)

    def __randomly_place_plane(self):
        """ 
        """
        ## place plane
        self.__plane_coordinate[0] = random.uniform(self.plane_placement_area["x_min"], self.plane_placement_area["x_max"])
        self.__plane_coordinate[1] = random.uniform(self.plane_placement_area["y_min"], self.plane_placement_area["y_max"])
        for plane_obj in self.__plane_object_collection.objects:
                plane_obj.location = self.__plane_coordinate

        ## rotate plane
        self.__plane_pose = [0, 0 , random.random() * 2 * math.pi]
        for plane_obj in self.__plane_object_collection.objects:
                plane_obj.rotation_euler = Euler(self.__plane_pose, 'XYZ')

    def scene_generate(self):
        """ 
        """ 
        self.__import_table_and_plane_asset()
        self.__randomly_place_plane()
        print("Scene Generate COMPLERED !!!")

if __name__ == '__main__':
    randomizer = SceneGenerateRandomizer()
    randomizer.scene_generate()