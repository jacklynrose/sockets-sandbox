from PiicoDev_SSD1306 import *
from PiicoDev_SSD1306 import PiicoDev_SSD1306
import network
import socket
from time import sleep
import machine
from machine import Pin
import struct
import os
import json
from adhoc_functions import LazyJSONLoader  as lazy

def plot_image(coordinates, desired_x, desired_y, display):
    # Find the maximum x and y values in the coordinates
    max_x = max(coord[0] for coord in coordinates)
    max_y = max(coord[1] for coord in coordinates)

    for x, y in coordinates:
        # Calculate the relative coordinates by subtracting from the maximum values
        relative_x = x + desired_x
        relative_y = y + desired_y
        
        # Plot the final coordinates using your pixel method
        display.pixel(relative_x, relative_y, 1)
    
    display.show()
    
def remove_image(coordinates, desired_x, desired_y, display):
    # Find the maximum x and y values in the coordinates
    max_x = max(coord[0] for coord in coordinates)
    max_y = max(coord[1] for coord in coordinates)

    for x, y in coordinates:
        # Calculate the relative coordinates by subtracting from the maximum values
        relative_x = x + desired_x
        relative_y = y + desired_y
        
        # Plot the final coordinates using your pixel method
        display.pixel(relative_x, relative_y, 0)
    
    display.show()

