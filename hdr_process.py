import cv2
import numpy as np

def load_images(filenames, times):
    images = []
    for filename in filenames:
        img = cv2.imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        images.append(img)

    return np.array(images), np.array(times, dtype=np.float32)

def create_hdr_image(images, times):
    calibrate = cv2.createCalibrateDebevec()
    response = calibrate.process(images, times)

    merge = cv2.createMergeDebevec()
    hdr = merge.process(images, times, response)

    return hdr

def save_hdr_image(hdr_image, output_filename):
    tonemap = cv2.createTonemap(2.2)
    ldr = tonemap.process(hdr_image)
    ldr = cv2.cvtColor(ldr, cv2.COLOR_RGB2BGR)

    cv2.imwrite(output_filename, ldr * 255)

if __name__ == "__main__":
    filenames = ["/home/kuba/Plocha/test_8_4_142037","/home/kuba/Plocha/test_8_4_100173", "/home/kuba/Plocha/test_8_4_193778"]
    exposure_times = [1/20, 1/125, 1/400]

    images, times = load_images(filenames, exposure_times)
    hdr_image = create_hdr_image(images, times)

    
    save_hdr_image(hdr_image, "/home/kuba/Plocha/output_hdr.jpg")
