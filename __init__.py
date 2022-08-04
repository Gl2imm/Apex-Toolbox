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
    "version": (1, 1),
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

ver = 1.1
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
    my_path = ("D:\\Personal\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_toolbox")
else:
    my_path = (os.path.dirname(os.path.realpath(__file__)))


    #OPERATOR         
########################################   
class RECOLORSETTINGS(bpy.types.PropertyGroup):
    folder_path: bpy.props.StringProperty(name="Folder",
                                        description="Select Recolor textures folder",
                                        default="",
                                        maxlen=1024,
                                        subtype="DIR_PATH")
  
     
class PROPERTIES_CUSTOM(bpy.types.PropertyGroup):
    
    name : bpy.props.StringProperty(name= "Name", default="folder_name", maxlen=40)
    
    cust_enum : bpy.props.EnumProperty(
        name = "Shader",
        description = "Shader for recolor",
        default='OP1',
        items = [('OP1', "Apex Shader", ""),
                 ('OP2', "S/G-Blender", "")    
                ]
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
                 ('OP3', "Coming soon", "")     
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
        return {'FINISHED'}
        

    
    
class BUTTON_CUSTOM2(bpy.types.Operator):
    bl_label = "BUTTON CUSTOM2"
    bl_idname = "object.button_custom2"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
           
    ########## OPTION - 1 (Apex Shader) ############
        if prefs.cust_enum == 'OP1':
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
                        imageBodyPart = imageNode.image.name.split(".")[0].split('_')[-2]
                        imageName = MatNodeTree.name
                        imageFormat = image.split('.')[1]
                                
                        if not any(imageType in x for x in texSets):
                            print(image,"could not be mapped.")        
                            continue
                        
                       
                        MatNodeTree.node_tree.nodes.clear()
     
                        for i in range(len(texSets)):
                            for j in range(len(texSets[i])):
                                if imageName == "wraith_base_eye" or imageName == "teeth" or imageName == "wraith_base_eyecornea" or imageName == "wraith_base_eyeshadow" or imageName == "wraith_base_hair":
                                    texImageName = imageName + '_' + texSets[i][j] + '.' + imageFormat
                                    texImage = bpy.data.images.get(texImageName)
                                    texFile = imagepath + '\\' + texImageName
                                else:
                                    texImageName = prefs.name + '_' + imageBodyPart + '_' + texSets[i][j] + '.' + imageFormat
                                    texImage = bpy.data.images.get(texImageName)
                                    texFile = imagepath + '\\' + prefs.name + '\\' + prefs.name + '_' + imageBodyPart + '\\' + texImageName
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

                            if i == 1:
                                NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                                NodeGroup.node_tree = bpy.data.node_groups.get('Apex Shader')
                                NodeGroup.location = (300,0)
                                NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                                NodeOutput.location = (500,0)
                                MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])
                            
                            #print(NodeGroup.node_tree) Apex Shader
                            #print(NodeOutput) Material Output
                            
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

    
    ########## OPTION - 2 (S/G-Blender) ############
        if prefs.cust_enum == 'OP2':
            if bpy.data.node_groups.get('S/G-Blender') == None:
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
                        imageBodyPart = imageNode.image.name.split(".")[0].split('_')[-2]
                        imageName = MatNodeTree.name
                        imageFormat = image.split('.')[1]
                                
                        if not any(imageType in x for x in texSets):
                            print(image,"could not be mapped.")        
                            continue
                        
                       
                        MatNodeTree.node_tree.nodes.clear()
                                
                        for i in range(len(texSets)):
                            for j in range(len(texSets[i])):
                                if imageName == "wraith_base_eye" or imageName == "teeth" or imageName == "wraith_base_eyecornea" or imageName == "wraith_base_eyeshadow" or imageName == "wraith_base_hair":
                                    texImageName = imageName + '_' + texSets[i][j] + '.' + imageFormat
                                    texImage = bpy.data.images.get(texImageName)
                                    texFile = imagepath + '\\' + texImageName
                                else:
                                    texImageName = prefs.name + '_' + imageBodyPart + '_' + texSets[i][j] + '.' + imageFormat
                                    texImage = bpy.data.images.get(texImageName)
                                    texFile = imagepath + '\\' + prefs.name + '\\' + prefs.name + '_' + imageBodyPart + '\\' + texImageName
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

                            if i == 1:
                                NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                                NodeGroup.node_tree = bpy.data.node_groups.get('S/G-Blender')
                                NodeGroup.location = (300,0)
                                NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                                NodeOutput.location = (500,0)
                                MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])
                            
                            #print(NodeGroup.node_tree) Apex Shader
                            #print(NodeOutput) Material Output
                            
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
    
    
    
class BUTTON_HDRI(bpy.types.Operator):
    bl_label = "BUTTON_HDRI"
    bl_idname = "object.button_hdri"
    bl_options = {'REGISTER', 'UNDO'}
    


    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        
        if prefs.cust_enum_hdri == 'OP1':
            if bpy.context.scene.world != "World":
                blender_default = bpy.data.worlds['World']
                scene.world = blender_default
                print("Blender Default World has been applied")
                    
        
        if prefs.cust_enum_hdri == 'OP2':
            if 'Party crasher HDRI' not in bpy.data.worlds:
                bpy.ops.wm.append(directory =my_path + blend_file + ap_world, filename ='Party crasher HDRI')
                party_crasher = bpy.data.worlds['Party crasher HDRI']
                scene.world = party_crasher
                print("Party crasher HDRI has been Appended and applied to the World")
            else:
                if bpy.context.scene.world != "Party crasher HDRI":
                    party_crasher = bpy.data.worlds['Party crasher HDRI']
                    scene.world = party_crasher
                    print("Party crasher HDRI is already inside and it's been applied to the World")

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
                


