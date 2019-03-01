#######################################################################
# Author:  Joao Nuno Carvalho                                         #
# Date:    25.02.2019                                                 #
# License: MIT Open source                                            #
# Mail:    joaonunocarv@gmail.com                                     #
# File:    masked_maze_generator_core.py                              #  
# Description: This is a implementation of a masked Maze Generator    #
#              using the method of depth-first search with recursive  #
#              backtracking. Generates the maze inside a mask.        #
# Note: This method of generating mazes is described in the           #
#       following Wikipedia page:                                     #
#       Maze generation algorithm                                     #
#       https://en.wikipedia.org/wiki/Maze_generation_algorithm       #
#                                                                     #
#       This program is a reimplementation in Python of the program   #
#       written in Javascript for processing normal mazes, but in     #
#       this reimplementation I modified it heavily, I changed the    #
#       render, I added a user defined mask, SVG output,              #
#       PNG output, animated GIF output and MPEG4 generation.         #
#       See also the following great videos explaining beautifully    #
#       the code and how the algorithm of backtracking works.         # 
#       https://github.com/CodingTrain/website/tree/master/           #
#       /CodingChallenges/CC_010_Maze_DFS/Processing/CC_010_Maze_DFS  #
#                                                                     #
#       Videos                                                        #
#       https://youtu.be/HyK_Q5rrcr4                                  #
#       https://youtu.be/D8UgRyRnvXU                                  #
#       https://youtu.be/8Ju_uxJ9v44                                  #
#       https://youtu.be/_p5IH0L63wo                                  #
#                                                                     #
#######################################################################
# (From the above Wikipedia page ... the algorithm....)               #
#                                                                     #
# Recursive backtracker                                               #
# The depth-first search algorithm of maze generation is frequently   #
# implemented using backtracking:                                     #
#                                                                     #
# 1. Make the initial cell the current cell and mark it as visited    #
# 2. While there are unvisited cells                                  #
#    1. If the current cell has any neighbours which have not been    #
#       visited                                                       #
#        1. Choose randomly one of the unvisited neighbours           #
#        2. Push the current cell to the stack                        #
#        3. Remove the wall between the current cell and the chosen   #
#           cell                                                      #
#        4. Make the chosen cell the current cell and mark it as      #
#           visited                                                   #
#    2. Else if stack is not empty                                    #
#        1. Pop a cell from the stack                                 #
#        2. Make it the current cell                                  #
#                                                                     #
#######################################################################


# Note: External libraries that have to be installed:
#   -svgwrite
#   -svglib
#   -imageio
#   -pillow
#   -moviepy  [Not using this one, for MP4 encoding use FFMPEG program ]

#######################################################################
# FFMPEG Comand to transform animated Gif into small movie:
#  
# ffmpeg -i animated.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" video.mp4
#######################################################################

# For Pillow lib
from __future__ import print_function

import sys 
import os

try:
    import svgwrite
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.split(os.path.abspath(__file__))[0]+'/..'))

import svgwrite
if svgwrite.version < (1,0,1):
    print("This script requires svgwrite 1.0.1 or newer for internal stylesheets.")
    sys.exit()


import random
import math


from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

import imageio    # External lib imageio

# Pillow lib
from PIL import Image

# moviepy lib
# from moviepy.editor import *
# import moviepy.editor as mpy

BOARD_WIDTH = "30cm"
BOARD_HEIGHT = "30cm"
BOARD_SIZE = (BOARD_WIDTH, BOARD_HEIGHT)
CSS_STYLES = """
    .background { fill: white; }
    .line { stroke: red; stroke-width: 0.8mm; }
    .blacksquare { fill: indigo; }
    .bluesquare { fill: blue ; }
    .highlightsquare { fill: green; }
"""

#    .line { stroke: firebrick; stroke-width: .1mm; }


