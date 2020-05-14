# Main Nebulae Source File
import ctcsound
import controlhandler as ch
import conductor
#import ui
import time
import threading
from Tkinter import *
import sys


# Test instrs
#instr = "a_granularlooper"
instr = "c_synth"
dir = "."

if len(sys.argv) == 1 : 
    print "usage:"
    print "python2 nebulae.py instrname [home dir]"
    print "home dir : where instr and audio folders live, defaults to current dir"
    sys.exit(-1)

if len(sys.argv) > 1 : 
    instr = sys.argv[1]


print "Instrument :" + instr

orc_handle = conductor.Conductor() # Initialize Audio File Tables and Csound Score/Orchestra

if len(sys.argv) > 2 : 
    dir = sys.argv[2]
    orc_handle.set_home_dir(dir)

orc_handle.generate_orc(instr)
configData = orc_handle.getConfigDict()
c = ctcsound.Csound()    # Create an instance of Csound
#c.setOption("-iadc") # Get this back in the game for local
c.setOption("-odac")  # Set option for Csound
c.setOption("-b1024") # More Conservative buffer
c.setOption("-B2048") # More Conservative buffer
#c.setOption("-b128") # Liberal Buffer
#c.setOption("-B256") # Liberal Buffer
#c.setOption("-+rtaudio=alsa") # Set option for Csound
#c.setOption("--sched")
c.setOption("-m7")  # Set option for Csound
c.compileOrc(orc_handle.curOrc)     # Compile Orchestra from String
c.readScore(orc_handle.curSco)     # Read in Score generated from notes 
c.start() # Start Csound

c_handle = ch.ControlHandler(c, orc_handle.numFiles(), configData) # Create handler for all csound comm.
#ui = ui.UserInterface(c_handle) # Create User Interface
pt = ctcsound.CsoundPerformanceThread(c.csound()) # Create CsoundPerformanceThread 
pt.play() # Begin Performing the Score in the perforamnce thread
c_handle.updateAll() # Update all values to ensure their at their initial state.

## Abstract these classes away when possible.
class SliderWrapper(object):
    def __init__(self, csound, channelName, slider):
        self.slider = slider
        self.name = channelName

    def update(self):
        val = self.slider.get()
        c_handle.channeldict[self.name].setValue(val)

