from tkinter import *

root = Tk()

frametop = Frame(root)
framebottom = Frame(root)
frameleft = Frame(framebottom)
frameright = Frame(framebottom)

text = Text(frametop)
scroll = Scrollbar(frametop, command=text.yview)
btn1 = Button(frameleft, text="Course")
btn2 = Button(frameleft, text="Abscences")
btn3 = Button(frameright, text="Notes")
btn4 = Button(frameright, text="Return")

text['yscrollcommand'] = scroll.set

frametop.pack(side=TOP, fill=BOTH, expand=1)
framebottom.pack(side=BOTTOM, fill=BOTH, expand=1)
frameleft.pack(side=LEFT, fill=BOTH, expand=1)
frameright.pack(side=RIGHT, fill=BOTH, expand=1)

text.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
scroll.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5, expand=1)
btn1.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
btn2.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5, expand=1)
btn3.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
btn4.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5, expand=1)

root.mainloop()