""" YOLOLabeler

Reference:
[1]https://blender.stackexchange.com/questions/153929/get-pixel-coord-in-rendered-image-of-pixel-coord-in-texture
[2]https://docs.blender.org/api/current/bpy_extras.object_utils.html#bpy_extras.object_utils.world_to_camera_view
[3]https://blender.stackexchange.com/questions/129473/typeerror-element-wise-multiplication-not-supported-between-matrix-and-vect


""" 

import bpy
import datetime
import os
import bpy_extras
from mathutils import Vector
import json


class YOLOLabeler:
    """ 
    """
    def __init__(self, 
                output_img_path = "C:/Users/user/Documents/project/synthDefect/gen_data/images",
                output_label_path = "C:/Users/user/Documents/project/synthDefect/gen_data/labels",
                texture_width = 15000,
                texture_height = 15000,
                scratches_global_coords_json_file_path = "C:/Users/user/Documents/project/synthDefect/SDG/scratches_global_coords_list.json",
                scratch_class_id = 0
                ): 
        """ 
        """
        self.output_img_path = output_img_path
        self.output_label_path = output_label_path
        self.__gen_img_id = None
        self.__render_machine_id = "a"
        self.texture_width = texture_width
        self.texture_height = texture_height
        self.scratches_global_coords_json_file_path = scratches_global_coords_json_file_path
        self.__scratches_texture_coords_list = list()
        self.__scratches_image_coords_list = list()
        self.__scratches_bbox_list = list()
        self.scratch_class_id = scratch_class_id

    def __create_gen_img_id(self):
        """Create a unique ID for generated synthetic image data."""
        now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
        time_id = now.strftime("%Y%m%d%H%M%S").zfill(15)
        render_machine_id = self.__render_machine_id
        self.__gen_img_id = render_machine_id + time_id

        return id


    def __get_scratches_texture_coords_list(self):
        """
        """
        # Get scratches texture coords from json file
        json_file = open(self.scratches_global_coords_json_file_path)
        self.__scratches_texture_coords_list = json.load(json_file)
        json_file.close()
        
    
    def __texture_coords_to_image_coords(self, point):
        """ 
        """
        x = point[0]
        y = self.texture_height - point[1]

        tex_w = self.texture_width
        tex_h = self.texture_height

        scene = bpy.data.scenes['Scene']
        camera =  bpy.data.objects['Camera']

        res_x =scene.render.resolution_x * scene.render.resolution_percentage / 100
        res_y = scene.render.resolution_y * scene.render.resolution_percentage / 100

        p = Vector((x * 2 / tex_w - 1.0, y * 2 / tex_h - 1.0, 0))

        scene.view_layers.update()
        p_camera = bpy_extras.object_utils.world_to_camera_view(scene, camera, bpy.data.objects["Plane"].matrix_world @ p) # [3] * -> @

        p_camera.x *= res_x
        p_camera.y = res_y - p_camera.y * res_y

        image_coord = [p_camera[0], p_camera[1]]

        return image_coord

    def __get_scratches_image_coords_list(self):
        """ 
        """
        for scratch in self.__scratches_texture_coords_list:
            scratch_image_coords = list()
            for point in scratch:
                image_coord = self.__texture_coords_to_image_coords(point)
                scratch_image_coords.append(image_coord)
            self.__scratches_image_coords_list.append(scratch_image_coords)

    def __get_scratches_bbox(self):
        """ 
        """
        # Get render image width & height
        scene = bpy.data.scenes['Scene']
        render_img_w = int(scene.render.resolution_x * scene.render.resolution_percentage / 100)
        render_img_h= int(scene.render.resolution_y * scene.render.resolution_percentage / 100)

        # Get scratch bbox top left and bottom right point
        for scratch in self.__scratches_image_coords_list:
            top_left = [min([point[0] for point in scratch]), min([point[1] for point in scratch])]
            bottom_right = [max([point[0] for point in scratch]), max([point[1] for point in scratch])]

            # Check bbox in camera view 
            if ((top_left[0] >= 0) and (top_left[1] >= 0) and (top_left[0] <= render_img_w) and (top_left[1] <= render_img_h)) or \
                ((bottom_right[0] >= 0) and (bottom_right[1] >= 0) and (bottom_right[0] <= render_img_w) and (bottom_right[1] <= render_img_h)):

                if top_left[0] > render_img_w:
                    top_left[0] = render_img_w

                if top_left[0] < 0 :
                    top_left[0] = 0

                if top_left[1] > render_img_h:
                    top_left[1] = render_img_h

                if top_left[1] < 0 :
                    top_left[1] = 0

                if bottom_right[0] > render_img_w:
                    bottom_right[0] = render_img_w

                if bottom_right[0] < 0 :
                    bottom_right[0] = 0

                if bottom_right[1] > render_img_h:
                    bottom_right[1] = render_img_h

                if bottom_right[1] < 0 :
                    bottom_right[1] = 0

                self.__scratches_bbox_list.append([[int(top_left[0]), int(top_left[1])], [int(bottom_right[0]), int(bottom_right[1])]])
            

    def __format_coordinates(self, coordinates, obj_class_id):
        """ 
        """
        # If the current object is in view of the camera
        if coordinates: 
            # Get the rendered image size
            render = bpy.data.scenes['Scene'].render
            fac = render.resolution_percentage * 0.01
            dw = 1./(render.resolution_x * fac)
            dh = 1./(render.resolution_y * fac)
            x = (coordinates[0][0] + coordinates[1][0])/2.0
            y = (coordinates[0][1] + coordinates[1][1])/2.0
            w = coordinates[1][0] - coordinates[0][0]
            h = coordinates[1][1] - coordinates[0][1]
            cx = x*dw
            cy = y*dh
            width = w*dw
            height = h*dh

        # Formulate line corresponding to the bounding box of one class
            txt_coordinates = str(obj_class_id) + ' ' + str(cx) + ' ' + str(cy) + ' ' + str(width) + ' ' + str(height) + '\n'

            return txt_coordinates
            # If the current object isn't in view of the camera, then pass
        else:
            pass


    def __get_all_coordinates(self):
        """ 
        """ 
        # Initialize the variable where we'll store the coordinates
        main_text_coordinates = ''
         # Loop through all of the scratches bbox
        for bbox in self.__scratches_bbox_list:
            text_coordinates = self.__format_coordinates(bbox, self.scratch_class_id)

            if text_coordinates:
                main_text_coordinates = main_text_coordinates + text_coordinates

        return main_text_coordinates # Return all coordinates

    def test(self):
        """ 
        """
        self.__get_scratches_texture_coords_list()
        #print(self.__scratches_texture_coords_list)
        self.__get_scratches_image_coords_list()
        #print(self.__scratches_image_coords_list)
        self.__get_scratches_bbox()
        print(self.__scratches_bbox_list)
        print(self.__get_all_coordinates())

    def render_img_and_save_label(self):
        """ 
        """ 
        #　Render and save png img
        self.__create_gen_img_id()
        img_file_path = os.path.join(self.output_img_path,  str(self.__gen_img_id)+".png")
        bpy.data.scenes["Scene"].render.filepath = img_file_path 
        print("Start Rendering Image")         
        bpy.ops.render.render(write_still=True, scene='Scene')
        print("End Rendering Image")

        # Get scratch bbox data, then save labels
        self.__get_scratches_texture_coords_list()
        self.__get_scratches_image_coords_list()
        self.__get_scratches_bbox()
        text_coordinates = self.__get_all_coordinates()
        splitted_coordinates = text_coordinates.split('\n')[:-1] # Delete last '\n' in coordinates
        text_file_path = os.path.join(self.output_label_path, str(self.__gen_img_id)+".txt")
        text_file = open(text_file_path, 'w+') # Open .txt file of the label
        text_file.write('\n'.join(splitted_coordinates))
        text_file.close()

        print("YOLO-coordinates:\n{}".format(splitted_coordinates))
        print("SAVE IMG AT {}".format(img_file_path))
        print("SAVE LABLE AT {}".format(text_file_path))
        print("Auto Labeling COMPLERED !!!")


if __name__ == '__main__':
    yolo_labeler = YOLOLabeler()
    yolo_labeler.render_img_and_save_label()  