#%% GUI
import sys
from PyQt5.QtWidgets import QListWidget, QDialog, QGridLayout, QListWidgetItem, QApplication, QLineEdit, QWidget, QVBoxLayout, QLabel, QGroupBox, QComboBox, QHBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtGui import QPixmap, QIcon,QImage
from os import listdir
from os.path import isfile, join
import cv2 as cv   
import datetime
import numpy as np


from cameraControl import CamControl

cam = CamControl()



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.cam_index = ''
        self.cam_number = 0
        self.selected_folder = ""
        self.foto_name = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        hbox_top = QHBoxLayout()



        # Box 1
        group_box = QGroupBox()
        group_box.setFixedSize(330, 240)

        group_layout = QVBoxLayout()

        # Kamery
        hbox = QHBoxLayout()

        label = QLabel('Cams:')
        hbox.addWidget(label)

        self.combo_box1 = self.create_combo_box_cameras(self.get_cams())
        hbox.addWidget(self.combo_box1)

        #button pro obnovení
        self.refresh_button = QPushButton("↻", self)
        self.refresh_button.clicked.connect(self.refresh_gui)
        self.refresh_button.setFixedWidth(40)

        hbox.addWidget(self.refresh_button, alignment=Qt.AlignRight)
        group_layout.addLayout(hbox)

        # Select folder
        folder = QVBoxLayout()
        self.browse = QLabel('Select folder:', self)
        folder.addWidget(self.browse)

        select_folder_button = QPushButton("Browse", self)
        select_folder_button.clicked.connect(self.select_folder)
        select_folder_button.setFixedWidth(65)
        folder.addWidget(select_folder_button)
        group_layout.addLayout(folder)

        # Images in folder
        group_box3 = QGroupBox("Folder content:")
        group_box3.setFixedSize(300, 100)  

        group_layout3 = QVBoxLayout()

        self.image_list = QListWidget()
        group_layout3.addWidget(self.image_list)

        group_box3.setLayout(group_layout3)
        group_layout.addWidget(group_box3)

        group_box.setLayout(group_layout)
        hbox_top.addWidget(group_box, 0, alignment=Qt.AlignLeft | Qt.AlignTop)



        # Box 2
        group_box2 = QGroupBox()
        group_box2.setFixedSize(330, 240)

        group_layout2 = QVBoxLayout()

        #modes
        hbox_modes = QHBoxLayout()

        modeslabel = QLabel('Modes:')
        hbox_modes.addWidget(modeslabel)

        self.combo_box3 = self.create_combo_box_modes(self.get_mods())
        hbox_modes.addWidget(self.combo_box3)

        group_layout2.addLayout(hbox_modes)

        #ISO
        hbox_iso = QHBoxLayout()

        isolabel = QLabel('ISO:')
        hbox_iso.addWidget(isolabel)

        self.combo_box2 = self.create_combo_box_iso(self.get_iso())
        hbox_iso.addWidget(self.combo_box2)

        group_layout2.addLayout(hbox_iso)

        #Whitebalance
        hbox_whitebal = QHBoxLayout()

        whiteballabel = QLabel('Whitebalance:')
        hbox_whitebal.addWidget(whiteballabel)

        self.combo_box4 = self.create_combo_box_whitebal(self.get_whitebal())
        hbox_whitebal.addWidget(self.combo_box4)

        group_layout2.addLayout(hbox_whitebal)
        
        #aperture
        hbox_aper = QHBoxLayout()

        aperlabel = QLabel('Aperture:')
        hbox_aper.addWidget(aperlabel)

        self.combo_box5 = self.create_combo_box_aper(self.get_aper())
        hbox_aper.addWidget(self.combo_box5)

        group_layout2.addLayout(hbox_aper)

        #shutterspeed
        hbox_shut = QHBoxLayout()

        shutlabel = QLabel('Shutterspeed:')
        hbox_shut.addWidget(shutlabel)

        self.combo_box6 = self.create_combo_box_shut(self.get_shutter())
        hbox_shut.addWidget(self.combo_box6)

        group_layout2.addLayout(hbox_shut)

        #imageformat
        hbox_imf = QHBoxLayout()

        imflabel = QLabel('Image format:')
        hbox_imf.addWidget(imflabel)

        self.combo_box7 = self.create_combo_box_imf(self.get_imgform())
        hbox_imf.addWidget(self.combo_box7)

        group_layout2.addLayout(hbox_imf)
        
        #focusmode
        hbox_focm = QHBoxLayout()

        focmlabel = QLabel('Focus mode:')
        hbox_focm.addWidget(focmlabel)

        self.combo_box8 = self.create_combo_box_focm(self.get_focusm())
        hbox_focm.addWidget(self.combo_box8)

        group_layout2.addLayout(hbox_focm)

        #drivemode
        hbox_drivm = QHBoxLayout()

        drivmlabel = QLabel('Drive mode:')
        hbox_drivm.addWidget(drivmlabel)

        self.combo_box9 = self.create_combo_box_drivm(self.get_drivem())
        hbox_drivm.addWidget(self.combo_box9)

        group_layout2.addLayout(hbox_drivm)

        #------
        group_box2.setLayout(group_layout2)
        hbox_top.addWidget(group_box2, 1    , alignment=Qt.AlignLeft | Qt.AlignTop) 

        layout.addLayout(hbox_top)



        # Box 3
        group_box3 = QGroupBox()
        group_box3.setFixedSize(660, 140)

        group_layout3 = QVBoxLayout()     
        
        # Foto name
        hbox_foto_name = QHBoxLayout()
        foto_name_label = QLabel("Foto name:")
        hbox_foto_name.addWidget(foto_name_label)

        self.foto_name_line_edit = QLineEdit()
        hbox_foto_name.addWidget(self.foto_name_line_edit)

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_input_foto)
        hbox_foto_name.addWidget(save_button)
        group_layout3.addLayout(hbox_foto_name)

        # Buttons "foto", "Start live view", "HDR image". Continuous
        hbox_buttons = QHBoxLayout()
        self.print_folder_button = QPushButton("Foto", self)
        self.print_folder_button.clicked.connect(self.take_picture)
        hbox_buttons.addWidget(self.print_folder_button)

        self.live_view_button = QPushButton('Start live view', self)
        self.live_view_button.clicked.connect(self.start_live_view)
        hbox_buttons.addWidget(self.live_view_button)

        self.hdr_button = QPushButton('Take a HDR image', self)
        self.hdr_button.clicked.connect(self.hdr_popup)
        hbox_buttons.addWidget(self.hdr_button)

        self.cont_button = QPushButton('Serial imaging', self)
        self.cont_button.clicked.connect(self.cont_imaging)
        hbox_buttons.addWidget(self.cont_button)

        group_layout3.addLayout(hbox_buttons)



        group_box3.setLayout(group_layout3)
        layout.addWidget(group_box3, alignment=Qt.AlignLeft | Qt.AlignTop)

        


        # functions to run after combo box change
        self.combo_box1.currentIndexChanged.connect(self.cam_box_change)
        self.combo_box2.currentIndexChanged.connect(self.iso_val_change)
        self.combo_box3.currentIndexChanged.connect(self.modes_val_change)
        self.combo_box4.currentIndexChanged.connect(self.whitebal_val_change)
        self.combo_box5.currentIndexChanged.connect(self.aper_val_change)
        self.combo_box6.currentIndexChanged.connect(self.shut_val_change)
        self.combo_box7.currentIndexChanged.connect(self.imgf_val_change)
        self.combo_box8.currentIndexChanged.connect(self.focm_val_change)
        self.combo_box9.currentIndexChanged.connect(self.drivem_val_change)


        self.setLayout(layout)

        self.setWindowTitle('Camera Control')
        #self.setFixedSize(600, 600)  
        self.show()

