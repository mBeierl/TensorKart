#!/usr/bin/env python

import sys
import pygame

import numpy as np

from PyQt5.QtGui import QPixmap, QScreen
from PyQt5.QtWidgets import QApplication

from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.io import imread

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def take_screenshot():
    img = QScreen.grabWindow(QApplication.primaryScreen(), QApplication.desktop().winId(), 0, 0, 320, 240)
    return img


# def prepare_image(img):
#     if(type(img) == wx._core.Bitmap):
#         buf = img.ConvertToImage().GetData()
#         img = np.frombuffer(buf, dtype='uint8')
#
#     img = img.reshape(480, 615, 3)
#     img = resize(img, [IMG_H, IMG_W])
#
#     return img


class XboxController:
    def __init__(self):
        try:
            pygame.init()

            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print('Initialized Joystick: {}'.format(self.joystick.get_name()))

            self.n_buttons = self.joystick.get_numbuttons()
            self.n_axes = self.joystick.get_numaxes()

        except:
            print('unable to connect to Xbox Controller')


    def read(self):
        pygame.event.pump()

        axes_buttons = []
        for i in range(self.n_axes):
            axes_buttons.append(self.joystick.get_axis(i))

        for i in range(self.n_buttons):
            axes_buttons.append(self.joystick.get_button(i))

        # x = self.joystick.get_axis(0)
        # y = self.joystick.get_axis(1)
        # a = self.joystick.get_button(0)
        # b = self.joystick.get_button(2) # b=1, x=2
        # rb = self.joystick.get_button(4)
        return axes_buttons #[x, y, a, b, rb]


    def manual_override(self):
        pygame.event.pump()
        return self.joystick.get_button(4) == 1


class Data(object):
    def __init__(self):
        self._X = np.load("data/X.npy")
        self._y = np.load("data/y.npy")
        self._epochs_completed = 0
        self._index_in_epoch = 0
        self._num_examples = self._X.shape[0]

    @property
    def num_examples(self):
        return self._num_examples

    def next_batch(self, batch_size):
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch
        return self._X[start:end], self._y[start:end]


def load_sample(sample):
    image_files = np.loadtxt(sample + '/data.csv', delimiter=',', dtype=str, usecols=(0,))
    joystick_values = np.loadtxt(sample + '/data.csv', delimiter=',', usecols=(1,2,3,4,5))
    return image_files, joystick_values


# training data viewer
def viewer(sample):
    image_files, joystick_values = load_sample(sample)

    plotData = []

    plt.ion()
    plt.figure('viewer', figsize=(16, 6))

    for i in range(len(image_files)):

        # joystick
        print(i, " ", joystick_values[i,:])

        # format data
        plotData.append( joystick_values[i,:] )
        if len(plotData) > 30:
            plotData.pop(0)
        x = np.asarray(plotData)

        # image (every 3rd)
        if (i % 3 == 0):
            plt.subplot(121)
            image_file = image_files[i]
            img = mpimg.imread(image_file)
            plt.imshow(img)

        # plot
        plt.subplot(122)
        plt.plot(range(i,i+len(plotData)), x[:,0], 'r')
        plt.hold(True)
        plt.plot(range(i,i+len(plotData)), x[:,1], 'b')
        plt.plot(range(i,i+len(plotData)), x[:,2], 'g')
        plt.plot(range(i,i+len(plotData)), x[:,3], 'k')
        plt.plot(range(i,i+len(plotData)), x[:,4], 'y')
        plt.draw()
        plt.hold(False)

        plt.pause(0.0001) # seconds
        i += 1


# prepare training data
# def prepare(samples):
#     print("Preparing data")
#
#     X = []
#     y = []
#
#     for sample in samples:
#         print sample
#
#         # load sample
#         image_files, joystick_values = load_sample(sample)
#
#         # add joystick values to y
#         y.append(joystick_values)
#
#         # load, prepare and add images to X
#         for image_file in image_files:
#             image = imread(image_file)
#             vec = prepare_image(image)
#             X.append(vec)
#
#     print("Saving to file...")
#     X = np.asarray(X)
#     y = np.concatenate(y)
#
#     np.save("data/X", X)
#     np.save("data/y", y)
#
#     print("Done!")
#     return


# if __name__ == '__main__':
#     if sys.argv[1] == 'viewer':
#         viewer(sys.argv[2])
#     elif sys.argv[1] == 'prepare':
#         prepare(sys.argv[2:])