class Cell:

    def __init__(self, gen_maze, i, j, inside_mask=True):
            self.gen_maze = gen_maze
            self.i           = i     # Cell num of Col
            self.j           = j     # Cell num of row
            self.walls       = [True, True, True, True]
            self.visited     = False
            self.inside_mask = inside_mask


    def index_test(self, i, j):
        inside_border = True
        if (i < 0) or (j < 0) or (i > self.gen_maze.cols - 1) or (j > self.gen_maze.rows - 1):
            inside_border = False 
        return (i, j, inside_border)


    def ret_if_is_inside_mask(self):
        if self.inside_mask == True:
            return self
        else:
            None


    def check_neighbors(self):
        top       = None
        right     = None
        bottom    = None
        left      = None

        i = self.i
        j = self.j

        grid = self.gen_maze.grid
        neighbors = []

        i_n, j_n, inside_border = self.index_test(i, j-1) 
        if inside_border:
            top    = grid[i_n][j_n].ret_if_is_inside_mask()
        i_n, j_n, inside_border = self.index_test(i+1, j) 
        if inside_border:
            right  = grid[i_n][j_n].ret_if_is_inside_mask()
        i_n, j_n, inside_border = self.index_test(i, j+1) 
        if inside_border:
            bottom = grid[i_n][j_n].ret_if_is_inside_mask()
        i_n, j_n, inside_border = self.index_test(i-1, j) 
        if inside_border:
            left   = grid[i_n][j_n].ret_if_is_inside_mask()

        if (top != None) and (not (top.visited)):
            neighbors.append(top)
        if (right != None) and (not (right.visited)):
            neighbors.append(right)
        if (bottom != None) and (not (bottom.visited)):
            neighbors.append(bottom)
        if (left != None) and (not (left.visited)):
            neighbors.append(left)

        if len(neighbors) > 0:
            r = random.randint( 0, len(neighbors) - 1 )
            return neighbors[r]
        else:
            return None


    def group(self, dwg, classname):
        return dwg.add(dwg.g(class_=classname))   


    def highlight(self, dwg):
        highlight_squares = self.group(dwg, "highlightsquare")
        w = self.gen_maze.w
        x = self.i * w
        y = self.j * w

        square = dwg.rect(insert=(x, y), size=(w, w))
        highlight_squares.add(square)


    def show(self, dwg):
        if self.inside_mask == False:
            return    # Only draws the lines inside the mask.
        lines = self.group(dwg, "line")
        w = self.gen_maze.w
        x = self.i * w
        y = self.j * w
        # stroke(255)
        if self.walls[0]:
            lines.add(dwg.line(start=(x, y), end=(x+w, y)))
        if self.walls[1]:
            lines.add(dwg.line(start=(x+w, y), end=(x+w, y+w)))
        if self.walls[2]:
            lines.add(dwg.line(start=(x+w, y+w), end=(x, y+w)))
        if self.walls[3]:
            lines.add(dwg.line(start=(x, y+w), end=(x, y)))
    
        if self.visited:
            blue_squares = self.group(dwg, "bluesquare")
            square = dwg.rect(insert=(x, y), size=(w, w))
            blue_squares.add(square)


def calc_num_squares(dim_max, cell_len): 
    return math.floor(dim_max / cell_len)


def gen_mask_key(i, j):
    return i*10000 + j


def gen_mask_key_reverse(key):
    i = math.floor(key / 10000)
    j = math.floor(key % 10000)
    return (i, j)


