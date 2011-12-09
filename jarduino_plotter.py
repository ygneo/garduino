import numpy as stats
import matplotlib
matplotlib.use('Agg')
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

class JarduinoPlotter(object):

    def __init__(self, description="Sand moisture read from Arduino"):
        self.data = []
        self.description = description 

    def add(self, value):
        self.data.append({'timestamp': time.time(), 'value': value})

    def plot(self, filename="plot.png"):
        # def ms_to_sec(x, pos):
        #     return x/<sec>
        # if folder and not os.path.exists (folder):
        #     raise IOError("folder '%s' not found" % folder)
        fig = plt.figure()

        #formatter = ticker.FuncFormatter(ms_to_sec)

        ax1 = fig.add_subplot(111)
        x = [d['timestamp'] for d in self.data]
        y = [d['value'] for d in self.data]
        ax1.plot(x, y)
        ax1.set_ylabel('Sand conductivity')
        ax1.set_xlabel("Time (s)")
        #ax1.xaxis.set_major_formatter(formatter)

        fig.suptitle("%s" % self.description, fontsize=8)
        filepath = os.path.join("./", "%s.png" % filename)
        plt.savefig(filepath, format="png")
        return
    
