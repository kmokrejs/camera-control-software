import subprocess
import datetime
import cv2 as cv

class CamControl:

    def __init__(self):
        pass

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
                # Rozdělení řádku na části podle mezer
                parts = line.split()

                # Získání názvu kamery a portu
                name = ' '.join(parts[:-1])
                port = parts[-1]
                    # Přidání názvu kamery a portu do příslušných seznamů
                camera_names.append(name)
                camera_ports.append(port)

            return camera_names, camera_ports


    def get_settings(self, port, settings=str):
            cmd = [ 'gphoto2', '--port', port, '--get-config='+settings]

            result = subprocess.check_output(cmd)

            dsettings_values=[]

            for line in result.decode('utf-8').split('\n'):
                if line.startswith('Choice:'):
                    parts = line.split()
                    temp = []
                    #if settings has more than 1 word, join them to one string
                    for part in range(2,len(parts)):
                        temp.append(parts[part])
                    
                    temp = ' '.join(temp)
                    dsettings_values.append(temp)

            return dsettings_values
    

    def current_settings(self, port, settings=str):

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
    

    def set_settings(self, port, settings=str, settings_value=str):

        cmd = [ 'gphoto2', '--port', port, '--set-config', settings+'='+settings_value]

        subprocess.run(cmd)


    def take_picture(self, path=str, photo_name=str):
        date = datetime.datetime.now()
        
        now = [str(date.day), str(date.month), str(date.microsecond)]

        now = '_'.join(now)

        cmd = [ 'gphoto2', '--capture-image-and-download', '--filename', path+'/'+photo_name+'_'+now]

        subprocess.run(cmd)

    def take_picture_hdr(self, path=str, photo_name=str):

        cmd = [ 'gphoto2', '--capture-image-and-download', '--filename', path+'/'+photo_name]

        subprocess.run(cmd)

    def live_view(self, camera_num):
        cap = cv.VideoCapture(camera_num)

        # Check if the webcam is opened correctly
        if not cap.isOpened():
            raise IOError("Cannot open webcam")

        while True:
            ret, frame = cap.read()
            if frame is None:
                print("Snímek nenalezen. Zkontrolujte index kamery nebo připojení kamery.")
                break
            frame = cv.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv.INTER_AREA)
            cv.imshow('Live View', frame)

            c = cv.waitKey(1)
            if c == 27:
                break

        cap.release()
        cv.destroyAllWindows()

# to-do: picturestyle, capture-movie <78s...>

    

