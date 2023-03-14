# !/usr/bin/python3
import pathlib
import pygubu
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

    def run(self):
        self.mainwindow.mainloop()

    def btn_load_image_clicked(self):
        pass

    def btn_process_image_clicked(self):
        pass


if __name__ == "__main__":
    app = ThesisGuiApp()
    app.run()
