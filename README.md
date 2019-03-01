# Masked Maze Generator
This is an implementation of a masked Maze Generator using the method of depth-first search with recursive backtracking. It generates the maze inside a mask. <br>
<br>
This method of generating mazes is described in the following Wikipedia page: <br>
[Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm) <br>


## License:
MIT open source

## Description

This program is a reimplementation in Python of the program written in Javascript for processing normal mazes, but in this reimplementation I modified it heavily, I changed the render, I added a user defined mask, SVG output, PNG output, animated GIF output and MPEG4 generation. <br>
See also the following great videos explaining beautifully the Javascript code and how the algorithm of backtracking works. <br> 

[Javscript github for code train](https://github.com/CodingTrain/website/tree/master/CodingChallenges/CC_010_Maze_DFS/Processing/CC_010_Maze_DFS) <br>

**Videos:** <br>
[Vídeo part 1](https://youtu.be/HyK_Q5rrcr4) <br>
[Video part 2](https://youtu.be/D8UgRyRnvXU) <br>
[Video part 3](https://youtu.be/8Ju_uxJ9v44) <br>
[Video part 4](https://youtu.be/_p5IH0L63wo) <br>   

**Features:** <br>
* It generates a maze for a given PNG mask input image with any color or n colors corresponding to the mask, parameterized. With any resolution.
* The length of the squares is configurable.
* The colors are configurable (Background color, lines colors, visited cell’s color, current cell color)
* The line with is configurable.
* It generates at the beginning a PNG sample with the position of the center of each square over the mask, as a black image with dotted white point’s.
* It generates images for each frame in SVG and PNG format.
* It generates an animated GIF file.
* It generates a highly compressed MP4 file (small file size) using with FFMPEG.
* It is reasonably fast, even on older hardware. 

## The startup mask that you create fresh or from a photo (can have many colors) [Peace Symbol].
![PNG of the startup mask](/png_masks/png_mask_peace_symbol_small.png)

## The test mask showing the center of the squares cell that will be generated
![PNG of the test mask](/png_masks/png_mask_peace_symbol_smallmask_test.png)

## The generated SVG's
![SVG of maze being constructed at the start](/a_output_svg/peace_symbol_maze_000010.svg)
![SVG of maze being constructed at the middle](/a_output_svg/peace_symbol_maze_000300.svg)
![SVG of maze being constructed at the end](/a_output_svg/peace_symbol_maze_000640.svg)

## The generated PNG's
![PNG of maze being constructed at the start](/b_output_png/peace_symbol_maze_000010.png)
![PNG of maze being constructed at the middle](/b_output_png/peace_symbol_maze_000300.png)
![PNG of maze being constructed at the end](/b_output_png/peace_symbol_maze_000640.png)

## The generated animated GIF
![Animated GIF of maze being constructed at the start](/c_output_anim_gif/peace_symbol_maze_anim.gif)


## Requirements for installation
I used the Anaconda Python 3.7 installation with a virtual environment. <br>
<br>
The required libs are: <br> 
* svgwrite
* svglib
* imageio
* pillow
* moviepy  [Not using this one, for MP4 encoding use FFMPEG program ]

## Steps to generate an animated masked maze.
1. First you have to generate the PNG mask in black with a background in other color (like white), or use a image and obtain with a image editor the color values that you will parameterize inside the source code on the test_01 function (see the commented examples). It can also also be a logo or a photo. This mask can be inside the directory /png_masks/, although you can put it in a different path. In this phase, if you have several blob's or letters that you would like to have filled with maze cells please connect them in the mask with small rectangles with at least the cell with length.
2. Configure the parameters inside the test_01 function,a t the end of the file, see commented examples.   
3. Then you will run the code with the command "python masked_maze_generator_core.py" and check inside the directories what is being generated. The order is:
   1. n frames in SVG
   2. n frames in PNG
   3. One animated GIF
   4. Then generate manually the MPEG4 file (MP4) with FFMPEG  
4. The command to generate the MPEG 4 file with FFMPEG is " ffmpeg -i animated.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" video.mp4 ", in with the animated.gif and video.mp4 as to be changed to your specific case.   

<br>
Note: This program was tested on Windows but it should also work on Linux and MAC, but i didn't tested, it probably needs some changes to the / or \ in (slash's) in the path's. <br>
<br>
Have fun! <br>
