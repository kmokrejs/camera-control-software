#%% GUI
import sys
from PyQt5.QtWidgets import QListWidget,  QListWidgetItem, QApplication, QLineEdit, QWidget, QVBoxLayout, QLabel, QGroupBox, QComboBox, QHBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QIcon,QImage
from os import listdir
from os.path import isfile, join
import cv2 as cv    

from cameraControl import CamControl

cam = CamControl()



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.cam_index = ''
        self.cam_number = 0
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
        group_box3.setFixedSize(300, 100)  # Nastaví velikost okna QGroupBox

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

        # Tlačítka "foto" a "spustit živý náhled"
        hbox_buttons = QHBoxLayout()
        self.print_folder_button = QPushButton("Foto", self)
        self.print_folder_button.clicked.connect(self.take_picture)
        hbox_buttons.addWidget(self.print_folder_button)

        self.live_view_button = QPushButton('Spustit živý náhled', self)
        self.live_view_button.clicked.connect(self.start_live_view)
        hbox_buttons.addWidget(self.live_view_button)
        group_layout3.addLayout(hbox_buttons)

        group_box3.setLayout(group_layout3)
        layout.addWidget(group_box3, alignment=Qt.AlignLeft | Qt.AlignTop)

        


        # Spustí funkci po zvolení hodnoty z rozbalovacího seznamu
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
        #self.setFixedSize(600, 600)  # Nastaví velikost okna
        self.show()

