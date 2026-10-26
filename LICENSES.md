# Лицензии используемых сторонних компонентов (Third-Party Licenses)

Программный продукт **GUI_YOLO** разработан Казаковым Данилом Викторовичем (GodsWarior) и распространяется под пермиссивной свободной лицензией **MIT License**.

Ниже приводится подробная информация о сторонних программных библиотеках, модулях и фреймворках, используемых в проекте, их правообладателях и лицензионных условиях.

---

## 1. Сводная таблица зависимостей

| Компонент / Библиотека | Назначение в проекте | Лицензия | Ссылка на репозиторий / сайт |
|---|---|---|---|
| **Ultralytics YOLOv8** | Детекция объектов, архитектура нейросети, веса и модуль обучения | AGPL-3.0 / Enterprise | [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) |
| **PyQt6** | Графический интерфейс пользователя (GUI), окна, виджеты | GPL-3.0 / Commercial | [riverbankcomputing.com](https://www.riverbankcomputing.com/software/pyqt/) |
| **OpenCV (`opencv-python`)** | Обработка изображений, захват видеопотока, нарезка кадров | Apache 2.0 | [opencv/opencv](https://github.com/opencv/opencv) |
| **PyTorch (`torch`, `torchvision`)** | Глубокое обучение, матричные вычисления на CPU/CUDA | BSD-3-Clause | [pytorch/pytorch](https://github.com/pytorch/pytorch) |
| **PyYAML** | Парсинг и генерация файлов конфигурации датасетов `data.yaml` | MIT | [yaml/pyyaml](https://github.com/yaml/pyyaml) |
| **NumPy** | Массивы, нормализация координат Bounding Box | BSD-3-Clause | [numpy/numpy](https://github.com/numpy/numpy) |

---

## 2. Подробные условия сторонних лицензий

### 2.1. Ultralytics YOLOv8 (AGPL-3.0 / Enterprise)
* **Правообладатель**: Copyright (c) 2023 Ultralytics Inc.
* **Условия**: Библиотека Ultralytics распространяется под лицензией GNU Affero General Public License v3.0 (AGPL-3.0) для открытых некоммерческих проектов и под Enterprise License для закрытых коммерческих систем. Исходный код GUI_YOLO открыт для сообщества, что соответствует условиям свободного использования AGPL-3.0.

### 2.2. PyQt6 (GPL-3.0 / Commercial)
* **Правообладатель**: Copyright (c) 2021 Riverbank Computing Limited.
* **Условия**: PyQt6 доступен под лицензией GNU General Public License v3.0 (GPL-3.0). Исходный код проекта GUI_YOLO опубликован на GitHub без ограничений на изучение и модификацию.

### 2.3. OpenCV (`opencv-python`) (Apache License 2.0)
* **Правообладатель**: Copyright (c) OpenCV team.
* **Условия**: Лицензия Apache 2.0 разрешает свободное коммерческое и некоммерческое использование, модификацию и распространение при условии сохранения уведомлений об авторских правах и текста лицензии Apache 2.0.

### 2.4. PyTorch (BSD-3-Clause)
* **Правообладатель**: Copyright (c) 2016-present Meta Platforms, Inc. and affiliates.
* **Условия**: Разрешается повторное распространение и использование в исходной и двоичной формах при сохранении оригинального уведомления об авторских правах.

### 2.5. PyYAML (MIT License)
* **Правообладатель**: Copyright (c) 2017-2020 Ingy döt Net, Kirill Simonov.
* **Условия**: Пермиссивная лицензия MIT допускает использование, копирование, изменение и объединение с сохранением уведомления об авторстве.

---

## 3. Юридическая совместимость и правила распространения

* Собственный исходный код проекта GUI_YOLO (модули `main.py`, `GUI.py`, `neural_network.py`, `network_training_etc.py`, `mask_and_neural_network.py`, `test.py`) лицензирован автором на условиях **MIT License**.
* Пользователи и разработчики, создающие производные продукты на базе GUI_YOLO, обязаны соблюдать условия лицензий зависимостей (в частности, требования AGPL-3.0 и GPL-3.0 при дистрибуции скомпилированных бинарных сборок приложения).
