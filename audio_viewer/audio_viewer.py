# -*- coding: utf-8 -*-

"""Main module."""
import os
import toga
from toga.style.pack import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import wave

import pyaudio


def GenerateSpectrum(filename):
    file = wave.open(filename, "rb")
    data = file.readframes(40000)
    data = np.fromstring(data, 'Int16')
    data = data.astype(float)
    NFFT = 128 
    Fs = 8000
    dt = 1.0/Fs
    t = np.arange(0.0, len(data)/Fs, dt)

    ax1 = plt.subplot(211)
    plt.plot(t, data)
    ax2 = plt.subplot(212, sharex=ax1)
    Pxx, freqs, bins, im = plt.specgram(data, NFFT=NFFT, Fs=Fs, noverlap=64)
    plt.savefig('Figure_temp.png')


#TODO: Add a file browser widget for loading the audio content
class SpectrumApp(toga.App):

    def loadAudio(self, filename):
        self.filename = filename
        self.file = wave.open(filename, "rb")
        paud = pyaudio.PyAudio()
        format = paud.get_format_from_width(self.file.getsampwidth())

        self.stream = paud.open(format = format,  
                                channels = self.file.getnchannels(),
                                rate = self.file.getframerate(),
                                output = True)

    def playback(self, widget):
        chunk = 1024

        print("play")
        self.file.rewind()
        data = self.file.readframes(chunk)  
        while data:
            self.stream.write(data)  
            data = self.file.readframes(chunk)

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name, size=(660, 520))
        self.ScrollContainer = toga.ScrollContainer()

        main_box = toga.Box()
        plot_box = toga.Box()

        main_box.style.padding = 10
        main_box.style.update(alignment=CENTER)
        main_box.style.update(direction=COLUMN)
        
        button = toga.Button('Play', on_press=self.playback, style=Pack(width=100))

        GenerateSpectrum(self.filename) 
        image_from_path = toga.Image('Figure_temp.png')
        imageview_from_path = toga.ImageView(image_from_path)
        imageview_from_path.style.update(height=480)
        imageview_from_path.style.update(width=640)
        plot_box.add(imageview_from_path)
        
        main_box.add(button)
        main_box.add(plot_box)

        self.main_window.content = main_box


        self.main_window.show()

def main():
    return SpectrumApp('Spectrum', 'org.spectrum')


if __name__ == '__main__':
    app = main()
    app.loadAudio('../resources/laurel8k.wav')
    app.main_loop()
