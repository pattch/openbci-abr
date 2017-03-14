import math
from pyaudio import PyAudio
import atexit

# TonePlayer object plays tones when told to do so
class TonePlayer():
    def __init__(self):
        # self.PyAudio = pyaudio.PyAudio

        #See http://en.wikipedia.org/wiki/Bit_rate#Audio
        self.BITRATE = 320000    #number of frames per second/frameset.

        self.FREQUENCY = 500    #Hz, waves per second, 261.63=C4-note.
        self.LENGTH = 0.18       #seconds to play sound

        if self.FREQUENCY > self.BITRATE:
            self.BITRATE = self.FREQUENCY+100

        self.NUMBEROFFRAMES = int(self.BITRATE * self.LENGTH)
        self.RESTFRAMES = self.NUMBEROFFRAMES % self.BITRATE
        self.WAVEDATA = ''
        self.ZEROBIAS = 128
        atexit.register(self.closePlayer)

    def setBitrate(self, br):
        self.BITRATE = br
        if self.FREQUENCY > self.BITRATE:
            self.BITRATE = self.FREQUENCY+100

        self.NUMBEROFFRAMES = int(self.BITRATE * self.LENGTH)
        self.RESTFRAMES = self.NUMBEROFFRAMES % self.BITRATE

    def openPlayer(self):
        self.p = PyAudio()
        self.stream = self.p.open(format = self.p.get_format_from_width(1),
                        channels = 1,
                        rate = self.BITRATE,
                        output = True)
        self.LATENCY = self.stream.get_output_latency()
        print(self.LATENCY)

    def renderWave(self,freq):
        amplitude = 127
        return self.renderWaveWithAmplitude(freq,amplitude)

    def renderWaveWithAmplitude(self,freq,amp):
        wave = ''
        # Build up waveform
        lim = 2000
        for x in xrange(self.NUMBEROFFRAMES):
            amplitude = amp
            if x <= lim:
                amplitude = int(amp * 1.0 * x / lim) # smooth opening
            # Start at num - lim => go to num => map to [1 to 0]
            if x >= self.NUMBEROFFRAMES - lim:
                amplitude = int(amp * (1 - (1.0 * (x - (self.NUMBEROFFRAMES - lim)) / lim))) # smooth closing
                # print(freq,x,amplitude)
            num = int(math.sin(x/((self.BITRATE/freq)/math.pi))*amplitude+self.ZEROBIAS)
            wave = wave+chr(num)

        # Build up silent frames
        for x in xrange(self.RESTFRAMES):
            # Smooth to absolute zero
            num = 0
            if x <= lim and lim <= self.RESTFRAMES:
                num = int(1.0 * self.ZEROBIAS * (lim - x) / lim)
            # print(self.RESTFRAMES,x,num)
            wave = wave+chr(num)

        return wave

    def renderWaves(self,frequencies):
        return [self.renderWave(freq) for freq in frequencies]

    def initWaves(self,frequencies):
        waves = self.renderWaves(frequencies)
        self.RENDEREDWAVES = {}
        for i in range(len(frequencies)):
            fr = frequencies[i]
            wave = waves[i]
            self.RENDEREDWAVES[fr] = wave

    def play(self, freq):
        self.FREQUENCY = freq
        wave = ''
        if not freq in self.RENDEREDWAVES:
            wave = self.renderWave(freq)
        else:
            wave = self.RENDEREDWAVES[freq]
        # # Build up waveform
        # for x in xrange(self.NUMBEROFFRAMES):
        #     self.WAVEDATA = self.WAVEDATA+chr(int(math.sin(x/((self.BITRATE/self.FREQUENCY)/math.pi))*127+128))
        #
        # # Build up silent frames
        # for x in xrange(self.RESTFRAMES):
        #     self.WAVEDATA = self.WAVEDATA+chr(128)
        #
        # print self.RENDEREDWAVES
        # print wave
        self.stream.write(wave)
        self.WAVEDATA = wave

    def closePlayer(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()