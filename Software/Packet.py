import serial
import time

lastCoords = [0, 0, 0]
ser = None
while ser is None:
    time.sleep(3)
    try:
        ser = serial.Serial('COM9', 115200)
    except BaseException:
        print("Ожидание подключения SerialPort...")
        ser = None
moveSpeed = 10000
while ser.in_waiting:
    print(ser.readline())

def sendMove(x, y, z):
    global ser, lastCoords
    if input(f'Подтвердить действие: "G01 X{x} Y{y} Z{z} F{moveSpeed}"? ') == "+":
        sendGCode(f'G01 X{x} Y{y} Z{z} F{moveSpeed}\n')
    while ser.in_waiting:
        print(ser.readline())
    # time.sleep(__getTime(lastCoords, [x, y, z]))
    lastCoords = [x, y, z]


def sendCutOn():
    global ser
    if input("Подтвердить действие: \"G01 E0 F800\"? ") == "+":
        sendGCode("G01 E0 F800\n")
    while ser.in_waiting:
        print(ser.readline())
    time.sleep(1)


def sendCutOff():
    global ser
    if input("Подтвердить действие: \"G01 E75 F800\"? ") == "+":
        sendGCode("G01 E15 F800\n")
    while ser.in_waiting:
        print(ser.readline())
    time.sleep(1)


def sendResetCoords():
    global ser, lastCoords
    if input("Подтвердить действие: \"G92 E75 X0 Y0 Z0\"? ") == "+":
        sendGCode("G92 E0 X0 Y0 Z0\n")
    while ser.in_waiting:
        print(ser.readline())
    lastCoords = [0, 0, 0]


def goToGlobalZero():
    global ser, lastCoords
    # if input("Подтвердить действие: \"G28\"? ") == "+":
    sendGCode("G28\n")
    while ser.in_waiting:
        print(ser.readline())
    lastCoords = [0, 0, 0]


def sendGCode(code):
    global ser
    try:
        ser.write(code.encode('ascii'))
    except BaseException:
        print("Произошла какая-то ошибка!")
        ser = None
        while ser is None:
            time.sleep(3)
            try:
                ser = serial.Serial('COM9', 115200)
            except BaseException:
                print("Ожидание подключения SerialPort...")
                ser = None
        ser.write(code.encode('ascii'))


def __getTime(lastCoordsF, newCoords):
    x0, y0, z0, x1, y1, z1 = lastCoordsF[0], lastCoordsF[1], lastCoordsF[2], newCoords[0], newCoords[1], newCoords[2]
    dist = ((x1-x0)**2+(y1-y0)**2+(z1-z0)**2)**0.5
    return dist//moveSpeed+3


def disconnect():
    ser.close()


def main():
    global ser
    while(True):
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
