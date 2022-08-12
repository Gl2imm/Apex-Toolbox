# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Apex Toolbox",
    "author": "Random Blender Dude",
    "version": (2, 0),
    "blender": (2, 90, 0),
    "location": "Operator",
    "description": "Apex models toolbox",
    "warning": "Im noob in python language",
    "category": "Object"
}


import bpy
import os
from bpy.types import Scene
from bpy.props import (BoolProperty,FloatProperty)

ver = 2.0
loadImages = True
texSets = [['albedoTexture'],['specTexture'],['emissiveTexture'],['scatterThicknessTexture'],['opacityMultiplyTexture'],['normalTexture'],['glossTexture'],['aoTexture'],['cavityTexture']]

blend_file = ("\\ApexShader.blend")
ap_node = ("\\NodeTree")
ap_object = ("\\Object")
ap_collection = ("\\Collection")
ap_material = ("\\Material")
ap_world = ("\\World")


mode = 1 #0 - Test Mode; 1 - Live mode

if mode == 0:
    my_path = ("E:\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_toolbox")
    #asset_folder = ("E:\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_Toolbox_Assets\\")
    asset_folder = ("D:\\Personal\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_Toolbox_Assets\\")
else:
    my_path = (os.path.dirname(os.path.realpath(__file__)))



    #OPERATOR         
########################################   
class apexToolsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
 
    asset_folder: bpy.props.StringProperty(name="Folder",
                                        description="Select Assets folder",
                                        default="",
                                        maxlen=1024,
                                        subtype="DIR_PATH")
                                        
    if mode == 0:
        #asset_folder = "E:\G-Drive\Blender\0. Setups\Apex\Apex_toolbox\Apex_Toolbox_Assets\\"
        asset_folder = ("D:\\Personal\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_Toolbox_Assets\\")
        
 
class PROPERTIES_CUSTOM(bpy.types.PropertyGroup):
    
    name : bpy.props.StringProperty(name= "Name", default="folder_name", maxlen=40) #not in use
    
                
                    
    ### For Autotex ####
    cust_enum : bpy.props.EnumProperty(
        name = "Shader",
        description = "Shader for recolor",
        default='OP1',
        items = [('OP1', "Apex Shader", ""),
                 ('OP2', "S/G-Blender", "")    
                ]
        )
        
    autotex_folder: bpy.props.StringProperty(name="Folder",
                                        description="Select textures folder",
                                        default="",
                                        maxlen=1024,
                                        subtype="DIR_PATH")
                                        
    aut_subf : BoolProperty(
    name="Have Sub-folders?",
    description="Autotex property",
    default = False
    )                                                
    
    ### For Recolor ####    
    cust_enum2 : bpy.props.EnumProperty(
        name = "Shader",
        description = "Shader for Autotex",
        default='OP1',
        items = [('OP1', "Apex Shader", ""),
                 ('OP2', "S/G-Blender", "")    
                ]
        )
        
    recolor_folder: bpy.props.StringProperty(name="Folder",
                                        description="Select Recolor textures folder",
                                        default="",
                                        maxlen=1024,
                                        subtype="DIR_PATH")
                                        
    rec_subf : BoolProperty(
    name="Have Sub-folders?",
    description="Recolor folder property",
    default = True
    ) 
    
    rec_alpha : BoolProperty(
    name="Plug Alpha?",
    description="Recolor Alpha property",
    default = True
    )                                                        

    cust_enum_shader : bpy.props.EnumProperty(
        name = "Shader",
        description = "Append Shader",
        default='OP1',
        items = [('OP1', "Apex Shader", ""),
                 ('OP2', "S/G-Blender", ""),
                 ('OP3', "Apex Cycles (Blue)", "")     
                ]
        )
    
    
    cust_enum_hdri : bpy.props.EnumProperty(
        name = "HDRI",
        description = "Append HDRI",
        default='OP1',
        items = [('OP1', "Blender Default", ""),
                 ('OP2', "Party Crasher", ""),
                 ('OP3', "Encore", ""),
                 ('OP4', "Habitat", ""),
                 ('OP5', "Kings Canyon", ""),
                 ('OP6', "Olympus", ""),
                 ('OP7', "Phase Runner", ""),
                 ('OP8', "Storm Point", ""),
                 ('OP9', "Worlds Edge", ""),     
                ]
        )

        
    my_bool : BoolProperty(
    name="Parent to Bone? (Not done yet)",
    description="Mirage Bone parent property",
    default = False
    )
    
    my_bool2 : BoolProperty(
    name="Parent to Bone? (Not done yet)",
    description="Flatline Bone parent property",
    default = False
    )    
    
    
