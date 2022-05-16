# OMes - Object Measure

A Python program to measure object size from camera.

### Install useful packages
```console
foo@bar:~$ pip install opencv-python pillow tkinter
```

### Changes to make before you use OMes
Make sure to place a square paper or any object to the left most of the camera's FOV 
and insert its dimension in code. put the dimension of reference object in ```self.size```.
```python
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("1400x700")
        self.video_source = video_source
        self.size = 450, 450
```

Default ```video_source``` is set to zero but if you are using an external webcam change this to 1.


### Run the script

```console
foo@bar:~$ python main.py
```
