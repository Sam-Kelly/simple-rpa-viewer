#!/bin/python
from tkinter import *
import rpatool
import PIL.Image as Image
import PIL.ImageTk as ImageTk
import sys
import io

class Viewer():

	def __init__(self):

		self.rpa = rpatool.RenPyArchive(sys.argv[1])

		root = Tk()
		self.listbox = Listbox(root, width=80)
		self.listbox.pack(side = LEFT, fill = BOTH)
		self.listbox.bind("<<ListboxSelect>>", self.onselect)
		self.listbox.bind("<KeyPress>", self.on_key_press)
		scrollbar = Scrollbar(root)
		scrollbar.pack(side = LEFT, fill = BOTH)
		for values in self.get_fpaths():
			self.listbox.insert(END, values)
		self.listbox.config(yscrollcommand = scrollbar.set)
		scrollbar.config(command = self.listbox.yview)
		self.label = Label(root)
		self.label.pack(side=LEFT, fill=BOTH)
		  
		root.mainloop()

	def get_fpaths(self):
		paths = [i for i in self.rpa.indexes.keys()]
		paths.sort()
		return paths

	def scale_im(self, image):
		# this function should work out how much to downscale an image so it fits 1280x720?
		height = image.height
		width = image.width
		goal_height = 720
		goal_width = 1280
		if height <= goal_height and width <= goal_width:
			pass
		else:
			scale_width = goal_width/width
			scale_height = goal_height/height

			scale_val = min(scale_width, scale_height)
			new_width = int(scale_val * width)
			new_height = int(scale_val * height)

			image = image.resize((new_width, new_height))
		return image


	def show_image(self, fname):
		f = self.rpa.read(fname)
		f = io.BytesIO(f)
		try:
			im = Image.open(f)
		except:
			print("failed to open with PIL", file=sys.stderr)
			return
		pilImage = self.scale_im(im)
		self.new_image = ImageTk.PhotoImage(pilImage)
		self.label.config(image=self.new_image)

	def onselect(self, event):
		index = event.widget.curselection()
		fpath = event.widget.get(index)
		self.show_image(fpath)

	def on_key_press(self, event):
		if event.char not in ('j', 'k'):
			return
		index = self.listbox.curselection()[0]
		self.listbox.selection_clear(0, END)
		if index == ():
			index = 0
		if event.char == "j":
			new_index = index + 1
		if event.char == "k":
			new_index = index - 1
		self.listbox.selection_set(new_index)
		self.listbox.see(new_index)
		self.listbox.event_generate("<<ListboxSelect>>")
		return	

Viewer()