class BUTTON_CUSTOM(bpy.types.Operator):
    bl_label = "BUTTON CUSTOM"
    bl_idname = "object.button_custom"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
           
    ########## OPTION - 1 (Apex Shader) ############
        if prefs.cust_enum2 == 'OP1':        
            if bpy.data.node_groups.get('Apex Shader') == None:
                selection = [obj.name for obj in bpy.context.selected_objects]
                bpy.ops.wm.append(directory =my_path + blend_file + ap_node, filename ='Apex Shader')
                for x in range(len(selection)):
                    bpy.data.objects[selection[x]].select_set(True)
                    x += 1
            
            for o in bpy.context.selected_objects:
                if o.type == 'MESH':
                    for mSlot in o.material_slots:
                        MatNodeTree = bpy.data.materials[mSlot.name]
                        try:
                            imageNode = MatNodeTree.node_tree.nodes["Image Texture"]
                        except:
                            print(MatNodeTree.name)
                            continue
                        try:
                            image = os.path.basename(bpy.path.abspath(imageNode.image.filepath))
                        except:
                            print(mSlot.name, "missing texture.")
                        imagepath = os.path.dirname(bpy.path.abspath(imageNode.image.filepath))
                        imageType = imageNode.image.name.split(".")[0].split('_')[-1]
                        imageName = MatNodeTree.name
                        imageFormat = image.split('.')[1]
                        
                        if not any(imageType in x for x in texSets):
                            print(image,"could not be mapped.")        
                            continue


                        MatNodeTree.node_tree.nodes.clear()
                        
                        for i in range(len(texSets)):
                            for j in range(len(texSets[i])):
                                texImageName = imageName + '_' + texSets[i][j] + '.' + imageFormat
                                texImage = bpy.data.images.get(texImageName)
                                texFile = imagepath + '\\' + texImageName
                                if not texImage and loadImages:
                                    if os.path.isfile(texFile):
                                        texImage = bpy.data.images.load(texFile)
                                if texImage:
                                    if i > 2:
                                        texImage.colorspace_settings.name = 'Non-Color'
                                    texImage.alpha_mode = 'CHANNEL_PACKED'
                                    texNode = MatNodeTree.node_tree.nodes.new('ShaderNodeTexImage')
                                    texNode.image = texImage
                                    texNode.name = str(i)
                                    texNode.location = (-50,50-260*i)
                                    break
                                
                                

                        NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                        NodeGroup.node_tree = bpy.data.node_groups.get('Apex Shader')
                        NodeGroup.location = (300,0)
                        NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                        NodeOutput.location = (500,0)
                        MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])
                            
                        ColorDict = {
                            "0": "Albedo Map",
                            "1": "Specular Map",
                            "2": "Emission",
                            "3": "SSS Map",
                            "4": "Alpha",     
                            "5": "Normal Map",
                            "6": "Glossiness Map",
                            "7": "AO"
                        }
                        AlphaDict = {
                            "0": "Alpha",
                            "3": "SSS Alpha",
                        }

                        for slot in AlphaDict:
                            try:
                                MatNodeTree.node_tree.links.new(NodeGroup.inputs[AlphaDict[slot]], MatNodeTree.node_tree.nodes[slot].outputs["Alpha"])
                            except:
                                pass
                        for slot in ColorDict:
                            try:
                                MatNodeTree.node_tree.links.new(NodeGroup.inputs[ColorDict[slot]], MatNodeTree.node_tree.nodes[slot].outputs["Color"])
                            except:
                                pass
                        mSlot.material.blend_method = 'HASHED'
        print("Textured",mSlot.name)
                        
    ########## OPTION - 2 (S/G Blender) ############
        if prefs.cust_enum2 == 'OP2':        
            if bpy.data.node_groups.get('S/G-Blender') == None:
                selection = [obj.name for obj in bpy.context.selected_objects]
                bpy.ops.wm.append(directory =my_path + blend_file + ap_node, filename ='S/G-Blender')
                for x in range(len(selection)):
                    bpy.data.objects[selection[x]].select_set(True)
                    x += 1
            
            for o in bpy.context.selected_objects:
                if o.type == 'MESH':
                    for mSlot in o.material_slots:
                        MatNodeTree = bpy.data.materials[mSlot.name]
                        try:
                            imageNode = MatNodeTree.node_tree.nodes["Image Texture"]
                        except:
                            print(MatNodeTree.name)
                            continue
                        try:
                            image = os.path.basename(bpy.path.abspath(imageNode.image.filepath))
                        except:
                            print(mSlot.name, "missing texture.")
                        imagepath = os.path.dirname(bpy.path.abspath(imageNode.image.filepath))
                        imageType = imageNode.image.name.split(".")[0].split('_')[-1]
                        imageName = MatNodeTree.name
                        imageFormat = image.split('.')[1]
                        
                        if not any(imageType in x for x in texSets):
                            print(image,"could not be mapped.")        
                            continue


                        MatNodeTree.node_tree.nodes.clear()
                        
                        for i in range(len(texSets)):
                            for j in range(len(texSets[i])):
                                texImageName = imageName + '_' + texSets[i][j] + '.' + imageFormat
                                texImage = bpy.data.images.get(texImageName)
                                texFile = imagepath + '\\' + texImageName
                                if not texImage and loadImages:
                                    if os.path.isfile(texFile):
                                        texImage = bpy.data.images.load(texFile)
                                if texImage:
                                    if i > 2:
                                        texImage.colorspace_settings.name = 'Non-Color'
                                    texImage.alpha_mode = 'CHANNEL_PACKED'
                                    texNode = MatNodeTree.node_tree.nodes.new('ShaderNodeTexImage')
                                    texNode.image = texImage
                                    texNode.name = str(i)
                                    texNode.location = (-50,50-260*i)
                                    break
                                
                                

                        NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                        NodeGroup.node_tree = bpy.data.node_groups.get('S/G-Blender')
                        NodeGroup.location = (300,0)
                        NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                        NodeOutput.location = (500,0)
                        MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])
                            
                        ColorDict = {
                            "0": "Diffuse map",
                            "1": "Specular map",
                            "2": "Emission input",
                            "3": "Subsurface",
                            "4": "Alpha input",     
                            "5": "Normal map",
                            "6": "Glossiness map",
                            "7": "AO map",
                            "8": "Cavity map",
                        }
                        AlphaDict = {
                            "0": "Alpha",
                            "3": "SSS Alpha",
                        }
                        

                        for slot in AlphaDict:
                            try:
                                MatNodeTree.node_tree.links.new(NodeGroup.inputs[AlphaDict[slot]], MatNodeTree.node_tree.nodes[slot].outputs["Alpha"])
                            except:
                                pass
                        for slot in ColorDict:
                            try:
                                MatNodeTree.node_tree.links.new(NodeGroup.inputs[ColorDict[slot]], MatNodeTree.node_tree.nodes[slot].outputs["Color"])
                            except:
                                pass
                        mSlot.material.blend_method = 'HASHED'
        print("Textured",mSlot.name)                        
                        
        return {'FINISHED'}
        

    
    
