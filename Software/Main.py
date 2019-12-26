import Analyze
import Moving
import Packet
import time


objects = []


def main():
    start()
    loop()
    end()


# Запуск 2-х асинхронных функций:
def start():
    scanObjects()
    prepareCNC()
    time.sleep(3)


# Функция подготовки станка к работе
def prepareCNC():
    # Перемещение к глобальному 0 (G28)
    Moving.goToZero()
    # Перемещение на точку базы
    Moving.goToBase()
    # Сброс координат (установка локального 0)
    Packet.sendResetCoords()
    Packet.sendCutOff()


# Функция поиска клубники по изображению с камеры
def scanObjects():
    global objects
    objects = Analyze.getAllObjects()
    if len(objects) == 0:
        print("Strawberry not found, exiting...")
        end()
        exit()


# Функция среза каждой клубники и её переноса на базу
def loop():
    for c_object in objects:
        Moving.goToLocalCoords(Analyze.getRealCoordX(c_object[0]), Analyze.getRealCoordY(c_object[2]), -1*(Analyze.getRealCoordZ(c_object[1])))
        Packet.sendCutOn()
        Moving.goToBaseInLocal()
        Packet.sendCutOff()


# Завершение работы программы и перемещение станка в глобальный 0
def end():
    Moving.goToZero()
    time.sleep(5)
    Packet.disconnect()
    print("End of program, thanks for using!")


if __name__ == '__main__':
    main()
