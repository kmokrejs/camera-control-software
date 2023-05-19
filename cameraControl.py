import subprocess
import datetime
import cv2 as cv

class CamControl:
    
    # Initializes the class
    def __init__(self):
        pass
    
    # Detects the camera connected and returns their names and ports
    def detect_camera(self):
            cmd = [ 'gphoto2', '--auto-detect']
            output = subprocess.check_output(cmd)    
            output = output.decode('utf-8')
            lines = output.splitlines()

            camera_lines = []

            for line in range(2,len(lines)):
                camera_lines.append(lines[line])
                
            camera_names = []
            camera_ports = []

            for line in camera_lines:
                parts = line.split()
                name = ' '.join(parts[:-1])
                port = parts[-1]
                camera_names.append(name)
                camera_ports.append(port)

            return camera_names, camera_ports

    # Gets the settings for a specific port and setting
    def get_settings(self, port, settings=str):
            # Input: port (str) - the port where the camera is connected
            # settings (str) - the settings to get from the camera
            
            cmd = [ 'gphoto2', '--port', port, '--get-config='+settings]
            result = subprocess.check_output(cmd)
            dsettings_values=[]

            for line in result.decode('utf-8').split('\n'):
                if line.startswith('Choice:'):
                    parts = line.split()
                    temp = []
                    for part in range(2,len(parts)):
                        temp.append(parts[part])
                    
                    temp = ' '.join(temp)
                    dsettings_values.append(temp)

            return dsettings_values
    
    # Gets the current settings for a specific port and setting
    def current_settings(self, port, settings=str):
        # Input: port (str) - the port where the camera is connected
        # settings (str) - the settings to get from the camera
        
        cmd = [ 'gphoto2', '--port', port, '--get-config='+settings]
        result = subprocess.check_output(cmd)
        current_settings = ''

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Current:'):
                parts = line.split()
                temp = []
                for part in range(1,len(parts)):
                    temp.append(parts[part])
                
                temp = ' '.join(temp)
                current_settings = temp

        return current_settings
    
    # Sets a specific setting for a specific port
    def set_settings(self, port, settings=str, settings_value=str):
        # Input: port (str) - the port where the camera is connected
        # settings (str) - the settings to set on the camera
        # settings_value (str) - the value to set for the settings
        
        cmd = [ 'gphoto2', '--port', port, '--set-config', settings+'='+settings_value]
        subprocess.run(cmd)

    # Takes a picture and saves it to a specific path with a specific name
    def take_picture(self, path=str, photo_name=str):
        # Input: path (str) - the path where the photo will be saved
        # photo_name (str) - the name to give the photo
        
        date = datetime.datetime.now()
        now = [str(date.day), str(date.month), str(date.microsecond)]
        now = '_'.join(now)
        cmd = [ 'gphoto2', '--capture-image-and-download', '--filename', path+'/'+photo_name+'_'+now]

        subprocess.run(cmd)

    # Takes a picture in HDR and saves it to a specific path with a specific name
    def take_picture_hdr(self, path=str, photo_name=str):
        # Input: path (str) - the path where the photo will be saved
        # photo_name (str) - the name to give the photo
        
        cmd = [ 'gphoto2', '--capture-image-and-download', '--filename', path+'/'+photo_name]
        subprocess.run(cmd)

    # Displays a live view from a specific camera 
    def live_view(self, camera_num):
        # Input: camera_num (int) - the number of the camera to view
        
        cap = cv.VideoCapture(camera_num)
        if not cap.isOpened():
            raise IOError("Cannot open webcam")

        while True:
            ret, frame = cap.read()
            if frame is None:
                print("Picture not found. Chceck camera index or camera connection.")
                break
            frame = cv.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv.INTER_AREA)
            cv.imshow('Live View', frame)
            c = cv.waitKey(1)
            if c == 27:
                break
        cap.release()
        cv.destroyAllWindows()  