class BUTTON_CUSTOM2(bpy.types.Operator):
    bl_label = "BUTTON CUSTOM2"
    bl_idname = "object.button_custom2"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        rec_subf = prefs.rec_subf
        rec_alpha = prefs.rec_alpha
        if mode == 0:
            recolor_folder = ("D:\Personal\G-Drive\Blender\Apex\models\Wraith\Materials\wraith_lgnd_v19_liberator_rc01\\")
            #recolor_folder = ("E:\G-Drive\Blender\Apex\models\Wraith\Materials\wraith_lgnd_v19_liberator_rc01\\")
        else:
            recolor_folder = prefs.recolor_folder
            
            
    ########## OPTION - 1 (Apex Shader) ############
        if prefs.cust_enum == 'OP1':
            print("\n######## RECOLORING MODEL: ########")
            if bpy.data.node_groups.get('Apex Shader') == None:
                selection = [obj.name for obj in bpy.context.selected_objects]
                bpy.ops.wm.append(directory =my_path + blend_file + ap_node, filename ='Apex Shader')
                for x in range(len(selection)):
                    bpy.data.objects[selection[x]].select_set(True)
                    x += 1
                print("Appended Apex Shader")
                    
            for o in bpy.context.selected_objects:
                if o.type == 'MESH':
                    for mSlot in o.material_slots:
                        MatNodeTree = bpy.data.materials[mSlot.name] #mSlot.name material name
                        
                        foldername = recolor_folder.split("\\")[-2] #folder name
                        imgBodyPart = mSlot.name.split('_')[-1] #part name
                        folderpath = recolor_folder + "\\" + foldername + "_" + imgBodyPart
                        img = folderpath + "_" + texSets[0][0] + '.png'
                        eyefolderpath = recolor_folder + '\\' + 'base'
                        eyeimg = recolor_folder + '\\' + mSlot.name + "_" + texSets[0][0] + '.png'
                        exist = 0
                        
                            
                        if rec_subf == False:
                            if os.path.exists(img) == True: #Consider only 1st image with albedo
                                exist = 1
                            else:
                                if mSlot.name == "wraith_base_eye" or mSlot.name == "teeth" or mSlot.name == "wraith_base_eyecornea" or mSlot.name == "wraith_base_eyeshadow" or mSlot.name == "wraith_base_hair":
                                    if os.path.exists(eyeimg) == True: #Consider only 1st image with albedo
                                        exist = 1
                                    else:
                                        print("Copy base images 'teeth_albedoTexture.png', 'wraith_base_eye_albedoTexture.png', etc. into " + "--" + recolor_folder + "--") 
                        else:
                            if os.path.exists(folderpath) == True: 
                                exist = 1
                            else:
                                if mSlot.name == "wraith_base_eye" or mSlot.name == "teeth" or mSlot.name == "wraith_base_eyecornea" or mSlot.name == "wraith_base_eyeshadow" or mSlot.name == "wraith_base_hair":
                                    if os.path.exists(eyefolderpath) == True:
                                        exist = 1
                                    else:
                                        print("Create folder named 'base' in " + "--" + recolor_folder + "--" + " Copy base images there 'teeth_albedoTexture.png', 'wraith_base_eye_albedoTexture.png', etc. ") 
                                        
                        if exist == 0:                                                                                                    
                            print("Textures for " + "--" + mSlot.name + "--" + " cannot be found")
                            print("Skipping") 
                            
                        if exist == 1:                            
                            MatNodeTree.node_tree.nodes.clear()
         
                            for i in range(len(texSets)):
                                for j in range(len(texSets[i])):
                                    if mSlot.name == "wraith_base_eye" or mSlot.name == "teeth" or mSlot.name == "wraith_base_eyecornea" or mSlot.name == "wraith_base_eyeshadow" or mSlot.name == "wraith_base_hair":
                                        texImageName = mSlot.name + '_' + texSets[i][j] + '.png'
                                        if rec_subf == True:
                                            texFile = recolor_folder + '\\' + 'base' + '\\' + texImageName
                                        else:
                                            texFile = recolor_folder + '\\' + texImageName
                                    else:
                                        texImageName = foldername + '_' + imgBodyPart + '_' + texSets[i][j] + '.png'
                                        #print("texImageName: " + texImageName)
                                        if rec_subf == True:
                                            texFile = recolor_folder + '\\' + foldername + '_' + imgBodyPart + '\\' + texImageName
                                        else:
                                            texFile = recolor_folder + '\\' + texImageName
                                            
          
                                    try:
                                        texImage = bpy.data.images.load(texFile)
                                    except:
                                        print("Unable to load image: " + texImageName)
                                        continue
                                            
                                    if texImage:
                                        if i > 2:
                                            texImage.colorspace_settings.name = 'Non-Color'
                                        texImage.alpha_mode = 'CHANNEL_PACKED'
                                        texNode = MatNodeTree.node_tree.nodes.new('ShaderNodeTexImage')
                                        texNode.image = texImage
                                        texNode.name = str(i)
                                        texNode.location = (-50,50-260*i)
                                        break

                            NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                            NodeGroup.node_tree = bpy.data.node_groups.get('Apex Shader')
                            NodeGroup.location = (300,0)
                            NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                            NodeOutput.location = (500,0)
                            MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])
                            
                            ColorDict = {
                                "0": "Albedo Map",
                                "1": "Specular Map",
                                "2": "Emission",
                                "3": "SSS Map",
                                "4": "Alpha",     
                                "5": "Normal Map",
                                "6": "Glossiness Map",
                                "7": "AO"
                            }
                            AlphaDict = {
                                "0": "Alpha",
                                "3": "SSS Alpha",
                            }
                            
                            if rec_alpha == True:
                                for slot in AlphaDict:
                                    try:
                                        MatNodeTree.node_tree.links.new(NodeGroup.inputs[AlphaDict[slot]], MatNodeTree.node_tree.nodes[slot].outputs["Alpha"])
                                    except:
                                        pass
                            else:
                                pass
                            for slot in ColorDict:
                                try:
                                    MatNodeTree.node_tree.links.new(NodeGroup.inputs[ColorDict[slot]], MatNodeTree.node_tree.nodes[slot].outputs["Color"])
                                except:
                                    pass
                            mSlot.material.blend_method = 'HASHED'
                            print("Textured",mSlot.name)
                        
    
    ########## OPTION - 2 (S/G-Blender) ############
        if prefs.cust_enum == 'OP2':
            print("\n######## RECOLORING MODEL: ########")
            if bpy.data.node_groups.get('S/G-Blender') == None:
                selection = [obj.name for obj in bpy.context.selected_objects]
                bpy.ops.wm.append(directory =my_path + blend_file + ap_node, filename ='S/G-Blender')
                for x in range(len(selection)):
                    bpy.data.objects[selection[x]].select_set(True)
                    x += 1
                print("Appended Apex Shader")
                    
            for o in bpy.context.selected_objects:
                if o.type == 'MESH':
                    for mSlot in o.material_slots:
                        MatNodeTree = bpy.data.materials[mSlot.name] #mSlot.name material name
                        
                        foldername = recolor_folder.split("\\")[-2] #folder name
                        imgBodyPart = mSlot.name.split('_')[-1] #part name
                        folderpath = recolor_folder + "\\" + foldername + "_" + imgBodyPart
                        img = folderpath + "_" + texSets[0][0] + '.png'
                        eyefolderpath = recolor_folder + '\\' + 'base'
                        eyeimg = recolor_folder + '\\' + mSlot.name + "_" + texSets[0][0] + '.png'
                        exist = 0
                        
                            
                        if rec_subf == False:
                            if os.path.exists(img) == True: #Consider only 1st image with albedo
                                exist = 1
                            else:
                                if mSlot.name == "wraith_base_eye" or mSlot.name == "teeth" or mSlot.name == "wraith_base_eyecornea" or mSlot.name == "wraith_base_eyeshadow" or mSlot.name == "wraith_base_hair":
                                    if os.path.exists(eyeimg) == True: #Consider only 1st image with albedo
                                        exist = 1
                                    else:
                                        print("Copy base images 'teeth_albedoTexture.png', 'wraith_base_eye_albedoTexture.png', etc. into " + "--" + recolor_folder + "--") 
                        else:
                            if os.path.exists(folderpath) == True: 
                                exist = 1
                            else:
                                if mSlot.name == "wraith_base_eye" or mSlot.name == "teeth" or mSlot.name == "wraith_base_eyecornea" or mSlot.name == "wraith_base_eyeshadow" or mSlot.name == "wraith_base_hair":
                                    if os.path.exists(eyefolderpath) == True:
                                        exist = 1
                                    else:
                                        print("Create folder named 'base' in " + "--" + recolor_folder + "--" + " Copy base images there 'teeth_albedoTexture.png', 'wraith_base_eye_albedoTexture.png', etc. ") 
                                        
                        if exist == 0:                                                                                                    
                            print("Textures for " + "--" + mSlot.name + "--" + " cannot be found")
                            print("Skipping") 
                            
                        if exist == 1:                            
                            MatNodeTree.node_tree.nodes.clear()
         
                            for i in range(len(texSets)):
                                for j in range(len(texSets[i])):
                                    if mSlot.name == "wraith_base_eye" or mSlot.name == "teeth" or mSlot.name == "wraith_base_eyecornea" or mSlot.name == "wraith_base_eyeshadow" or mSlot.name == "wraith_base_hair":
                                        texImageName = mSlot.name + '_' + texSets[i][j] + '.png'
                                        if rec_subf == True:
                                            texFile = recolor_folder + '\\' + 'base' + '\\' + texImageName
                                        else:
                                            texFile = recolor_folder + '\\' + texImageName
                                    else:
                                        texImageName = foldername + '_' + imgBodyPart + '_' + texSets[i][j] + '.png'
                                        #print("texImageName: " + texImageName)
                                        if rec_subf == True:
                                            texFile = recolor_folder + '\\' + foldername + '_' + imgBodyPart + '\\' + texImageName
                                        else:
                                            texFile = recolor_folder + '\\' + texImageName
                                            
          
                                    try:
                                        texImage = bpy.data.images.load(texFile)
                                    except:
                                        print("Unable to load image: " + texImageName)
                                        continue
                                            
                                    if texImage:
                                        if i > 2:
                                            texImage.colorspace_settings.name = 'Non-Color'
                                        texImage.alpha_mode = 'CHANNEL_PACKED'
                                        texNode = MatNodeTree.node_tree.nodes.new('ShaderNodeTexImage')
                                        texNode.image = texImage
                                        texNode.name = str(i)
                                        texNode.location = (-50,50-260*i)
                                        break

                            NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                            NodeGroup.node_tree = bpy.data.node_groups.get('S/G-Blender')
                            NodeGroup.location = (300,0)
                            NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                            NodeOutput.location = (500,0)
                            MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])
                            
                            ColorDict = {
                                "0": "Diffuse map",
                                "1": "Specular map",
                                "2": "Emission input",
                                "3": "Subsurface",
                                "4": "Alpha input",     
                                "5": "Normal map",
                                "6": "Glossiness map",
                                "7": "AO map",
                                "8": "Cavity map",
                            }
                            AlphaDict = {
                                "0": "Alpha input",
                                "3": "SSS Alpha",
                            }
                            
                            if rec_alpha == True:
                                for slot in AlphaDict:
                                    try:
                                        MatNodeTree.node_tree.links.new(NodeGroup.inputs[AlphaDict[slot]], MatNodeTree.node_tree.nodes[slot].outputs["Alpha"])
                                    except:
                                        pass
                            else:
                                pass
                            for slot in ColorDict:
                                try:
                                    MatNodeTree.node_tree.links.new(NodeGroup.inputs[ColorDict[slot]], MatNodeTree.node_tree.nodes[slot].outputs["Color"])
                                except:
                                    pass
                            mSlot.material.blend_method = 'HASHED'
                            print("Textured",mSlot.name)            

        return {'FINISHED'}
        