#-------------------Functions--------------------------------

    def select_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder = QFileDialog.getExistingDirectory(self, "Select folder", "", options=options)

        if folder:
            self.selected_folder = folder
            self.browse.setText("Path: " + folder)
            self.update_image_list()

    def take_picture(self):
        if self.selected_folder:
            cam.take_picture(self.selected_folder, self.foto_name)
            self.update_image_list()
            
        else:
            print("Žádná složka nebyla vybrána.")
        
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
            vals = cam.get_iso_values(self.cam_index)
            cam.set_iso(self.cam_index, vals[index])
        except:
            return
        
    def modes_val_change(self, index):
        try:
            vals = cam.get_modes(self.cam_index)
            cam.set_mode(self.cam_index, vals[index])

            self.update_iso_vals(self.get_iso())
            iso_def = cam.current_iso_value(self.cam_index)
            for i in range(0,len(self.iso_vals)):
                if self.iso_vals[i] == iso_def:
                    self.combo_box2.setCurrentIndex(i)
            
            self.update_whitebal_vals(self.get_whitebal())
            wb_def = cam.current_whitebalance_value(self.cam_index)
            for i in range(0,len(self.whitebal_vals)):
                if self.whitebal_vals[i] == wb_def:
                    self.combo_box4.setCurrentIndex(i)

            
            self.update_aper_vals(self.get_aper())
            ap_def = cam.current_aperture_value(self.cam_index)
            for i in range(0,len(self.aper_vals)):
                if self.aper_vals[i] == ap_def:
                    self.combo_box5.setCurrentIndex(i)
            
            self.update_shutter_vals(self.get_shutter())
            sh_def = cam.current_shutterspeed_value(self.cam_index)
            for i in range(0,len(self.shut_vals)):
                if self.shut_vals[i] == sh_def:
                    self.combo_box6.setCurrentIndex(i)
            
            self.update_imgform_vals(self.get_imgform())
            imgf_def = cam.current_image_format(self.cam_index)
            for i in range(0,len(self.imf_vals)):
                if self.imf_vals[i] == imgf_def:
                    self.combo_box7.setCurrentIndex(i)
            
            
            self.update_focus_vals(self.get_focusm())
            focm_def = cam.current_focusmode(self.cam_index)
            for i in range(0,len(self.focm_vals)):
                if self.focm_vals[i] == focm_def:
                    self.combo_box8.setCurrentIndex(i)
            
            self.update_drive_vals(self.get_drivem())
            drivm_def = cam.current_focusmode(self.cam_index)
            for i in range(0,len(self.drivm_vals)):
                if self.drivm_vals[i] == drivm_def:
                    self.combo_box9.setCurrentIndex(i)

        except:
            return

    def whitebal_val_change(self, index):
        try:
            vals = cam.get_whitebalance_values(self.cam_index)
            cam.set_whitebalance(self.cam_index, vals[index])
        except:
            return
    
    def aper_val_change(self, index):
        try:
            vals = cam.get_aperture_values(self.cam_index)
            if len(vals) > 1:
                cam.set_aperture(self.cam_index, vals[index])
            
            return
        except:
            return
        
    def shut_val_change(self, index):
        try:
            vals = cam.get_shutterspeed_values(self.cam_index)
            
            cam.set_shutterspeed(self.cam_index, vals[index])
            
            return
        except:
            return
    
    def imgf_val_change(self, index):
        try:
            vals = cam.get_image_format(self.cam_index)
            
            cam.set_image_format(self.cam_index, vals[index])
            
            return
        except:
            return

    def focm_val_change(self, index):
        try:
            vals = cam.get_focusmode(self.cam_index)
            
            cam.set_focusmode(self.cam_index, vals[index])
            
            return
        except:
            return

    def drivem_val_change(self, index):
        try:
            vals = cam.get_drivemode(self.cam_index)
            
            cam.set_drivemode(self.cam_index, vals[index])
            
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
                
            default_value = cam.current_iso_value(self.cam_index)
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
                
            default_value = cam.current_mode(self.cam_index)
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
                
            default_value = cam.current_whitebalance_value(self.cam_index)
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
                
            default_value = cam.current_aperture_value(self.cam_index)
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
                
            default_value = cam.current_shutterspeed_value(self.cam_index)
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
                
            default_value = cam.current_image_format(self.cam_index)
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
                
            default_value = cam.current_focusmode(self.cam_index)
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
                    
                default_value = cam.current_drivemode(self.cam_index)
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
           vals = ['No camera connected']
        else:
            try:
                vals = cam.get_iso_values(self.cam_index)
                self.iso_vals = vals
                return vals
            except:
                vals = ['No camera connected']
                return vals

        return vals     

    def get_mods(self):
        cams, ports = cam.detect_camera()
        if not cams:
           vals = ['No camera connected']
        else:
            try:
                vals = cam.get_modes(self.cam_index)
                self.modes_vals = vals
                return vals
            except:
                vals = ['No camera connected']
                return vals

        return vals 

    def get_whitebal(self):
        if self.cam_index == '':
           vals = ['No camera connected']
        else:
            try:
                vals = cam.get_whitebalance_values(self.cam_index)
                self.whitebal_vals = vals
                return vals
            except:
                vals = ['No camera connected']
                return vals

        return vals

    def get_aper(self):
        if self.cam_index == '':
           vals = ['No camera connected']
        else:
            try:
                vals = cam.get_aperture_values(self.cam_index)
                if len(vals) > 1:
                    self.aper_vals = vals
                else:
                    vals = ["Auto"]

                return vals
            except:
                vals = ['No camera connected']
                return vals

        return vals

    def get_shutter(self):
        if self.cam_index == '':
           vals = ['No camera connected']
        else:
            try:
                vals = cam.get_shutterspeed_values(self.cam_index)
                self.shut_vals = vals
                return vals
            except:
                vals = ['No camera connected']
                return vals

        return vals
    
    def get_imgform(self):
        if self.cam_index == '':
           vals = ['No camera connected']
        else:
            try:
                vals = cam.get_image_format(self.cam_index)
                self.imf_vals = vals
                return vals
            except:
                vals = ['No camera connected']
                return vals

        return vals
    
    def get_focusm(self):
        if self.cam_index == '':
           vals = ['No camera connected']
        else:
            try:
                vals = cam.get_focusmode(self.cam_index)
                self.focm_vals = vals
                return vals
            except:
                vals = ['No camera connected']
                return vals

        return vals

    def get_drivem(self):
            if self.cam_index == '':
                vals = ['No camera connected']
            else:
                try:
                    vals = cam.get_drivemode(self.cam_index)
                    self.drivm_vals = vals
                    return vals
                except:
                    vals = ['No camera connected']
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
            print("Žádná kamera nebyla vybrána.")

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
