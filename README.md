# **Camera Control Software**

This project provides a software interface for controlling DSLR cameras using the gphoto2 library. It includes a graphical user interface (GUI) to facilitate interaction with the camera.

### **Components**
gui.py: This file contains the code for the GUI that controls the camera. It allows the user to change various camera settings and modes, and also view live output from the camera.
CameraControl.py: This file defines a class that uses gphoto2 command-line commands to communicate with the camera.

### **Usage**
To use this software, run gui.py to open the GUI. From the GUI, you can select your camera, change its settings, and view its output.

### **Known Issues**
After changing the modes of the camera or selecting a new camera, the GUI may freeze. This is due to the time-consuming process of changing modes and detecting the camera. Please be patient during this process.
The live view operates like continuous imaging, which results in a slow frame rate. This aspect of the software is still under development and may contain bugs.

### **Development Status**
This software is currently under development, so it may be improved and updated over time. Check back for updates, and feel free to contribute to the project if you can!