class BUTTON_SHADERS(bpy.types.Operator):
    bl_label = "BUTTON_SHADERS"
    bl_idname = "object.button_shaders"
    bl_options = {'REGISTER', 'UNDO'}
    


    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        
        if prefs.cust_enum_shader == 'OP1':
            if bpy.data.node_groups.get('Apex Shader') == None:
                bpy.ops.wm.append(directory =my_path + blend_file + ap_node, filename ='Apex Shader')
                print("Apex Shader Appended")
            else:
                print("Apex Shader Already exist")
        if prefs.cust_enum_shader == 'OP2':
            if bpy.data.node_groups.get('S/G-Blender') == None:
                bpy.ops.wm.append(directory =my_path + blend_file + ap_node, filename ='S/G-Blender')
                print("S/G-Blender Appended")
            else:
                print("S/G-Blender Already exist")
        if prefs.cust_enum_shader == 'OP3':
            if bpy.data.node_groups.get('Apex Cycles (Blue)') == None:
                bpy.ops.wm.append(directory =my_path + blend_file + ap_node, filename ='Apex Cycles (Blue)')
                print("Apex Cycles (Blue) Appended")
            else:
                print("Apex Cycles (Blue) Already exist")
        return {'FINISHED'}  
    
    

class BUTTON_HDRIFULL(bpy.types.Operator):
    bl_label = "BUTTON_HDRIFULL"
    bl_idname = "object.button_hdrifull"
    bl_options = {'REGISTER', 'UNDO'}
    

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        
        
        blend_file = ("\\Assets.blend")

        if mode == 0:
            #asset_folder = ("E:\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_Toolbox_Assets\\")
            asset_folder = ("D:\\Personal\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_Toolbox_Assets\\")
        else:
            asset_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder
        
            
        if prefs.cust_enum_hdri == 'OP1':
            hdri_name = "World"                    
        
        if prefs.cust_enum_hdri == 'OP2':
            hdri_name = "Party crasher HDRI"
            
        if prefs.cust_enum_hdri == 'OP3':
            hdri_name = "Encore HDRI"
            
        if prefs.cust_enum_hdri == 'OP4':
            hdri_name = "Habitat HDRI"
            
        if prefs.cust_enum_hdri == 'OP5':
            hdri_name = "Kings Canyon HDRI"
            
        if prefs.cust_enum_hdri == 'OP6':
            hdri_name = "Olympus HDRI"
            
        if prefs.cust_enum_hdri == 'OP7':
            hdri_name = "Phase Runner HDRI"
            
        if prefs.cust_enum_hdri == 'OP8':
            hdri_name = "Storm Point HDRI"
            
        if prefs.cust_enum_hdri == 'OP9':
            hdri_name = "Worlds Edge HDRI"      
            

        if hdri_name not in bpy.data.worlds:
            bpy.ops.wm.append(directory =asset_folder + blend_file + ap_world, filename =hdri_name)
            hdri = bpy.data.worlds[hdri_name]
            scene.world = hdri
            print(hdri_name + " has been Appended and applied to the World")            
        else:
            if bpy.context.scene.world != hdri_name:
                hdri = bpy.data.worlds[hdri_name]
                scene.world = hdri
                print(hdri_name + " is already inside and it's been applied to the World") 
        
        
        return {'FINISHED'}  


######### Wraith Buttons ###########    
    
# Wraith Portal #
class WR_BUTTON_PORTAL(bpy.types.Operator):
    bl_label = "WR_BUTTON_PORTAL"
    bl_idname = "object.wr_button_portal"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.data.objects.get('wraith_portal') == None:
            bpy.ops.wm.append(directory =my_path + blend_file + ap_object, filename ='wraith_portal')
            print("Wraith Portal Appended")
        else:
            print("Wraith Portal already inside")
        return {'FINISHED'}      
   


######### Gibby Buttons ###########    

class GB_BUTTON_ITEMS(bpy.types.Operator):
    bl_label = "GB_BUTTON_ITEMS"
    bl_idname = "object.gb_button_items"
    bl_options = {'REGISTER', 'UNDO'}
    gibby : bpy.props.StringProperty(name= "Added")


    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        gibby = (self.gibby)
        bubble_items_friendly = [
                {'name': 'Gibby bubble friendly'}, 
                {'name': 'Gibby bubble core friendly'}, 
                {'name': 'Gibby bubble image friendly'},
                {'name': 'Gibby bubble rod friendly'}
                ]    
        bubble_items_enemy = [
                {'name': 'Gibby bubble enemy'}, 
                {'name': 'Gibby bubble core enemy'}, 
                {'name': 'Gibby bubble image enemy'},
                {'name': 'Gibby bubble rod enemy'}
                ]                   
    
           
        #Gibby Dome Shield friendly
        if gibby == "Gibby bubble friendly":
            if bpy.data.objects.get(gibby) == None:
                bpy.ops.wm.append(directory =my_path + blend_file + ap_object, files=bubble_items_friendly)
                print("Gibby Friendly Bubble Appended")
            else:
                print("Gibby Friendly Bubble already exist")
        
        #Gibby Dome Shield enemy        
        if gibby == "Gibby bubble enemy":
            if bpy.data.objects.get(gibby) == None:
                bpy.ops.wm.append(directory =my_path + blend_file + ap_object, files=bubble_items_enemy)
                print("Gibby Enemy Bubble Appended")
            else:
                print("Gibby Enemy Bubble already exist")
                
        return {'FINISHED'} 
    
       
   
######### Mirage Buttons ###########    
    
