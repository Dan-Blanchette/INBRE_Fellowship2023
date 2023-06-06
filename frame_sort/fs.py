'''
@Author: Dan Blanchette
@Date_Modified 6/2/2023
@Description: This program will allow a researcher to specify a file directory for their
   chosen image set and sort them by frame identification number(for a time series).
   For this data set, there are 6 specimens concatonated into one live image video with 
   19 z-pos as part of the confocal image stack.
'''
import os, glob, os.path
import shutil as sh



def make_data_folder():

    cwd = os.getcwd()
    # make a subdirectory inside the cwd called greenImgs
    newFolder = os.path.join(cwd, 'greenImgs/')
    # if the folder doesn't exist already
    if not os.path.isdir(newFolder):
        # make the folder
        os.mkdir(newFolder)

    return 0   

def specimen_sort():
   specimen = 1
   # file_sort()
   for i in range(1, 115):
      # print(i % 19)
      if i % 19 == 0:
         print("Specimen_" + str(specimen))
         specimen += 1

# create new folders T1 -> T(n) for image sorting
def channel_subfolders():

    # open green channel image folder
    path_to_files = 'greenImgs/'

    # get the total number of files in the folder
    # shoould = num_specimens * num_frames * tot_zPos
    tot_files = len([name for name in os.listdir(path_to_files)
                if os.path.isfile(os.path.join(path_to_files, name))])
    # print(tot_files)

    frame_no = 0
    # a list of object codes which allow the program to sort data based on string matching
    object_codes = ['_T']
    for i in range(tot_files):
        # if the remainder of i mod (total images per frame per specimen) is 0
        '''NOTE: value 114 was calculated based on # number of specimens * total number of z-positions in each frame series'''
        if i % 114 == 0:
            # print("Frames_" + str(frame_no))
            # increment the frame count
            frame_no += 1
            # take the file folder path and name the folders frames_ concatonated with the modulus count
            frameFolderPath = os.path.join(path_to_files, 'frames_' + str(frame_no))
        # if a directory name frames_+frame_no does not exist already
        if not os.path.isdir(frameFolderPath):
            # make the directory and name it
            os.mkdir(frameFolderPath)
        
        






# read file all contents for each specimen and sort them into their respective frame folder
# increment to the next frame identifier and continue until end of folder
def main():
   
   folder_created = make_data_folder()
   if folder_created == 0:
   	channel_subfolders()
   # specimen_sort()




if __name__ == "__main__":
    main()