import plugin_interface as plugintypes
# from plugins.toneplayer import TonePlayer as tp
from plugins.tonehandler import ToneHandler as th

class PluginTone(plugintypes.IPluginExtended):
    def activate(self):
        print "Tone Activated"
        self.timer = 0
        self.batch = {}
        self.tone = th()
        # self.tone = tp()
        # self.tone.openPlayer()
        self.wait_time = 1 # Seconds to wait in between samples
        self.wait_length = 125 * self.wait_time
        # Length to play the tone plus 0.3 seconds - board samples at 125Hz
        self.window_length = int((self.tone.getToneLength() * 125) + (0.3 * 125))
        self.label = 0
        self.waiting = False
        self.filename = 'out.txt'

    def __call__(self, sample):
        if sample:
            if not self.waiting:
                sample_data = sample.channel_data
                for i in range(len(sample_data)):
                    sample = sample_data[i]
                    if i in self.batch and self.batch[i]:
                        self.batch[i].append(sample)
                    else:
                        self.batch[i] = [sample]
                # print '\t'.join([str(x) for x in sample_data]) + '\t' + str(self.label)
                # self.batch.extend(sample_data)

            self.timer += 1

            # Wait for P300 etc in between samples
            if self.waiting and self.timer >= self.wait_length:
                self.handleFinishedWait()
            # Play a tone and record ABR
            elif not self.waiting and self.timer >= self.window_length:
                self.handleFinishedBatch()

    def handleFinishedBatch(self):
        # Whether this batch occured when we played a tone
        # Format of output: CHANNEL_NUM:num \t num \t num,...,label:num
        # self.batch.append(self.label)
        samplestr = []
        for channel, sample_batch in self.batch.iteritems():
            samplestr.append(str(channel) + ':' + '\t'.join([str(sample) for sample in sample_batch]))
        samplestr = ','.join(samplestr)
        samplestr += ',label:' + str(self.label) + '\n'
        print samplestr
        with open(self.filename, "a") as f:
            f.write(samplestr)
        self.batch = {}
        self.timer = 0
        self.waiting = True

        # Play tone or don't play tone
        if self.label == 0:
            self.tone.playTone()
            self.label = 1
        else:
            self.label = 0

    def handleFinishedWait(self):
        self.batch = {}
        self.timer = 0
        self.waiting = False
