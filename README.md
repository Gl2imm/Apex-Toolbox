# Apex-Toolbox
Small tool for Blender artists working with Apex Legends models

                                            ####################################			
                                                       Apex Toolbox
                                            ####################################

Hi All. This tool were created to assist and simplify workflow for Apex Legends models in Blender. Here i collect and organize useful tools/addons/operations all in one place.



                                            ####################################			
                                                     USAGE INSTRUCTIONS:
                                            ####################################

1. Most of the tools in the Addon are designed and scaled to Apex models actual size. To size up the model to the correct scale you may do the following:
	a) Import Model
	b) Select bones
	c) Scale down to - 0.0254 (Shortcut for Scale is "S")
	Without correct scale some of the effects will look small/big, colors or textures might be offset too. 
2. Mods/effects/addons added inside are free to use/modify or were created by me/community for this Addon



                                            ####################################			
                                                      Help and Credits:
                                            ####################################
											
											
####################################			
        Auto_tex:
####################################
 
A little tool that will help you to texture Apex Models automatically. A small improvement being done to this addon. Previously if you select the objects and use the addon - it will Append "Apex Shader" and un-select all objects. Well, not anymore. :)

Credits: Addon Created by llenoco. There is no link to the github, as the Addon were posted in Legion Discord https://discord.gg/ADek6fxVGe



####################################			
        Re-color:
####################################

Tool to re-color (re-texture) the model with the new or updated texture available in the game files. This is modified version of Auto_tex. Most of the code is same with small changes here and there.

Howto:
		a) Extract/Download new textures (it must have texture folders inside with endings like "_body", "_jumpkit", etc.)
		b) Place new textures in the existing model "_image" folder
		eg: Wraith have model with folder name "pilot_light_wraith_legendary_01" and the texture folder downloaded named "wraith_lgnd_v19_liberator_rc01"
			place "wraith_lgnd_v19_liberator_rc01" folder inside "/pilot_light_wraith_legendary_01/_images/" folder
		c) copy the name of the new textures folder (eg:"wraith_lgnd_v19_liberator_rc01") and place it in the addon field
		d) select the shader that you like
		e) press Re-texture
To be done: Figure out the way for user to specify custom directory for textures



####################################			
     Append Shaders and HDRI:
####################################

Shaders: A tool to Append shaders to your scene or set HDRI for renders.
Credits: Apex Shader - taken from Apex Auto_tex. S/G Blender, 
		 Apex Cycles (Blue) - taken from the open sources.

HDRI: A tool to Append and set HDRI for renders.
Credits: Party crasher - Thx to @Space for sharing this HDRI on "3D Art Discord" https://discord.gg/VcZh5rC



                                            ####################################			
                                                        Apex Effects:
                                            ####################################


####################################			
             Wraith:
####################################

Portal - spawns the portal made procedurally with nodes. Currently it is animated within 60 frames.
To be done: If someone can modify it to endless cycle - pls share it in Legion Discord in #3D-shenanigans. I will be glad to update the shader and keep your credits.
Credits: Inspired from this video https://www.youtube.com/watch?v=sMFYCJUix-Y, some nodes were taken from there and modified.
![Wraith Portal](https://i.ibb.co/SmKQT59/Apex-toolbox-2.png)


####################################			
             Mirage:
####################################

Decoy - applying outline to the model. Adding endless animated particle system, Decoy text, Floor with bloom and Icon that pop up when enemy shoot Decoy.
		Can be parented to Legend.
Howto: Do not select eyes or other internal meshes, as it will add outline to it too. Adding floor bloom (currently works on flat surfaces). Select Bone object to parent effect to it. Best to parent before adding animation to the model.

Credits: This mod was inspired by Outline Helper - https://felineentity.gumroad.com/l/ZmTIT. Partial pieces of code were taken from there and modified according to the needs.
![Mirage Decoy](https://i.ibb.co/K6vLcgV/Apex-toolbox-3.png)


####################################			
             Weapons:
####################################

Flatline - Reactive skin flames and bloom from Assimilation skin model. Can parent to model.
Howto: Auto Parenting works only for the correct flatline model "flatline_v20_assim". Best to parent before adding animation to the model.
![Flatline - Reactive skin](https://i.ibb.co/sqV3fTh/Apex-toolbox-4.png)


####################################			
             Badges:
####################################

4k Badge - adding in-game 4000 Damage badge made in 3D
20 Bomb Badge - adding in-game 20 Kills badge made in 3D
Credits: Thx to PeeT for sharing this cool model in Legion Discord.
![Badges](https://i.ibb.co/GkZnrGj/Apex-toolbox-5.png)
