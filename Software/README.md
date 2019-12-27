# StrawberryCollector
## Программа технического зрения для распознавания плодоножек клубники и выдачи управляюещего сигнала на манипулятор

### Как установить 

1. Установите ```Python``` версии не ниже 3.6
2. Установите ```pip```
3. Перейдите в папку Software
4. Запустите ```pip install -r requirements.txt```

### Как запустить

1. Подключите web-камеру
2. Подключите ЧПУ устройство принимающее ```G-CODE``` команды (нужно изменить номер ```COM```-порта в файле ```Packet.py``` на ```9``` строчке)
3. Запустить ```Main.py```

### Используемые библиотеки

1. [```Python-OpenCV```](https://opencv.org/) + [```Darknet/YOLO ```](https://pjreddie.com/darknet/yolo/)
2. [```PySerial```](https://pypi.org/project/pyserial/)
3. [```NumPy```](https://numpy.org/)

### Нейросеть

* Архитектура ```YOLO v3 tiny```
* Сеть обучена на ```OIDv4``` на 4 классах (```помидор```, ```огурец```, ```клубника```, ```домашнее растение```), по 1000 изображений на каждый класс
* Блокнот ```Yolo_train.ipynb``` для обучения в папке ```Training```. Хорошо работает на [```Google Colab```](https://colab.research.google.com/)

### Пример работы сети

![alt text](https://github.com/wooferclaw/StrawberryCollector/blob/master/Software/example.gif "Пример работы сети")


