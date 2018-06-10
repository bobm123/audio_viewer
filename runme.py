

"""A simple script that brings up the giu app"""

from audio_viewer.audio_viewer import main
app = main()
app.loadAudio('resources/laurel8k.wav')
app.main_loop()