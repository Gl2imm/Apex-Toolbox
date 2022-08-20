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
    "version": (2, 1),
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

ver = 2.1
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
    #my_path = ("E:\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_toolbox")
    #ast_fldr = ("E:\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_Toolbox_Assets\\")
    #rec_folder = ("E:\\G-Drive\\Blender\\Apex\\models\\0. Guns\\flatline_v20_assim_w\\Materials\\flatline_react_v20_assim_rt01_main\\") #recolour folder
    #rec_folder = ("E:\\G-Drive\\Blender\\Apex\\models\\Wraith\\Materials\\wraith_lgnd_v19_liberator_rc01\\") #recolour folder
    
    
    my_path = ("D:\\Personal\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_toolbox")    
    ast_fldr = ("D:\\Personal\\G-Drive\\Blender\\0. Setups\\Apex\\Apex_toolbox\\Apex_Toolbox_Assets\\")
    #rec_folder = ("D:\Personal\G-Drive\Blender\Apex\models\Wraith\Materials\wraith_lgnd_v19_liberator_rc01\\") #recolour folder
    #rec_folder = ("D:\\Personal\\G-Drive\\Blender\\Apex\\models\Wraith\\pilot_light_wraith_legendary_01\\_images\\") #recolour folder
    rec_folder = ("D:\\Personal\\G-Drive\\Blender\\Apex\\models\\0. Guns\\flatline_v20_assim_w\\Materials\\flatline_react_v20_assim_rt01_main\\") #recolour folder
else:
    my_path = (os.path.dirname(os.path.realpath(__file__)))


all_loot_items = {
    '0': 'White Armor',
    '1': 'Blue Armor',
    '2': 'Purple Armor',
    '3': 'Gold Armor',
    '4': 'Red Armor',
    '5': 'White Helmet',
    '6': 'Blue Helmet',
    '7': 'Purple Helmet',
    '8': 'Gold Helmet',
    '9': 'Red Helmet',
    '10': 'Phoenix Kit',
    '11': 'Shield Battery',
    '12': 'Shield Cell',
    '13': 'Med Kit',
    '14': 'Syringe',
    '15': 'Health Injector',
    '16': 'Grenade',
    '17': 'Arc Star',
    '18': 'Thermite',
    '19': 'Backpack Lv.4',
    '20': 'Backpack Lv.3',
    '21': 'Backpack Lv.2',
    '22': 'Backpack Lv.1',
    '23': 'Light Ammo',
    '24': 'Heavy Ammo',
    '25': 'Energy Ammo',
    '26': 'Shotgun Ammo',
    '27': 'Respawn Beacon',
    '28': 'Knockdown Shield',
    '29': 'Heat Shield',
    '30': 'Death Box',
    }
            

### add +1 to item end range ###
armor_range = (0,5)
helmet_range = (5,10)    
meds_range = (10,16)
nades_range = (16,19)
bag_range = (19,23)
ammo_range = (23,27)
other_range = (27,31)

all_seer_items = {
    '0': 'Seer Ultimate',
    }
    
all_skydive_items = {
    '0': 'Skydive Ranked S9 Diamond',
    '1': 'Skydive Ranked S9 Master',
    '2': 'Skydive Ranked S9 Predator',
    }         
    
    
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
        asset_folder = ast_fldr
        
 
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
                 ('OP2', "Apex Lobby", ""),
                 ('OP3', "Party Crasher", ""),
                 ('OP4', "Encore", ""),
                 ('OP5', "Habitat", ""),
                 ('OP6', "Kings Canyon (Old)", ""),
                 ('OP7', "Kings Canyon (New)", ""),
                 ('OP8', "Kings Canyon (Night)", ""),
                 ('OP9', "Olympus", ""),
                 ('OP10', "Phase Runner", ""),
                 ('OP11', "Storm Point", ""),
                 ('OP12', "Worlds Edge", ""),
                 ('OP13', "Sky", ""),     
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
    

