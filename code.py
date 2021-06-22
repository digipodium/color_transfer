from color_transfer import color_transfer
import numpy as np
import argparse
import cv2
import os

def show_image(title, image, width = 300):
	# resize the image to have a constant width, just to
	# make displaying the images take up less screen real
	# estate
	r = width / float(image.shape[1])
	dim = (width, int(image.shape[0] * r))
	resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

	# show the resized image
	cv2.imshow(title, resized)

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')



def initialize(source_img,target_img,clip=True,preserve=True):
	# load the images
	source = cv2.imread(source_img)
	target = cv2.imread(target_img)

	# transfer the color distribution from the source image
	# to the target image
	transfer = color_transfer(source, target, clip=clip, preserve_paper=preserve)

	# check to see if the output image should be saved
	output = os.path.join('output',"new_"+os.path.basename(target_img))
	cv2.imwrite(output, transfer)

	# show the images and wait for a key press
	show_image("Source", source)
	show_image("Target", target)
	show_image("Transfer", transfer)
	cv2.waitKey(0)
	return output