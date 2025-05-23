import json
import yaml
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QWidget,
    QStackedWidget, QSpinBox, QTextEdit, QLabel
)
from PyQt6.QtGui import QIcon
from ultralytics import YOLO

import neural_network
import network_training_etc
import mask_and_neural_network


CONFIG_PATH = "config.json"


def load_config():
    try:
        with open(CONFIG_PATH, "r") as file:
            config = json.load(file)
    except FileNotFoundError:
        config = {}

    default_config = {
        "model_path": "yolo8n.pt",
        "video_path": "videoTest2.mp4",
        "output_folder": "output_images",
        "dataset_path": "dataset",
        "epochs": 15,
        "batch": 2,
        "imgsz": 640,
        "num_classes": 4,
        "class_names": ["Hole", "class1", "class2", "class3"],
        "data_yaml_path": "data.yaml"
    }

    for key, value in default_config.items():
        if key not in config:
            config[key] = value

    return config


def save_config(config):
    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=4)

def update_data_yaml(num_classes, class_names):
    config = load_config()
    data_yaml_path = config.get("data_yaml_path", "data.yaml")

    data = {
        'train': 'dataset/train/images',
        'val': 'dataset/valid/images',
        'test': 'dataset/test/images',
        'nc': num_classes,
        'names': class_names
    }

    try:
        with open(data_yaml_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        print(f"Файл {data_yaml_path} успешно обновлён!")
    except Exception as e:
        print(f"Ошибка при обновлении {data_yaml_path}: {e}")


class YOLO_GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("network_icon.png"))
        self.setWindowTitle("YOLO neural network")
        self.setGeometry(200, 200, 400, 300)
        self.config = load_config()
        self.model = YOLO(self.config["model_path"])

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.main_menu = self.create_main_menu()
        self.usage_menu = self.create_usage_menu()
        self.training_menu = self.create_training_menu()

        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.usage_menu)
        self.stack.addWidget(self.training_menu)

        self.stack.setCurrentWidget(self.main_menu)

    def create_main_menu(self):
        layout = QVBoxLayout()

        btn_usage = QPushButton("Использование сети")
        btn_usage.clicked.connect(lambda: self.stack.setCurrentWidget(self.usage_menu))
        layout.addWidget(btn_usage)

        btn_training = QPushButton("Обучение сети")
        btn_training.clicked.connect(lambda: self.stack.setCurrentWidget(self.training_menu))
        layout.addWidget(btn_training)

        btn_exit = QPushButton("Выход")
        btn_exit.clicked.connect(self.close)
        layout.addWidget(btn_exit)

        container = QWidget()
        container.setLayout(layout)
        return container

    def create_usage_menu(self):
        layout = QVBoxLayout()

        btn_model = QPushButton("Выбрать модель")
        btn_model.clicked.connect(self.select_model)
        layout.addWidget(btn_model)

        btn_image = QPushButton("Выбрать изображение")
        btn_image.clicked.connect(self.process_image)
        layout.addWidget(btn_image)

        btn_video = QPushButton("Выбрать видео")
        btn_video.clicked.connect(self.process_video)
        layout.addWidget(btn_video)

        btn_camera = QPushButton("Запуск камеры")
        btn_camera.clicked.connect(self.display_from_camera)
        layout.addWidget(btn_camera)

        btn_back = QPushButton("Назад")
        btn_back.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_menu))
        layout.addWidget(btn_back)

        container = QWidget()
        container.setLayout(layout)
        return container

    def create_training_menu(self):
        layout = QVBoxLayout()

        self.spin_classes = QSpinBox()
        self.spin_classes.setMinimum(1)
        self.spin_classes.setMaximum(20)
        self.spin_classes.setValue(self.config["num_classes"])
        layout.addWidget(QLabel("Количество классов:"))
        layout.addWidget(self.spin_classes)

        self.text_classes = QTextEdit()
        self.text_classes.setPlaceholderText("Введите названия классов через запятую")
        self.text_classes.setText(", ".join(self.config["class_names"]))
        layout.addWidget(QLabel("Названия классов:"))
        layout.addWidget(self.text_classes)

        btn_model = QPushButton("Выбрать модель")
        btn_model.clicked.connect(self.select_model)
        layout.addWidget(btn_model)

        btn_slice = QPushButton("Обрезать видео на фотографии")
        btn_slice.clicked.connect(self.slice_video)
        layout.addWidget(btn_slice)

        btn_marking = QPushButton("Разметить фотографии")
        btn_marking.clicked.connect(self.manual_marking)
        layout.addWidget(btn_marking)

        btn_train = QPushButton("Обучить сеть")
        btn_train.clicked.connect(self.train_network)
        layout.addWidget(btn_train)

        btn_back = QPushButton("Назад")
        btn_back.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_menu))
        layout.addWidget(btn_back)

        container = QWidget()
        container.setLayout(layout)
        return container

    def display_from_camera(self):
        mask_and_neural_network.display_from_camera(model=self.model)

    def select_model(self):
        model_path, _ = QFileDialog.getOpenFileName(self, "Выберите модель YOLO", "", "YOLO Weights (*.pt)")
        if model_path:
            self.config["model_path"] = model_path
            save_config(self.config)
            self.model = YOLO(model_path)
            QMessageBox.information(self, "Успех", f"Модель загружена: {model_path}")

    def process_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.jpg *.png)")
        if image_path:
            self.config["image_path"] = image_path
            save_config(self.config)
            neural_network.process_image(image_path, self.model)

    def process_video(self):
        video_path, _ = QFileDialog.getOpenFileName(self, "Выберите видео", "", "Videos (*.mp4 *.avi)")
        if video_path:
            self.config["video_path"] = video_path
            save_config(self.config)
            neural_network.process_video(video_path, self.model)

    def slice_video(self):
        video_path, _ = QFileDialog.getOpenFileName(self, "Выберите видео", "", "Videos (*.mp4 *.avi)")
        folder_to_save = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения фотографий", "")
        folder_to_save = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения фотографий", "")
        if video_path and folder_to_save:
            self.config["video_path"] = video_path
            self.config["output_folder"] = folder_to_save
            save_config(self.config)
            network_training_etc.splitVideoToImages(video_path=self.config["video_path"],
                                                    output_folder=self.config["output_folder"], frame_interval=1)
            QMessageBox.information(self, "Успех", f"Фотографии помещены в {self.config['output_folder']}")

    def manual_marking(self):
        folder_with_images = QFileDialog.getExistingDirectory(self, "Выберите папку с фотографиями", "")
        folder_to_save = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения датасета", "")
        if folder_to_save and folder_with_images:
            self.config["dataset_path"] = folder_to_save
            self.config["output_folder"] = folder_with_images
            network_training_etc.manualMarking(full_images_path=self.config["output_folder"],
                                               dataset_path=self.config["dataset_path"])

    def train_network(self):
        try:
            model = YOLO(self.config["model_path"])

            dataset_dir = QFileDialog.getExistingDirectory(self, "Выберите папку с датасетом")
            if not dataset_dir:
                QMessageBox.warning(self, "Отмена", "Вы не выбрали папку с датасетом.")
                return

            data_yaml_path = os.path.join(os.path.dirname(__file__), "data.yaml")
            if not os.path.exists(data_yaml_path):
                QMessageBox.critical(self, "Ошибка", "Файл data.yaml не найден.")
                return

            with open(data_yaml_path, 'r') as f:
                data_config = yaml.safe_load(f)

            # Обновление путей к датасету
            data_config["train"] = os.path.join(dataset_dir, "train/images")
            data_config["val"] = os.path.join(dataset_dir, "valid/images")
            data_config["test"] = os.path.join(dataset_dir, "test/images")

            # Обновление количества классов и их названий
            num_classes = self.spin_classes.value()
            class_names = [name.strip() for name in self.text_classes.toPlainText().split(",") if name.strip()]

            if len(class_names) != num_classes:
                QMessageBox.warning(self, "Ошибка", "Количество классов и названий не совпадает.")
                return

            data_config["nc"] = num_classes
            data_config["names"] = class_names

            with open(data_yaml_path, 'w') as f:
                yaml.safe_dump(data_config, f, default_flow_style=False, allow_unicode=True)

            save_dir = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения модели")
            if not save_dir:
                QMessageBox.warning(self, "Отмена", "Вы не выбрали папку для сохранения.")
                return

            network_training_etc.network_learning(
                model=model,
                data_path=data_yaml_path,
                save_dir=save_dir,
                epochs=self.config["epochs"],
                batch=self.config["batch"]
            )

            QMessageBox.information(self, "Обучение", "Обучение завершено!")
        except RuntimeError as e:
            QMessageBox.critical(self, "Ошибка", str(e))