# Mirage Decoy #
class MR_BUTTON_DECOY(bpy.types.Operator):
    bl_label = "Decoy Outline Thickness"
    bl_idname = "object.mr_button_decoy"
    bl_options = {'REGISTER', 'UNDO'}
    mr_decoy : bpy.props.StringProperty(name= "Added")
    
    
    #Operator Properties
    outline_thickness : FloatProperty(
        name = "Outline Thickness",
        description = "Thickness of the applied outline",
        default = 0.23,
        min = 0,
        max = 1000000
    )

        
    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs   
        sel = bpy.context.selected_objects
        mr_decoy = (self.mr_decoy)
        decoy_items = [
                {'name': 'Decoy'}, 
                {'name': 'Floor_bloom'}, 
                {'name': 'Flare Generator'},
                {'name': 'Decoy Effects'},
                {'name': 'Decoy flare'},
                {'name': 'Decoy Text'},
                {'name': 'Decoy text triangle'},
                {'name': 'Psyche_Out'}
                ]
        
        # Mirage Decoy Effect Add #               
        if mr_decoy == "Decoy":
            if bpy.data.objects.get('Decoy') == None:
                # Copy current selection #
                selection = [obj.name for obj in bpy.context.selected_objects]
                # Append Objects #
                bpy.ops.wm.append(directory =my_path + blend_file + ap_object, files=decoy_items)
                 # Unselect all in selected #
                for obj in bpy.context.selected_objects:
                    obj.select_set(False)
                # Select initially selected #
                for x in range(len(selection)):
                    bpy.data.objects[selection[x]].select_set(True)
                    x += 1 
                # Append Material #               
                bpy.ops.wm.append(directory =my_path + blend_file + ap_material, filename ='Mirage_decoy_Material')
                # Unselect all in selected #
                for obj in bpy.context.selected_objects:
                    obj.select_set(False)
                # Select initially selected #
                for x in range(len(selection)):
                    bpy.data.objects[selection[x]].select_set(True)
                    x += 1

                print("Mirage Decoy Effect Appended, Material applied. Adding Modifier")
            else:
                print("Mirage Decoy Effect already exist. Adding Modifier only")
            

                   
            for obj in sel:
                if obj.type in ["MESH", "CURVE"]:
                    bpy.context.view_layer.objects.active = obj

                    #Material

                    mat_missing = True

                    for slot in obj.data.materials:
                        if slot is not None:
                            if slot.name == "Mirage_decoy_Material":
                                mat_missing = False

                    if mat_missing:
                        mat = bpy.data.materials.get("Mirage_decoy_Material")
                        bpy.context.object.data.materials.append(mat)


                    #Modifier

                    exists = False

                    for mod in bpy.context.object.modifiers:
                        if mod.name == "mirage_decoy":
                            exists = True

                    if exists:
                        mod = bpy.context.object.modifiers["mirage_decoy"]
                        mod.thickness = -(self.outline_thickness)
                    else: 
                        obj.modifiers.new("mirage_decoy","SOLIDIFY")
                        mod = obj.modifiers["mirage_decoy"]
                        mod.use_flip_normals = True
                        mod.use_rim = False
                        mod.thickness = -(self.outline_thickness)
                        mod.material_offset = 999
                        
            print("Mirage Decoy Effect Modifier Added") 

        # Mirage Decoy Effect Parenting #
        if mr_decoy == "Decoy_parent":
            sel_objects = bpy.context.selected_objects
            sel_names = [obj.name for obj in bpy.context.selected_objects]
            
                
            if not bpy.context.selected_objects:
                print("Nothing selected. Please select Model Bones in Object Mode")
            else:
                if len(sel_objects) > 1:
                    print("More than 1 Object slected. Please select only 1 Bone Object")
                else:
                    for bones in sel_objects:
                        if bones.type in ["ARMATURE"]:
                            if bpy.data.objects.get('Decoy') == None:
                                print("Decoy Effect not Found. Pls add Effect first")
                            else:
                                #print(sel_objects.type)
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.select_all(action='DESELECT')
                                bpy.context.view_layer.objects.active = None
                                bpy.data.objects['Decoy'].select_set(True)
                                bpy.data.objects[sel_names[0]].select_set(True)
                                bpy.context.view_layer.objects.active = bpy.data.objects[sel_names[0]]
                                

                                arm = bpy.data.objects['Decoy']
                                bpy.ops.object.mode_set(mode='EDIT')
                                bpy.ops.armature.select_all(action='DESELECT')
                                

                                bones_to_select = ['Bone']
                                for bone in arm.data.edit_bones:
                                    if bone.name in bones_to_select:
                                        bone.select = True
                                        
                                arm = bpy.data.objects[sel_names[0]]
                                bones_to_select = ['def_c_spineA']
                                for bone in arm.data.edit_bones:
                                    if bone.name in bones_to_select:
                                        bone.select = True 
                                        
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.parent_set(type='OBJECT')
                                
                                print("Parenting Decoy Effect to Mirage Done")
                        else:
                            print("Selected Object is Not a Bone. Pls Select Bones")                                

        return {'FINISHED'} 
                

######### Valkyrie Buttons ###########    

class VK_BUTTON_ITEMS(bpy.types.Operator):
    bl_label = "VK_BUTTON_ITEMS"
    bl_idname = "object.vk_button_items"
    bl_options = {'REGISTER', 'UNDO'}
    valk : bpy.props.StringProperty(name= "Added")


    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        valk = (self.valk)
        flames_items = [
                {'name': 'Flames left'}, 
                {'name': 'Flames right'} 
                ]    
    
           
        #Valk Flames
        if valk == "Flames":
            if bpy.data.objects.get('Flames left') == None:
                bpy.ops.wm.append(directory =my_path + blend_file + ap_object, files=flames_items)
                print("Valkyrie Flames Bubble Appended")
            else:
                print("Valkyrie Flames Bubble already exist")
        

        # Valk Flames Parenting #
        if valk == "Flames_parent":
            sel_objects = bpy.context.selected_objects
            sel_names = [obj.name for obj in bpy.context.selected_objects]
            
                
            if not bpy.context.selected_objects:
                print("Nothing selected. Please select Model Bones in Object Mode")
            else:
                if len(sel_objects) > 1:
                    print("More than 1 Object slected. Please select only 1 Bone Object")
                else:
                    for bones in sel_objects:
                        if bones.type in ["ARMATURE"]:
                            if bpy.data.objects.get('Flames left') == None:
                                print("Flames Effect not Found. Pls add Effect first")
                            else:
                                #Deselect All and select only bones that were chosen
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.select_all(action='DESELECT')
                                bpy.context.view_layer.objects.active = None
                                bpy.data.objects[sel_names[0]].select_set(True)
                                bpy.context.view_layer.objects.active = bpy.data.objects[sel_names[0]]
                                
                                #Select left turbine bone in Bone Edit Mode       
                                arm = bpy.data.objects[sel_names[0]]
                                bpy.ops.object.mode_set(mode='EDIT')
                                bones_to_select = ['def_l_turbine']
                                for bone in arm.data.edit_bones:
                                    if bone.name in bones_to_select:
                                        bone.select = True 
                                
                                #Exit out Edit Mode and Deselect All    
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.select_all(action='DESELECT')
                                
                                #Select Flames, Select bones that were chosen, set bones active and parent to them
                                bpy.data.objects['Flames left'].select_set(True)
                                bpy.data.objects[sel_names[0]].select_set(True)
                                bpy.context.view_layer.objects.active = bpy.data.objects[sel_names[0]]
                                bpy.ops.object.parent_set(type='BONE')
                                
                                #Deselect All and select only bones that were chosen    
                                bpy.ops.object.select_all(action='DESELECT')
                                bpy.data.objects[sel_names[0]].select_set(True)
                                bpy.context.view_layer.objects.active = bpy.data.objects[sel_names[0]] 
                                
                                #Select right turbine bone in Bone Edit Mode       
                                arm = bpy.data.objects[sel_names[0]]
                                bpy.ops.object.mode_set(mode='EDIT')
                                bones_to_select = ['def_r_turbine']
                                for bone in arm.data.edit_bones:
                                    if bone.name in bones_to_select:
                                        bone.select = True 
                                
                                #Exit out Edit Mode and Deselect All    
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.select_all(action='DESELECT')
                                
                                #Select Flames, Select bones that were chosen, set bones active and parent to them
                                bpy.data.objects['Flames right'].select_set(True)
                                bpy.data.objects[sel_names[0]].select_set(True)
                                bpy.context.view_layer.objects.active = bpy.data.objects[sel_names[0]]
                                bpy.ops.object.parent_set(type='BONE') 
                                
                                bpy.ops.object.select_all(action='DESELECT')                                                              
                                                                
                                print("Parenting Flames to Valkyrie Done")
                        else:
                            print("Selected Object is Not a Bone. Pls Select Bones") 
                
        return {'FINISHED'} 
    
    

