from Tkinter import *
import tkMessageBox

window = Tk()
window.wm_withdraw()

#centre screen message
window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
run = tkMessageBox.askyesno(title  = "Run Backup?", message = "It has been 24 hours since your last backup\nRun Backup Now?")

