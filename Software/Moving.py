import Packet

def goToZero():
    Packet.goToGlobalZero()


def goToBase():
    Packet.sendMove(1585, 0, 550)
    Packet.sendMove(1585, 0, 140)


def goToBaseInLocal():
    Packet.sendMove(0, 0, 0)


def goToLocalCoords(x, y, z):
    Packet.sendMove(x, Packet.lastCoords[1], z)
    Packet.sendMove(x, y, z)