class create_UI:
    def __init__(self, display, fonts, images):
        self.display = display
        self.fonts = lazy(fonts)
        self.images_dict = lazy(images)
        self.initialise()
        
    def initialise(self):
        background = self.images_dict.get('background')
        power = self.images_dict.get('power')
        self.plot_image(background['pizel_values'], 0, 0)
        self.display_image((0,0), 'power')
        self.plot_image(self.fonts.get('19')['C']['pizel_values'], 105, 17)
        self.plot_image(self.fonts.get('19')['C']['pizel_values'], 33, 45)
        self.plot_image(self.fonts.get('9')['colon']['pizel_values'], 96, 1)
        self.plot_image(self.images_dict.get('degrees')['pizel_values'],28, 42)
        self.plot_image(self.images_dict.get('degrees')['pizel_values'],80, 50)
        self.plot_image(self.images_dict.get('degrees')['pizel_values'],100, 15)
        
    def plot_image(self, coordinates, desired_x, desired_y):
        # Find the maximum x and y values in the coordinates
        max_x = max(coord[0] for coord in coordinates)
        max_y = max(coord[1] for coord in coordinates)

        for x, y in coordinates:
            # Calculate the relative coordinates by subtracting from the maximum values
            relative_x = x + desired_x
            relative_y = y + desired_y
            
            # Plot the final coordinates using your pixel method
            self.display.pixel(relative_x, relative_y, 1)
        
        self.display.show()
    
    def remove_image(self, coordinates, desired_x, desired_y):
        # Find the maximum x and y values in the coordinates
        max_x = max(coord[0] for coord in coordinates)
        max_y = max(coord[1] for coord in coordinates)

        for x, y in coordinates:
            # Calculate the relative coordinates by subtracting from the maximum values
            relative_x = x + desired_x
            relative_y = y + desired_y
            
            # Plot the final coordinates using your pixel method
            self.display.pixel(relative_x, relative_y, 0)
        
        self.display.show()

    def display_text(self, coordinates, text, size):
        blank = self.create_blank(size)
        font = self.fonts.get(str(size))
        for c, coordinate in enumerate(coordinates):
            t = text[c]
            self.remove_image(blank, coordinate[0], coordinate[1])
            self.plot_image(font[t]['pizel_values'], coordinate[0], coordinate[1])
    
    def remove_text(self, coordinates, size):
        blank = self.create_blank(size)
        font = self.fonts.get(str(size))
        for c, coordinate in enumerate(coordinates):
            self.remove_image(blank, coordinate[0], coordinate[1])

    def create_blank(self, size):
        pixels = []
        for y in range(size):
            for x in range(size):
                pixels.append((x, y))

        return pixels
            
    def display_image(self, coordinates, image_name):
        image = self.images_dict.get(image_name)
        size = image['size'][0]
        blank = self.create_blank(size)
        self.remove_image(blank, coordinates[0], coordinates[1])
        self.plot_image(image['pizel_values'], coordinates[0], coordinates[1])

    def time(self, time):
        locations = [(80, 0), (87, 0), (103, 0), (110, 0)]
        self.display_text(locations, time, 9)
            
    def outdoor_temp(self, temp):
        locations = [(0,45),(15, 45)]
        self.display_text(locations, temp, 19)

    def weather_1(self, icon):
        location = (0, 15)
        self.display_image(location, icon)
        
    def weather_2(self, icon):
        location = (25, 15)
        self.display_image(location, icon)
        
    def mode(self, mode):
        if mode == 'heat':
            icon = 'flame'
        if mode == 'cool':
            icon = 'snowflake'
        if mode == 'auto':
            icon = 'Auto'
        
        location = (108,43)
        self.display_image(location, icon)
        
    def fan(self, fan):
        if fan == '0':
            icon = 'low_fan'
        if fan == '1':
            icon = 'medium_fan'
        if fan == '2':
            icon = 'full_fan'
        
        location = (86,43)
        self.display_image(location, icon)
        
        
    def set_temp(self, temp):
        locations = [(66,53),(73, 53)]
        self.display_text(locations, temp, 9)
        
    def indoor_temp(self, temp):
        locations = [(66,17),(81, 17)]
        self.display_text(locations, temp, 19)
        
    def LR_swing(self, swing):
        image = self.images_dict.get('left-right')
        coordinates = (66, 37)
        if swing == 0:
            self.remove_image(image['pizel_values'], coordinates[0], coordinates[1])
        if swing == 1:
            self.plot_image(image['pizel_values'], coordinates[0], coordinates[1])
            
    def UD_swing(self, swing):
        image = self.images_dict.get('up-down')
        coordinates = (75, 37)
        if swing == 0:
            self.remove_image(image['pizel_values'], coordinates[0], coordinates[1])
        if swing == 1:
            self.plot_image(image['pizel_values'], coordinates[0], coordinates[1])
    
    def wifi_connect(self, connected):
        image = self.images_dict.get('wifi')
        coordinates = (15,0)
        if connected == 0:
            self.remove_image(image['pizel_values'], coordinates[0], coordinates[1])
        if connected == 1:
            self.plot_image(image['pizel_values'], coordinates[0], coordinates[1])

    def socket_connect(self, connected):
        image = self.images_dict.get('network')
        coordinates = (30,0)
        if connected == 0:
            self.remove_image(image['pizel_values'], coordinates[0], coordinates[1])
        if connected == 1:
            self.plot_image(image['pizel_values'], coordinates[0], coordinates[1])
            
    def error(self, error):
        image = self.images_dict.get('error')
        coordinates = (45,0)
        if error == 0:
            self.remove_image(image['pizel_values'], coordinates[0], coordinates[1])
        if error == 1:
            self.plot_image(image['pizel_values'], coordinates[0], coordinates[1])
            
    def battery(self, charge):
        coordinates = (70,0)
        if charge == 0:
            image = self.images_dict.get('empty_battery')
            self.plot_image(image['pizel_values'], coordinates[0], coordinates[1])
        if charge == 1:
            image = self.images_dict.get('medium_battery')
            self.plot_image(image['pizel_values'], coordinates[0], coordinates[1])
        if charge == 2:
            image = self.images_dict.get('full_battery')
            self.plot_image(image['pizel_values'], coordinates[0], coordinates[1])
    
    def AC_OFF(self):
        #remove_swing
        self.UD_swing(0)
        self.LR_swing(0)
        #remove_temp
        locations = [(66,53),(73, 53)]
        self.remove_text(locations, 9)
        #remove_fan
        location = (86,43)
        blank = self.create_blank(19)
        self.remove_image(blank, location[0], location[1])
        #remove_mode
        location = (108,43)
        blank = self.create_blank(19)
        self.remove_image(blank, location[0], location[1])
        
            
    
