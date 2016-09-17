"""
This module is used to pull individual sprites from sprite sheets.
"""
import pygame
import constants

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name_array):
        """ Constructor. Pass in the array of file name of the sprite sheet. """
        if len(file_name_array) == 1:
            self.sprite_sheet = pygame.image.load(file_name_array[0]).convert()
        else:
            base = pygame.image.load(file_name_array[0])
            for img in file_name_array:
                layer = pygame.image.load(img)
                base.blit(layer, (0,0))
            self.sprite_sheet = base.convert()


    def get_image(self, x, y, width, height, color, char_width, char_height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([char_width, char_height]).convert()
        image.fill(color)
        image.set_colorkey(color)

        # Do calculations to find the middle and center it based on that.
        off_x = (char_width - width)/2
        off_y = (char_height - height)

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (off_x, off_y), (x, y, width, height))

        # set transparent color
        image.set_colorkey(color)

        # Return the image
        return image
