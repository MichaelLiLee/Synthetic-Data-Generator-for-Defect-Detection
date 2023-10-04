""" PlaneTextureRandomizer

Reference:
[1]https://blender.stackexchange.com/questions/189712/how-to-add-a-new-stop-to-the-color-ramp

""" 

import bpy
import random

class PlaneTextureRandomizer:
    def __init__(self, 
                surface_color_noise_texture_scale_range = {"X": {"min": 300,"max": 500}, "Y": {"min": 15,"max": 30}},
                surface_color_noise_texture_params = {"Scale": 5, "Detail": 5, "Roughness": 0.6, "Distortion": 3},
                surface_color_color_ramp_params = {"Stop0_color": (0.5, 0.478, 0.478, 1) ,"Pos0": {"min": 0,"max": 0.2}, 
                                                   "Stop1_color": (0.956, 0.913, 0.913, 1) ,"Pos1": {"min": 0.8,"max": 1}},
                surface_color_value_range = {"min": 0.8, "max": 1.2},
                surface_roughness_noise_texture_location_range = {"Z": {"min":0, "max":1}},
                surface_roughness_noise_texture_params = {"Scale": 5, "Detail": 5, "Roughness": 0.6, "Distortion": 3},
                surface_roughness_color_ramp_params = {"Stop0_color": (0.15, 0.15, 0.15, 1) ,"Pos0": {"min": 0,"max": 0.2}, 
                                                      "Stop1_color": (0.35, 0.35, 0.35, 1) ,"Pos1": {"min": 0.8,"max": 1}},
                surface_roughness_add_range = {"min": -0.05, "max": 0.05},
                surface_bump_strength_range = {"min": 0.01, "max": 0.03},
                defect_color_noise_texture_location_range = {"Z": {"min": 0, "max": 1}},
                defect_color_noise_texture_params = {"Scale": {"min": 5, "max": 10}},
                defect_color_color_ramp_params = {"Stop0_color": (0.5, 0.478, 0.478, 1) ,"Pos0": {"min": 0,"max": 0.2}, 
                                               "Stop1_color": (0.956, 0.913, 0.913, 1) ,"Pos1": {"min": 0.8,"max": 1}},
                defect_color_value_range = {"min": 0.8, "max": 1.2},
                defect_roughness_noise_texture_location_range = {"Z": {"min": 2, "max": 3}},
                defect_roughness_noise_texture_params = {"Scale": {"min": 5, "max": 10}},
                defect_roughness_color_ramp_params = {"Stop0_color": (0.125, 0.125, 0.125, 1) ,"Pos0": {"min": 0,"max": 0.2}, 
                                                   "Stop1_color": (0.225, 0.225, 0.225, 1) ,"Pos1": {"min": 0.8,"max": 1}},
                defect_roughness_add_range = {"min": -0.05, "max": 0.05},
                defect_bump_bottom_color_ramp_params = {"Stop0_color": (1, 1, 1, 1) ,"Stop1_color": (0, 0, 0, 1)},
                defect_bump_top_color_ramp_params = {"Stop0_color": (0.5, 0.5, 0.5, 1) ,"Stop1_color": (1, 1, 1, 1)},
                defect_bump_strength_range = {"min": 0.1, "max": 0.2},
                defect_masks_img_paths = {"bottom": "C:/Users/user/Documents/project/synthDefect/Assets/DefectMask/defect_bottom_mask.png",
                                       "top": "C:/Users/user/Documents/project/synthDefect/Assets/DefectMask/defect_top_mask.png",
                                       "mix": "C:/Users/user/Documents/project/synthDefect/Assets/DefectMask/defect_mix_mask.png"}
                ):

        self.__collections_need_assign_material = [bpy.data.collections["PlaneCollection"]]
        self.__object_need_assign_material = None
        self.__nodes = None
        self.__links = None
        self.surface_color_noise_texture_scale_range = surface_color_noise_texture_scale_range
        self.surface_color_noise_texture_params = surface_color_noise_texture_params
        self.surface_color_color_ramp_params = surface_color_color_ramp_params 
        self.surface_color_value_range = surface_color_value_range
        self.surface_roughness_noise_texture_location_range = surface_roughness_noise_texture_location_range
        self.surface_roughness_noise_texture_params = surface_roughness_noise_texture_params
        self.surface_roughness_color_ramp_params = surface_roughness_color_ramp_params
        self.surface_roughness_add_range = surface_roughness_add_range
        self.surface_bump_strength_range = surface_bump_strength_range
        self.defect_color_noise_texture_location_range = defect_color_noise_texture_location_range
        self.defect_color_noise_texture_params = defect_color_noise_texture_params
        self.defect_color_color_ramp_params = defect_color_color_ramp_params
        self.defect_color_value_range = defect_color_value_range
        self.defect_roughness_noise_texture_location_range = defect_roughness_noise_texture_location_range
        self.defect_roughness_noise_texture_params = defect_roughness_noise_texture_params
        self.defect_roughness_color_ramp_params = defect_roughness_color_ramp_params
        self.defect_roughness_add_range = defect_roughness_add_range
        self.defect_bump_bottom_color_ramp_params = defect_bump_bottom_color_ramp_params
        self.defect_bump_top_color_ramp_params = defect_bump_top_color_ramp_params
        self.defect_bump_strength_range = defect_bump_strength_range
        self.defect_masks_img_paths = defect_masks_img_paths


    def __get_plane_need_assign_material(self):
        """ 
        """
        for collection in self.__collections_need_assign_material:
            for obj in collection.objects:
                self.__object_need_assign_material = obj


    def __create_new_aluminum_material(self):
        """ 
        """
        # Create a new material name "Aluminium"
        Aluminium_mat_exist = False

        for mat in bpy.data.materials:
            if mat.name == "Aluminium":
                Aluminium_mat_exist = True
        
        if Aluminium_mat_exist == False:   
            new_mat_name = "Aluminium"
            bpy.data.materials.new(name=new_mat_name)

        # Use "Aluminium" nodes
        bpy.data.materials["Aluminium"].use_nodes = True

        # "Aluminium" nodes & links references
        self.__nodes = bpy.data.materials["Aluminium"].node_tree.nodes
        self.__links = bpy.data.materials["Aluminium"].node_tree.links

        # Clear all nodes
        self.__nodes.clear()

        # Assign "Aluminium" material to object
        obj = self.__object_need_assign_material
        mat = bpy.data.materials["Aluminium"]

        if obj.data.materials: 
            obj.data.materials[0] = mat # assign to 1st material slot
        else:
            obj.data.materials.append(mat) # no slots


    def __create_aluminum_surface_material_nodes(self):
        """ 
        """ 
        nodes = self.__nodes
        links = self.__links

        # Add new nodes
        # surface base color
        node_TextureCoordinate_Surface = nodes.new("ShaderNodeTexCoord")
        node_TextureCoordinate_Surface.name = "TextureCoordinate_Surface"

        node_Mapping_Surface_BaseColor = nodes.new("ShaderNodeMapping")
        node_Mapping_Surface_BaseColor.name = "Mapping_Surface_BaseColor"

        node_NoiseTexture_Surface_BaseColor = nodes.new("ShaderNodeTexNoise")
        node_NoiseTexture_Surface_BaseColor.name = "NoiseTexture_Surface_BaseColor"

        node_ColorRamp_Surface_BaseColor = nodes.new("ShaderNodeValToRGB")
        node_ColorRamp_Surface_BaseColor.name = "ColorRamp_Surface_BaseColor"

        node_HueSaturationValue_Surface_BaseColor = nodes.new("ShaderNodeHueSaturation")
        node_HueSaturationValue_Surface_BaseColor.name = "HueSaturationValue_Surface_BaseColor"

        # surface roughness
        node_Mapping_Surface_Roughness = nodes.new("ShaderNodeMapping")
        node_Mapping_Surface_Roughness.name = "Mapping_Surface_Roughness"

        node_NoiseTexture_Surface_Roughness = nodes.new("ShaderNodeTexNoise")
        node_NoiseTexture_Surface_Roughness.name = "NoiseTexture_Surface_Roughness"

        node_ColorRamp_Surface_Roughness = nodes.new("ShaderNodeValToRGB")
        node_ColorRamp_Surface_Roughness.name = "ColorRamp_Surface_Roughness"

        node_Add_Surface_Roughness = nodes.new("ShaderNodeMath")
        node_Add_Surface_Roughness.name = "Add_Surface_Roughness"

        # surface bump
        node_Bump_Surface_Bump = nodes.new("ShaderNodeBump")
        node_Bump_Surface_Bump.name = "Bump_Surface_Bump"

        # surface bsdf
        node_BSDF_Surface = nodes.new("ShaderNodeBsdfPrincipled")
        node_BSDF_Surface.name = "BSDF_Surface"

        # Locate nodes
        node_TextureCoordinate_Surface.location = (0, 0)
        node_Mapping_Surface_BaseColor.location = (300, 0)
        node_NoiseTexture_Surface_BaseColor.location = (600, 0)
        node_ColorRamp_Surface_BaseColor.location = (900, 0)
        node_HueSaturationValue_Surface_BaseColor.location = (1400, 0)
        node_Mapping_Surface_Roughness.location = (500, -500)
        node_NoiseTexture_Surface_Roughness.location = (700, -500)
        node_ColorRamp_Surface_Roughness.location = (900, -500)
        node_Add_Surface_Roughness.location = (1200, -500)
        node_Bump_Surface_Bump.location = (1500, -500)
        node_BSDF_Surface.location = (1800, 0)

        # Link nodes 
        links.new(node_TextureCoordinate_Surface.outputs["UV"], node_Mapping_Surface_BaseColor.inputs["Vector"])
        links.new(node_Mapping_Surface_BaseColor.outputs["Vector"], node_NoiseTexture_Surface_BaseColor.inputs["Vector"])
        links.new(node_NoiseTexture_Surface_BaseColor.outputs["Fac"], node_ColorRamp_Surface_BaseColor.inputs["Fac"])
        links.new(node_ColorRamp_Surface_BaseColor.outputs["Color"], node_HueSaturationValue_Surface_BaseColor.inputs["Color"])
        links.new(node_HueSaturationValue_Surface_BaseColor.outputs["Color"], node_BSDF_Surface.inputs["Base Color"])

        links.new(node_Mapping_Surface_BaseColor.outputs["Vector"], node_Mapping_Surface_Roughness.inputs["Vector"])
        links.new(node_Mapping_Surface_Roughness.outputs["Vector"], node_NoiseTexture_Surface_Roughness.inputs["Vector"])
        links.new(node_NoiseTexture_Surface_Roughness.outputs["Fac"], node_ColorRamp_Surface_Roughness.inputs["Fac"])
        links.new(node_ColorRamp_Surface_Roughness.outputs["Color"], node_Add_Surface_Roughness.inputs["Value"])
        links.new(node_Add_Surface_Roughness.outputs["Value"], node_BSDF_Surface.inputs["Roughness"])
        links.new(node_Add_Surface_Roughness.outputs["Value"], node_Bump_Surface_Bump.inputs["Height"])
        links.new(node_Bump_Surface_Bump.outputs["Normal"], node_BSDF_Surface.inputs["Normal"])


    def __create_aluminum_defect_material_nodes(self):
        """ 
        """ 
        nodes = self.__nodes
        links = self.__links

        # Add new nodes
        # defect base color
        node_TextureCoordinate_Defect = nodes.new("ShaderNodeTexCoord")
        node_TextureCoordinate_Defect.name = "TextureCoordinate_Defect"

        node_Mapping_Defect_BaseColor = nodes.new("ShaderNodeMapping")
        node_Mapping_Defect_BaseColor.name = "Mapping_Defect_BaseColor"

        node_NoiseTexture_Defect_BaseColor = nodes.new("ShaderNodeTexNoise")
        node_NoiseTexture_Defect_BaseColor.name = "NoiseTexture_Defect_BaseColor"

        node_ColorRamp_Defect_BaseColor = nodes.new("ShaderNodeValToRGB")
        node_ColorRamp_Defect_BaseColor.name = "ColorRamp_Defect_BaseColor"

        node_HueSaturationValue_Defect_BaseColor = nodes.new("ShaderNodeHueSaturation")
        node_HueSaturationValue_Defect_BaseColor.name = "HueSaturationValue_Defect_BaseColor"

        # defect roughness
        node_Mapping_Defect_Roughness = nodes.new("ShaderNodeMapping")
        node_Mapping_Defect_Roughness.name = "Mapping_Defect_Roughness"

        node_NoiseTexture_Defect_Roughness = nodes.new("ShaderNodeTexNoise")
        node_NoiseTexture_Defect_Roughness.name = "NoiseTexture_Defect_Roughness"

        node_ColorRamp_Defect_Roughness = nodes.new("ShaderNodeValToRGB")
        node_ColorRamp_Defect_Roughness.name = "ColorRamp_Defect_Roughness"

        node_Add_Defect_Roughness = nodes.new("ShaderNodeMath")
        node_Add_Defect_Roughness.name = "Add_Defect_Roughness"

        # defect bump
        node_Mapping_Defect_Bump = nodes.new("ShaderNodeMapping")
        node_Mapping_Defect_Bump.name = "Mapping_Defect_Bump"

        node_ImageTexture_Defect_Bump_Bottom = nodes.new("ShaderNodeTexImage")
        node_ImageTexture_Defect_Bump_Bottom.name = "ImageTexture_Defect_Bump_Bottom"

        node_ImageTexture_Defect_Bump_Top = nodes.new("ShaderNodeTexImage")
        node_ImageTexture_Defect_Bump_Top.name = "ImageTexture_Defect_Bump_Top"

        node_ColorRamp_Defect_Bump_Bottom = nodes.new("ShaderNodeValToRGB")
        node_ColorRamp_Defect_Bump_Bottom.name = "ColorRamp_Defect_Bump_Bottom"

        node_ColorRamp_Defect_Bump_Top = nodes.new("ShaderNodeValToRGB")
        node_ColorRamp_Defect_Bump_Top.name = "ColorRamp_Defect_Bump_Top"

        node_Multiply_Defect_Bump = nodes.new("ShaderNodeMath")
        node_Multiply_Defect_Bump.name = "Multiply_Defect_Bump"
        node_Multiply_Defect_Bump.operation = "MULTIPLY"

        node_Bump_Defect_Bump = nodes.new("ShaderNodeBump")
        node_Bump_Defect_Bump.name = "Bump_Defect_Bump"

        # defect bsdf
        node_BSDF_Defect = nodes.new("ShaderNodeBsdfPrincipled")
        node_BSDF_Defect.name = "BSDF_Defect"

        # Locate nodes
        node_TextureCoordinate_Defect.location = (0, -1200)
        node_Mapping_Defect_BaseColor.location = (300, -1200)
        node_NoiseTexture_Defect_BaseColor.location = (600, -1200)
        node_ColorRamp_Defect_BaseColor.location = (900, -1200)
        node_HueSaturationValue_Defect_BaseColor.location = (1200, -1200)

        node_Mapping_Defect_Roughness.location = (300, -1700)
        node_NoiseTexture_Defect_Roughness.location = (600, -1700)
        node_ColorRamp_Defect_Roughness.location = (900, -1700)
        node_Add_Defect_Roughness.location = (1200, -1700)

        node_Mapping_Defect_Bump.location = (300, -2200)
        node_ImageTexture_Defect_Bump_Bottom.location = (600, -2200)
        node_ImageTexture_Defect_Bump_Top.location = (600, -2700)
        node_ColorRamp_Defect_Bump_Bottom.location = (900, -2200)
        node_ColorRamp_Defect_Bump_Top.location = (900, -2700)
        node_Multiply_Defect_Bump.location = (1200, -2200)
        node_Bump_Defect_Bump.location = (1500, -2200)
        node_BSDF_Defect.location = (1800, -1200)

        # Link nodes
        links.new(node_TextureCoordinate_Defect.outputs["UV"], node_Mapping_Defect_BaseColor.inputs["Vector"])
        links.new(node_Mapping_Defect_BaseColor.outputs["Vector"], node_NoiseTexture_Defect_BaseColor.inputs["Vector"])
        links.new(node_NoiseTexture_Defect_BaseColor.outputs["Fac"], node_ColorRamp_Defect_BaseColor.inputs["Fac"])
        links.new(node_ColorRamp_Defect_BaseColor.outputs["Color"], node_HueSaturationValue_Defect_BaseColor.inputs["Color"])
        links.new(node_HueSaturationValue_Defect_BaseColor.outputs["Color"], node_BSDF_Defect.inputs["Base Color"])

        links.new(node_TextureCoordinate_Defect.outputs["UV"], node_Mapping_Defect_Roughness.inputs["Vector"])
        links.new(node_Mapping_Defect_Roughness.outputs["Vector"], node_NoiseTexture_Defect_Roughness.inputs["Vector"])
        links.new(node_NoiseTexture_Defect_Roughness.outputs["Fac"], node_ColorRamp_Defect_Roughness.inputs["Fac"])
        links.new(node_ColorRamp_Defect_Roughness.outputs["Color"], node_Add_Defect_Roughness.inputs[0])
        links.new(node_Add_Defect_Roughness.outputs[0], node_BSDF_Defect.inputs["Roughness"])

        links.new(node_TextureCoordinate_Defect.outputs["UV"],  node_Mapping_Defect_Bump.inputs["Vector"])
        links.new(node_Mapping_Defect_Bump.outputs["Vector"], node_ImageTexture_Defect_Bump_Bottom.inputs["Vector"])
        links.new(node_Mapping_Defect_Bump.outputs["Vector"], node_ImageTexture_Defect_Bump_Top.inputs["Vector"])
        links.new(node_ImageTexture_Defect_Bump_Bottom.outputs["Color"], node_ColorRamp_Defect_Bump_Bottom.inputs["Fac"])
        links.new(node_ImageTexture_Defect_Bump_Top.outputs["Color"], node_ColorRamp_Defect_Bump_Top.inputs["Fac"])
        links.new(node_ColorRamp_Defect_Bump_Bottom.outputs["Color"], node_Multiply_Defect_Bump.inputs[0])
        links.new(node_ColorRamp_Defect_Bump_Top.outputs["Color"], node_Multiply_Defect_Bump.inputs[1])
        links.new(node_Multiply_Defect_Bump.outputs[0], node_Bump_Defect_Bump.inputs["Height"])
        links.new(node_Bump_Defect_Bump.outputs["Normal"], node_BSDF_Defect.inputs["Normal"])

    def __create_aluminum_material_mix_nodes(self):
        """ 
        """
        nodes = self.__nodes
        links = self.__links

        # Add new nodes
        node_TextureCoordinate_Mix = nodes.new("ShaderNodeTexCoord")
        node_TextureCoordinate_Mix.name = "TextureCoordinate_Mix"

        node_Mapping_Mix = nodes.new("ShaderNodeMapping")
        node_Mapping_Mix.name = "Mapping_Mix"

        node_ImageTexture_Mix = nodes.new("ShaderNodeTexImage")
        node_ImageTexture_Mix.name = "ImageTexture_Mix"

        node_MixShader = nodes.new("ShaderNodeMixShader")
        node_MixShader.name = "MixShader"

        node_MaterialOutput = nodes.new("ShaderNodeOutputMaterial")
        node_MaterialOutput.name = "MaterialOutput"


        # Locate nodes
        node_TextureCoordinate_Mix.location = (1200, 500)
        node_Mapping_Mix.location = (1500, 500)
        node_ImageTexture_Mix.location = (1800, 500)
        node_MixShader.location = (2200, 0)
        node_MaterialOutput.location = (2500, 0)

        # Link nodes
        links.new(node_TextureCoordinate_Mix.outputs["UV"], node_Mapping_Mix.inputs["Vector"])
        links.new(node_Mapping_Mix.outputs["Vector"], node_ImageTexture_Mix.inputs["Vector"])
        links.new(node_ImageTexture_Mix.outputs["Color"], node_MixShader.inputs["Fac"])

        # reference BSDF_Surface & BSDF_Defect node
        node_BSDF_Surface = self.__nodes["BSDF_Surface"]
        node_BSDF_Defect = self.__nodes["BSDF_Defect"]

        links.new(node_BSDF_Surface.outputs["BSDF"], node_MixShader.inputs[1])
        links.new(node_BSDF_Defect.outputs["BSDF"], node_MixShader.inputs[2])
        links.new(node_MixShader.outputs["Shader"], node_MaterialOutput.inputs["Surface"])

    def __randomly_set_material_parameters(self):
        """ 
        """
        # References nodes - surface color
        node_Mapping_Surface_BaseColor =  self.__nodes["Mapping_Surface_BaseColor"]
        node_NoiseTexture_Surface_BaseColor = self.__nodes["NoiseTexture_Surface_BaseColor"]
        node_ColorRamp_Surface_BaseColor = self.__nodes["ColorRamp_Surface_BaseColor"]
        node_HueSaturationValue_Surface_BaseColor = self.__nodes["HueSaturationValue_Surface_BaseColor"]
        # References nodes - surface roughness
        node_Mapping_Surface_Roughness = self.__nodes["Mapping_Surface_Roughness"]
        node_NoiseTexture_Surface_Roughness = self.__nodes["NoiseTexture_Surface_Roughness"]
        node_ColorRamp_Surface_Roughness = self.__nodes["ColorRamp_Surface_Roughness"]
        node_Add_Surface_Roughness = self.__nodes["Add_Surface_Roughness"]
        # References nodes - surface bunp 
        node_Bump_Surface_Bump = self.__nodes["Bump_Surface_Bump"]
        # References nodes - defect color
        node_Mapping_Defect_BaseColor = self.__nodes["Mapping_Defect_BaseColor"]
        node_NoiseTexture_Defect_BaseColor = self.__nodes["NoiseTexture_Defect_BaseColor"]
        node_ColorRamp_Defect_BaseColor = self.__nodes["ColorRamp_Defect_BaseColor"]
        node_HueSaturationValue_Defect_BaseColor = self.__nodes["HueSaturationValue_Defect_BaseColor"]
        # References nodes - defect roughness
        node_Mapping_Defect_Roughness = self.__nodes["Mapping_Defect_Roughness"]
        node_NoiseTexture_Defect_Roughness = self.__nodes["NoiseTexture_Defect_Roughness"]
        node_ColorRamp_Defect_Roughness = self.__nodes["ColorRamp_Defect_Roughness"]
        node_Add_Defect_Roughness = self.__nodes["Add_Defect_Roughness"]
        # References nodes - defect bump
        node_ImageTexture_Defect_Bump_Bottom = self.__nodes["ImageTexture_Defect_Bump_Bottom"]
        node_ImageTexture_Defect_Bump_Top = self.__nodes["ImageTexture_Defect_Bump_Top"]
        node_ColorRamp_Defect_Bump_Bottom = self.__nodes["ColorRamp_Defect_Bump_Bottom"]
        node_ColorRamp_Defect_Bump_Top = self.__nodes["ColorRamp_Defect_Bump_Top"]
        node_Bump_Defect_Bump = self.__nodes["Bump_Defect_Bump"]
        # References nodes - bsdf
        node_BSDF_Surface = self.__nodes["BSDF_Surface"]
        node_BSDF_Defect = self.__nodes["BSDF_Defect"]
        node_ImageTexture_Mix = self.__nodes["ImageTexture_Mix"]

        # Set params - surface color
        node_Mapping_Surface_BaseColor.inputs["Scale"].default_value[0] = \
        round(random.uniform(self.surface_color_noise_texture_scale_range["X"]["min"], self.surface_color_noise_texture_scale_range["X"]["max"]), 4)

        node_Mapping_Surface_BaseColor.inputs["Scale"].default_value[1] = \
        round(random.uniform(self.surface_color_noise_texture_scale_range["Y"]["min"], self.surface_color_noise_texture_scale_range["Y"]["max"]), 4)

        node_NoiseTexture_Surface_BaseColor.inputs["Scale"].default_value = self.surface_color_noise_texture_params["Scale"]
        node_NoiseTexture_Surface_BaseColor.inputs["Detail"].default_value = self.surface_color_noise_texture_params["Detail"]
        node_NoiseTexture_Surface_BaseColor.inputs["Roughness"].default_value = self.surface_color_noise_texture_params["Roughness"]
        node_NoiseTexture_Surface_BaseColor.inputs["Distortion"].default_value = self.surface_color_noise_texture_params["Distortion"]

        node_ColorRamp_Surface_BaseColor.color_ramp.elements[0].color = self.surface_color_color_ramp_params["Stop0_color"] # [1]
        node_ColorRamp_Surface_BaseColor.color_ramp.elements[0].position = \
        round(random.uniform(self.surface_color_color_ramp_params["Pos0"]["min"], self.surface_color_color_ramp_params["Pos0"]["max"]), 4)
        node_ColorRamp_Surface_BaseColor.color_ramp.elements[1].color = self.surface_color_color_ramp_params["Stop1_color"]
        node_ColorRamp_Surface_BaseColor.color_ramp.elements[1].position = \
        round(random.uniform(self.surface_color_color_ramp_params["Pos1"]["min"], self.surface_color_color_ramp_params["Pos1"]["max"]), 4)

        node_HueSaturationValue_Surface_BaseColor.inputs["Value"].default_value = \
        round(random.uniform(self.surface_color_value_range["min"], self.surface_color_value_range["max"]), 4)

        # Set params - surface roughness
        node_Mapping_Surface_Roughness.inputs["Scale"].default_value[2] = \
        round(random.uniform(self.surface_roughness_noise_texture_location_range["Z"]["min"], self.surface_roughness_noise_texture_location_range["Z"]["max"]), 4)
        
        node_NoiseTexture_Surface_Roughness.inputs["Scale"].default_value = self.surface_roughness_noise_texture_params["Scale"]
        node_NoiseTexture_Surface_Roughness.inputs["Detail"].default_value = self.surface_roughness_noise_texture_params["Detail"]
        node_NoiseTexture_Surface_Roughness.inputs["Roughness"].default_value = self.surface_roughness_noise_texture_params["Roughness"]
        node_NoiseTexture_Surface_Roughness.inputs["Distortion"].default_value = self.surface_roughness_noise_texture_params["Distortion"]

        node_ColorRamp_Surface_Roughness.color_ramp.elements[0].color = self.surface_roughness_color_ramp_params["Stop0_color"]
        node_ColorRamp_Surface_Roughness.color_ramp.elements[0].position = \
        round(random.uniform(self.surface_roughness_color_ramp_params["Pos0"]["min"], self.surface_roughness_color_ramp_params["Pos0"]["max"]), 4)
        node_ColorRamp_Surface_Roughness.color_ramp.elements[1].color = self.surface_roughness_color_ramp_params["Stop1_color"]
        node_ColorRamp_Surface_Roughness.color_ramp.elements[1].position = \
        round(random.uniform(self.surface_roughness_color_ramp_params["Pos1"]["min"], self.surface_roughness_color_ramp_params["Pos1"]["max"]), 4)

        node_Add_Surface_Roughness.inputs[1].default_value = \
        round(random.uniform(self.surface_roughness_add_range["min"], self.surface_roughness_add_range["max"]), 4)

        # Set params - surface bump
        node_Bump_Surface_Bump.inputs["Strength"].default_value = \
        round(random.uniform(self.surface_bump_strength_range["min"], self.surface_bump_strength_range["max"]), 4)

        # Set params - defect color
        node_Mapping_Defect_BaseColor.inputs["Scale"].default_value[2] = \
        round(random.uniform(self.defect_color_noise_texture_location_range["Z"]["min"], self.defect_color_noise_texture_location_range["Z"]["max"]), 4)
        
        node_NoiseTexture_Defect_BaseColor.inputs["Scale"].default_value = \
        round(random.uniform(self.defect_color_noise_texture_params["Scale"]["min"], self.defect_color_noise_texture_params["Scale"]["max"]), 4)

        node_ColorRamp_Defect_BaseColor.color_ramp.elements[0].color = self.defect_color_color_ramp_params["Stop0_color"]
        node_ColorRamp_Defect_BaseColor.color_ramp.elements[0].position = \
        round(random.uniform(self.defect_color_color_ramp_params["Pos0"]["min"], self.defect_color_color_ramp_params["Pos0"]["max"]), 4)
        node_ColorRamp_Defect_BaseColor.color_ramp.elements[1].color = self.defect_color_color_ramp_params["Stop1_color"]
        node_ColorRamp_Defect_BaseColor.color_ramp.elements[1].position = \
        round(random.uniform(self.defect_color_color_ramp_params["Pos1"]["min"], self.defect_color_color_ramp_params["Pos1"]["max"]), 4)

        node_HueSaturationValue_Defect_BaseColor.inputs["Value"].default_value = \
        round(random.uniform(self.defect_color_value_range["min"], self.defect_color_value_range["max"]), 4)

        # Set params - defect roughness
        node_Mapping_Defect_Roughness.inputs["Location"].default_value[2] = \
        round(random.uniform(self.defect_roughness_noise_texture_location_range["Z"]["min"], self.defect_roughness_noise_texture_location_range["Z"]["max"]), 4) 
        
        node_NoiseTexture_Defect_Roughness.inputs["Scale"].default_value = \
        round(random.uniform(self.defect_color_noise_texture_params["Scale"]["min"], self.defect_color_noise_texture_params["Scale"]["max"]), 4)

        node_ColorRamp_Defect_Roughness.color_ramp.elements[0].color = self.defect_roughness_color_ramp_params["Stop0_color"]
        node_ColorRamp_Defect_Roughness.color_ramp.elements[0].position = \
        round(random.uniform(self.defect_roughness_color_ramp_params["Pos0"]["min"], self.defect_roughness_color_ramp_params["Pos0"]["max"]), 4)
        node_ColorRamp_Defect_Roughness.color_ramp.elements[1].color = self.defect_roughness_color_ramp_params["Stop1_color"]
        node_ColorRamp_Defect_Roughness.color_ramp.elements[1].position = \
        round(random.uniform(self.defect_roughness_color_ramp_params["Pos1"]["min"], self.defect_roughness_color_ramp_params["Pos1"]["max"]), 4)

        node_Add_Defect_Roughness.inputs[1].default_value = \
        round(random.uniform(self.defect_roughness_add_range["min"], self.defect_roughness_add_range["max"]), 4)

        # Set params - defect bump
        node_ColorRamp_Defect_Bump_Bottom.color_ramp.elements[0].color = self.defect_bump_bottom_color_ramp_params["Stop0_color"]
        node_ColorRamp_Defect_Bump_Bottom.color_ramp.elements[1].color = self.defect_bump_bottom_color_ramp_params["Stop1_color"]
        node_ColorRamp_Defect_Bump_Top.color_ramp.elements[0].color = self.defect_bump_top_color_ramp_params["Stop0_color"]
        node_ColorRamp_Defect_Bump_Top.color_ramp.elements[1].color = self.defect_bump_top_color_ramp_params["Stop1_color"]
        node_Bump_Defect_Bump.inputs["Strength"].default_value = \
        round(random.uniform(self.defect_bump_strength_range["min"], self.defect_bump_strength_range["max"]), 4)

        # Set params - all image textures
        defect_mix_mask_img_name = self.defect_masks_img_paths["mix"].split("/")[-1]
        defect_bottom_mask_img_name = self.defect_masks_img_paths["bottom"].split("/")[-1]
        defect_top_mask_img_name = self.defect_masks_img_paths["top"].split("/")[-1]  

        if bpy.data.images.get(defect_mix_mask_img_name):
            bpy.data.images.remove(bpy.data.images[defect_mix_mask_img_name])

        if bpy.data.images.get(defect_bottom_mask_img_name):
            bpy.data.images.remove(bpy.data.images[defect_bottom_mask_img_name])

        if bpy.data.images.get(defect_top_mask_img_name):
            bpy.data.images.remove(bpy.data.images[defect_top_mask_img_name])

        node_ImageTexture_Mix.image = bpy.data.images.load(self.defect_masks_img_paths["mix"])
        node_ImageTexture_Defect_Bump_Bottom.image = bpy.data.images.load(self.defect_masks_img_paths["bottom"])
        node_ImageTexture_Defect_Bump_Top.image = bpy.data.images.load(self.defect_masks_img_paths["top"])

        # Set params - bsdf Metallic
        node_BSDF_Surface.inputs["Metallic"].default_value = 1
        node_BSDF_Defect.inputs["Metallic"].default_value = 1


    def plane_texture_randomize(self):
        """ 
        """
        self.__get_plane_need_assign_material()
        self.__create_new_aluminum_material()
        self.__create_aluminum_surface_material_nodes()
        self.__create_aluminum_defect_material_nodes()
        self.__create_aluminum_material_mix_nodes()
        self.__randomly_set_material_parameters()

        print("Plane Texture Randomize COMPLERED !!!")


if __name__ == '__main__':
    randomizer = PlaneTextureRandomizer()
    randomizer.plane_texture_randomize()