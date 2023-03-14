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
    global img

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
        self.loaded_image = ip.get_ROI(img)
        
        # display image
        w, h = self.loaded_image.shape[:2]
        self.cnv_loaded_image.config(width = w + 50, height = h + 50)
        self.loaded_image_to_display = Image.fromarray(self.loaded_image)
        self.loaded_image_to_display = ImageTk.PhotoImage(self.loaded_image_to_display)
        self.cnv_loaded_image.create_image(0, 0, image = self.loaded_image_to_display, anchor = "nw")

        # activate process image button
        self.btn_process_image.configure(state = "normal")

    def btn_process_image_clicked(self):
        # process loaded image
        processed_image = ip.segmentation(self.loaded_image)
        processed_image = ip.morphological_closing_and_opening(processed_image)
        
        # display processed image
        w, h = processed_image.shape[:2]
        self.cnv_processed_image.config(width = w + 50, height = h + 50)
        self.processed_image_to_display = Image.fromarray(processed_image)
        self.processed_image_to_display = ImageTk.PhotoImage(self.processed_image_to_display)
        self.cnv_processed_image.create_image(0, 0, image = self.processed_image_to_display, anchor = "nw")

        # getting the image length
        px_length = ip.horizontal_image_projection(processed_image, threshold = 20)
        length_scaling_factor = ip.get_length_scaling_factor()
        actual_length = int(length_scaling_factor * px_length)

        # getting the image outer diameter
        px_od = ip.vertical_image_projection(processed_image, threshold = 20)
        od_scaling_factor = ip.get_od_scaling_factor()
        actual_od = int(od_scaling_factor * px_od)

        # report generation
        self.lbl_acquired_length.configure(state = "normal", text = actual_length)
        self.lbl_acquired_outer_diameter.configure(state = "normal", text = actual_od)


if __name__ == "__main__":
    app = ThesisGuiApp()
    app.run()