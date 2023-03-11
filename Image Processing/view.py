import image_processing as ip
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk

def processImage(image):
    global display_image
    global canvas
    global processed_label
    # process image here

    img = ImageTk.getimage(image)
    w, h = img.size

    # convert Image to np array
    processed_img = ip.np.asarray(img)
    # processed_img = ip.to_grayscale(processed_img)
    processed_img = ip.get_ROI(processed_img)

    ip.cv2.imshow('ROI', processed_img)
    ip.cv2.waitKey(0)
    ip.cv2.destroyAllWindows()

    # segmented image
    processed_img = ip.segmentation(processed_img)
   
    # image after morphological operations
    processed_img = ip.morphological_closing_and_opening(processed_img)
    
    # convert np array to PIL image to display
    temp_img = Image.fromarray(processed_img)
    display_image = ImageTk.PhotoImage(temp_img)

    # getting the height
    pixel_height = ip.vertical_image_projection(processed_img, 50)
    h_scalar_factor = ip.get_length_scaling_factor()
    height = round(pixel_height * h_scalar_factor, 2)
    f_height = int(height * 10)

    #getting the diameter
    pixel_diameter = ip.horizontal_image_projection(processed_img, 50)
    d_scalar_factor = ip.get_od_scaling_factor()
    diameter = round(pixel_diameter * d_scalar_factor, 2)
    f_diameter = int(diameter*10)

    # display image
    processed_label.destroy()
    processed_label = Label(windows,text="Processed Image", font=('Ariel', 22, 'bold'))
    processed_label.place(x=(w+(w/2)+225), y=7)

    label = Label(windows, image = display_image, width=w, height=h)
    label.place(x=(w+340),y=50)

    btnOpenImage = Button(windows, text="Open file", width=12, command=openDialog)
    txt_height =  str(f_height) + " mm"
    txt_diameter =  str(f_diameter) + " mm"
    # actual_h = "Actual Height: " + str(245)
    # actual_d = "Actual Diameter: " + str(245)

    # report generation
    canvas.delete("all") 
    canvas = Canvas(windows, height=150, width=200)
    canvas.place(x=20, y=133)
    canvas.create_rectangle(5, 5, 200, 150, outline='black')
    canvas.create_text(100,20, text="Report", font=('Ariel', 18, 'bold'))

    canvas.create_text(51, 60, text="Height: ", font=('Ariel', 12))
    canvas.create_text(100, 60, text=txt_height, font=('Ariel', 12 ))
    canvas.create_text(60, 80, text="Diameter: ", font=('Ariel', 12 ))
    canvas.create_text(120, 80, text=txt_diameter, font=('Ariel', 12 ))
    
   

def openDialog():
    global windows
    global image
    global btnOpenImage
    global btnProcessImage
    global captured_label
    global processed_label
    global label

    address = filedialog.askopenfilename(title="Select file", 
    filetypes= (("Images", ("*.jpg", "*.png", "*.bmp")), ("All Items", "*.*")))

    img = Image.open(address)
    w, h = img.size
    new_w, new_h = int(w/2), int(h/2)
    img = img.resize((new_w, new_h))
    image = ImageTk.PhotoImage(img)

    canvas.delete("all")
    captured_label.destroy()
    label.destroy()
    processed_label.destroy()

    captured_label = Label(windows,text="Captured Image", font=('Ariel', 22, 'bold'))
    captured_label.place(x=((new_w/2)+140), y=7)
  
    label = Label(windows, image = image, width=(new_w), height=(new_h))
    label.place(x=250,y=50)

    btnProcessImage.config(state = NORMAL)
    btnProcessImage = Button(windows, text="Process Image", width=12, command=lambda: processImage(image), state=NORMAL)
    btnOpenImage = Button(windows, text="Open file", width=12, command=openDialog)
    

 # creating a  main window for the application
windows = Tk()
windows.title("Automatic Dimension Measurement of Griffin Beakers")
windows.geometry("900x1300")

# initializing widgets inside the windows
captured_label = Label(windows,text="Captured Image", font=('Ariel', 22, 'bold'), fg='white')
processed_label = Label(windows,text="Processed Image", font=('Ariel', 22, 'bold'), fg='white')
canvas = Canvas(windows, height=400, width=200)
label = Label(windows)

btnOpenImage = Button(windows, text="Open file", width=12, command=openDialog)
btnOpenImage.place(x=70,y=60)

btnProcessImage = Button(windows, text="Process Image", width=12, command=lambda: processImage(image), state=DISABLED)
btnProcessImage.place(x=70,y=95)


windows.mainloop()