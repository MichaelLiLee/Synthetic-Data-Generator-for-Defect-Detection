"""SDGParameter 
"""

class SDGParameter:
     def __init__(self):
         self.gen_num = 1000
         self.blender_exe_path = "C:/program Files/Blender Foundation/Blender 3.4/blender"
         self.asset_table_folder_path = "C:/Users/user/Documents/project/synthDefect/Assets/TableModel"
         self.asset_plane_folder_path = "C:/Users/user/Documents/project/synthDefect/Assets/PlaneModel"
         self.mask_imgs_save_paths = {"bottom": "C:/Users/user/Documents/project/synthDefect/Assets/DefectMask/defect_bottom_mask.png",
                                        "top": "C:/Users/user/Documents/project/synthDefect/Assets/DefectMask/defect_top_mask.png",
                                        "mix": "C:/Users/user/Documents/project/synthDefect/Assets/DefectMask/defect_mix_mask.png"}
         self.scratches_global_coords_list_to_json_save_path = "C:/Users/user/Documents/project/synthDefect/SDG/scratches_global_coords_list.json"
         self.defect_masks_img_paths = {"bottom": "C:/Users/user/Documents/project/synthDefect/Assets/DefectMask/defect_bottom_mask.png",
                                       "top": "C:/Users/user/Documents/project/synthDefect/Assets/DefectMask/defect_top_mask.png",
                                       "mix": "C:/Users/user/Documents/project/synthDefect/Assets/DefectMask/defect_mix_mask.png"}
         self.asset_table_texture_folder_path = "C:/Users/user/Documents/project/synthDefect/Assets/TableTexture"
         self.asset_hdri_lighting_folder_path = "C:/Users/user/Documents/project/synthDefect/Assets/HdriLighting"
         self.output_img_path = "C:/Users/user/Documents/project/synthDefect/gen_data/images"
         self.output_label_path = "C:/Users/user/Documents/project/synthDefect/gen_data/labels"
         self.scratches_global_coords_json_file_path = "C:/Users/user/Documents/project/synthDefect/SDG/scratches_global_coords_list.json"
         self.camera_focal_length = 35
         self.camera_sensor_width = 36
         self.img_resolution_x = 3000
         self.img_resolution_y = 3000
         self.cycle_samples = 512
         self.plane_placement_area = {"x_min":-0.2, "x_max": 0.2, "y_min":-0.2, "y_max":0.2}
         self.scratch_mask_width = 15000
         self.scratch_mask_height = 15000
         self.scratch_size_range = {"min": 300, "max": 2000}
         self.scratch_line_vertices_range = {"min": 2, "max": 4}
         self.scratch_smooth_probability = 0.5
         self.scratch_num_range = {"min": 10, "max": 20}
         self.scratch_top_thickness_range = {"min": 5, "max": 10}
         self.scratch_bottom_thickness_range = {"min": 1, "max": 3}
         self.surface_color_noise_texture_scale_range = {"X": {"min": 300,"max": 500}, "Y": {"min": 15,"max": 30}}
         self.surface_color_noise_texture_params = {"Scale": 5, "Detail": 5, "Roughness": 0.6, "Distortion": 3}
         self.surface_color_color_ramp_params = {"Stop0_color": (0.5, 0.478, 0.478, 1) ,"Pos0": {"min": 0,"max": 0.2}, 
                                                 "Stop1_color": (0.956, 0.913, 0.913, 1) ,"Pos1": {"min": 0.8,"max": 1}}
         self.surface_color_value_range = {"min": 0.8, "max": 1.2}
         self.surface_roughness_noise_texture_location_range = {"Z": {"min":0, "max":1}}
         self.surface_roughness_noise_texture_params = {"Scale": 5, "Detail": 5, "Roughness": 0.6, "Distortion": 3}
         self.surface_roughness_color_ramp_params = {"Stop0_color": (0.15, 0.15, 0.15, 1) ,"Pos0": {"min": 0,"max": 0.2}, 
                                                     "Stop1_color": (0.35, 0.35, 0.35, 1) ,"Pos1": {"min": 0.8,"max": 1}}
         self.surface_roughness_add_range = {"min": -0.05, "max": 0.05}
         self.surface_bump_strength_range = {"min": 0.01, "max": 0.03}
         self.defect_color_noise_texture_location_range = {"Z": {"min": 0, "max": 1}}
         self.defect_color_noise_texture_params = {"Scale": {"min": 5, "max": 10}}
         self.defect_color_color_ramp_params = {"Stop0_color": (0.5, 0.478, 0.478, 1) ,"Pos0": {"min": 0,"max": 0.2}, 
                                                "Stop1_color": (0.956, 0.913, 0.913, 1) ,"Pos1": {"min": 0.8,"max": 1}}
         self.defect_color_value_range = {"min": 0.8, "max": 1.2}
         self.defect_roughness_noise_texture_location_range = {"Z": {"min": 2, "max": 3}}
         self.defect_roughness_noise_texture_params = {"Scale": {"min": 5, "max": 10}}
         self.defect_roughness_color_ramp_params = {"Stop0_color": (0.125, 0.125, 0.125, 1) ,"Pos0": {"min": 0,"max": 0.2}, 
                                                   "Stop1_color": (0.225, 0.225, 0.225, 1) ,"Pos1": {"min": 0.8,"max": 1}}
         self.defect_roughness_add_range = {"min": -0.05, "max": 0.05}
         self.defect_bump_bottom_color_ramp_params = {"Stop0_color": (1, 1, 1, 1) ,"Stop1_color": (0, 0, 0, 1)}
         self.defect_bump_top_color_ramp_params = {"Stop0_color": (0.5, 0.5, 0.5, 1) ,"Stop1_color": (1, 1, 1, 1)}
         self.defect_bump_strength_range = {"min": 0.1, "max": 0.2}
         self.texture_scale_range = {"min": 1 , "max": 10}
         self.hdri_lighting_strength_range = {"min": 0.6 , "max": 1.3}
         self.fibonacci_sphere_radius_range = {"min":0.1, "max":0.2}
         self.fibonacci_sphere_sample_area = 0.0001
         self.camera_normal_angle_range = {"min":50, "max": 90}
         self.camera_offset_location_range = {"min": - 0.003 , "max": 0.003}
         self.camera_offset_rotation_range = {"min":-5, "max":5}
         self.chromatic_aberration_probability = 0.25
         self.blur_probability = 0.25
         self.exposure_probability = 0.25
         self.noise_probability = 0.25
         self.white_balance_probability = 0.25
         self.brightness_probability = 0.25
         self.contrast_probability = 0.25
         self.hue_probability = 0.25
         self.saturation_probability = 0.25
         self.chromatic_aberration_value_range = {"min": 0.1, "max": 1}
         self.blur_value_range = {"min": 2, "max": 4}
         self.exposure_value_range = {"min": -0.5, "max": 0.5}
         self.noise_value_range = {"min": 1.6, "max": 1.8}
         self.white_balance_value_range = {"min": 5500, "max": 7500}
         self.brightness_value_range = {"min": -5.0, "max": 5.0}
         self.contrast_value_range = {"min": -5.0, "max": 5.0}
         self.hue_value_range = {"min": 0.48, "max": 0.52}
         self.saturation_value_range = {"min": 0.8, "max": 1.2}
         self.scratch_class_id = 0