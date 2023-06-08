#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue Jun 21 10:37:11 2022

@author: Dan Blanchette

Copyright (c) 2022, Dan Blanchette
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree. 
"""

import counter_cell_v1 as count
    

# main Function
def main():
    # this line can be replaced with os user input for pathing. For now the specified path is used for testing in Spyder IDE 
    # as it does not handle user I/O well (crashes).
    path = '../greenImgs/frames_1'
    # find all the files in the specified directory that start with a number value
    filelist = sorted(count.os.listdir(path), 
                   key=lambda x: int(count.os.path.splitext(x)[0]))
    # for all images in the directory, run the cells_only function for image analysis
    for image_file in filelist :
       count.cells_only(path + image_file)


    return 0

if __name__=="__main__":
    main()