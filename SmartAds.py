#!/usr/bin/python

import sys
sys.path.append('./Models')
import numpy as np

PYTHON_VERSION = sys.version_info[0]

if PYTHON_VERSION == 2:
    import Tkinter as tk
    from ttk import Frame, Button
else:
    import tkinter as tk
    from tkinter import Frame, Button

from PIL import Image
from PIL import ImageTk

import time
import glob

import cv2
from agutils import resize_with_ratio


class SmartAds():
    def __init__(self, image_paths):
        
        # Image current index to show
        self.index = 0
        self.alpha = 0
        self.fade_time = 1
        self.curStep = 0


        self.root = tk.Tk()
        self.root.title('Smart Ads System')

        # make app be in fullscreen mode
        self.root.overrideredirect(True)
        self.root.overrideredirect(False)
        self.root.attributes('-fullscreen', True)
        
        # get the image size
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # make the root window the size of the image
        self.root.geometry('{}x{}+{}+{}'.format(self.screen_width, self.screen_height, 0, 0))

        # pick an image file you have .bmp  .jpg  .gif.  .png
        # load the file and covert it to a Tkinter image object
        self.image_paths = self.__load_images(image_paths)
        print('Length of image array: ', len(self.image_paths))

        # Read images
        self.current_image = self.__read_images(self.image_paths[self.index])
                
        # Use a label as a panel
        self.panel = tk.Label(self.root, image=self.current_image)
        self.panel.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        print("Display image {}".format(self.index))

        self.root.after(2000, self.__update_image_no_fading)
        self.root.mainloop()

  
    def __load_images(self, image_paths):
        return glob.glob(image_paths)


    def __read_images(self, single_image_path):
        image = Image.open(single_image_path)
        # image = resize_with_ratio(image, self.screen_width, self.screen_height)
        image = image.resize((self.screen_width, self.screen_height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(image)


    def __update_image_fading(self):
        '''This function to show Images consequencely
        '''
        print("Current image", self.index)

        # Get the current image
        self.current_image = cv2.imread(self.image_paths[self.index])
        self.current_image = cv2.resize(self.current_image, (self.screen_width, self.screen_height))
        
        # Get the next image
        if self.index + 1 < len(self.image_paths):
            self.next_image = cv2.imread(self.image_paths[self.index + 1])
        else:
            self.next_image = cv2.imread(self.image_paths[0])

        self.next_image = cv2.resize(self.next_image, (self.screen_width, self.screen_height))

        self.showed_image = cv2.addWeighted(self.next_image, self.alpha, self.current_image, 1.0 - self.alpha, 0)

        # Show Image
        # convert the images to PIL format...
        simage = cv2.cvtColor(self.showed_image, cv2.COLOR_BGR2RGB)
        simage = Image.fromarray(simage)
 
		# ...and then to ImageTk format
        simage = ImageTk.PhotoImage(simage)
        
        self.panel.configure(image=simage)
        self.panel.image = simage

        # cProfile.run('re.compile("foo|bar")')
        # Update alpha and fading
        if self.alpha == 0:
            self.alpha += 0.05
            self.root.after(3000, self.__update_image_fading)       # Set to call again in 3 seconds
        else:
            self.alpha += 0.05
            # Update new index
            if self.alpha >= 1.0:
                self.alpha = 0

                if (self.index + 1) <= (len(self.image_paths) - 1):
                    self.index += 1  
                else:
                    self.index = 0

            self.root.after(self.fade_time, self.__update_image_fading)       # Set to call again in 1ms


    def __update_image_no_fading(self):
        '''This function to show Images consequencely
        '''

        if (self.index + 1) <= (len(self.image_paths) - 1):
            self.index += 1  
        else:
            self.index = 0

        print("Current image", self.index)

        # Get the current image
        self.current_image = cv2.imread(self.image_paths[self.index])
        self.current_image = cv2.resize(self.current_image, (self.screen_width, self.screen_height))
        
        # Show Image
        # convert the images to PIL format...
        simage = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        simage = Image.fromarray(simage)
 
		# ...and then to ImageTk format
        simage = ImageTk.PhotoImage(simage)
        
        self.panel.configure(image=simage)
        self.panel.image = simage

        self.root.after(3000, self.__update_image_no_fading)       # Set to call again in 3 seconds


# TEST

def main():
    file_paths = '/mnt/Data/MegaSyns/Projects/Smart-Advertising-Systems/Ads_images/*/*.jpg'
    print(len(file_paths))
    SmartAds(file_paths)

if __name__ == '__main__':
    main()