############   AUTOTEX   ##############    
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
        

    
############   RECOLOR   ##############     
class BUTTON_CUSTOM2(bpy.types.Operator):
    bl_label = "BUTTON CUSTOM2"
    bl_idname = "object.button_custom2"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        rec_alpha = prefs.rec_alpha
        texSets = [['albedoTexture'],['specTexture'],['emissiveTexture'],['scatterThicknessTexture'],['opacityMultiplyTexture'],['normalTexture'],['glossTexture'],['aoTexture'],['cavityTexture']]
        ttf_texSets = [['col'],['spc'],['ilm'],['nml'],['gls'],['ao']]
        
        if mode == 0:
            recolor_folder = rec_folder
        else:
            recolor_folder = prefs.recolor_folder
            
            
        ######## Check if Asset Folder installed ######## 
        if mode == 0:
            asset_folder_set = ast_fldr
        else:
            asset_folder_set =bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder
        assets_set = 0
        if os.path.exists(asset_folder_set) == True:
            asset_folder_set = asset_folder_set.split("\\")[-2]
            if asset_folder_set == "Apex_Toolbox_Assets":
                if mode == 0:
                    asset_folder_set = ast_fldr
                else:
                    asset_folder_set =bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder
                assets_set = 1            
        
        print("asset_folder_set: " + asset_folder_set)       
        
        body_parts = [
                "head",
                "helmet",
                "hair",
                "eye",
                "eyecornea",
                "eyeshadow",
                "teeth",
                "body",
                "v_arms",
                "boots",
                "gauntlet",
                "jumpkit",
                "gear"
                ]    
            
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


    ########## OPTION - 2 (S/G-Blender) ############
        if prefs.cust_enum == 'OP2':
            print("\n######## RECOLORING MODEL: ########")
            if bpy.data.node_groups.get('S/G-Blender') == None:
                selection = [obj.name for obj in bpy.context.selected_objects]
                bpy.ops.wm.append(directory =my_path + blend_file + ap_node, filename ='S/G-Blender')
                for x in range(len(selection)):
                    bpy.data.objects[selection[x]].select_set(True)
                    x += 1
                print("S/G Blender Shader")
                
                
        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                for mSlot in o.material_slots:
                    MatNodeTree = bpy.data.materials[mSlot.name] #mSlot.name material name
                    
                    mSlot_clean = mSlot.name
                    if "." in mSlot.name:
                        mSlot_clean = mSlot.name.split(".")[0] 

                    #rec_folder2 = ("D:\Personal\G-Drive\Blender\Apex\models\Wraith\Materials\wraith_lgnd_v19_liberator_rc01\\") #recolour folder
                    #rec_folder2 = ("D:\\Personal\\G-Drive\\Blender\\Apex\\models\Wraith\\pilot_light_wraith_legendary_01\\_images\\") #recolour folder
                    #rec_folder2 = ("C:\\Users\\User\\Downloads\\pilots\\materials\\") #TTF2 recolour folder
                    #rec_folder2 = ("D:\\Personal\\G-Drive\\Blender\\Apex\\models\\Wraith\\pov_pilot_light_wraith_legendary_01\\_images\\") #POV recolour folder
                    #rec_folder2 = ("D:\\Personal\\G-Drive\\Blender\\Apex\\models\\0. Guns\\flatline_v20_assim_w\\Materials\\flatline_react_v20_assim_rt01_main\\") #recolour folder
                    #rec_folder2 = ("D:\\Personal\\G-Drive\\Blender\\Apex\\models\\0. Guns\\flatline_v20_assim_w\\_images\\") #recolour folder
                    #recolor_folder = rec_folder2

                    try: 
                        foldername = recolor_folder.split("\\")[-2] #folder name
                    except:
                        print("Materials Folder not selected")
                    else:    
                        foldernameSplit = foldername.split("_")[-1] #folder suffix _main _body to check forattachments
                        folderpath = recolor_folder 
                        imgBodyPart = mSlot_clean.split('_')[-1] #part name 
                        try:
                            ttf = mSlot_clean.split('_')[-2]  #ttf2 models
                        except:
                            continue
                        exist = 0                            
                        weapon = 1
                        
                        for b in range(len(body_parts)):
                            if body_parts[b] in mSlot_clean:
                                weapon = 0
                                break    
                                                                                    
                        ######## Weapon Codes ########
                        if weapon == 1:
                            if foldername == "_images": #normal autotex
                                foldername = mSlot_clean
                                
                            if foldernameSplit != imgBodyPart: #check if this is attachment
                                foldername = mSlot_clean
                        
                        ######## Legend Codes ########    
                        if weapon == 0:
                            if foldername == "_images":              #normal autotex
                                foldername = mSlot_clean  
                            else:                                    #with sub folders
                                if body_parts[b] == "v_arms":        #with sub folders and check for v_arms in name
                                    folderpath = recolor_folder + foldername + "_" + body_parts[b]
                                    foldername = foldername + "_" + body_parts[b]  
                                else: 
                                    folderpath = recolor_folder + foldername + "_" + imgBodyPart
                                    foldername = foldername + "_" + imgBodyPart                                     
                                    if ttf == "skn":   #TTF Texturing
                                        folderpath = recolor_folder + mSlot_clean
                                        foldername = mSlot_clean
                                        texSets = ttf_texSets
           
                        
                        texFile = folderpath + '\\' + foldername + '_' + texSets[0][0] + ".png" #check if albedo image exist, if not dont proceed clear nodes
                        
                        if os.path.isfile(texFile):
                            exist = 1
                        else:
                            if weapon == 0:
                                if assets_set == 1:
                                    texFile = asset_folder_set + "0. Legend_base" + '\\' + mSlot_clean + '_' + texSets[0][0] + ".png" #Set path for Base files from assets folder
                                else:
                                    texFile = recolor_folder + "base" + '\\' + mSlot_clean + '_' + texSets[0][0] + ".png" #check legend base files in the "Base" folder
                                if os.path.isfile(texFile):
                                    if assets_set == 1:
                                        folderpath = asset_folder_set + "0. Legend_base"
                                        foldername = mSlot_clean                                        
                                    else:
                                        folderpath = recolor_folder + "base"
                                        foldername = mSlot_clean
                                    exist = 1
                                if ttf == "skn":                                #TTF Try look different skin folders
                                    skn_name = mSlot_clean.rsplit('_', 2)[0]
                                    for s in ("_skn_02", "_skn_31"):
                                        texFile = recolor_folder + skn_name + s + '\\' + skn_name + s + '_' + texSets[0][0] + ".png" #Set path for Base files from assets folder
                                        if os.path.isfile(texFile):
                                            print(texFile)
                                            folderpath = recolor_folder + skn_name + s
                                            foldername = skn_name + s
                                            exist = 1
                                            break
                                        
                        if exist == 1: 
                            MatNodeTree.node_tree.nodes.clear()
                            
                            for i in range(len(texSets)):
                                for j in range(len(texSets[i])):
                                    texFile = folderpath + '\\' + foldername + '_' + texSets[i][j] + ".png"
                                    if os.path.isfile(texFile):                         #if texture is absent - skip it
                                        texImage = bpy.data.images.load(texFile)
                                    else:
                                        print(foldername + '_' + texSets[i][j] + ".png" + " Not in folder. Skipping.")
                                        texImage = None
                                    if texImage:
                                        if i > 2:
                                            texImage.colorspace_settings.name = 'Non-Color'
                                        texImage.alpha_mode = 'CHANNEL_PACKED'
                                        texNode = MatNodeTree.node_tree.nodes.new('ShaderNodeTexImage')
                                        texNode.image = texImage
                                        texNode.name = str(i)
                                        texNode.location = (-50,50-260*i)
                                        break 
                                    
                            ########## OPTION - 1 (Apex Shader) ############        
                            if prefs.cust_enum == 'OP1':        
                                NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                                NodeGroup.node_tree = bpy.data.node_groups.get('Apex Shader')
                                NodeGroup.location = (300,0)
                                NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                                NodeOutput.location = (500,0)
                                MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])
                                
                                if ttf == "skn":
                                    ColorDict = {
                                        "0": "Albedo Map",
                                        "1": "Specular Map",
                                        "2": "Emission",
                                        "3": "Normal Map",
                                        "4": "Glossiness Map",     
                                        "5": "AO"
                                    }                                    
                                else:
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
                                
                            ########## OPTION - 2 (S/G-Blender) ############
                            if prefs.cust_enum == 'OP2': 
                                NodeGroup = MatNodeTree.node_tree.nodes.new('ShaderNodeGroup')
                                NodeGroup.node_tree = bpy.data.node_groups.get('S/G-Blender')
                                NodeGroup.location = (300,0)
                                NodeOutput = MatNodeTree.node_tree.nodes.new('ShaderNodeOutputMaterial')
                                NodeOutput.location = (500,0)
                                MatNodeTree.node_tree.links.new(NodeOutput.inputs[0], NodeGroup.outputs[0])
                                
                                if ttf == "skn":
                                    ColorDict = {
                                        "0": "Diffuse map",
                                        "1": "Specular map",
                                        "2": "Emission input",
                                        "3": "Normal map",
                                        "4": "Glossiness map",     
                                        "5": "AO map"
                                    }                                    
                                else:
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
                            print("Textured",mSlot_clean) 
                            print("  ")                               

                        else:
                            print("Material '" + mSlot_clean + "' Cannot be Textured") 
                            print("Image '" + foldername + '_' + texSets[0][0] + ".png' Not found in '" + folderpath + "'")
                            print("######### LOG FOR DEBUGGING #########")
                            print("recolor_folder: " + recolor_folder)
                            print("mSlot_clean: " + mSlot_clean)
                            print("foldername: " + foldername)
                            print("foldernameSplit: " + foldernameSplit)
                            print("imgBodyPart: " + imgBodyPart)
                            print("ttf: " + ttf)
                            print("texFile: " + texFile)
                            print("  ")  

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
            asset_folder = ast_fldr
        else:
            asset_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder
 
 
        if prefs.cust_enum_hdri == 'OP1':
            hdri_name = "World"                    

        if prefs.cust_enum_hdri == 'OP2':
            hdri_name = "Apex Lobby HDRI" 
                    
        if prefs.cust_enum_hdri == 'OP3':
            hdri_name = "Party crasher HDRI"
            
        if prefs.cust_enum_hdri == 'OP4':
            hdri_name = "Encore HDRI"
            
        if prefs.cust_enum_hdri == 'OP5':
            hdri_name = "Habitat HDRI"
            
        if prefs.cust_enum_hdri == 'OP6':
            hdri_name = "Kings Canyon HDRI"
            
        if prefs.cust_enum_hdri == 'OP7':
            hdri_name = "Kings Canyon New HDRI"
            
        if prefs.cust_enum_hdri == 'OP8':
            hdri_name = "Kings Canyon Night HDRI"                        
            
        if prefs.cust_enum_hdri == 'OP9':
            hdri_name = "Olympus HDRI"
            
        if prefs.cust_enum_hdri == 'OP10':
            hdri_name = "Phase Runner HDRI"
            
        if prefs.cust_enum_hdri == 'OP11':
            hdri_name = "Storm Point HDRI"
            
        if prefs.cust_enum_hdri == 'OP12':
            hdri_name = "Worlds Edge HDRI" 
            
        if prefs.cust_enum_hdri == 'OP13':
            hdri_name = "Sky HDRI"                  
            

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
            asset_folder = ast_fldr
        else:
            asset_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder

                
        if bpy.data.objects.get(self.badge) == None:
            bpy.ops.wm.append(directory =asset_folder + blend_file + ap_object, filename =self.badge)
            print(self.badge + " Appended")
        else:
            print(self.badge + " already inside")
  
        return {'FINISHED'} 
    
    
