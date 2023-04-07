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
            

    def get_modes(self, port):
        cmd = [ 'gphoto2', '--port', port, '--get-config=autoexposuremode']

        result = subprocess.check_output(cmd)

        modes=[]

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Choice:'):
                parts = line.split()
                temp = []
                #if settings has more than 1 word, join them to one string
                for part in range(2,len(parts)):
                    temp.append(parts[part])
                
                temp = ' '.join(temp)
                modes.append(temp)

        return modes


    def set_mode(self, port, mode = str):

        cmd = [ 'gphoto2', '--port', port, '--set-config', 'autoexposuremode='+mode]

        subprocess.run(cmd)

        
    def current_mode(self, port):

        cmd = [ 'gphoto2', '--port', port, '--get-config=autoexposuremode']

        result = subprocess.check_output(cmd)

        mode = ''

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Current:'):
                parts = line.split()
                temp = []
                #if settings has more than 1 word, join them to one string
                if len(parts) >= 2:
                    for part in range(1,len(parts)):
                        temp.append(parts[part])
                else:
                    temp = parts

                temp = ' '.join(temp)
                mode = temp

        return mode
    
#-------------------------------------------------------------------------------------

    def get_iso_values(self, port):

        cmd = [ 'gphoto2', '--port', port, '--get-config=iso']

        result = subprocess.check_output(cmd)

        iso_values=[]

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Choice:'):
                parts = line.split()
                iso_values.append(parts[2])

        return iso_values


    def current_iso_value(self, port):

        cmd = [ 'gphoto2', '--port', port, '--get-config=iso']

        result = subprocess.check_output(cmd)

        iso_values=''

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Current:'):
                parts = line.split()
                iso_values = parts[1]

        return iso_values


    def set_iso(self, port, iso = str):

        cmd = [ 'gphoto2', '--port', port, '--set-config', 'iso='+iso]

        subprocess.run(cmd)

#-------------------------------------------------------------------------------------

    def get_whitebalance_values(self, port):

        cmd = [ 'gphoto2', '--port', port, '--get-config=whitebalance']

        result = subprocess.check_output(cmd)

        whitebalance_values= []

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Choice:'):
                parts = line.split()
                whitebalance_values.append(parts[2])

        return whitebalance_values


    def current_whitebalance_value(self, port):

        cmd = [ 'gphoto2', '--port', port, '--get-config=whitebalance']

        result = subprocess.check_output(cmd)

        whitebalance = ''

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Current:'):
                parts = line.split()
                whitebalance= parts[1]

        return whitebalance


    def set_whitebalance(self, port, balance = str):

        cmd = [ 'gphoto2', '--port', port,'--set-config', 'whitebalance='+balance]

        subprocess.run(cmd)

#-------------------------------------------------------------------------------------

    def get_aperture_values(self, port):

        cmd = [ 'gphoto2', '--port', port, '--get-config=aperture']

        result = subprocess.check_output(cmd)

        aperture_values= []

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Choice:'):
                parts = line.split()
                aperture_values.append(parts[2])

        return aperture_values


    def current_aperture_value(self, port):

        cmd = [ 'gphoto2', '--port', port, '--get-config=aperture']

        result = subprocess.check_output(cmd)

        aperture = ''

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Current:'):
                parts = line.split()
                aperture= parts[1]

        return aperture


    def set_aperture(self, port, aperture = int):

        cmd = [ 'gphoto2', '--port', port, '--set-config', 'aperture='+str(aperture)]

        subprocess.run(cmd)

#-------------------------------------------------------------------------------------


    def get_shutterspeed_values(self, port):

        cmd = [ 'gphoto2', '--port', port, '--get-config=shutterspeed']

        result = subprocess.check_output(cmd)

        suhtterspeed_values= []

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Choice:'):
                parts = line.split()
                suhtterspeed_values.append(parts[2])

        return suhtterspeed_values


    def current_shutterspeed_value(self, port):

        cmd = [ 'gphoto2', '--port', port, '--get-config=shutterspeed']

        result = subprocess.check_output(cmd)

        shutterspeed = ''

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Current:'):
                parts = line.split()
                shutterspeed= parts[1]

        return shutterspeed


    def set_shutterspeed(self, port, shutterspeed = str):

        cmd = [ 'gphoto2', '--port', port, '--set-config', 'shutterspeed='+shutterspeed]

        subprocess.run(cmd)

