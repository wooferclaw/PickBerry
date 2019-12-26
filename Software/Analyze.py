import cv2
import numpy as np
import time

# Точность проверки кол-ва клубники
accuracy = 20

net = cv2.dnn.readNet("weights/yolov3-tiny_obj.weights", "cfg/yolov3-tiny_obj.cfg")
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))
# CAP_DSHOW - Подключение бибилиотеки Windows для работы с внешними устройствами
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0


def getAllObjects():
    object_arrays = []
    for i in range(accuracy):
        object_arrays.append(__getObjects())
    sr_count = len(object_arrays)
    sum = 0
    for i in object_arrays:
        sum += len(i)
    sr_count = sum // sr_count
    if sr_count == 0:
        return []
    result_object_arrays = []
    for i in object_arrays:
        if len(i) == sr_count:
            result_object_arrays.append(i)
    return __checkObjects(result_object_arrays)


def __checkObjects(object_arrays):
    result = []
    for i in range(len(object_arrays[0])):
        result.append([0, 0, 0, 0])
    for objects in object_arrays:
        for i in range(len(objects)):
            for j in range(4):
                result[i][j] += objects[i][j]
    for c_object in result:
        for i in range(4):
            c_object[i] = c_object[i] // len(object_arrays)
    print(result)
    # print(getRealCoordX(getRealCoordY(result[0][2]), result[0][0]))
    # print(getRealCoordX(getRealCoordY(result[1][2]), result[1][0]))
    print(getRealCoordX(result[0][0]), getRealCoordY(result[0][2]), getRealCoordZ(result[0][1]))
    print(getRealCoordX(result[1][0]), getRealCoordY(result[1][2]), getRealCoordZ(result[1][1]))
    return result


def __getObjects():
    global frame_id
    _, frame = cap.read()
    frame_id += 1
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.1:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([center_x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    for i, box in enumerate(boxes):
        x, y, w, h = box
        color = colors[class_ids[i]]
        cv2.line(frame, (x, y), (x, y + w), color, 2)
        cv2.rectangle(frame, (x - 5, y - 15), (x + 5, y - 5), color, 2)
    cv2.imshow("Image", frame)
    # print(frame.shape)
    cv2.waitKey(1)
    return boxes


def getRealCoordY(w):
    return 185
    F = 139*389
    print(F)
    #if F / w > 2170:
    #    return 170
    return int(F * w / 50) // 1000


def getRealCoordX(w):
    k = 44/640
    res = w * k
    if res < 0:
        return 0
    return (int(res)+1)*10


def getRealCoordZ(w):
    k = 34/480
    res = w * k
    if res < 0:
        return 0
    if res > 123:
        return 123
    return (int(res)-4)*10+5


def main():
    getAllObjects()


if __name__ == '__main__':
    main()