class Application(Frame):
    def __init__(self, master=None):
        master.title("Nebulae Instr Tester")
        self.items = []
        self.notes = []
        Frame.__init__(self,master,width=1000,height=1000)
        self.grid()
        self.createUI()
        self.master.protocol("WM_DELETE_WINDOW",self.quit)

    def createUI(self):
        tick_size = 1.0/4096.0
        self.size = 600
        self.canvas = Canvas(self, height=self.size, width=self.size)
        self.canvas.grid(row=0, column=0)
        # Start
        self.startSlider = Scale(self.canvas, from_=0.0, to=1.0, resolution=tick_size, command=self.updateControls, label="Start")
        self.startSlider.grid(row=1,column=1)
        self.startSlider.set(c_handle.getValue("start"))
        self.startUpdater = SliderWrapper(c, "start", self.startSlider)
        # Size
        self.sizeSlider = Scale(self.canvas, from_=0.0, to=1.0, resolution=tick_size, command=self.updateControls, label="Size")
        self.sizeSlider.grid(row=1,column=3)
        self.sizeSlider.set(c_handle.getValue("size"))
        self.sizeUpdater = SliderWrapper(c, "size", self.sizeSlider)
        # Blend
        self.blendSlider = Scale(self.canvas, from_=0.0, to=1.0, resolution=tick_size, command=self.updateControls, label="Blend")
        self.blendSlider.grid(row=3,column=1)
        self.blendSlider.set(c_handle.getValue("blend"))
        self.blendUpdater = SliderWrapper(c, "blend", self.blendSlider)
        # Density
        self.densitySlider = Scale(self.canvas, from_=0.0, to=1.0, resolution=tick_size, command=self.updateControls, label="Density")
        self.densitySlider.grid(row=2,column=1)
        self.densitySlider.set(c_handle.getValue("density"))
        self.densityUpdater = SliderWrapper(c, "density", self.densitySlider)
        # Overlap
        self.overlapSlider = Scale(self.canvas, from_=0.0, to=1.0, resolution=tick_size, command=self.updateControls, label="Overlap")
        self.overlapSlider.grid(row=2,column=3)
        self.overlapSlider.set(c_handle.getValue("overlap"))
        self.overlapUpdater = SliderWrapper(c, "overlap", self.overlapSlider)
        # Window
        self.windowSlider = Scale(self.canvas, from_=0.0, to=1.0, resolution=tick_size, command=self.updateControls, label="Window")
        self.windowSlider.grid(row=3,column=3)
        self.windowSlider.set(c_handle.getValue("window"))
        self.windowUpdater = SliderWrapper(c, "window", self.windowSlider)
        # Speed
        self.speedSlider = Scale(self.canvas, from_=0.0, to=1.0, resolution=tick_size, command=self.updateControls, label="Speed")
        self.speedSlider.grid(row=2,column=2)
        self.speedSlider.set(c_handle.getValue("speed"))
        self.speedUpdater = SliderWrapper(c, "speed", self.speedSlider)
        # Pitch
        self.pitchSlider = Scale(self.canvas, from_=0.0, to=1.0, resolution=tick_size, command=self.updateControls, label="Pitch")
        self.pitchSlider.grid(row=1,column=2)
        self.pitchSlider.set(c_handle.getValue("pitch"))
        self.pitchUpdater = SliderWrapper(c, "pitch", self.pitchSlider)
        # Freeze
        self.freezeButtonState = IntVar()
        self.freezeButton = Checkbutton(self.canvas, text="Freeze", var=self.freezeButtonState, command=self.handleFreeze)
        self.freezeButton.grid(row=4,column=3)
        # Reset
        self.resetButton = Button(self.canvas, text="Reset", command=self.handleReset)
        self.resetButton.grid(row=4,column=2)
        # Next
        self.nextButton = Button(self.canvas, text="Next", command=self.handleNext)
        self.nextButton.grid(row=4,column=1)
        # Source
        self.sourceButtonState = IntVar()
        self.sourceButton = Checkbutton(self.canvas, text="Source", var=self.sourceButtonState, command=self.handleSource)
        self.sourceButton.grid(row=4,column=4)
        # Source
        self.recordButtonState = IntVar()
        self.recordButton = Checkbutton(self.canvas, text="Record", var=self.recordButtonState, command=self.handleRecord)
        self.recordButton.grid(row=4,column=5)

    def updateControls(self, val):
        self.startUpdater.update()
        self.sizeUpdater.update()
        self.blendUpdater.update()
        self.densityUpdater.update()
        self.overlapUpdater.update()
        self.windowUpdater.update()
        self.speedUpdater.update()
        self.pitchUpdater.update()
        c_handle.updateAll()

    def handleRecord(self):
        print "Handling Record!"
        c_handle.channeldict["record"].setValue(self.recordButtonState.get())
        c_handle.updateAll()

    def handleFreeze(self):
        print "Handling Freeze!"
        c_handle.channeldict["freeze"].setValue(self.freezeButtonState.get())
        c_handle.updateAll()

    def handleReset(self):
        print "Handling Reset!"
        c_handle.channeldict["reset"].setValue(1)
        c_handle.updateAll()
        c_handle.channeldict["reset"].setValue(0)

    def handleNext(self):
        print "Handling Next!"
        cur_file = c_handle.getValue("file")
        cur_file += 1
        if cur_file >= c_handle.numFiles:
            cur_file = 0
        c_handle.channeldict["file"].setValue(cur_file)
        c_handle.updateAll()
        print "Current file index: " + str(cur_file)

    def handleSource(self):
        print "Handling Source!"
        c_handle.channeldict["source"].setValue(self.sourceButtonState.get())
        c_handle.updateAll()

    def quit(self):
        self.master.destroy()
        pt.stop()
        pt.join()

app = Application(Tk())
app.mainloop()
c.stop
del c
