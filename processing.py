import os
import cv2
import numpy as np

# pip install matplotlib
import matplotlib.pyplot as plt

path = "assets/upload/"
url = f"{os.getenv('SERVER_URL')}/{path}"

def adjustImages(image):
    # konversi gambar dari RGB ke HSV
    imagetoHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definisi rentang warna merah dalam HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(imagetoHSV, lower_red1, upper_red1)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(imagetoHSV, lower_red2, upper_red2)

    mask_red = mask1 + mask2

    # Definisi rentang warna biru dalam HSV
    lower_blue = np.array([100, 150, 50])  # Rentang bawah biru (Hue 100-140)
    upper_blue = np.array([140, 255, 255])  # Rentang atas biru

    mask_blue = cv2.inRange(imagetoHSV, lower_blue, upper_blue)

    # Gabungkan kedua mask
    mask = mask_red + mask_blue




    # Buat area merah menjadi putih
    image[mask > 0] = [255, 255, 255]


    # Lakukan dilasi untuk mengisi celah pada pinggiran
    kernel = np.ones((5, 5), np.uint8)  # Kernel untuk dilasi
    mask = cv2.dilate(mask, kernel, iterations=1)
    # Buat area merah menjadi putih
    image[mask > 0] = [255, 255, 255]


    # cropping qris
    # resize gambar
    image = cv2.resize(image, (1400, 1972))  # satuan piksel

    # ambil dimensi gambar
    height, width, _ = image.shape
    crop_size = [800, 250]  # (100 x 100 piksel)

    # dimulai dari pojok atas kiri dengan koordinat [0, 0]
    start_x = 0
    start_y = 0

    image[start_y:start_y + crop_size[1], start_x:start_x + crop_size[0]] = [255, 255, 255]


    # crop icon
    crop_size = [400, 200]  # (100 x 100 piksel)

    # dimulai dari pojok kanan, bawah dengan koordinat x = ukuran maksimal width, dan y ukuran maksimal
    start_x = width - crop_size[0]
    start_y = height - crop_size[1]

    image[start_y:start_y + crop_size[1], start_x:start_x + crop_size[0]] = [255, 255, 255]


    # hapus background
    # mengkonversi gambar RGB ke citra grayscale atau keabu-abuan
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Misalnya kita akan mendeteksi abu-abu di rentang nilai pixel 120 - 160
    lower_gray = 230
    upper_gray = 255

    # Buat mask untuk abu-abu
    mask = cv2.inRange(gray_image, lower_gray, upper_gray)
    image[mask > 0] = [255, 255, 255]

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # cv2.imwrite("test-f.png", image)

    return image