class MazeGenerator:

    def __init__(self, i_init, j_init, x_max, y_max, cell_len, maze_name="maze_building_process", mask_dic = None):
        self.w               = cell_len                     # Length of the square of the cell.
        self.x_max           = x_max     
        self.y_max           = y_max
        self.cols            = calc_num_squares( x_max, self.w)   # Dimensions of the grid.
        self.rows            = calc_num_squares( y_max, self.w)    
                
        self.maze_name       = maze_name
        self.subdir_svg      = "./a_output_svg/"
        self.subdir_png      = "./b_output_png/"
        self.subdir_anim_gif = "./c_output_anim_gif/"
        self.counter         = 0
        self.file_svg_lst    = []

        self.mask_dic = mask_dic

        self.i_init = i_init
        self.j_init = j_init

        self.cells_inside_mask_lst = []

        self.grid            = self.initialization()
        self.stack           = []                           # Used for backtracking.
        if self.grid[i_init][j_init].inside_mask == False:
            raise AssertionError("ERROR in MazeGenerator i_int and j_init aren't inside the mask if the is a mask!")
        self.curr_cell       = self.grid[i_init][j_init]


    def initialization(self):
        grid_new = []
        inside_mask = True
        for i in range(self.cols):        
            row = []
            for j in range(self.rows):
                if self.mask_dic != None:
                    key = gen_mask_key(i, j)
                    if key in self.mask_dic:
                        inside_mask = True
                    else:
                        inside_mask = False
                cell_tmp =  Cell(self, i, j, inside_mask)   
                row.append( cell_tmp )
                if inside_mask == True:
                    # Used for faster drawing.
                    self.cells_inside_mask_lst.append( cell_tmp )
            grid_new.append(row)
        return grid_new


    def remove_walls(self, cell_a, cell_b):
        a = cell_a
        b = cell_b

        x = a.i - b.i
        if x == 1:
            a.walls[3] = False
            b.walls[1] = False
        elif x == -1:
            a.walls[1] = False
            b.walls[3] = False
        
        y = a.j - b.j
        if y == 1:
            a.walls[0] = False
            b.walls[2] = False
        elif y == -1:
            a.walls[2] = False
            b.walls[0] = False


    def draw_step(self):
        filename = self.maze_name + "_%06d.svg" % (self.counter)
        self.file_svg_lst.append(filename)
        filepath = self.subdir_svg + filename

        dwg = svgwrite.Drawing(filepath, size=BOARD_SIZE)
        self.counter += 1

        # checkerboard has a size of 10cm x 10cm;
        # defining a viewbox with the size of 80x80 means, that a length of 1
        # is 10cm/80 == 0.125cm (which is for now the famous USER UNIT)
        # but I don't have to care about it, I just draw 8x8 squares, each 10x10 USER-UNITS
        
        # dwg.viewbox(0, 0, 80, 80)
        dwg.viewbox(0, 0, self.x_max, self.y_max)

        # always use css for styling
        dwg.defs.add(dwg.style(CSS_STYLES))
        
        # set background
        dwg.add(dwg.rect(size=('100%','100%'), class_='background'))

        # Draw the maze.
        
        # for j in range(self.rows):
        #     for i in range(self.cols):
        #         cell = self.grid[i][j]
        #         cell.show(dwg)

        # Optimized version.
        for cell in self.cells_inside_mask_lst:
            cell.show(dwg)

        self.curr_cell.visited = True
        self.curr_cell.highlight(dwg)

        dwg.save()

        # STEP 1
        next_cell = self.curr_cell.check_neighbors()
        if next_cell != None:
            # print("i= %d, j= %d" % (next_cell.i, next_cell.j) )

            next_cell.visited = True

            # STEP 2
            self.stack.append(self.curr_cell)

            # STEP 3
            self.remove_walls(self.curr_cell, next_cell)

            # STEP 4
            self.curr_cell = next_cell
        elif len(self.stack) > 0:
            # If doesn't have neighbors it makes backtraking.
            # self.curr_cell = self.stack.pop(len(self.stack) - 1)
            self.curr_cell = self.stack.pop()
            # print("pop## i= %d, j= %d" % (self.curr_cell.i, self.curr_cell.j) )
        else:
            return False        
        return True


    def generate(self):
        print("Start generating SVG's ...")
        while(True):
            if self.draw_step() == False:
                break
        print("...ending generating SVG's")


    def set_seed(self, value):
            random.seed(value)


    def process_svg_to_png_to_anin_gif(self):

        # self.subdir_svg      = "./output_svg/"
        # self.subdir_png      = "./output_png/"
        # self.subdir_anim_gif = "./output_anim_gif/"

        # n SVG -> n PNG
        print("Start converting SVG's to PNG ...")
        file_png_lst = []
        for file_svg in self.file_svg_lst:
            filepath_svg = self.subdir_svg + file_svg
            file_png = file_svg[:-4] + ".png"
            file_png_lst.append(file_png)
            filepath_png = self.subdir_png + file_png
            
            drawing = svg2rlg(filepath_svg)
            renderPM.drawToFile(drawing, filepath_png, fmt="PNG")
        print("...ending converting SVG's to PNG ")


        # n PNG -> 1 anim GIF
        print("Start creating anim GIF from n PNG's ...")
        images = []
        for file_png in file_png_lst:
            filepath_png = self.subdir_png      + file_png
            file_gif = self.maze_name + "_anim.gif"
            filepath_gif = self.subdir_anim_gif + file_gif
            images.append(imageio.imread(filepath_png))
        imageio.mimsave(filepath_gif, images)
        print("...ending creating anim GIF from n PNG's")




# This function is to process the last part manually is something goes wrong.
def manual_n_png_to_anim_gif(png_dir_path_from, anim_gif_dir_path_to, maze_name):
        # n PNG -> 1 anim GIF
        print("Start manually creating anim GIF from n PNG's ...")
        files_png_lst = sorted((fn for fn in os.listdir(png_dir_path_from)))
        counter = 0
        with imageio.get_writer(anim_gif_dir_path_to + maze_name + "_anim.gif", mode='I') as writer:
            for filename_png in files_png_lst:
                if counter % 100 == 0:
                    print(filename_png)
                counter += 1
                image = imageio.imread(png_dir_path_from + filename_png)
                writer.append_data(image)
        writer.close()
        print("...ending manually creating anim GIF from n PNG's")


# def anim_gif_to_mp4(filepath_anim_gif):
#     print("Begin from animated GIF to MP4 video...")
#     video_clip = mpy.VideoFileClip(filepath_anim_gif)
#     video_clip.write_videofile(filepath_anim_gif[-4] + ".mp4")
#     # video_clip.write_videofile(filepath_anim_gif[-4] + ".avi")
#     print("...end from animated GIF to MP4 video.")