######### Badge Buttons ###########    
class BDG_BUTTON_SPAWN(bpy.types.Operator):
    bl_label = "BDG_BUTTON_SPAWN"
    bl_idname = "object.bdg_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    badge : bpy.props.StringProperty(name= "Added")


    def execute(self, context):
        blend_file = ("\\Assets.blend")

        if mode == 0:
            #asset_folder = ("E:\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_Toolbox_Assets\\")
            asset_folder = ("D:\\Personal\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_Toolbox_Assets\\")
        else:
            asset_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder

                
        if bpy.data.objects.get(self.badge) == None:
            bpy.ops.wm.append(directory =asset_folder + blend_file + ap_object, filename =self.badge)
            print(self.badge + " Appended")
        else:
            print(self.badge + " already inside")
  
        return {'FINISHED'}                 



######### Weapons Buttons ###########    
class WPN_BUTTON_SPAWN(bpy.types.Operator):
    bl_label = "WPN_BUTTON_SPAWN"
    bl_idname = "object.wpn_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    weapon : bpy.props.StringProperty(name= "Added")


    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        weapon = (self.weapon)
           
        #Flatline flame button
        if weapon == "flatline_s4_glow_hex_LOD0_SEModelMesh.125":
            if bpy.data.objects.get(weapon) == None:
                bpy.ops.wm.append(directory =my_path + blend_file + ap_object, filename =weapon)
                print("Flatline Flames Effect Appended")
            else:
                print("Flatline Flames Effect already exist")
        
        #Flatline flame parent button
        if weapon == "flatline_parent_flame":
            if bpy.data.objects.get("flatline_s4_glow_hex_LOD0_SEModelMesh.125") == None:
                print("Flatline Flames Effect not Found. Pls add Effect first")
            else:
                if bpy.data.objects.get("flatline_v20_assim_w_LOD0_skel") == None:
                    print("Flatline model <<flatline_v20_assim_w>> not detected. Add the model then click Parent it")
                else:
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = None
                    bpy.data.objects['flatline_s4_glow_hex_LOD0_skel'].select_set(True)
                    bpy.data.objects['flatline_v20_assim_w_LOD0_skel'].select_set(True)
                    bpy.context.view_layer.objects.active = bpy.data.objects['flatline_v20_assim_w_LOD0_skel']
                    

                    arm = bpy.data.objects['flatline_s4_glow_hex_LOD0_skel']
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.armature.select_all(action='DESELECT')
                    

                    bones_to_select = ['static_prop']
                    for bone in arm.data.edit_bones:
                        if bone.name in bones_to_select:
                            bone.select = True
                            
                    arm = bpy.data.objects['flatline_v20_assim_w_LOD0_skel']
                    bones_to_select = ['def_c_base']
                    for bone in arm.data.edit_bones:
                        if bone.name in bones_to_select:
                            bone.select = True 
                            
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.parent_set(type='BONE')
                    print("Parenting Flames to Flatline Done")

            '''    
            if bpy.data.objects.get(self.weapon) == None:
                bpy.ops.wm.append(directory =my_path + blend_file + ap_object, filename =self.badge)
                print(self.weapon + " Appended")
            else:
                print(self.weapon + " already inside")
            '''
  
        return {'FINISHED'}   
              

######### Loot Items Buttons ###########    
class LT_BUTTON_SPAWN(bpy.types.Operator):
    bl_label = "LT_BUTTON_SPAWN"
    bl_idname = "object.lt_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    loot : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        loot = (self.loot)
        
        blend_file = ("\\Assets.blend")

        if mode == 0:
            #asset_folder = ("E:\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_Toolbox_Assets\\")
            asset_folder = ("D:\\Personal\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_Toolbox_Assets\\")
        else:
            asset_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder        

        loot_items_body = [
            {'name': 'w_loot_cha_shield_upgrade_body_LOD0_skel'}, 
            {'name': 'w_loot_cha_shield_upgrade_body_LOD0_SEModelMesh.106'}, 
            {'name': 'w_loot_cha_shield_upgrade_body_LOD0_SEModelMesh.107'}
            ]
            
        loot_items_helmet = [
            {'name': 'w_loot_cha_shield_upgrade_head_LOD0_skel'}, 
            {'name': 'w_loot_cha_shield_upgrade_head_LOD0_SEModelMesh.108'}, 
            {'name': 'w_loot_cha_shield_upgrade_head_LOD0_SEModelMesh.109'}
            ]         
        
        if loot == "armor white" or loot == "armor blue" or loot == "armor purple" or loot == "armor gold" or loot == "armor red":
            bpy.ops.wm.append(directory =asset_folder + blend_file + ap_object, files=loot_items_body)
        if loot == "helmet white" or loot == "helmet blue" or loot == "helmet purple" or loot == "helmet gold" or loot == "helmet red":
            bpy.ops.wm.append(directory =asset_folder + blend_file + ap_object, files=loot_items_helmet)    
        selection = [obj.name for obj in bpy.context.selected_objects]
            
        for obj in bpy.context.selected_objects:
            obj.select_set(False)
        
        bpy.data.objects[selection[1]].select_set(True)
        mat = bpy.data.objects[selection[1]].active_material
                    
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        node_gold = nodes['RGB']
        node_blue = nodes['RGB.001']
        node_purple = nodes['RGB.002']
        node_red = nodes['RGB.003']
        node_output = nodes['Armor shader']
 
        
        if loot == "armor white":    
            print("White Body Armor Appended")
            
        if loot == "armor blue":
            link = links.new(node_blue.outputs[0], node_output.inputs[0])
            print("Blue Body Armor Appended")    
         
        if loot == "armor purple":
            link = links.new(node_purple.outputs[0], node_output.inputs[0])
            print("Purple Body Armor Appended")
            
        if loot == "armor gold":
            link = links.new(node_gold.outputs[0], node_output.inputs[0])
            print("Gold Body Armor Appended")
            
        if loot == "armor red":
            link = links.new(node_red.outputs[0], node_output.inputs[0])
            print("Red Body Armor Appended")
            
        if loot == "helmet white":    
            print("White Helmet Appended")
            
        if loot == "helmet blue":
            link = links.new(node_blue.outputs[0], node_output.inputs[0])
            print("Blue Helmet Appended")    
         
        if loot == "helmet purple":
            link = links.new(node_purple.outputs[0], node_output.inputs[0])
            print("Purple Helmet Appended")
            
        if loot == "helmet gold":
            link = links.new(node_gold.outputs[0], node_output.inputs[0])
            print("Gold Helmet Appended")
            
        if loot == "helmet red":
            link = links.new(node_red.outputs[0], node_output.inputs[0])
            print("Red Helmet Appended")    
            
        return {'FINISHED'} 

    
    #PANEL UI
