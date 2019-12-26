import cv2
import numpy as np
import time

# Точность проверки кол-ва клубники
accuracy = 20

net = cv2.dnn.readNet("weights/yolov3-tiny_obj.weights", "cfg/yolov3-tiny_obj.cfg")
# Второй способ отображения точки среза клубники
# classes = []
# with open("obj.names", "r") as f:
#    classes = [line.strip() for line in f.readlines()]
# colors = np.random.uniform(0, 255, size=(len(classes), 3))
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
# cv2.CAP_DSHOW - Подключение бибилиотеки Windows для работы с внешними устройствами
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0
G_I = 1


def get_all_objects():
    objects_arrays = []
    for i in range(accuracy):
        objects_arrays.append(get_objects())
    sr_count = len(objects_arrays)
    amount_object_sum = 0
    for objects in objects_arrays:
        amount_object_sum += len(objects)
    sr_count = amount_object_sum // sr_count
    if sr_count == 0:
        return []
    result_objects_array = []
    for objects in objects_arrays:
        if len(objects) == sr_count:
            result_objects_array.append(objects)
    return check_objects(result_objects_array)


def check_objects(object_arrays):
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
    # print(result)
    # print(getRealCoordX(getRealCoordY(result[0][2]), result[0][0]))
    # print(getRealCoordX(getRealCoordY(result[1][2]), result[1][0]))
    # print(getRealCoordX(result[0][0]), getRealCoordY(result[0][2]), getRealCoordZ(result[0][1]))
    # print(getRealCoordX(result[1][0]), getRealCoordY(result[1][2]), getRealCoordZ(result[1][1]))
    # print(getRealCoordX(result[2][0]), getRealCoordY(result[2][2]), getRealCoordZ(result[2][1]))
    return result


def get_objects():
    global frame_id, G_I
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
                # x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([center_x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    for i, box in enumerate(boxes):
        x, y, w, h = box
        # Второй способ отображения точки среза клубники
        # color = colors[class_ids[i]]
        # cv2.line(frame, (x, y), (x, y + w), color, 2)
        color = np.random.uniform(0, 255, size=1)[0]
        cv2.rectangle(frame, (x - 5, y - 15), (x + 5, y - 5), color, 2)
        cv2.line(frame, (x, 0), (x, 480), color, 2)
        cv2.line(frame, (0, y - 10), (640, y - 10), color, 2)
        texts = ["X: " + str(get_real_coordinate_x(x)), "Y:" + str(get_real_coordinate_z(y)),
                 "Distance: " + str(get_real_coordinate_y(w))]
        cur_y = 10
        for text in texts:
            cv2.putText(frame, text, (x + 7, y + cur_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
            cur_y += 15
    cv2.imshow("Image", frame)
    cv2.imwrite(f"img/image_{G_I}.png", frame)
    G_I += 1
    # print(frame.shape)
    cv2.waitKey(1)
    return boxes


def get_real_coordinate_y(width):
    return 185 + width * 0
    # Реализация нахождения расстояния по ширине объекта
    # (работает не всегда корректно)
    # F = 139 * 389
    # return int(F / width)


def get_real_coordinate_x(w):
    k = 44 / 640
    res = w * k
    if res < 0:
        return 0
    return (int(res) + 1) * 10


def get_real_coordinate_z(y):
    k = 34 / 480
    res = y * k
    return (int(res) - 4) * 10 + 5


def main():
    get_all_objects()


if __name__ == '__main__':
    main()