######### Legends Effects Seer ###########    
class SEER_BUTTON_SPAWN(bpy.types.Operator):
    bl_label = "SEER_BUTTON_SPAWN"
    bl_idname = "object.seer_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    lgnd_effect : bpy.props.StringProperty(name= "Added")


    def execute(self, context):
        lgnd_effect = self.lgnd_effect
        
        lgnd_effect_items = {
            'Seer Ultimate': [
                {'name': 'Seer Ultimate'},            
            ],
            }  

        #### Main loop for Seer items ####    
        for i in range(len(all_seer_items)):
            item = all_seer_items.get(str(i))
            split_item = item.split()

            if lgnd_effect == all_seer_items.get(str(i)):
                
                ### Ultimate ###
                if i == 0:
                    bpy.ops.wm.append(directory =my_path + blend_file + ap_object, files=lgnd_effect_items.get(item))
                    
                print(item + " Appended") 
                break
            
        
        return {'FINISHED'}                       


######### Skydive Effects ###########    
class SKY_BUTTON_SPAWN(bpy.types.Operator):
    bl_label = "SKY_BUTTON_SPAWN"
    bl_idname = "object.sky_button_spawn"
    bl_options = {'REGISTER', 'UNDO'}
    sky_effect : bpy.props.StringProperty(name= "Added")


    def execute(self, context):
        sky_effect = self.sky_effect
        
        sky_effect_items = {
            'Skydive Ranked S9': [
                {'name': 'Skydive Ranked S9'}, 
                {'name': 'Skydive Ranked S9 trails'},           
            ],
            } 

        
        # Skydive Parenting #
        if sky_effect == "Skydive_parent":
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
                            if bpy.data.objects.get('Skydive Ranked S9') == None:
                                print("Skydive not Found. Pls add Effect first")
                            else:
                                #Deselect All and select only bones that were chosen
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.select_all(action='DESELECT')
                                bpy.context.view_layer.objects.active = None
                                bpy.data.objects[sel_names[0]].select_set(True)
                                bpy.context.view_layer.objects.active = bpy.data.objects[sel_names[0]]
                                
                                #Select POV bone in Bone Edit Mode       
                                arm = bpy.data.objects[sel_names[0]]
                                bpy.ops.object.mode_set(mode='EDIT')
                                arm.data.edit_bones['jx_c_pov'].select = True  
                                
                                #Exit out Edit Mode and Deselect All    
                                bpy.ops.object.mode_set(mode='OBJECT')
                                bpy.ops.object.select_all(action='DESELECT')
                                
                                #Select Skydive, Select bones that were chosen, set bones active and parent to them
                                bpy.data.objects['Skydive Ranked S9'].select_set(True)
                                bpy.data.objects[sel_names[0]].select_set(True)
                                bpy.context.view_layer.objects.active = bpy.data.objects[sel_names[0]]
                                bpy.ops.object.parent_set(type='BONE')

                                bpy.ops.object.select_all(action='DESELECT')                                                              
                                                                
                                print("Parenting Skydive Done")
                        else:
                            print("Selected Object is Not a Bone. Pls Select Bones") 
        else:
            def color():
                selection = [obj.name for obj in bpy.context.selected_objects]
                for obj in bpy.context.selected_objects:
                    obj.select_set(False)
                bpy.data.objects[selection[0]].select_set(True)
                mat = bpy.data.objects[selection[0]].active_material
                nodes = mat.node_tree.nodes['Skydive Group Color S9'].node_tree.nodes
                links = mat.node_tree.nodes['Skydive Group Color S9'].node_tree.links
                node_output = nodes['Group Output']
                colours = {
                    'Diamond': nodes['RGB.001'],
                    'Master': nodes['RGB.002'],
                    'Predator': nodes['RGB.003'],
                    } 
                node_color = colours.get(split_item[1])
                link = links.new(node_color.outputs[0], node_output.inputs[0])
                
                                
            #### Main loop for Skydive items ####    
            for i in range(len(all_skydive_items)):
                item = all_skydive_items.get(str(i))
                split_item = item.rsplit(" ",1)

                if sky_effect == all_skydive_items.get(str(i)):
                     ### Ranked S9 ###
                    bpy.ops.wm.append(directory =my_path + blend_file + ap_object, files=sky_effect_items.get(split_item[0]))
                    color()
                        
                    print(item + " Appended")             
            
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
        
        blend_file = ("\\Assets.blend") #items shifted to assets
        
        #### this one for test purposes ####
        if mode == 0:
            asset_folder = ast_fldr
        else:    
            asset_folder = bpy.context.preferences.addons['Apex_toolbox'].preferences.asset_folder


        loot_items = {
            'Armor': [
                {'name': 'w_loot_cha_shield_upgrade_body_LOD0_skel'},            
                {'name': 'w_loot_cha_shield_upgrade_body_LOD0_SEModelMesh.106'}, 
                {'name': 'w_loot_cha_shield_upgrade_body_LOD0_SEModelMesh.107'}
            ],
            'Helmet': [
                {'name': 'w_loot_cha_shield_upgrade_head_LOD0_skel'}, 
                {'name': 'w_loot_cha_shield_upgrade_head_LOD0_SEModelMesh.108'}, 
                {'name': 'w_loot_cha_shield_upgrade_head_LOD0_SEModelMesh.109'}
            ],
            'Phoenix Kit': [
                {'name': 'w_loot_wep_iso_phoenix_kit_v1_LOD0_skel'}, 
                {'name': 'w_loot_wep_iso_phoenix_kit_v1_LOD0_SEModelMesh.135'}, 
                {'name': 'w_loot_wep_iso_phoenix_kit_v1_LOD0_SEModelMesh.136'}
            ],
            'Shield Battery': [
                {'name': 'w_loot_wep_iso_shield_battery_large_LOD0_skel'}, 
                {'name': 'w_loot_wep_iso_shield_battery_large_LOD0_SEModelMesh.137'}, 
                {'name': 'w_loot_wep_iso_shield_battery_large_LOD0_SEModelMesh.138'}
            ],
            'Shield Cell': [
                {'name': 'w_loot_wep_iso_shield_battery_small_LOD0_skel'}, 
                {'name': 'w_loot_wep_iso_shield_battery_small_LOD0_SEModelMesh.139'}, 
                {'name': 'w_loot_wep_iso_shield_battery_small_LOD0_SEModelMesh.140'}
            ],
            'Med Kit': [
                {'name': 'w_loot_wep_iso_health_main_large_LOD0_skel'}, 
                {'name': 'w_loot_wep_iso_health_main_large_LOD0_SEModelMesh.133'}
            ],
            'Syringe': [
                {'name': 'w_loot_wep_iso_health_main_small_LOD0_skel'}, 
                {'name': 'w_loot_wep_iso_health_main_small_LOD0_SEModelMesh.134'}
            ],
            'Health Injector': [
                {'name': 'w_health_injector_LOD0_skel'}, 
                {'name': 'w_health_injector_LOD0_SEModelMesh.084'}
            ],            
            'Grenade': [
                {'name': 'm20_f_grenade_LOD0_skel'}, 
                {'name': 'm20_f_grenade_LOD0_SEModelMesh.147'}
            ],
            'Arc Star': [
                {'name': 'w_loot_wep_iso_shuriken_LOD0_skel'}, 
                {'name': 'w_loot_wep_iso_shuriken_LOD0_SEModelMesh.142'}
            ],
            'Thermite': [
                {'name': 'w_thermite_grenade_LOD0_skel'}, 
                {'name': 'w_thermite_grenade_LOD0_SEModelMesh.143'}
            ], 
            'Backpack Lv.3': [
                {'name': 'w_loot_char_backpack_heavy_LOD0_skel'}, 
                {'name': 'w_loot_char_backpack_heavy_LOD0_SEModelMesh.118'}
            ],    
            'Backpack Lv.2': [
                {'name': 'w_loot_char_backpack_medium_LOD0_skel'}, 
                {'name': 'w_loot_char_backpack_medium_LOD0_SEModelMesh.120'}
            ],    
            'Backpack Lv.1': [
                {'name': 'w_loot_char_backpack_light_LOD0_skel'}, 
                {'name': 'w_loot_char_backpack_light_LOD0_SEModelMesh.119'}
            ], 
            'Light Ammo': [
                {'name': 'w_loot_wep_ammo_sc_LOD0_skel'}, 
                {'name': 'w_loot_wep_ammo_sc_LOD0_SEModelMesh.123'}
            ], 
            'Heavy Ammo': [
                {'name': 'w_loot_wep_ammo_hc_LOD0_skel'}, 
                {'name': 'w_loot_wep_ammo_hc_LOD0_SEModelMesh.121'}
            ], 
            'Energy Ammo': [
                {'name': 'w_loot_wep_ammo_nrg_LOD0_skel'}, 
                {'name': 'w_loot_wep_ammo_nrg_LOD0_SEModelMesh.122'}
            ],
            'Shotgun Ammo': [
                {'name': 'w_loot_wep_ammo_shg_LOD0_skel'}, 
                {'name': 'w_loot_wep_ammo_shg_LOD0_SEModelMesh.124'}
            ], 
            'Respawn Beacon': [
                {'name': 'beacon_capsule_01_LOD0_skel'}, 
                {'name': 'beacon_capsule_01_LOD0_SEModelMesh.144'}
            ],  
            'Knockdown Shield': [
                {'name': 'w_loot_wep_iso_shield_down_v1_LOD0_skel'}, 
                {'name': 'w_loot_wep_iso_shield_down_v1_LOD0_SEModelMesh.141'}
            ],  
            'Heat Shield': [
                {'name': 'loot_void_ring_LOD0_skel'}, 
                {'name': 'loot_void_ring_LOD0_SEModelMesh.146'}
            ],  
            'Death Box': [
                {'name': 'death_box_01_gladcard_LOD0_skel.001'}, 
                {'name': 'death_box_01_gladcard_LOD0_SEModelMesh.145'}
            ],                                                                                                                                                                       
            }  

            
        def armor_color():
            selection = [obj.name for obj in bpy.context.selected_objects]
            for obj in bpy.context.selected_objects:
                obj.select_set(False)
            bpy.data.objects[selection[1]].select_set(True)
            mat = bpy.data.objects[selection[1]].active_material
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            node_output = nodes['Armor shader']
            colours = {
                'Blue': nodes['RGB.001'],
                'Purple': nodes['RGB.002'],
                'Gold': nodes['RGB'],
                'Red': nodes['RGB.003'],
                } 
            if split_item[0] == "White":
                pass
            else:
                node_color = colours.get(split_item[0])
                link = links.new(node_color.outputs[0], node_output.inputs[0]) 
                
        
        #### Main loop for Loot items ####    
        for i in range(len(all_loot_items)):
            item = all_loot_items.get(str(i))
            split_item = item.split()

            if loot == all_loot_items.get(str(i)):
                
                ### Body Armor ###
                if i in range(*armor_range):
                    bpy.ops.wm.append(directory =asset_folder + blend_file + ap_object, files=loot_items.get(split_item[1]))
                    armor_color()
                    
                ### Helmet ###                    
                if i in range(*helmet_range):
                    bpy.ops.wm.append(directory =asset_folder + blend_file + ap_object, files=loot_items.get(split_item[1]))
                    armor_color()
                
                ### Meds ###                    
                if i in range(*meds_range):
                    bpy.ops.wm.append(directory =asset_folder + blend_file + ap_object, files=loot_items.get(item))

                ### Nades ###                    
                if i in range(*nades_range):
                    bpy.ops.wm.append(directory =asset_folder + blend_file + ap_object, files=loot_items.get(item))

                ### Ammo ###                    
                if i in range(*ammo_range):
                    bpy.ops.wm.append(directory =asset_folder + blend_file + ap_object, files=loot_items.get(item))

                ### Backpack ###                    
                if i in range(*bag_range):
                    bpy.ops.wm.append(directory =asset_folder + blend_file + ap_object, files=loot_items.get(item))
                  
                ### Backpack ###                    
                if i in range(*other_range):
                    bpy.ops.wm.append(directory =asset_folder + blend_file + ap_object, files=loot_items.get(item))
                                      
                print(item + " Appended") 
                break
            

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
            asset_folder = ast_fldr
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
            asset_folder = ast_fldr
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
            

        ######### Seer #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_seer else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_seer', icon=icon, icon_only=True)
        row.label(text='Seer')
        # some data on the subpanel
        if context.scene.subpanel_effects_seer:
            box = layout.box()
            
            # Wraith subpanel 1
            for n in range(len(all_seer_items)):
                if n == 0:
                    box.operator('object.seer_button_spawn', text = all_seer_items.get(str(n))).lgnd_effect = all_seer_items.get(str(n))            
            #box.operator("object.seer_button_spawn", text = "Seer Ultimate").lgnd_effect = "Seer Ultimate"

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
                    for n in range(len(all_loot_items)):
                        if n in range(*armor_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))
                    
                # Helmet subpanel 2
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop2 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop2', icon=icon, icon_only=False, text='Helmet                                 ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop2:
                     for n in range(len(all_loot_items)):
                        if n in range(*helmet_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n)) 
                    
                # Heals subpanel 3
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop3 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop3', icon=icon, icon_only=False, text='Heals                                    ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop3:
                    for n in range(len(all_loot_items)):
                        if n in range(*meds_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))
                            
                # Nades subpanel 4
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop4 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop4', icon=icon, icon_only=False, text='Nades                                    ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop4:
                    for n in range(len(all_loot_items)):
                        if n in range(*nades_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n)) 
                            
                # Ammo subpanel 5
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop5 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop5', icon=icon, icon_only=False, text='Ammo                                    ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop5:
                    for n in range(len(all_loot_items)):
                        if n in range(*ammo_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))                               
                            
                # Backpacks subpanel 6
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop6 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop6', icon=icon, icon_only=False, text='Backpacks                              ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop6:
                    for n in range(len(all_loot_items)):
                        if n in range(*bag_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))  
                            
                # Others subpanel 7
                icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_loot_prop7 else 'RIGHTARROW'
                box.prop(context.scene, 'subpanel_effects_loot_prop7', icon=icon, icon_only=False, text='Other                                       ')
                # some data on the subpanel
                if context.scene.subpanel_effects_loot_prop7:
                    for n in range(len(all_loot_items)):
                        if n in range(*other_range):
                            box.operator('object.lt_button_spawn', text = all_loot_items.get(str(n))).loot = all_loot_items.get(str(n))                                                                                  
                        


        ######### Skydive #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_effects_sky else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_effects_sky', icon=icon, icon_only=True)
        row.label(text='Skydive (Experimental)')
        # some data on the subpanel
        if context.scene.subpanel_effects_sky:
            box = layout.box()

            for n in range(len(all_skydive_items)):
                split = box.split(factor = 0.08)
                col = split.column(align = True)
                col.label(text='')
                split.operator('object.sky_button_spawn', text = all_skydive_items.get(str(n))).sky_effect = all_skydive_items.get(str(n))
            split = box.split(factor = 0.6)
            col = split.column(align = True)
            col.label(text='')         
            split.operator('object.sky_button_spawn', text = "Parent it").sky_effect = "Skydive_parent" 
            box.label(text='*Sel Model Bones before Parenting') 
            box.label(text='*Parent before import animation')           


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
        SEER_BUTTON_SPAWN,
        SKY_BUTTON_SPAWN, 
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
    Scene.subpanel_effects_seer = BoolProperty(default=False)    
    Scene.subpanel_effects_weapons = BoolProperty(default=False)
    Scene.subpanel_effects_weapons_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_badges = BoolProperty(default=False)
    Scene.subpanel_effects_loot = BoolProperty(default=False)
    Scene.subpanel_effects_loot_prop1 = BoolProperty(default=False)
    Scene.subpanel_effects_loot_prop2 = BoolProperty(default=False)
    Scene.subpanel_effects_loot_prop3 = BoolProperty(default=False) 
    Scene.subpanel_effects_loot_prop4 = BoolProperty(default=False) 
    Scene.subpanel_effects_loot_prop5 = BoolProperty(default=False) 
    Scene.subpanel_effects_loot_prop6 = BoolProperty(default=False)
    Scene.subpanel_effects_loot_prop7 = BoolProperty(default=False)
    Scene.subpanel_effects_sky = BoolProperty(default=False)


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
    del Scene.subpanel_effects_seer    
    del Scene.subpanel_effects_weapons
    del Scene.subpanel_effects_weapons_prop1
    del Scene.subpanel_effects_badges
    del Scene.subpanel_effects_loot
    del Scene.subpanel_effects_loot_prop1
    del Scene.subpanel_effects_loot_prop2
    del Scene.subpanel_effects_loot_prop3 
    del Scene.subpanel_effects_loot_prop4 
    del Scene.subpanel_effects_loot_prop5
    del Scene.subpanel_effects_loot_prop6
    del Scene.subpanel_effects_loot_prop7 
    del Scene.subpanel_effects_sky 
        

if __name__ == "__main__":
    register()