######### Badge Buttons ###########    
class BDG_BUTTON_SPAWN(bpy.types.Operator):
    bl_label = "BDG_BUTTON_SPAWN"
    bl_idname = "object.bdg_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    badge : bpy.props.StringProperty(name= "Added")


    def execute(self, context):
        if bpy.data.objects.get(self.badge) == None:
            bpy.ops.wm.append(directory =my_path + blend_file + ap_object, filename =self.badge)
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
                
        
        
        ######### Readme First ###########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_readme else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_readme', icon=icon, icon_only=True)
        row.label(text = "Readme First", icon= "ERROR")
        # some data on the subpanel
        if context.scene.subpanel_readme:
            box = layout.box()
            box.label(text = "All Credits, Help and Instructions")
            box.label(text = "inside this addon .zip file")
            row = layout.row()
            row.label(text = "------------------------------------------------------")



        ######### Auto_tex ###########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_status_0 else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_status_0', icon=icon, icon_only=True)
        row.label(text = "Auto_tex (by llenoco)", icon= "TEXTURE")
        # some data on the subpanel
        if context.scene.subpanel_status_0:
            box = layout.box()
            box.operator("object.button_custom", text = "Texture Model")
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
            box.label(text = "Put texture folder in '_images'")
            box.label(text = "Paste folder name below")
            
            #Folder Name
            row = layout.row()
            layout.prop(prefs, "name")
            ######### Filepath ###########
            #row = layout.row()
            #row.prop(recolor_settings, "folder_path")
            
            
            #Shader Select
            row = layout.row()
            layout.prop(prefs, "cust_enum")
            #ADD Button2
            row = layout.row()
            row.operator("object.button_custom2", text = "Re-texture Model")
            row = layout.row()
            row.label(text = "------------------------------------------------------")
            
        
        ######### Append Shader ###########
        # subpanel
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_status_2 else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_status_2', icon=icon, icon_only=True)
        row.label(text = "Append Shaders & HDRI", icon= "NODE_MATERIAL")
        # some data on the subpanel
        if context.scene.subpanel_status_2:
            box = layout.box()

            box.prop(prefs, 'cust_enum_shader')
            split = box.split(factor = 0.6)
            col = split.column(align = True)
            split.operator("object.button_shaders", text = "Add Shader")

            box.prop(prefs, 'cust_enum_hdri')
            split = box.split(factor = 0.6)
            col = split.column(align = True)
            split.operator("object.button_hdri", text = "Set HDRI") 
            
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
                            
            


        ######### Badges #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_badges else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_badges', icon=icon, icon_only=True)
        row.label(text='Badges')
        # some data on the subpanel
        if context.scene.subpanel_effects_badges:
            box = layout.box()
            # Badges
            box.operator('object.bdg_button_spawn', text = "4K Badge (3D)").badge = "Badge - 4k Damage"
            box.operator('object.bdg_button_spawn', text = "20 Bomb Badge (3D)").badge = "Badge - 20 Bombs"



    #CLASS REGISTER 
##########################################
classes = (RECOLORSETTINGS, PROPERTIES_CUSTOM, BUTTON_CUSTOM, BUTTON_CUSTOM2, BUTTON_SHADERS, BUTTON_HDRI, WR_BUTTON_PORTAL, MR_BUTTON_DECOY, AUTOTEX_MENU, EFFECTS_PT_panel, BDG_BUTTON_SPAWN, WPN_BUTTON_SPAWN)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.my_prefs = bpy.props.PointerProperty(type= PROPERTIES_CUSTOM)
    bpy.types.Scene.recolor_settings = bpy.props.PointerProperty(type=RECOLORSETTINGS)
    Scene.subpanel_readme = BoolProperty(default=False)
    Scene.subpanel_status_0 = BoolProperty(default=False)
    Scene.subpanel_status_1 = BoolProperty(default=False)
    Scene.subpanel_status_2 = BoolProperty(default=False)
    Scene.subpanel_effects_wraith = BoolProperty(default=False)
    Scene.subpanel_effects_wraith_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_mirage = BoolProperty(default=False)
    Scene.subpanel_effects_mirage_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_weapons = BoolProperty(default=False)
    Scene.subpanel_effects_weapons_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_badges = BoolProperty(default=False)
    
    


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.my_prefs
    del bpy.types.Scene.recolor_settings
    del Scene.subpanel_readme
    del Scene.subpanel_status_0
    del Scene.subpanel_status_1
    del Scene.subpanel_status_2
    del Scene.subpanel_effects_wraith
    del Scene.subpanel_effects_wraith_prop1
    del Scene.subpanel_effects_mirage
    del Scene.subpanel_effects_mirage_prop1
    del Scene.subpanel_effects_weapons
    del Scene.subpanel_effects_weapons_prop1
    del Scene.subpanel_effects_badges
    


if __name__ == "__main__":
    register()