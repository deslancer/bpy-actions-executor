import json

import bpy
import os

filepath = bpy.data.filepath
blend_filename = os.path.basename(filepath)
clean_filename = blend_filename.split(".")[0]
directory = os.path.dirname(filepath)
out_textures_dir = os.path.join(directory, "textures")
out_json_dir = os.path.join(directory, "structs")
is_output_exists = os.path.exists(out_textures_dir)
is_json_exists = os.path.exists(out_json_dir)
if not is_output_exists:
    os.mkdir(out_textures_dir)
    print('Folder has been created')

if not is_json_exists:
    os.mkdir(out_json_dir)
    print('Folder has been created')

hierarchy = {
    clean_filename: []
}

for ob in bpy.data.objects:
    if ob.type == "MESH":
        for mat_slot in ob.material_slots:
            if mat_slot.material:
                nodes = mat_slot.material.node_tree.nodes
                for n in nodes:
                    if n.type == 'TEX_IMAGE':
                        if n.image:
                            path = os.path.join(out_textures_dir, f"{clean_filename}#{mat_slot.material.name}#{n.image.name}")

                            hierarchy[clean_filename].append({
                                mat_slot.material.name: n.image.name
                            })
                            n.image.save_render(path)

with open(os.path.join(out_json_dir, f"{clean_filename}.json"), "w") as outfile:
    json.dump(hierarchy, outfile)
