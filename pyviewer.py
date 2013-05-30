import dicom
import pygame
from pygame.locals import *
import array
import sys
import getopt
import pywt
opts, extraparams = getopt.getopt(sys.argv[1:], 't:')
threshold = 0
for o, p in opts:
    if o in ['-t', '--threshold']:
        threshold = int(p, 10)
dcmimg = dicom.read_file("mdb001.dcm")
pixeldata = array.array('B', dcmimg.PixelData)
pygame.init()
window = pygame.display.set_mode((1024, 1024))
pygame.display.set_caption('Dicom Image')
screen = pygame.display.get_surface()
dcm_surface = pygame.Surface((dcmimg.Rows, dcmimg.Columns))


def draw():
    global threshold
    global dcm_surface
    pxarray = pygame.PixelArray(dcm_surface)
    x = 0
    for i in range(0, dcmimg.Rows):
        for j in range(0, dcmimg.Columns):
            pxarray[j][i] = (pixeldata[x], pixeldata[x + 1], pixeldata[x + 2])
            x = x + 3
    coeffs = pywt.dwt2(pxarray, pywt.Wavelet('haar'))
    cA, (cH, cV, cD) = coeffs
    dim = cD.shape
    print dim
    for i in range(0, dim[0]):
        for j in range(0, dim[1]):
            pxarray[j][i] = int(cD[j][i])
    dcm_surface = dcm_surface.copy()
    screen.blit(dcm_surface, (0, 0))
    pygame.display.flip()
    print "done"


def input(events):
    global threshold
    global drawing
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
draw()
while True:
    input(pygame.event.get())
