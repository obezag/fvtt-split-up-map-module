import os
import json

from shutil import copyfile

#global variables, because bad practices are good fun!
module = "module.json"
ffmpeg_location = "" # Leave blank if you don't want to bother trying to recompress stuff. Probably better. If installed to your path, just put "ffmpeg"; otherwise, copy the entire path, e.g. C:\Users\Me\ffmpeg.exe
image_ext = ".webp"

def make_dir_safe(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

def copy_file_safe(src, dst):
    if not os.path.isfile(dst):
        copyfile(src, dst)

def abs_to_relative(abspath):
    temp_path = abspath
    while os.path.isabs(temp_path):
        temp_path = temp_path[1:]
    return temp_path

def acquire_relative_subpath(relativePath, parent):
    return_path = os.path.normpath(relativePath).replace(os.path.normpath(parent), "")
    return abs_to_relative(return_path)

def get_module_relative_path(moduleName):
    return os.path.join("modules", moduleName)

def copy_to_new_directory(module_based_relative_path, module_name, original_parent_path, new_parent_path, new_module_name):
    subpath = acquire_relative_subpath(module_based_relative_path, get_module_relative_path(module_name))
    new_relative_path = "HELP ME"
    original_file_location = os.path.join(original_parent_path, subpath)
    new_file_location = ""

    if os.path.isfile(original_file_location):
        # If we're not using FFMPEG to reduce the file size, or if it's not an image
        ext = os.path.splitext(subpath)[1]
        if ffmpeg_location == "" or ext not in [".png", ".jpg", ".jpeg"]:
            new_file_location = os.path.join(os.path.normpath(new_parent_path), subpath)
            copy_file_safe(original_file_location, new_file_location)
            new_relative_path = os.path.normpath(os.path.join(get_module_relative_path(new_module_name), subpath))
        else:
            new_file_location = os.path.join(os.path.normpath(new_parent_path), os.path.splitext(subpath)[0] + image_ext)
            new_relative_path = os.path.normpath(os.path.join(get_module_relative_path(new_module_name), os.path.splitext(subpath)[0] + image_ext))
            os.system("{ffmpeg} -n -i {input} -pix_fmt yuv420p -c:v libwebp -lossless 0 -compression_level 6 -qscale 75 -preset drawing -pix_fmt yuv420p {output}".format(ffmpeg=ffmpeg_location, input=original_file_location, output=new_file_location))
        print(">>> >>> >>> File at **{file_loc}** copied to **{new_file_loc}**.".format(file_loc=original_file_location, new_file_loc=new_file_location))
    else:
        print("!!! !!! !!! Could not find the file at {file_loc}. Setting to empty.".format(file_loc=original_file_location))
        new_relative_path = ""

    return new_relative_path.replace("\\", "/") # We need the paths to be stored linux-like in the DB file to match the original, so do this.


# Identify the module folder.
folder_exists = False
while not folder_exists:
    input_folder = input("Please paste the folder location for the map module you want to split up (on Windows, you can use shift + insert).\nInput Folder Location: ")
    if os.path.isdir(input_folder):
        folder_exists = True
    else:
        print(">>> The folder at {} does not exist. Please confirm the location and try again.".format(input_folder))

# Read in the main module file.
with open(os.path.join(input_folder, "module.json")) as jf:
    module_json = json.load(jf)

# Identify the maps.db file and other required subdirectories.
required_sub_directories = [abs_to_relative(root.replace(input_folder, "")) for root, dirs, files in os.walk(input_folder)]
"""for subdir in requiredSubDirectories:
    print(subdir)"""

mapsdb_path = None
for pack in module_json["packs"]:
    if pack["entity"] == "Scene":
        mapsdb_path = pack["path"]

if mapsdb_path is None:
    print("!!! I was unable to find the path for the scene compendium in the module.json file. I don't know what to do here, so good bye and good luck!")
    exit

mapsdb_path = abs_to_relative(mapsdb_path)

# Find out how many maps are in the pack.
with open(os.path.join(input_folder, mapsdb_path)) as mdbf:
    map_infos = [json.loads(line) for line in mdbf.readlines()]

print(">>> There are {} maps in this module.".format(len(map_infos)))


# For each map, create a new folder and populate it with files.
output_folder = input("Give me a directory where you want the individual modules to be created. This will take up a lot of space and create {mapCount} folders.\nOutput Folder Location: ".format(mapCount=len(map_infos)))

while not os.path.isdir(output_folder):
    output_folder = input(">>> ** {} ** is not an existing valid directory path. Please create the directory in your file manager and re-enter the directory name.\nOutput Folder Location: ".format(output_folder))

count = 0
for map_info in map_infos:
    count += 1

    # identify the map's name
    map_name = map_info.get("name", None)
    if map_info is None:
        print("!!! !!! Map on line {} does not have a name. Skipping")
        continue
    
    # make a new directory with appropriate subdirectories based on the map's name
    split_module_name = module_json["name"] + "-" + "".join(ch if ch.isalnum() else "-" for ch in map_name.lower())
    split_module_path = os.path.join(output_folder, split_module_name)
    make_dir_safe(split_module_path)
    for rsd in required_sub_directories:
        make_dir_safe(os.path.join(split_module_path, rsd))
    
    # identify every file that is linked in the map, copy it to the new subdirectory, and update the database with the new location
    new_map_info = json.loads(json.dumps(map_info))
    # 1. Copy the map images, tokens and sounds over.
    print(">>> Procesing ... {folder}.".format(folder=split_module_name))
    print(">>> >>> Moving files to {folder}.".format(folder=split_module_name))
    if "img" in map_info:
        if len(map_info["img"]) > 0: #If the value is filled
            new_map_info["img"] = copy_to_new_directory(map_info["img"], module_json["name"], input_folder, split_module_path, split_module_name)
    if "tiles" in map_info:
        for i in range(0, len(map_info["tiles"])):
            tile = map_info["tiles"][i]
            if len(tile.get("img", "")) > 0:
                new_map_info["tiles"][i]["img"] = copy_to_new_directory(tile["img"], module_json["name"], input_folder, split_module_path, split_module_name)
    if "sounds" in map_info:
        for i in range(0, len(map_info["sounds"])):
            sound = map_info["sounds"][i]
            if len(sound.get("path", "")) > 0:
                new_map_info["sounds"][i]["path"] = copy_to_new_directory(sound["path"], module_json["name"], input_folder, split_module_path, split_module_name)

    #2. Write the newly modified maps.db object. 
    with open(os.path.join(split_module_path, mapsdb_path), "w") as mf:
        json.dump(new_map_info, mf)
    print(">>> >>> Successfully wrote modified scene compendium db file.")

    #3. Write the module.json file.
    new_module_json = json.loads(json.dumps(module_json))
    new_module_json["name"] = split_module_name
    new_module_json["title"] = new_module_json["title"] + " | {}".format(map_name)
    scene_pack = None
    for pack in new_module_json["packs"]:
        if pack["entity"] == "Scene":
            scene_pack = pack
            break
    if scene_pack is not None:
        scene_pack["label"] = scene_pack["label"] + " | {}".format(map_name)
        new_module_json["packs"] = [scene_pack]

    with open(os.path.join(split_module_path, "module.json"), "w") as mf:
        json.dump(new_module_json, mf)
    print(">>> >>> Successfully wrote the modified module.json file.")
print("Finished splitting the module. Please check your output folder!")
