import Packet


def go_to_zero():
    Packet.go_to_global_zero()


def go_to_base():
    Packet.send_move(1585, 0, 550)
    Packet.send_move(1585, 0, 140)


def go_to_base_in_local():
    Packet.send_move(0, 0, 0)


def go_to_local_coordinates(x, y, z):
    Packet.send_move(x, Packet.last_coordinates[1], z)
    Packet.send_move(x, y, z)