# Return's a dic with the position and the mask colours.
def process_mask(filepath_mask, cell_len, color_mask_lst):
    im = Image.open(filepath_mask).convert('RGB')
    px = im.load()
    print("\n\n", filepath_mask, im.format, "%dx%d" % im.size, im.mode, "\n\n" )
    mask_dic = {}
    mask_img_x_max, mask_img_y_max = im.size

    i_max = calc_num_squares(mask_img_x_max, cell_len) 
    j_max = calc_num_squares(mask_img_y_max, cell_len) 

    i_init = -1
    j_init = -1

    flag_execute_one_time = True

    for i in range(i_max):
        for j in range(j_max):
            i_p = i * cell_len + cell_len // 2 
            j_p = j * cell_len + cell_len // 2
            color_rgb = px[i_p,j_p]
            inside_mask = False

            # # Black letters in mask.
            # if color_rgb == (0, 0, 0):
            #     inside_mask = True
            #     key = gen_mask_key(i, j)
            #     mask_dic[key] = "B"

            if color_rgb in color_mask_lst:
                inside_mask = True
                key = gen_mask_key(i, j)
                mask_dic[key] = "B"

            if flag_execute_one_time == True and inside_mask == True:
                flag_execute_one_time = False
                i_init = i
                j_init = j
                print("i, j = ", i,", ", j)
                print("i_p, j_p = ", i_p,", ", j_p)

    im.close()

    img_target = Image.new(im.mode, im.size, color=0)
    px_target = img_target.load()

    for key, val in mask_dic.items():
        i_n, j_n = gen_mask_key_reverse(key)
        i_p = i_n * cell_len + cell_len // 2 
        j_p = j_n * cell_len + cell_len // 2
        pixel = (255, 255, 255)
        px_target[i_p, j_p] = pixel 
    
    img_target.save(filepath_mask[:-4] + "mask_test.png", "PNG")

    return (i_init, j_init, mask_dic, mask_img_x_max, mask_img_y_max) 


###############
# Unit test's #
###############

def test_01(res_lst):
    # Test 01
    print("\nRunning test 01....\n")
    ok = True    
    
    # Deploy last used
    #
    # filepath_mask = "./deploy_png_mascara/deploy_mascara_medio_connected.png"
    # cell_len = 10 # 10 # 25  # 10 # 50
    # maze_name = "deploy_maze"
    # color_mask_lst = [ (239, 67, 34), (255, 255, 255) ]


    # ALTlab
    #
    # filepath_mask  = "./altlab_png_mask/altlab_mask_large_connected.png"
    # cell_len       = 25 # 15 
    # maze_name      = "altlab_maze"
    # color_mask_lst = [ (0, 0, 0) ]


    # Test for Debug
    #
    # filepath_mask = "./altlab_png_mask/small_teste.png"
    # cell_len = 100
    # maze_name = "small_test"
    # color_mask_lst = [ (0, 0, 0) ]


    # peace_symbol
    #
    filepath_mask  = "./png_masks/png_mask_peace_symbol_small.png"
    cell_len       = 6 # 10 
    maze_name      = "peace_symbol_maze"
    color_mask_lst = [ (0, 0, 0) ]


    i_init, j_init, mask_dic, mask_img_x_max, mask_img_y_max  = process_mask(filepath_mask, cell_len, color_mask_lst )


    mz_01 = MazeGenerator( i_init=i_init, j_init=j_init, x_max=mask_img_x_max, y_max=mask_img_y_max,
                           cell_len=cell_len, maze_name=maze_name, mask_dic=mask_dic)
    mz_01.set_seed(1)
    print("Begin generating.....\n\n\n")
    mz_01.generate()
    mz_01.process_svg_to_png_to_anin_gif()

    res_lst.append(ok)
    if ok == True:
        print("...Test 01 PASSED.")
  

def runTests():
    res = []
    
    test_01(res)
    # test_02(res)
    # test_03(res)
    
    if all(res):
        print("\n** PASSED ALL TESTS! **")


if __name__ == "__main__":
    print("Start running tests to MazeGenerator....\n\n")
    runTests()
    print("\n...Finished running tests to MazeGenerator....")

    # Generating the mp4 video automatically (has a problem with downloading FFMPEG,
    # see how to execute the comand manually at the be beginning of this file )
    #
    # filepath_anim_gif = "./c_output_anim_gif/maze_anim_v2_medio_uma_letra_10.gif"
    # anim_gif_to_mp4(filepath_anim_gif)

    # Generating manually the animated GIF. 
    #
    # png_dir_path_from    = "./b_output_png/"
    # anim_gif_dir_path_to = "./c_output_anim_gif/"
    # maze_name            = "ALTlab_maze"
    # manual_n_png_to_anim_gif(png_dir_path_from, anim_gif_dir_path_to, maze_name)



# Google Python Naming Conventions:
#   module_name, package_name, ClassName, method_name, ExceptionName, function_name,
#   GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name

