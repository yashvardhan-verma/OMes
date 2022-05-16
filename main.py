import tkinter
import PIL.Image
import PIL.ImageTk
import cv2
import height_width_detector


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("1400x700")
        self.video_source = video_source
        self.size = 450, 450

        self.vid = MyVideoCapture(self.video_source)

        # live Video feed canvas
        self.canvas = tkinter.Canvas(window, width=self.size[0], height = self.size[1])
        self.canvas.place(x = 10, y = 10)

        # Drag and Drop
        # self.variable = tkinter.StringVar(self.window)
        # self.options = ["0", "1", "2", "3"]
        # self.variable.set(self.options[0])
        # self.camera_drop_down = tkinter.OptionMenu(self.window, self.variable, *self.options)
        # self.camera_drop_down.place(x = 40, y = 500)

        # Snapshot Button
        self.btn_snapshot = tkinter.Button(window, text="Snapshot", width=50, command = self.snapshot)
        self.btn_snapshot.place(x = 20, y = 400)

        # To Show Height
        self.l_height = tkinter.Label(text="Height :  ")
        self.d_height = tkinter.Label(self.window)
        self.l_height.place(x=500, y=400)
        self.d_height.place(x=600, y=400)

        # To Show Width
        self.l_width = tkinter.Label(text="Width :  ")
        self.d_width = tkinter.Label(self.window)
        self.l_width.place(x=500, y=420)
        self.d_width.place(x=600, y=420)

        # To Show Number Of Objects
        self.l_number = tkinter.Label(text="Number of object :  ")
        self.num_object = tkinter.Label(self.window)
        self.l_number.place(x=500, y=440)
        self.num_object.place(x=600, y=440)

        # Shows Current Camera
        self.current_cam = tkinter.Label(text="Current Camera : ")
        self.val_current_cam = tkinter.Label(self.window)
        self.current_cam.place(x=500, y=460)
        self.val_current_cam.place(x=600, y=460)

        self.delay = 15
        self.update()
        self.window.mainloop()

        # for showing image.
    def render_image(self, image, X, Y):
        load = PIL.Image.open(image) # Opening Image
        load.thumbnail(self.size, PIL.Image.ANTIALIAS) # Fitting Image to Frame Size
        render = PIL.ImageTk.PhotoImage(load)
        img = tkinter.Label(self.window, image=render) # Showing Rendered Image side to the Live Feed
        img.image = render
        img.place(x=X, y=Y)

        # Printing Dimension of First object
    def show_dimension(self):
        dimension_list = height_width_detector.height_width("frame-current.jpg")
        self.num_object.config(text=len(dimension_list))
        self.d_width.config(text=dimension_list[0][1])
        self.d_height.config(text=dimension_list[0][0])

    def snapshot(self):  # take a snapshot, a driver function for most of working
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite('frame-current.jpg', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            height_width_detector.height_width("frame-current.jpg") # finding contours
            self.render_image("frame-contours.jpg", 1000, 10) # writing image with contours
            self.show_dimension()

    # Driver Function for next Frame
    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.Image.fromarray(frame)
            self.photo.thumbnail(self.size, PIL.Image.ANTIALIAS)
            self.photo = PIL.ImageTk.PhotoImage(self.photo)
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        self.window.after(self.delay, self.update)

    # def get_height_and_weight(self):
    #     print(height_width_detector.height_width("frame-current.jpg"))

class MyVideoCapture:
    def __init__(self, video_source):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

App(tkinter.Tk(),"Height and Weight", 0)