####################################
class AUTOTEX_MENU(bpy.types.Panel):
    bl_label = "Apex Toolbox (v." + str(ver) + ")"
    bl_idname = "OBJECT_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Apex Tools"
    
    
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prefs = scene.my_prefs
        if mode == 0:
            addon_assets = prefs
            folder = 'recolor_folder'
        else:
            addon_assets =bpy.context.preferences.addons['Apex_toolbox'].preferences
            folder = 'asset_folder'
        
        ######## Check if Asset Folder installed ######## 
        if mode == 0:
            asset_folder_set = asset_folder
        else:
            asset_folder_set =bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder
        assets_set = 0

        if os.path.exists(asset_folder_set) == True:
            asset_folder_set = asset_folder_set.split("\\")[-2]
            if asset_folder_set == "Apex_Toolbox_Assets":
                assets_set = 1            
        
        if assets_set != 1:
            row = layout.row()
            row.label(text = "Extra Assets Disabled", icon= "PANEL_CLOSE")
        else:
            row = layout.row()
            row.label(text = "Extra Assets Enabled", icon= "CHECKMARK")
                        
        ######### Readme First ###########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_readme else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_readme', icon=icon, icon_only=True)
        row.label(text = "Readme First", icon= "QUESTION")
        # some data on the subpanel
        if context.scene.subpanel_readme:
            box = layout.box()
            box.label(text = "All Credits, Help and Instructions")
            box.label(text = "inside this addon .zip file")
            if assets_set != 1:
                box.label(text = "------")
                box.label(text = "To install extra assets go to")
                box.label(text = "github.com/Gl2imm/Apex-Toolbox") 
                box.label(text = "Download, unzip and specify below")
                box.label(text = "folder name must be 'Apex_Toolbox_Assets'")
                box.label(text = "addon recognize only this folder")     
            row = layout.row()
            #row = layout.row()
            
            box.prop(addon_assets, folder)
            
            
            row.label(text = "------------------------------------------------------")



        ######### Auto_tex ###########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_status_0 else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_status_0', icon=icon, icon_only=True)
        row.label(text = "Auto_tex (by llenoco)", icon= "TEXTURE")
        # some data on the subpanel
        if context.scene.subpanel_status_0:
            row = layout.row()
            layout.prop(prefs, "cust_enum2")
            #ADD Button2
            row = layout.row()
            row.operator("object.button_custom", text = "Texture Model")
            row = layout.row()
            row.label(text = "------------------------------------------------------")
            
                    
        
        ######### Re-color ###########
        # subpanel
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_status_1 else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_status_1', icon=icon, icon_only=True)
        row.label(text = "Re-color", icon = "NODE_TEXTURE")
        # some data on the subpanel
        if context.scene.subpanel_status_1:
            box = layout.box()
            box.label(text = "Select Texture Folder")

            box.prop(prefs, 'recolor_folder')
            box.prop(prefs, 'rec_subf')
            box.prop(prefs, 'rec_alpha')
            box.prop(prefs, 'cust_enum')
            split = box.split(factor = 0.5)
            col = split.column(align = True)
            split.operator("object.button_custom2", text = "Re-Color")
            row = layout.row()
            row.label(text = "------------------------------------------------------")
            
        
        ######### Append Shader ###########
        # subpanel
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_status_2 else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_status_2', icon=icon, icon_only=True)
        if assets_set == 0:
            row.label(text = "Append Shaders", icon= "NODE_MATERIAL")
        else:
            row.label(text = "Append Shaders & HDRI", icon= "NODE_MATERIAL")
        # some data on the subpanel
        if context.scene.subpanel_status_2:
            box = layout.box()
           
            box.prop(prefs, 'cust_enum_shader')
            split = box.split(factor = 0.6)
            col = split.column(align = True)
            split.operator("object.button_shaders", text = "Add Shader")

            if assets_set == 0:
                pass
            else:
                box.prop(prefs, 'cust_enum_hdri')
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                split.operator("object.button_hdrifull", text = "Set HDRI") 
            
            row = layout.row()
            row.label(text = "------------------------------------------------------")



