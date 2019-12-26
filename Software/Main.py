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
    scan_objects()
    prepare_cnc()
    time.sleep(3)


# Функция подготовки станка к работе
def prepare_cnc():
    # Перемещение к глобальному 0 (G28)
    Moving.go_to_zero()
    # Перемещение на точку базы
    Moving.go_to_base()
    # Сброс координат (установка локального 0)
    Packet.send_reset_coordinates()
    Packet.send_cut_off()


# Функция поиска клубники по изображению с камеры
def scan_objects():
    global objects
    objects = Analyze.get_all_objects()
    if len(objects) == 0:
        print("Strawberry not found, exiting...")
        end()
        exit()


# Функция среза каждой клубники и её переноса на базу
def loop():
    for c_object in objects:
        Moving.go_to_local_coordinates(Analyze.get_real_coordinate_x(c_object[0]),
                                       Analyze.get_real_coordinate_y(c_object[2]),
                                       -1 * (Analyze.get_real_coordinate_z(c_object[1])))
        Packet.send_cut_on()
        Moving.go_to_base_in_local()
        Packet.send_cut_off()


# Завершение работы программы и перемещение станка в глобальный 0
def end():
    Moving.go_to_zero()
    time.sleep(5)
    Packet.disconnect()
    print("End of program, thanks for using!")


if __name__ == '__main__':
    main()
