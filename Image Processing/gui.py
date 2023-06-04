# !/usr/bin/python3
import pathlib
import pygubu
import math
import image_processing as ip
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
        self.loaded_image = image = Image.open(address)

        #preprocessing
        w, h = image.size
        new_h, new_w = int(h / 5), int(w / 5)
        img = image.resize((new_w, new_h))
        temp_img = ip.np.asarray(img)

        # display image
        ip.cv2.imshow("Loaded Image", temp_img);

        #ROI
        self.loaded_image = ip.get_ROI(temp_img)

        # display extracted ROI image
        ip.cv2.imshow("ROI Extracted Image", self.loaded_image)

        # activate process image button
        self.btn_process_image.configure(state = "normal")

    def btn_process_image_clicked(self):
        # process loaded image
        self.loaded_image = processed_image = ip.morphological_closing_and_opening(ip.segmentation(self.loaded_image))

        # display processed image
        ip.cv2.imshow("Processed Image", processed_image)

        # getting the image length
        px_length = ip.vertical_image_projection(processed_image)
        length_scaling_factor = ip.CONST_HSCALING
        actual_length = math.floor(length_scaling_factor * px_length)

        # getting the image outer diameter
        px_od = ip.horizontal_image_projection(processed_image)
        od_scaling_factor = ip.CONST_ODSCALING
        actual_od = math.floor(od_scaling_factor * px_od)

        # report generation
        self.lbl_acquired_length.configure(state = "normal", text = actual_length)
        self.lbl_acquired_outer_diameter.configure(state = "normal", text = actual_od)
        self.lbl_acquired_volume.configure(state = "normal", text = ip.identify_volume(length = actual_length, od = actual_od))

if __name__ == "__main__":
    app = ThesisGuiApp()
    app.run()