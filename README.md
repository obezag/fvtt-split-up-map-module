# fvtt-split-up-map-module
This is a simple Python script that splits up any (hopefully) map-pack module for Foundry VTT into an individual module for each map.

# Purpose
Many members of the Foundry VTT community make beautiful map packs that contain dozens of high-quality, large maps that are already kitted out with lights, walls, music and tiles. Many DMs either host their VTTs on cloud servers with limited storage (like Digital Ocean) or on The Forge. 

To avoid maps a DM is not using taking up their allotted space on their host, it makes sense to split up the single many-maps module into many single-map modules that can be uploaded to the server and removed as needed. This is tedious to do by hand.

This script intends to do it mostly automatically.

# Introduction to Python
Python is an interpreted scripting language. To run a Python script, you need to install the Python interpreter onto your computer (and preferably add it to your path). 

You can install the latest version of Python 3.x from the official source: https://www.python.org/downloads/windows/

If you follow the default installation instructions, Python should be installed to your path. To check if it is, after installation, open a command prompt and type _python_ followed by the _enter_ key. If you get anything other than "'python' is not a recognized internal or external command, operable program or batch file." you're good to go. To leave the python interpreter that you just opened, either close the command line window or type exit() followed by the _enter_ key.

To run this script, open a command window in the folder that has the script in it and enter _.\python fvtt-split-up-map-module.py_. 

(You can open a powershell window, command's cooler, younger brother in a folder by navigating to the folder in Windows Explorer and holding _shift_ while right clicking and then selecting "Open Powershell Window Here".)


# Using the Program
This is a Python script. It should run on any machine, but you will have to install the Python runtime environment and be comfortable running a script using it. 

## Step 1: Acquire Module Files and Information
If you're a normal Foundry VTT user, you probably are used to downloading map packs by going to Foundry's Module management page and pasting in a link that looks like this https://...........cool-maps.json 

What we want to do is open that link directly in your browser. That link will download and open the module's JSON file (which is like a text file's cooler, younger brother). If you look at the bottom of the module's JSON file, you should see the word _download_ followed by the link to a zip file. This zip file contains all of the information for all of your maps, all of the images, sound files, wall, light and other information.

Open that link in your browser to download the module to your computer. Once it's downloaded, unzip it to a suitable location. You will need the path to the folder that contains the file "module.json" for the script.

## Step 2: Run the script
In a command prompt, run _python fvtt-split-up-map-module.py_. I apologize that the program's output is so ugly.

The program will ask you for the path to the folder containing the module's "module.json" folder. Give it that path and press enter.

The program will then ask you for the path to an output folder. Create the folder in Windows Explorer and then enter its location in the program. (I would recommend creating this folder directly on your C:\ drive, to account for the unfortunate fact that Windows paths have a character limit and this script creates long file names).

The program will then, in that output folder, create one folder containing one module for each map in the original module. (This can easily take up twice the space on your local hard drive as the original module, because shared assets like music and tiles will be duplicated to each map where they are used; but each single-map module will be much smaller than the single many-map module.)

If your original module is named "Great-Free-Maps", each new module will be named something like "great-free-maps-goblin-ambush" or "great-free-maps-prison-escape"

# Uploading your smaller, sleeker individual map module to The Forge
Unfortunately, I do not use The Forge, so I have not been able to test this, but it should work.

