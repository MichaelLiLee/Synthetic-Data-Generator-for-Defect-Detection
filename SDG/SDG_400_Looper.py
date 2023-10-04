# Prevent to create __pycache__ file
import sys
sys.dont_write_bytecode = True

import subprocess
import os
from SDG_200_SDGParameter import SDGParameter
import collections
import time

class Looper:
    """ 
    A class for repeatedly run the file SDG_300_DataGenerator.py in Blender, this class also provide the Estimated time consumption 
    to generate n synthetic images, and save the current configuration to a txt file.

    Attributes
    ----------
    __gen_num (int): The quantity of synthetic images needed to be generated.
    __gen_num_counter (int): The quantity of synthetic images that have already been generated.
    __remain_gen_num (int): The quantity of synthetic images remaining to be generated.
    __start_time (float): The starting time of synthetic image generation.
    __end_time (float): The ending time of synthetic image generation.
    __time_seque (deque of float): A seque to temporarily store time consumed for generating 20 synthetic images.
    __time_list (list of float): A list to temporarily store time consumed for generating 20 synthetic images.
    __average_time_consume_per_img (float): Average time consumed to generate one synthetic image.
    __gen_1k_imgs_eta (str): Estimated time consumption to generate 1000 synthetic images.
    __gen_n_imgs_eta (str): Estimated time consumption to generate n(n=__remain_gen_num) synthetic images.
    __logger (dict of str: depend on parameter type): Log configuration form SDGParameter class.

    Methods
    -------
    __convert_time(): Converts seconds into days, hours, minutes, and seconds.
    __caculate_gen_imgs_eta(): Calculate the time consumption for generating synthetic images.
    loop(): Repeatedly run the file SDG_300_DataGenerator.py in Blender.

    References
    ----------
    [1]Convert to day, hour, minutes and seconds, https://www.w3resource.com/python-exercises/python-basic-exercise-65.php
    [2]Command Line Arguments, https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html

    """ 

    def __init__(self, gen_num =  5000):
        self.__gen_num = gen_num
        self.__gen_num_counter = 0
        self.__remain_gen_num = 0
        self.__start_time = 0
        self.__end_time = 0
        self.__time_seque = collections.deque(maxlen=20)
        self.__time_list = list()
        self.__average_time_consume_per_img = 1
        self.__gen_1k_imgs_eta = None # Format dd:hh:mm:ss
        self.__gen_n_imgs_eta = None # Format dd:hh:mm:ss


    def __convert_time(self, time):
        """Converts seconds into days, hours, minutes, and seconds[1].""" 
        day = time // (24 * 3600)
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
     
        return "d:h:m:s-> %d:%02d:%02d:%02d" % (day, hour, minutes, seconds)


    def __caculate_gen_imgs_eta(self):
        """Calculate the time consumption for generating synthetic images."""
        time_consume = self.__end_time - self.__start_time
        self.__time_seque.appendleft(time_consume)
        time_list = list(self.__time_seque)
        self.__average_time_consume_per_img = sum(time_list) / len(time_list)
        
        # Calculate gen_1k_imgs_time_consume
        gen_1k_imgs_time_consume = self.__average_time_consume_per_img * 1000
        self.__gen_1k_imgs_eta = self.__convert_time(time = gen_1k_imgs_time_consume)
        
        # Calculate gen_num imgs time consume
        self.__remain_gen_num = self.__gen_num - self.__gen_num_counter
        gen_n_imgs_time_consume = self.__average_time_consume_per_img * self.__remain_gen_num
        self.__gen_n_imgs_eta = self.__convert_time(time = gen_n_imgs_time_consume)


    def loop(self):
        """Repeatedly run the file SDG_300_DataGenerator.py in Blender."""
        # Passing gen_num param
        parameter = SDGParameter()
        self.__gen_num = parameter.gen_num

        while self.__gen_num_counter < self.__gen_num:

            # Log start time
            self.__start_time = time.time()

            # Get blender exe path
            blender_exe_path = parameter.blender_exe_path

            # Get SDG_300_DataGenerator.py path
            module_path = os.path.dirname(os.path.abspath(__file__))
            data_generator_path = os.path.join(module_path,"SDG_300_DataGenerator.py")

            # Set args[2]
            args = [
                blender_exe_path,
                "--python", # Run the given Python script file.
                data_generator_path,
                "--window-geometry","0","0","100","100", # Open with lower left corner at <sx>, <sy> and width and height as <w>, <h>.
                "--no-window-focus" # Open behind other windows and without taking focus.
                ]

            # Create new process
            subprocess.run(args)

            self.__gen_num_counter += 1
            
            # Log end time
            self.__end_time = time.time()

            self.__caculate_gen_imgs_eta()

            print(f"Generate 1 Image ETA: {int(self.__average_time_consume_per_img)} Seconds")
            print(f"Generate 1k Images ETA: {self.__gen_1k_imgs_eta}")
            print(f"Already Generated {self.__gen_num_counter}/{self.__gen_num} Images")
            print(f"Remain {self.__remain_gen_num} Images Need To Generate, ETA: {self.__gen_n_imgs_eta}")

        print(f"Generate {self.__gen_num} Images COMPLERED !!!")


if __name__ == '__main__':
    looper = Looper()
    looper.loop()