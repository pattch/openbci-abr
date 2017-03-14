from plugins.toneplayer import TonePlayer as tp
import random

class ToneHandler():
    def __init__(self):
        self.tone = tp()
        self.tone.openPlayer()
        self.frequencies = [
            32,
            64,
            125,
            250,
            500,
            1000,
            2000,
            4000,
            8000,
            16000
        ]
        self.tone.initWaves(self.frequencies)

    def playTone(self, fr = None):
        if not fr:
            fr = random.choice(self.frequencies)
        self.tone.play(fr)

    def close(self):
        self.tone.closePlayer()

    def getToneLength(self):
        return self.tone.LENGTH