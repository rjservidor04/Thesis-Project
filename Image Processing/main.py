import view

 # creating a  main window for the application
windows = view.Tk()
windows.title("Automatic Dimension Measurement of Griffin Beakers")
windows.geometry("900x500")

# initializing elements inside the windows
captured_label = view.Label(windows,text="Captured Image", font=('Ariel', 22, 'bold'), fg='white')
processed_label = view.Label(windows,text="Processed Image", font=('Ariel', 22, 'bold'), fg='white')
canvas = view.Canvas(windows, height=400, width=200)
label = view.Label(windows)

btnOpenImage = view.Button(windows, text="Open file", width=12, command=view.openDialog)
btnOpenImage.place(x=70,y=60)

btnProcessImage = view.Button(windows, text="Process Image", width=12, command=lambda: view.processImage(view.image), state=view.DISABLED)
btnProcessImage.place(x=70,y=95)

windows.mainloop()