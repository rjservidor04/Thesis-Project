# !/usr/bin/python3
import image_processing as ip
import pathlib
import pygubu
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "thesis_gui.ui"

class ThesisGuiApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("top", master)
        builder.connect_callbacks(self)

        self.cnv_loaded_image = builder.get_object("cnv_loaded_image")
        self.cnv_processed_image = builder.get_object("cnv_processed_image")
        self.btn_process_image = builder.get_object("btn_process_image")

        self.lbl_acquired_length = builder.get_object("lbl_acquired_length")
        self.lbl_acquired_outer_diameter = builder.get_object("lbl_acquired_outer_diameter")
        self.lbl_acquired_volume = builder.get_object("lbl_acquired_volume")

    def run(self):
        self.mainwindow.mainloop()

    def btn_load_image_clicked(self):
        # load image
        address = filedialog.askopenfilename(title="Select file", 
        filetypes= (("Images", ("*.jpg", "*.png", "*.bmp")), ("All Items", "*.*")))
        img = Image.open(address)
        w, h = img.size
        new_w, new_h = int(w/2), int(h/2)
        img = img.resize((new_w, new_h))
        self.loaded_image = ImageTk.PhotoImage(img)

        # display image
        self.cnv_loaded_image.config(width = new_w, height = new_h)
        self.cnv_loaded_image.create_image(0, 0, image = self.loaded_image, anchor = "nw")

        # activate process image button
        self.btn_process_image.configure(state = "normal")

    def btn_process_image_clicked(self):
        # process loaded image
        arr = ip.np.asarray(self.loaded_image)
        self.processed_image = ip.get_ROI(arr)
        self.processed_image = ip.segmentation(self.processed_image)
        self.processed_image = ip.morphological_closing_and_opening(self.processed_image)
        
        # display processed image
        self.cnv_processed_image.create_image(0, 0, image = self.processed_image, anchor = "nw")

        # getting the image length
        px_length = ip.vertical_image_projection(self.processed_image, threshold = 50)
        length_scaling_factor = ip.get_length_scaling_factor()
        actual_length = round(px_length * length_scaling_factor, 2)

        # getting the image outer diameter
        px_od = ip.horizontal_image_projection(self.processed_image, threshold = 50)
        od_scaling_factor = ip.get_od_scaling_factor()
        actual_od = round(px_od * od_scaling_factor, 2)

        # report generation
        self.lbl_acquired_length.configure(state = "normal", text = "" + actual_length)
        self.lbl_acquired_outer_diameter(state = "normal", text = "" + actual_od)


if __name__ == "__main__":
    app = ThesisGuiApp()
    app.run()