#-------------------------------------------------------------------------------------

    def get_image_format(self, port):
        cmd = [ 'gphoto2', '--port', port, '--get-config=imageformat']

        result = subprocess.check_output(cmd)

        modes=[]

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Choice:'):
                parts = line.split()
                temp = []
                #if settings has more than 1 word, join them to one string
                for part in range(2,len(parts)):
                    temp.append(parts[part])
                
                temp = ' '.join(temp)
                modes.append(temp)

        return modes


    def set_image_format(self, port, format = str):

        cmd = [ 'gphoto2', '--port', port, '--set-config', 'imageformat='+format]

        subprocess.run(cmd)


    def current_image_format(self, port):

        cmd = [ 'gphoto2', '--port', port, '--get-config=imageformat']

        result = subprocess.check_output(cmd)

        mode = ''

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Current:'):
                parts = line.split()
                temp = []
                for part in range(1,len(parts)):
                    temp.append(parts[part])
                
                temp = ' '.join(temp)
                mode = temp

        return mode
    
#-------------------------------------------------------------------------------------

    def get_focusmode(self, port):
        cmd = [ 'gphoto2', '--port', port, '--get-config=focusmode']

        result = subprocess.check_output(cmd)

        focusmodes=[]

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Choice:'):
                parts = line.split()
                temp = []
                #if settings has more than 1 word, join them to one string
                for part in range(2,len(parts)):
                    temp.append(parts[part])
                
                temp = ' '.join(temp)
                focusmodes.append(temp)

        return focusmodes

    def set_focusmode(self, port, focusmode):

        cmd = [ 'gphoto2', '--port', port, '--set-config', 'focusmode='+focusmode]

        subprocess.run(cmd)


    def current_focusmode(self, port):

        cmd = [ 'gphoto2', '--port', port, '--get-config=focusmode']

        result = subprocess.check_output(cmd)

        focusmode = ''

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Current:'):
                parts = line.split()
                temp = []
                for part in range(1,len(parts)):
                    temp.append(parts[part])
                
                temp = ' '.join(temp)
                focusmode = temp

        return focusmode

#-------------------------------------------------------------------------------------

    def get_drivemode(self, port):
        cmd = [ 'gphoto2', '--port', port, '--get-config=drivemode']

        result = subprocess.check_output(cmd)

        drivemodes=[]

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Choice:'):
                parts = line.split()
                temp = []
                #if settings has more than 1 word, join them to one string
                for part in range(2,len(parts)):
                    temp.append(parts[part])
                
                temp = ' '.join(temp)
                drivemodes.append(temp)

        return drivemodes

    def set_drivemode(self, port, drivemode):

        cmd = [ 'gphoto2', '--port', port, '--set-config', 'drivemode='+drivemode]

        subprocess.run(cmd)


    def current_drivemode(self, port):

        cmd = [ 'gphoto2', '--port', port, '--get-config=drivemode']

        result = subprocess.check_output(cmd)

        drivemode = ''

        for line in result.decode('utf-8').split('\n'):
            if line.startswith('Current:'):
                parts = line.split()
                temp = []
                for part in range(1,len(parts)):
                    temp.append(parts[part])
                
                temp = ' '.join(temp)
                drivemode = temp

        return drivemode

#-------------------------------------------------------------------------------------



    def take_picture(self, path=str, photo_name=str):
        date = datetime.datetime.now()
        
        now = [str(date.day), str(date.month), str(date.microsecond)]

        now = '_'.join(now)

        cmd = [ 'gphoto2', '--capture-image-and-download', '--filename', path+'/'+photo_name+'_'+now]

        subprocess.run(cmd)

#-------------------------------------------------------------------------------------

    def live_view(self, camera_num):
        print(camera_num)
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

    

