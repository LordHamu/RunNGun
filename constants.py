"""
Global constants
"""
import pygame

pygame.font.init()
arial = pygame.font.match_font('arial')

# Colors
BLACK    = (0,0,0)
WHITE    = (255,255,255)
BLUE     = (0,0,255)
GREEN    = (0,255,0)
RED      = (255,0,0)

# Text Fonts
smallText = pygame.font.Font(arial, 20)
largeText = pygame.font.Font(arial,115)

# Screen dimensions
DWIDTH        = 1024
DHEIGHT       = 600
HALF_WIDTH    = 512
HALF_HEIGHT   = 300