#-------------------Functions--------------------------------

    def cont_imaging(self):
        if self.selected_folder != "" and self.foto_name != "":
                cam.take_picture(self.selected_folder, self.foto_name)
                cam.take_picture(self.selected_folder, self.foto_name)
                cam.take_picture(self.selected_folder, self.foto_name)
                self.update_image_list()
        else:
            print("No folder or foto name selected.")
            


    def hdr_popup(self):
        self.popup = QDialog(self)
        self.popup.setWindowTitle("HDR popup")
        self.popup.setFixedSize(400, 180)

        palette = self.popup.palette()
        palette.setColor(QPalette.Window, QColor(181, 181, 181))
        self.popup.setPalette(palette)

        grid = QGridLayout()

        
        self.shutterspeed_values = cam.get_settings(self.cam_index, 'shutterspeed')

        self.combo_boxes_hdr = [QComboBox(self.popup) for _ in range(3)]

        exposure_times_label = QLabel("Select exposure times", self.popup)
        grid.addWidget(exposure_times_label, 0, 0)

        for i, combo_box_hdr in enumerate(self.combo_boxes_hdr):
            for value in self.shutterspeed_values:
                combo_box_hdr.addItem(value)
            grid.addWidget(combo_box_hdr, i+1, 0)
        
        save_button = QPushButton("Take picture and process HDR", self.popup)
        save_button.clicked.connect(self.save_and_shoot)
        grid.addWidget(save_button, 4, 0)

        self.popup.setLayout(grid)
        self.popup.exec_()

    def save_and_shoot(self):
        if self.selected_folder != "":
            self.date = datetime.datetime.now()
            names = []
            selected_values = [combo_box.currentText() for combo_box in self.combo_boxes_hdr]
            values = []
            
            try:
                if selected_values[0] and selected_values[1] != "auto":
                    if selected_values[0] != selected_values[1]:
                        if selected_values[0] != selected_values[2]:
                            if selected_values[1] != selected_values[2]:
                                for shutterspeed in selected_values:
                                    cam.set_settings(self.cam_index, settings='shutterspeed', settings_value=shutterspeed)
                                    sh_sp = shutterspeed.replace("/",".")
                                    sh_split = shutterspeed.split("/")
                                    values.append(int(sh_split[0])/int(sh_split[1]))
                                    name = "hdr_"+str(self.date.hour)+"_"+str(self.date.minute)+"/"+"hdr"+sh_sp
                                    cam.take_picture_hdr(self.selected_folder, name)
                                    names.append(self.selected_folder+"/"+name)
                                self.update_image_list()
                    
            except:
                return print("Selected mode does not support shutterspeed value change or selected shutterspeed values are same! Change mode!")
        else:
            print("No folder selected.")

        try:
            self.process_hdr(values,names)
            self.popup.close()
        except:
            print("Selected  shutterspeed values are same!")

    def process_hdr(self, values, paths):
        images = []
        for filename in paths:
            img = cv.imread(filename)
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            images.append(img)
        
        images = np.array(images)
        times = np.array(values, dtype=np.float32)

        calibrate = cv.createCalibrateDebevec()
        response = calibrate.process(images, times)

        merge = cv.createMergeDebevec()
        hdr_image = merge.process(images, times, response)

        tonemap = cv.createTonemap(2.2)
        ldr = tonemap.process(hdr_image)
        ldr = cv.cvtColor(ldr, cv.COLOR_RGB2BGR)

        cv.imwrite(self.selected_folder+"/"+"hdr_"+str(self.date.hour)+"_"+str(self.date.minute)+".jpg", ldr * 255)

    def select_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder = QFileDialog.getExistingDirectory(self, "Select folder", "", options=options)

        if folder:
            self.selected_folder = folder
            self.browse.setText("Path: " + folder)
            self.update_image_list()

    def take_picture(self):
        if self.selected_folder != "" and self.foto_name != "":
            cam.take_picture(self.selected_folder, self.foto_name)
            self.update_image_list()
            
        else:
            print("No folder or foto name selected.")
        
    def save_input_foto(self):
        self.foto_name = self.foto_name_line_edit.text()


    def cam_box_change(self, index):
        cams, ports = cam.detect_camera()
        if not cams:
            self.cam_index = ''
        else:
            self.cam_index = ports[index]
            self.cam_number = index
        
        try:
            iso_vals = self.get_iso()
            self.update_iso_vals(iso_vals)
            modes = self.get_mods()
            self.update_modes_val(modes)
            whitebal_vals = self.get_whitebal()
            self.update_whitebal_vals(whitebal_vals)
            aper_vals = self.get_aper()
            self.update_aper_vals(aper_vals)
            shutt_vals = self.get_shutter()
            self.update_shutter_vals(shutt_vals)
            imgf_vals = self.get_imgform()
            self.update_imgform_vals(imgf_vals)
            focm_vals = self.get_focusm()
            self.update_focus_vals(focm_vals)
            drivm_vals = self.get_drivem()
            self.update_drive_vals(drivm_vals)


            return ports[index]
        except:
            return 

    def iso_val_change(self, index):
        try:
            vals = cam.get_settings(self.cam_index, settings='iso')
            cam.set_settings(self.cam_index, settings='iso', settings_value=vals[index])
        except:
            return
        
    def modes_val_change(self, index):
        try:
            vals = cam.get_settings(self.cam_index, settings='autoexposuremode')
            cam.set_settings(self.cam_index, settings='autoexposuremode', settings_value=vals[index])

            self.update_iso_vals(self.get_iso())
            iso_def = cam.current_settings(self.cam_index, settings='autoexposuremode')
            for i in range(0,len(self.iso_vals)):
                if self.iso_vals[i] == iso_def:
                    self.combo_box2.setCurrentIndex(i)
            
            self.update_whitebal_vals(self.get_whitebal())
            wb_def = cam.current_settings(self.cam_index, settings='whitebalance')
            for i in range(0,len(self.whitebal_vals)):
                if self.whitebal_vals[i] == wb_def:
                    self.combo_box4.setCurrentIndex(i)

            
            self.update_aper_vals(self.get_aper())
            ap_def = cam.current_settings(self.cam_index, settings='aperture')
            for i in range(0,len(self.aper_vals)):
                if self.aper_vals[i] == ap_def:
                    self.combo_box5.setCurrentIndex(i)
            
            self.update_shutter_vals(self.get_shutter())
            sh_def = cam.current_settings(self.cam_index, settings='shutterspeed')
            for i in range(0,len(self.shut_vals)):
                if self.shut_vals[i] == sh_def:
                    self.combo_box6.setCurrentIndex(i)
            
            self.update_imgform_vals(self.get_imgform())
            imgf_def = cam.current_settings(self.cam_index, settings='imageformat')
            for i in range(0,len(self.imf_vals)):
                if self.imf_vals[i] == imgf_def:
                    self.combo_box7.setCurrentIndex(i)
            
            
            self.update_focus_vals(self.get_focusm())
            focm_def = cam.current_settings(self.cam_index, settings='focusmode')
            for i in range(0,len(self.focm_vals)):
                if self.focm_vals[i] == focm_def:
                    self.combo_box8.setCurrentIndex(i)
            
            self.update_drive_vals(self.get_drivem())
            drivm_def = cam.current_settings(self.cam_index, settings='drivemode')
            for i in range(0,len(self.drivm_vals)):
                if self.drivm_vals[i] == drivm_def:
                    self.combo_box9.setCurrentIndex(i)

        except:
            return

    def whitebal_val_change(self, index):
        try:
            vals = cam.get_settings(self.cam_index, settings='whitebalance')
            cam.set_settings(self.cam_index, settings='whitebalance', settings_value=vals[index])
        except:
            return
    
    def aper_val_change(self, index):
        try:
            vals = cam.get_settings(self.cam_index, settings='aperture')
            if len(vals) > 1:
                cam.set_settings(self.cam_index, settings='aperture', settings_value=vals[index])
            
            return
        except:
            return
        
    def shut_val_change(self, index):
        try:
            vals = cam.get_settings(self.cam_index, settings='shutterspeed')
            
            cam.set_settings(self.cam_index, settings='shutterspeed', settings_value=vals[index])
            
            return
        except:
            return
    
    def imgf_val_change(self, index):
        try:
            vals = cam.get_settings(self.cam_index, settings='imageformat')
            
            cam.set_settings(self.cam_index, settings='imageformat', settings_value=vals[index])
            
            return
        except:
            return

    def focm_val_change(self, index):
        try:
            vals = cam.get_settings(self.cam_index, settings='focusmode')
            
            cam.set_settings(self.cam_index, settings='focusmode', settings_value=vals[index])
            
            return
        except:
            return

    def drivem_val_change(self, index):
        try:
            vals = cam.get_settings(self.cam_index, settings='drivemode')
            
            cam.set_settings(self.cam_index, settings='drivemode', settings_value=vals[index])
            
            return
        except:
            return


    def create_combo_box_cameras(self, options):
        combo_box = QComboBox()
        for option in options:
            combo_box.addItem(option)
                
            default_value = options[0]
            index = combo_box.findText(default_value)
            combo_box.setCurrentIndex(index)

        return combo_box
          
    def create_combo_box_iso(self, options):
        
        if self.cam_index == '':
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)

                default_value = options[0]
                index = combo_box.findText(default_value)
                combo_box.setCurrentIndex(index)

            return combo_box
        
        else:
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)
                
            default_value = cam.current_settings(self.cam_index, settings='iso')
            for i in range(0,len(self.iso_vals)):
                if self.iso_vals[i] == default_value:
                    combo_box.setCurrentIndex(i)
                                
            return combo_box
        
    def create_combo_box_modes(self, options):
        cams, ports = cam.detect_camera()
        if not cams:
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)

                default_value = options[0]
                index = combo_box.findText(default_value)
                combo_box.setCurrentIndex(index)

            return combo_box
        
        else:
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)
                
            default_value = cam.current_settings(self.cam_index, settings='autoexposuremode')
            for i in range(0,len(self.modes_vals)):
                if self.modes_vals[i] == default_value:
                    combo_box.setCurrentIndex(i)

            
            return combo_box
    
    def create_combo_box_whitebal(self, options):
        
        if self.cam_index == '':
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)

                default_value = options[0]
                index = combo_box.findText(default_value)
                combo_box.setCurrentIndex(index)

            return combo_box
        
        else:
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)
                
            default_value = cam.current_settings(self.cam_index, settings='whitebalance')
            for i in range(0,len(self.whitebal_vals)):
                if self.whitebal_vals[i] == default_value:
                    combo_box.setCurrentIndex(i)
                    
            return combo_box
        
    def create_combo_box_aper(self, options):
        
        if self.cam_index == '':
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)

                default_value = options[0]
                index = combo_box.findText(default_value)
                combo_box.setCurrentIndex(index)

            return combo_box
        
        else:
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)
                
            default_value = cam.current_settings(self.cam_index, settings='aperture')
            for i in range(0,len(self.whitebal_vals)):
                if self.whitebal_vals[i] == default_value:
                    combo_box.setCurrentIndex(i)
                    
            return combo_box

    def create_combo_box_shut(self, options):
        
        if self.cam_index == '':
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)

                default_value = options[0]
                index = combo_box.findText(default_value)
                combo_box.setCurrentIndex(index)

            return combo_box
        
        else:
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)
                
            default_value = cam.current_settings(self.cam_index, settings='shutterspeed')
            for i in range(0,len(self.shut_vals)):
                if self.shut_vals[i] == default_value:
                    combo_box.setCurrentIndex(i)
                    
            return combo_box
        
    def create_combo_box_imf(self, options):
        
        if self.cam_index == '':
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)

                default_value = options[0]
                index = combo_box.findText(default_value)
                combo_box.setCurrentIndex(index)

            return combo_box
        
        else:
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)
                
            default_value = cam.current_settings(self.cam_index, settings='imageformat')
            for i in range(0,len(self.imf_vals)):
                if self.imf_vals[i] == default_value:
                    combo_box.setCurrentIndex(i)
                    
            return combo_box

    def create_combo_box_focm(self, options):
        
        if self.cam_index == '':
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)

                default_value = options[0]
                index = combo_box.findText(default_value)
                combo_box.setCurrentIndex(index)

            return combo_box
        
        else:
            combo_box = QComboBox()
            for option in options:
                combo_box.addItem(option)
                
            default_value = cam.current_settings(self.cam_index, settings='focusmode')
            for i in range(0,len(self.focm_vals)):
                if self.focm_vals[i] == default_value:
                    combo_box.setCurrentIndex(i)
                    
            return combo_box

    def create_combo_box_drivm(self, options):
            
            if self.cam_index == '':
                combo_box = QComboBox()
                for option in options:
                    combo_box.addItem(option)

                    default_value = options[0]
                    index = combo_box.findText(default_value)
                    combo_box.setCurrentIndex(index)

                return combo_box
            
            else:
                combo_box = QComboBox()
                for option in options:
                    combo_box.addItem(option)
                    
                default_value = cam.current_settings(self.cam_index, settings='drivemode')
                for i in range(0,len(self.drivm_vals)):
                    if self.drivm_vals[i] == default_value:
                        combo_box.setCurrentIndex(i)
                        
                return combo_box



    def get_cams(self):
        try:
            cams, ports = cam.detect_camera()
            if not cams:
                raise ValueError("No camera connected")
            
            self.cam_index = ports[0]
            return cams
        except ValueError as error:
            return [str(error)]
        
    def get_iso(self):
        if self.cam_index == '':
           vals = ['No values']
        else:
            try:
                vals = cam.get_settings(self.cam_index, settings='iso')
                self.iso_vals = vals
                return vals
            except:
                vals = ['No values']
                return vals

        return vals     

    def get_mods(self):
        cams, ports = cam.detect_camera()
        if not cams:
           vals = ['No values']
        else:
            try:
                vals = cam.get_settings(self.cam_index, settings='autoexposuremode')
                self.modes_vals = vals
                return vals
            except:
                vals = ['No values']
                return vals

        return vals 

    def get_whitebal(self):
        if self.cam_index == '':
           vals = ['No values']
        else:
            try:
                vals = cam.get_settings(self.cam_index, settings='whitebalance')
                self.whitebal_vals = vals
                return vals
            except:
                vals = ['No values']
                return vals

        return vals

    def get_aper(self):
        if self.cam_index == '':
           vals = ['No values']
        else:
            try:
                vals = cam.get_settings(self.cam_index, settings='aperture')
                if len(vals) > 1:
                    self.aper_vals = vals
                else:
                    vals = ["Auto"]

                return vals
            except:
                vals = ['No values']
                return vals

        return vals

    def get_shutter(self):
        if self.cam_index == '':
           vals = ['No values']
        else:
            try:
                vals = cam.get_settings(self.cam_index, settings='shutterspeed')
                self.shut_vals = vals
                return vals
            except:
                vals = ['No values']
                return vals

        return vals
    
    def get_imgform(self):
        if self.cam_index == '':
           vals = ['No values']
        else:
            try:
                vals = cam.get_settings(self.cam_index, settings='imageformat')
                self.imf_vals = vals
                return vals
            except:
                vals = ['No values']
                return vals

        return vals
    
    def get_focusm(self):
        if self.cam_index == '':
           vals = ['No values']
        else:
            try:
                vals = cam.get_settings(self.cam_index, settings='focusmode')
                self.focm_vals = vals
                return vals
            except:
                vals = ['No values']
                return vals

        return vals

    def get_drivem(self):
            if self.cam_index == '':
                vals = ['No values']
            else:
                try:
                    vals = cam.get_settings(self.cam_index, settings='drivemode')
                    self.drivm_vals = vals
                    return vals
                except:
                    vals = ['No values']
                    return vals

            return vals


    def update_iso_vals(self, values):
        self.combo_box2.clear()
        self.combo_box2.addItems(values)

    def update_modes_val(self, values):
        self.combo_box3.clear()
        self.combo_box3.addItems(values)

    def update_whitebal_vals(self, values):
        self.combo_box4.clear()
        self.combo_box4.addItems(values)
    
    def update_aper_vals(self, values):
        self.combo_box5.clear()
        self.combo_box5.addItems(values)

    def update_image_list(self):
        self.image_list.clear()

        if hasattr(self, "selected_folder"):
            all_files = listdir(self.selected_folder)
            print("All files in folder:", all_files)

            image_files = [
                f for f in all_files
                if isfile(join(self.selected_folder, f))
            ]

            print("Image files:", image_files) 

            for img_file in image_files:
                img_path = join(self.selected_folder, img_file)
                image = QImage(img_path)

                if image.isNull():
                    print(f"Failed to load image: {img_file}")
                    continue
                    
                pixmap = QPixmap.fromImage(image)
                pixmap = pixmap.scaled(30, 30, Qt.KeepAspectRatio) 

                item = QListWidgetItem()
                item.setIcon(QIcon(pixmap))
                item.setText(img_file)
                self.image_list.addItem(item)
        else:
            self.image_list.setText("")

    def update_shutter_vals(self, values):
        self.combo_box6.clear()
        self.combo_box6.addItems(values)
    
    def update_imgform_vals(self, values):
        self.combo_box7.clear()
        self.combo_box7.addItems(values)

    def update_focus_vals(self, values):
        self.combo_box8.clear()
        self.combo_box8.addItems(values)

    def update_drive_vals(self, values):
        self.combo_box9.clear()
        self.combo_box9.addItems(values)
    

    def start_live_view(self):
        if self.cam_index:
            cam.live_view(self.cam_number)
        else:
            print("No camera selected")

    def refresh_gui(self):
        
        try:
            cams, ports = cam.detect_camera()
            if not cams:
                raise ValueError("No camera connected")
            
            cameras = self.get_cams()
            self.combo_box1.clear()
            self.combo_box1.addItems(cameras)

        except ValueError as error:
            return [str(error)]
        

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