######### Apex effects Tab ########### 
class EFFECTS_PT_panel(bpy.types.Panel):
    bl_parent_id = "OBJECT_PT_panel"
    bl_label = "APEX EFFECTS COLLECTION"  
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_options = {"DEFAULT_CLOSED"}
    

    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prefs = scene.my_prefs
        
        
        if mode == 0:
            asset_folder_set = asset_folder
        else:
            asset_folder_set =bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder
        assets_set = 0

        if os.path.exists(asset_folder_set) == True:
            asset_folder_set = asset_folder_set.split("\\")[-2]
            if asset_folder_set == "Apex_Toolbox_Assets":
                assets_set = 1
        
                        
        ######### Wraith #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_wraith else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_wraith', icon=icon, icon_only=True)
        row.label(text='Wraith')
        # some data on the subpanel
        if context.scene.subpanel_effects_wraith:
            box = layout.box()
            
            # Wraith subpanel 1
            box.operator("object.wr_button_portal", text = "Spawn Portal")

            """
            # Wraith subpanel 2
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_wraith_prop1 else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_effects_wraith_prop1', icon=icon, icon_only=False, text='Wraith with properties')
            # some data on the subpanel
            if context.scene.subpanel_effects_wraith_prop1:
                split = box.split(factor = 0.08)
                col = split.column(align = True)
                col.label(text='1.')
                split.operator("object.wr_button_portal", text = "Spawn Portal") 
            """           


        ######### Gibraltar #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_gibby else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_gibby', icon=icon, icon_only=True)
        row.label(text='Gibraltar')
        # some data on the subpanel
        if context.scene.subpanel_effects_gibby:
            box = layout.box()
            
            # Gibraltar subpanel 1
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_gibby_prop1 else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_effects_gibby_prop1', icon=icon, icon_only=False, text='Dome Shield                          ')
            # some data on the subpanel
            if context.scene.subpanel_effects_gibby_prop1:
                split = box.split(factor = 0.08)
                col = split.column(align = True)
                col.label(text='')
                split.operator('object.gb_button_items', text = "Friendly").gibby = "Gibby bubble friendly"
                split.operator('object.gb_button_items', text = "Enemy").gibby = "Gibby bubble enemy"
                
                

        ######### Mirage #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_mirage else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_mirage', icon=icon, icon_only=True)
        row.label(text='Mirage')
        # some data on the subpanel
        if context.scene.subpanel_effects_mirage:
            box = layout.box()
            
            # Mirage subpanel 1
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_mirage_prop1 else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_effects_mirage_prop1', icon=icon, icon_only=False, text='Decoy                                    ')
            # some data on the subpanel
            if context.scene.subpanel_effects_mirage_prop1:
                split = box.split(factor = 0.08)
                col = split.column(align = True)
                col.label(text='')
                split.operator('object.mr_button_decoy', text = "Add Effect").mr_decoy = "Decoy"
                split.operator('object.mr_button_decoy', text = "Parent it").mr_decoy = "Decoy_parent" 
                box.label(text='*Sel Model Bones before Parenting')
                
            
            """
            # Mirage subpanel 2
            box.operator("object.wr_button_portal", text = "Spawn Portal")
            """     


        ######### Valkyrie #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_valkyrie else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_valkyrie', icon=icon, icon_only=True)
        row.label(text='Valkyrie')
        # some data on the subpanel
        if context.scene.subpanel_effects_valkyrie:
            box = layout.box()
            
            # Mirage subpanel 1
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_valkyrie_prop1 else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_effects_valkyrie_prop1', icon=icon, icon_only=False, text='Flames                                    ')
            # some data on the subpanel
            if context.scene.subpanel_effects_valkyrie_prop1:
                split = box.split(factor = 0.08)
                col = split.column(align = True)
                col.label(text='')
                split.operator('object.vk_button_items', text = "Add Flames").valk = "Flames"
                split.operator('object.vk_button_items', text = "Parent them").valk = "Flames_parent" 
                box.label(text='*Sel Model Bones before Parenting')
                
            
            """
            # Mirage subpanel 2
            box.operator("object.wr_button_portal", text = "Spawn Portal")
            """    
            

        ######### Weapons #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_weapons else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_weapons', icon=icon, icon_only=True)
        row.label(text='Weapons')
        # some data on the subpanel
        if context.scene.subpanel_effects_weapons:
            box = layout.box()
            
            # Flatline subpanel 1
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_weapons_prop1 else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_effects_weapons_prop1', icon=icon, icon_only=False, text='Flatline Flames (v20_assim)')
            # some data on the subpanel
            if context.scene.subpanel_effects_weapons_prop1:
                split = box.split(factor = 0.08)
                col = split.column(align = True)
                col.label(text='')
                split.operator('object.wpn_button_spawn', text = "Add Effect").weapon = "flatline_s4_glow_hex_LOD0_SEModelMesh.125"
                split.operator('object.wpn_button_spawn', text = "Parent it").weapon = "flatline_parent_flame"
                            
            

        if assets_set == 1:
            ######### Badges #########
            row = layout.row()
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_badges else 'RIGHTARROW'
            row.prop(context.scene, 'subpanel_effects_badges', icon=icon, icon_only=True)
            row.label(text='Badges (3D)')
            # some data on the subpanel
            if context.scene.subpanel_effects_badges:
                box = layout.box()
                # Badges
                box.operator('object.bdg_button_spawn', text = "4K Badge").badge = "Badge - 4k Damage"
                box.operator('object.bdg_button_spawn', text = "20 Bomb Badge").badge = "Badge - 20 Bombs"
                box.operator('object.bdg_button_spawn', text = "Predator S3 Badge").badge = "Badge - Predator S3"
                
                
                
            ######### Loot Items #########
            row = layout.row()
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot else 'RIGHTARROW'
            row.prop(context.scene, 'subpanel_effects_loot', icon=icon, icon_only=True)
            row.label(text='Loot Items')
            # some data on the subpanel
            if context.scene.subpanel_effects_loot:
                box = layout.box()
                
                # Body Armor subpanel 1
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop1 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop1', icon=icon, icon_only=False, text='Body Armor                          ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop1:
                    box.operator('object.lt_button_spawn', text = "White Armor").loot = "armor white"
                    box.operator('object.lt_button_spawn', text = "Blue Armor").loot = "armor blue"
                    box.operator('object.lt_button_spawn', text = "Purple Armor").loot = "armor purple"
                    box.operator('object.lt_button_spawn', text = "Gold Armor").loot = "armor gold"
                    box.operator('object.lt_button_spawn', text = "Red Armor").loot = "armor red"
                    
                # Helmet subpanel 2
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop2 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop2', icon=icon, icon_only=False, text='Helmet                                 ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop2:
                    box.operator('object.lt_button_spawn', text = "White Helmet").loot = "helmet white"
                    box.operator('object.lt_button_spawn', text = "Blue Helmet").loot = "helmet blue"
                    box.operator('object.lt_button_spawn', text = "Purple Helmet").loot = "helmet purple"
                    box.operator('object.lt_button_spawn', text = "Gold Helmet").loot = "helmet gold"
                    box.operator('object.lt_button_spawn', text = "Red Helmet").loot = "helmet red"            



    #CLASS REGISTER 
##########################################
classes = (
        apexToolsPreferences,
        PROPERTIES_CUSTOM, 
        BUTTON_CUSTOM, 
        BUTTON_CUSTOM2, 
        BUTTON_SHADERS, 
        BUTTON_HDRIFULL, 
        WR_BUTTON_PORTAL, 
        GB_BUTTON_ITEMS, 
        MR_BUTTON_DECOY, 
        AUTOTEX_MENU, 
        EFFECTS_PT_panel, 
        VK_BUTTON_ITEMS, 
        BDG_BUTTON_SPAWN, 
        WPN_BUTTON_SPAWN,
        LT_BUTTON_SPAWN
        )

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.my_prefs = bpy.props.PointerProperty(type= PROPERTIES_CUSTOM)
    Scene.subpanel_readme = BoolProperty(default=False)
    Scene.subpanel_status_0 = BoolProperty(default=False)
    Scene.subpanel_status_1 = BoolProperty(default=False)
    Scene.subpanel_status_2 = BoolProperty(default=False)
    Scene.subpanel_effects_wraith = BoolProperty(default=False)
    Scene.subpanel_effects_wraith_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_gibby = BoolProperty(default=False)
    Scene.subpanel_effects_gibby_prop1 = BoolProperty(default=False)    
    Scene.subpanel_effects_mirage = BoolProperty(default=False)
    Scene.subpanel_effects_mirage_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_valkyrie = BoolProperty(default=False)
    Scene.subpanel_effects_valkyrie_prop1 = BoolProperty(default=False)    
    Scene.subpanel_effects_weapons = BoolProperty(default=False)
    Scene.subpanel_effects_weapons_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_badges = BoolProperty(default=False)
    Scene.subpanel_effects_loot = BoolProperty(default=False)
    Scene.subpanel_effects_loot_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_loot_prop2 = BoolProperty(default=False)    


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.my_prefs
    del Scene.subpanel_readme
    del Scene.subpanel_status_0
    del Scene.subpanel_status_1
    del Scene.subpanel_status_2
    del Scene.subpanel_effects_wraith
    del Scene.subpanel_effects_wraith_prop1
    del Scene.subpanel_effects_gibby
    del Scene.subpanel_effects_gibby_prop1    
    del Scene.subpanel_effects_mirage
    del Scene.subpanel_effects_mirage_prop1
    del Scene.subpanel_effects_valkyrie
    del Scene.subpanel_effects_valkyrie_prop1    
    del Scene.subpanel_effects_weapons
    del Scene.subpanel_effects_weapons_prop1
    del Scene.subpanel_effects_badges
    del Scene.subpanel_effects_loot
    del Scene.subpanel_effects_loot_prop1
    del Scene.subpanel_effects_loot_prop2    
        

if __name__ == "__main__":
    register()