Follow the instructions here (https://forums.forge-vtt.com/t/importing-worlds-modules-systems-w-video-tutorial/454), but only select the parent folder for the single map module you want to upload (e.g. the folder named "great-free-maps-prison-escape"). 

When you and your players are done with the map, you can uninstall the module as you normally do to delete it from your system and free up that space. (A note regarding space saving: you will also have to delete the scene that you imported from the module's compendium.)

# Uploading your smaller, sleeker individual map module to a Cloud Service provider.
If you have your FoundryVTT set up on a cloud service provider, you probably do not need much help here. 

1. Remote into your provider, preferably with some kind of file-managing software. (Personally, I use WinSCP (https://winscp.net/eng/download.php), because I am not a command line king.)
2. Navigate to your /foundrydata/Data/modules/ folder.
3. In that folder, copy the entire "great-free-maps-prison-escape" folder. (You should have now in the modules folder a new folder "great-free-maps-prison-escape" which contains all of the appropriate information to generate your maps.)
4. If your world is currently launched, return to setup. In your modules tab, you should see "great-free-maps-prison-escape". (If you do not return to setup, the module will not load.)
5. Launch your world; enable the module; import your map.
6. If you uninstall the module (and delete the imported scene as well!) you will free up any space used for the map, when you are done with it.

# Advanced Function: Recompress Images
Some map makers like to make map-packs of lossless, beautiful maps. These lossless maps are very large, but a bit of lossy compression wouldn't hurt them. 


**WARNING**: Prepare a new folder for the output; don't try to overwrite previous output!
**WARNING**: This will take _much_ longer, so be prepared to wait because high-quality compression takes a minute or thirty.
**WARNING**: These apply to ALL of the below in this section.

__Default Recompression__
If you have FFMPEG installed on your computer, you can tell the script to save a re-compressed image in the new module, instead of just copying over the old one. (There's generally no point to doing this if your images are already compressed. If you have maps that are on the order of a few Megabytes, I would not bother with this.)

Here's how you do it:
1. In the script, find the variable "ffmpeg_location"
2. Set its value to "ffmpeg" (if ffmpeg is installed on your path) or to the absolute path to _ffmpeg.exe_. 
3. Save the script.
4. When you run it now, the script will compress each PNG and JPG image to a lossy webp with default acceptable settings.


__Change Compression Level__
You can also modify the level of compression used by ffmpeg easily:
1. Find the section of code that references "os.system()". The command here passes flags to ffmpeg. 
2. If you want a larger, higher-quality lossy image, increase the value behind _-qscale_ (it can go up to 100). 
3. If you want a smaller, lower-quality lossy image, decrease the value behind _-qscale_ (it can go down to 0).
4. If you want a lossless image, because lossless webp is generally better than other lossless formats, pump _-qscale_ to 100 and set _-lossless_ to 1.
5. If you suspect that _-preset drawing_ doesn't match your use case, delete it!
(-libwebp documentation: http://underpop.online.fr/f/ffmpeg/help/libwebp.htm.gz)

__Change Output Format or Re-Compressing Tool__
You can change the output format to another file type entirely, if you're comfortable with ffmpeg, as long as you modify the os.system() command flags appropriately _and_ change the "image_ext" to the approrpiate file extension.

You could even use an entirely different command line program, as long as you modify the ffmpeg_location and image_ext variables appropriately and the os.system() command.

__Add Additional Image Types__
By default, the recompression only occurs with ".png" and ".jpg" and ".jpeg" images, because I am too lazy to enumerate all possible image types or find a more intelligent way to recognize an image file.

If your preferred map maker creates image files with different file extensions and you want to recompress those bad boys, find the part of the code where ".jpg" and ".png" are enumerated. Add your extension as a string to that list, and the recompression code should work with your images too! (ffmpeg can handle just about any image type.)

# Warnings: Run at your own Risk
This program didn't explode my computer. It is, however, a very janky program. Run at your own risk!

While this program works on the map packs I tested it on, it may not work for you. Rather than reading about how Foundry VTT's "db" format works, I just treated it like oddly-formatted JSON. Only cool people (like you) read documentation. I am not a cool person. (If you find a free map pack that this does not work for, feel free to open an issue, and I may or may not look at it.)

In the same vein, just because it works now doesn't mean it will work in the future, especially if Foundry VTT updates their "db" format.

This works on my Windows 10 machine. It will probably work on Linux, but I can't guarantee it. It'll probably work on your Windows 10 machine, but I can't guarantee that either.
