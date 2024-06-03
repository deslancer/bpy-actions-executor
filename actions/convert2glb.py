import bpy
import os
from mathutils import Quaternion

filepath = bpy.data.filepath
blend_filename = os.path.basename(filepath)
clean_filename = blend_filename.split(".")[0]
directory = os.path.dirname(filepath)
output_dir = os.path.join(directory, "output_gltf")
is_output_exists = os.path.exists(output_dir)
if not is_output_exists:
    os.mkdir(output_dir)
    print('Folder has been created')

bpy.ops.import_scene.gltf(filepath=os.path.join(directory, 'Wheel_01.glb'))

wheel_sides = ["BL", "BR", "FL", "FR"]
wheels_positions = []


def set_wheels():
    wheels_positions.append(bpy.data.objects["BL"].location)
    wheels_positions.append(bpy.data.objects["BR"].location)
    wheels_positions.append(bpy.data.objects["FL"].location)
    wheels_positions.append(bpy.data.objects["FR"].location)

    bpy.data.objects['Wheel_Objects'].select_set(True)
    for index, side in enumerate(wheel_sides):
        bpy.ops.object.duplicate()
        duplicated_obj = bpy.context.object
        duplicated_obj.name = f"{side}_Wheel_Object"
        duplicated_obj.location = wheels_positions[index]

    br_wheel = bpy.data.objects['BR_Wheel_Object']
    fr_wheel = bpy.data.objects['FR_Wheel_Object']
    q_axis = [0.0, 1.0, 0.0, 3.1415]

    q_delta = Quaternion(q_axis)
    q1 = q_delta @ br_wheel.rotation_quaternion
    q2 = q_delta @ fr_wheel.rotation_quaternion
    br_wheel.rotation_quaternion = q1
    fr_wheel.rotation_quaternion = q2


set_wheels()
bpy.ops.export_scene.gltf(filepath=f'{os.path.join(output_dir, clean_filename)}.glb')
