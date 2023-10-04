# Add SDG related python files path to system path
import sys
import os
module_path = os.path.dirname(os.path.abspath(__file__))
sys_path_list = []
for p in sys.path:
    sys_path_list.append(p)
if module_path not in sys_path_list:
    sys.path.append(module_path)

# Prevent to create __pycache__ file[1]
sys.dont_write_bytecode = True

import bpy

from SDG_000_Initializer import Initializer
from SDG_010_SceneGenerateRandomizer import SceneGenerateRandomizer
from SDG_020_ScratchRandomizer import ScratchRandomizer
from SDG_030_PlaneTextureRandomizer import PlaneTextureRandomizer
from SDG_040_TableTextureRandomizer import TableTextureRandomizer
from SDG_050_LightRandomizer import LightRandomizer
from SDG_060_CameraPoseRandomizer import CameraPoseRandomizer
from SDG_070_CameraEffectRandomizer import CameraEffectRandomizer
from SDG_100_YOLOLabeler import YOLOLabeler
from SDG_200_SDGParameter import SDGParameter


class DataGenerator:
    """ 
    """

    def gen_one_data(self):
        """
        main data generate flow
        """ 

         ## blender env init
        initializer = Initializer()
        parameter = SDGParameter()
        initializer.camera_focal_length = parameter.camera_focal_length
        initializer.camera_sensor_width = parameter.camera_sensor_width
        initializer.img_resolution_x = parameter.img_resolution_x
        initializer.img_resolution_y = parameter.img_resolution_y
        initializer.cycle_samples = parameter.cycle_samples
        initializer.init()

        ## scene generate
        scene_generate_randomizer = SceneGenerateRandomizer()
        scene_generate_randomizer.asset_plane_folder_path = parameter.asset_plane_folder_path # passing params
        scene_generate_randomizer.asset_table_folder_path = parameter.asset_table_folder_path
        scene_generate_randomizer.plane_placement_area = parameter.plane_placement_area
        scene_generate_randomizer.scene_generate()

        # scratch mask randomize
        scratch_randomizer = ScratchRandomizer()
        scratch_randomizer.scratch_mask_width = parameter.scratch_mask_width
        scratch_randomizer.scratch_mask_height = parameter.scratch_mask_height
        scratch_randomizer.scratch_size_range = parameter.scratch_size_range
        scratch_randomizer.scratch_line_vertices_range = parameter.scratch_line_vertices_range
        scratch_randomizer.scratch_smooth_probability = parameter.scratch_smooth_probability
        scratch_randomizer.scratch_num_range = parameter.scratch_num_range
        scratch_randomizer.scratch_top_thickness_range = parameter.scratch_top_thickness_range
        scratch_randomizer.scratch_bottom_thickness_range = parameter.scratch_bottom_thickness_range
        scratch_randomizer.mask_imgs_save_paths = parameter.mask_imgs_save_paths
        scratch_randomizer.scratches_global_coords_list_to_json_save_path = parameter.scratches_global_coords_list_to_json_save_path

        scratch_randomizer.scratch_randomize()

        # texture randomize
        plane_texture_randomizer = PlaneTextureRandomizer()
        table_texture_randomizer = TableTextureRandomizer()

        plane_texture_randomizer.surface_color_noise_texture_scale_range = parameter.surface_color_noise_texture_scale_range
        plane_texture_randomizer.surface_color_noise_texture_params = parameter.surface_color_noise_texture_params
        plane_texture_randomizer.surface_color_color_ramp_params = parameter.surface_color_color_ramp_params
        plane_texture_randomizer.surface_color_value_range = parameter.surface_color_value_range

        plane_texture_randomizer.surface_roughness_noise_texture_location_range = parameter.surface_roughness_noise_texture_location_range
        plane_texture_randomizer.surface_roughness_noise_texture_params = parameter.surface_roughness_noise_texture_params
        plane_texture_randomizer.surface_roughness_color_ramp_params = parameter.surface_roughness_color_ramp_params
        plane_texture_randomizer.surface_roughness_add_range = parameter.surface_roughness_add_range

        plane_texture_randomizer.surface_bump_strength_range = parameter.surface_bump_strength_range

        plane_texture_randomizer.defect_color_noise_texture_location_range = parameter.defect_color_noise_texture_location_range
        plane_texture_randomizer.defect_color_noise_texture_params = parameter.defect_color_noise_texture_params
        plane_texture_randomizer.defect_color_color_ramp_params = parameter.defect_color_color_ramp_params
        plane_texture_randomizer.defect_color_value_range = parameter.defect_color_value_range

        plane_texture_randomizer.defect_roughness_noise_texture_location_range = parameter.defect_roughness_noise_texture_location_range
        plane_texture_randomizer.defect_roughness_noise_texture_params = parameter.defect_roughness_noise_texture_params
        plane_texture_randomizer.defect_roughness_color_ramp_params = parameter.defect_roughness_color_ramp_params
        plane_texture_randomizer.defect_roughness_add_range = parameter.defect_roughness_add_range

        plane_texture_randomizer.defect_bump_bottom_color_ramp_params = parameter.defect_bump_bottom_color_ramp_params
        plane_texture_randomizer.defect_bump_top_color_ramp_params = parameter.defect_bump_top_color_ramp_params
        plane_texture_randomizer.defect_bump_strength_range = parameter.defect_bump_strength_range
        plane_texture_randomizer.defect_masks_img_paths = parameter.defect_masks_img_paths

        table_texture_randomizer.asset_table_texture_folder_path = parameter.asset_table_texture_folder_path
        table_texture_randomizer.texture_scale_range = parameter.texture_scale_range

        plane_texture_randomizer.plane_texture_randomize()
        table_texture_randomizer.table_texture_randomize()

        ## light randomize
        light_randomizer = LightRandomizer()
        light_randomizer.asset_hdri_lighting_folder_path = parameter.asset_hdri_lighting_folder_path # passing params
        light_randomizer.hdri_lighting_strength_range = parameter.hdri_lighting_strength_range
        light_randomizer.light_randomize()

        ## camera pose randomize
        camera_pose_randomizer = CameraPoseRandomizer()
        camera_pose_randomizer.fibonacci_sphere_radius_range = parameter.fibonacci_sphere_radius_range # passing params
        camera_pose_randomizer.fibonacci_sphere_sample_area = parameter.fibonacci_sphere_sample_area
        camera_pose_randomizer.camera_normal_angle_range = parameter.camera_normal_angle_range
        camera_pose_randomizer.camera_offset_location_range = parameter.camera_offset_location_range
        camera_pose_randomizer.camera_offset_rotation_range = parameter.camera_offset_rotation_range
        camera_pose_randomizer.camera_pose_randomize()

        ## camera effect randomize
        camera_effect_randomizer = CameraEffectRandomizer()
        camera_effect_randomizer.camera_focal_length = parameter.camera_focal_length # passing params
        camera_effect_randomizer.img_resolution_x = parameter.img_resolution_x
        camera_effect_randomizer.img_resolution_y = parameter.img_resolution_y
        camera_effect_randomizer.max_samples = parameter.cycle_samples
        camera_effect_randomizer.chromatic_aberration_probability = parameter.chromatic_aberration_probability
        camera_effect_randomizer.chromatic_aberration_value_range = parameter.chromatic_aberration_value_range
        camera_effect_randomizer.blur_probability = parameter.blur_probability
        camera_effect_randomizer.blur_value_range = parameter.blur_value_range
        camera_effect_randomizer.exposure_probability = parameter.exposure_probability
        camera_effect_randomizer.exposure_value_range = parameter.exposure_value_range
        camera_effect_randomizer.noise_probability = parameter.noise_probability
        camera_effect_randomizer.noise_value_range = parameter.noise_value_range
        camera_effect_randomizer.white_balance_probability = parameter.white_balance_probability
        camera_effect_randomizer.white_balance_value_range = parameter.white_balance_value_range
        camera_effect_randomizer.brightness_probability = parameter.brightness_probability
        camera_effect_randomizer.brightness_value_range = parameter.brightness_value_range
        camera_effect_randomizer.contrast_probability = parameter.contrast_probability
        camera_effect_randomizer.contrast_value_range = parameter.contrast_value_range
        camera_effect_randomizer.hue_probability = parameter.hue_probability
        camera_effect_randomizer.hue_value_range = parameter.hue_value_range
        camera_effect_randomizer.saturation_probability = parameter.saturation_probability
        camera_effect_randomizer.saturation_value_range = parameter.saturation_value_range

        ## Update blender env view layer 
        bpy.data.scenes["Scene"].view_layers.update()

        ## rendering & labeling image
        yolo_labeler = YOLOLabeler()
        yolo_labeler.output_img_path = parameter.output_img_path
        yolo_labeler.output_label_path = parameter.output_label_path
        yolo_labeler.texture_width = parameter.scratch_mask_width
        yolo_labeler.texture_height = parameter.scratch_mask_height
        yolo_labeler.scratches_global_coords_json_file_path = parameter.scratches_global_coords_json_file_path
        yolo_labeler.scratch_class_id = parameter.scratch_class_id
        yolo_labeler.render_img_and_save_label()

        print("Components Initialize Completed!!!")

        sys.exit()


if __name__ == '__main__':
    datagen = DataGenerator()
    datagen.gen_one_data()