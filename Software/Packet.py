import serial
import time

last_coordinates = [0, 0, 0]
ser = None
while ser is None:
    time.sleep(3)
    try:
        ser = serial.Serial('COM9', 115200)
    except serial.SerialException:
        print("Ожидание подключения SerialPort...")
        ser = None
moveSpeed = 10000
while ser.in_waiting:
    print(ser.readline())


def send_move(x, y, z):
    global ser, last_coordinates
    # if input(f'Подтвердить действие: "G01 X{x} Y{y} Z{z} F{moveSpeed}"? ') == "+":
    send_g_code(f'G01 X{x} Y{y} Z{z} F{moveSpeed}\n')
    while ser.in_waiting:
        print(ser.readline())
    time.sleep(get_time(last_coordinates, [x, y, z]))
    last_coordinates = [x, y, z]


def send_cut_on():
    global ser
    # if input("Подтвердить действие: \"G01 E0 F800\"? ") == "+":
    send_g_code("G01 E0 F10000\n")
    while ser.in_waiting:
        print(ser.readline())
    time.sleep(1)


def send_cut_off():
    global ser
    # if input("Подтвердить действие: \"G01 E75 F800\"? ") == "+":
    send_g_code("G01 E20 F10000\n")
    while ser.in_waiting:
        print(ser.readline())
    time.sleep(1)


def send_reset_coordinates():
    global ser, last_coordinates
    # if input("Подтвердить действие: \"G92 E75 X0 Y0 Z0\"? ") == "+":
    send_g_code("G92 E20 X0 Y0 Z0\n")
    while ser.in_waiting:
        print(ser.readline())
    last_coordinates = [0, 0, 0]


def go_to_global_zero():
    global ser, last_coordinates
    # if input("Подтвердить действие: \"G28\"? ") == "+":
    send_g_code("G28\n")
    while ser.in_waiting:
        print(ser.readline())
    last_coordinates = [0, 0, 0]


def send_g_code(code):
    global ser
    try:
        ser.write(code.encode('ascii'))
    except serial.SerialException:
        ser = None
        while ser is None:
            time.sleep(3)
            try:
                ser = serial.Serial('COM9', 115200)
            except serial.SerialException:
                print("Ожидание подключения SerialPort...")
                ser = None
        ser.write(code.encode('ascii'))


def get_time(first_coordinates, new_coordinates):
    x0, y0, z0, x1, y1, z1 = first_coordinates[0], first_coordinates[1], first_coordinates[2], \
                             new_coordinates[0], new_coordinates[1], new_coordinates[2]
    dist = ((x1 - x0) ** 2 + (y1 - y0) ** 2 + (z1 - z0) ** 2) ** 0.5
    return dist // moveSpeed + 3


def disconnect():
    ser.close()


def main():
    global ser
    while True:
        s = input("Введите G-Code: ") + "\n"
        if s == "exit\n":
            disconnect()
            break
        if s != "\n":
            ser.write(s.encode('ascii'))
        while ser.in_waiting:
            print(ser.readline())


if __name__ == '__main__':
    main()
