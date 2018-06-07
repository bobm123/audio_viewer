
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import pyaudio  
import toga
from toga.style.pack import *
import wave 


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



class SpectrumApp(toga.App):


    filename = "laurel8k.wav"
    file = wave.open(filename, "rb")
    paud = pyaudio.PyAudio()
    format = paud.get_format_from_width(file.getsampwidth())
    #open stream  
    stream = paud.open(format = format,  
                    channels = file.getnchannels(),  
                    rate = file.getframerate(),  
                    output = True)

    def playback(self, widget):
        chunk = 1024

        print("play")
        self.file.rewind()
        data = self.file.readframes(chunk)  
        while data:
            self.stream.write(data)  
            data = self.file.readframes(chunk)

    def actionOpenFileDialog(self, widget):
        try:
            fname = self.main_window.open_file_dialog(
                title="Open Audio File",
            )
            self.label.text = "File to open:" + fname
        except ValueError:
            self.label.text = "Open file dialog was canceled"

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name, size=(720, 580))
        self.ScrollContainer = toga.ScrollContainer()

        plot_box = toga.Box()

        button = toga.Button('Play', on_press=self.playback, style=Pack(width=100))

        GenerateSpectrum(self.filename) 
        image_from_path = toga.Image('Figure_temp.png')
        imageview_from_path = toga.ImageView(image_from_path)
        imageview_from_path.style.update(height=480)
        imageview_from_path.style.update(width=640)
        plot_box.add(imageview_from_path)
        
        self.things = toga.Group('File')

        cmdOpen = toga.Command(
            self.actionOpenFileDialog,
            label='Open',
            tooltip='Open Audio File',
            group=self.things
        )

        self.commands.add(cmdOpen)

        # Label to show responses.
        self.label = toga.Label('Ready.')

        # Outermost box
        outer_box = toga.Box(
            children=[self.label, button, plot_box],
            style=Pack(
                flex=1,
                direction=COLUMN,
                alignment=CENTER,
                padding=10
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        self.main_window.show()

def main():
    return SpectrumApp('Spectrum', 'org.spectrum')


if __name__ == '__main__':
    app = main()
    app.main_loop()
