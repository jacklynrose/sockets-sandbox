from PiicoDev_SSD1306 import *
from PiicoDev_SSD1306 import PiicoDev_SSD1306
import network
import socket
from time import sleep
import machine
from machine import Pin
import struct
from display_bitmap import plot_image, remove_image
import os
import json

display = create_PiicoDev_SSD1306(freq=400000)

display.fill(0)

from PiicoDev_SSD1306 import *

# Opening JSON file
with open('images.json', 'r') as openfile:
    images_dict = json.load(openfile)

with open('text_19px.json', 'r') as openfile:
    text_19 = json.load(openfile)

with open('text_9px.json', 'r') as openfile:
    text_9 = json.load(openfile)

fonts = {}
fonts[9] = text_9
fonts[19] = text_19


class create_UI:
    def __init__(self, display, fonts, images):
        self.display = display
        self.fonts = fonts
        self.images_dict = images

    def initialise(self):
        background = self.images_dict['background']
        power = self.images_dict['power']
        self.plot_image(background['pizel_values'], 0, 0, display)
        self.display_image((0, 0), 'power', display)
        self.plot_image(text_19['C']['pizel_values'], 105, 17, display)
        self.plot_image(text_19['C']['pizel_values'], 33, 45, display)
        self.plot_image(text_9['colon']['pizel_values'], 96, 1, display)
        self.plot_image(images_dict['degrees']['pizel_values'], 28, 42, display)
        self.plot_image(images_dict['degrees']['pizel_values'], 80, 50, display)
        self.plot_image(images_dict['degrees']['pizel_values'], 100, 15, display)

    def plot_image(self, coordinates, desired_x, desired_y, display):
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

    def display_text(self, coordinates, text, size, display):
        blank = self.create_blank(size)
        font = self.fonts[size]
        for c, coordinate in enumerate(coordinates):
            t = text[c]
            self.remove_image(blank, coordinate[0], coordinate[1], display)
            self.plot_image(font[t]['pizel_values'], coordinate[0], coordinate[1], display)

    def create_blank(self, size):
        pixels = []
        for y in range(size):
            for x in range(size):
                pixels.append((x, y))

        return pixels

    def display_image(self, coordinates, image_name):
        image = self.images_dict[image_name]
        size = image['size'][0]
        blank = self.create_blank(size)
        self.remove_image(blank, coordinates[0], coordinates[1], self.display)
        self.plot_image(image['pizel_values'], coordinates[0], coordinates[1], self.display)

    def time(time, display):
        locations = [(80, 0), (87, 0), (103, 0), (110, 0)]
        display_text(locations, time, 9, display)

    def outdoor_temp(temp, display):
        locations = [(0, 45), (15, 45)]
        display_text(locations, temp, 19, display)

    def weather_1(icon, display):
        location = (0, 15)
        display_image(location, icon, display)

    def weather_2(icon, display):
        location = (25, 15)
        display_image(location, icon, display)

    def mode(mode, display):
        if mode == 'heat':
            icon = 'flame'
        if mode == 'cool':
            icon = 'snowflake'
        if mode == 'auto':
            icon = 'Auto'

        location = (108, 43)
        display_image(location, icon, display)

    def fan(fan, display):
        if fan == 0:
            icon = 'low_fan'
        if fan == 1:
            icon = 'medium_fan'
        if fan == 2:
            icon = 'full_fan'

        location = (86, 43)
        display_image(location, icon, display)

    def set_temp(temp, display):
        locations = [(66, 55), (73, 55)]
        display_text(locations, temp, 9, display)

    def indoor_temp(temp, display):
        locations = [(66, 17), (81, 17)]
        display_text(locations, temp, 19, display)

    def LR_swing(swing):
        image = images_dict['left-right']
        coordinates = (66, 37)
        if swing == 0:
            remove_image(image['pizel_values'], coordinates[0], coordinates[1], display)
        if swing == 1:
            plot_image(image['pizel_values'], coordinates[0], coordinates[1], display)

    def UD_swing(swing):
        image = images_dict['up-down']
        coordinates = (75, 37)
        if swing == 0:
            remove_image(image['pizel_values'], coordinates[0], coordinates[1], display)
        if swing == 1:
            plot_image(image['pizel_values'], coordinates[0], coordinates[1], display)


background = images_dict['background']
wifi = images_dict['wifi']
network = images_dict['network']
error = images_dict['error']
battery = images_dict['medium_battery']
power = images_dict['power']
full_fan = images_dict['full_fan']

plot_image(background['pizel_values'], 0, 0, display)
display_image((0, 0), 'power', display)
plot_image(text_19['C']['pizel_values'], 105, 17, display)
plot_image(text_19['C']['pizel_values'], 33, 45, display)
plot_image(text_9['colon']['pizel_values'], 96, 1, display)
plot_image(images_dict['degrees']['pizel_values'], 28, 42, display)
plot_image(images_dict['degrees']['pizel_values'], 80, 50, display)
plot_image(images_dict['degrees']['pizel_values'], 100, 15, display)

plot_image(wifi['pizel_values'], 15, 0, display)
plot_image(network['pizel_values'], 30, 0, display)
plot_image(error['pizel_values'], 45, 0, display)
plot_image(battery['pizel_values'], 70, 0, display)

# weather
weather_1('sun', display)
weather_2('cloud', display)
outdoor_temp(str(25), display)

# aircon
mode('cool', display)
fan(2, display)
set_temp(str(22), display)
indoor_temp(str(22), display)
LR_swing(1)
UD_swing(1)

display.show()


