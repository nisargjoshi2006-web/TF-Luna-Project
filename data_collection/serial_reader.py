import serial
import csv
import os

arduino = serial.Serial('COM8', 115200)

file_exists = os.path.exists('data/distance_data.csv')

with open('data/distance_data.csv', 'a', newline='') as file:

    writer = csv.writer(file)

    if os.path.getsize('data/distance_data.csv') == 0:
        writer.writerow(["Distance"])

    print("Reading TF-Luna Data...")

    while True:
        try:
            distance = arduino.readline().decode().strip()
            distance = int(distance)

            print(distance)

            writer.writerow([distance])
            file.flush()

        except:
            pass