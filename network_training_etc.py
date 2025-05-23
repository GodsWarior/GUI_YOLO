import time
import cv2
import os
import yaml
import shutil
import json


def normalize_coordinates(x1, y1, x2, y2, img_width, img_height):
    """
    Нормализует координаты (x1, y1, x2, y2) для YOLO.
    """
    x_center = ((x1 + x2) / 2) / img_width
    y_center = ((y1 + y2) / 2) / img_height
    width = abs(x2 - x1) / img_width
    height = abs(y2 - y1) / img_height
    return x_center, y_center, width, height


def splitVideoToImages(video_path='videoTest2.mp4', output_folder='output_images', frame_interval=1):
    """
        Делит видео на кадры в формате jpg и соханяет их.
    """
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Ошибка открытия видеофайла: {video_path}")
        return

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            timestamp = int(time.time() * 1000)
            output_path = os.path.join(output_folder, f'{timestamp}_frame_{saved_count:05d}.jpg')
            cv2.imwrite(output_path, frame)
            print(f"Сохранено: {output_path}")
            saved_count += 1
        frame_count += 1
    cap.release()


def resize_image(image, size=(640, 640)):
    return cv2.resize(image, size)


def update_data_yaml():
    data_yaml_path = 'data.yaml'
    data = {
        'train': 'dataset/train/images',
        'val': 'dataset/valid/images',
        'test': 'dataset/test/images',
        'nc': 4,
        'names': ['Hole', 'class1', 'class2', 'class3']
    }
    with open(data_yaml_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=None, sort_keys=False)
    print(f"Updated {data_yaml_path}")


def draw_rectangle(event, x, y, flags, param):
    """
            Метод для отрисовки прямоугольников на месте выделения объектов.
    """
    param_dict = param
    window_name = param_dict['window_name']
    colors = param_dict['colors']
    original_image = param_dict['original_image']
    annotations = param_dict['annotations']
    current_class = param_dict['current_class']

    if event == cv2.EVENT_LBUTTONDOWN:
        param_dict['drawing'] = True
        param_dict['ix'], param_dict['iy'] = x, y

    elif event == cv2.EVENT_MOUSEMOVE and param_dict.get('drawing', False):
        image = original_image.copy()
        for annotation in annotations:
            cls, x1, y1, x2, y2 = annotation
            cv2.rectangle(image, (x1, y1), (x2, y2), colors[cls], 2)
        cv2.rectangle(image, (param_dict['ix'], param_dict['iy']), (x, y), colors[current_class], 2)
        cv2.imshow(window_name, image)

    elif event == cv2.EVENT_LBUTTONUP:
        param_dict['drawing'] = False
        annotations.append((current_class, param_dict['ix'], param_dict['iy'], x, y))
        image = original_image.copy()
        for annotation in annotations:
            cls, x1, y1, x2, y2 = annotation
            cv2.rectangle(image, (x1, y1), (x2, y2), colors[cls], 2)
        cv2.imshow(window_name, image)

    elif event == cv2.EVENT_RBUTTONDOWN and annotations:
        annotations.pop()
        image = original_image.copy()
        for annotation in annotations:
            cls, x1, y1, x2, y2 = annotation
            cv2.rectangle(image, (x1, y1), (x2, y2), colors[cls], 2)
        cv2.imshow(window_name, image)


def manualMarking(full_images_path='output_images', dataset_path='dataset'):
    os.makedirs(dataset_path, exist_ok=True)
    train_images_path = os.path.join(dataset_path, 'train', 'images')
    train_labels_path = os.path.join(dataset_path, 'train', 'labels')
    os.makedirs(train_images_path, exist_ok=True)
    os.makedirs(train_labels_path, exist_ok=True)

    ready_images_path = os.path.join(full_images_path, 'ready')
    os.makedirs(ready_images_path, exist_ok=True)

    window_name = 'Annotation Tool'
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

    for filename in os.listdir(full_images_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(full_images_path, filename)
            image = cv2.imread(image_path)
            image = resize_image(image)
            original_image = image.copy()
            annotations = []
            current_class = 0

            param_dict = {
                'window_name': window_name,
                'colors': colors,
                'original_image': original_image,
                'annotations': annotations,
                'current_class': current_class,
                'drawing': False,
                'ix': -1,
                'iy': -1
            }

            cv2.namedWindow(window_name)
            cv2.setMouseCallback(window_name, draw_rectangle, param_dict)

            while True:
                image_with_annotations = original_image.copy()
                for annotation in annotations:
                    cls, x1, y1, x2, y2 = annotation
                    cv2.rectangle(image_with_annotations, (x1, y1), (x2, y2), colors[cls], 2)
                cv2.imshow(window_name, image_with_annotations)
                key = cv2.waitKey(1) & 0xFF

                if key == ord(' '):
                    output_image_path = os.path.join(train_images_path, filename)
                    cv2.imwrite(output_image_path, original_image)
                    print(f"Saved image to {output_image_path}")

                    label_filename = os.path.splitext(filename)[0] + '.txt'
                    label_file_path = os.path.join(train_labels_path, label_filename)
                    with open(label_file_path, 'w') as f:
                        for annotation in annotations:
                            cls, x1, y1, x2, y2 = annotation
                            x_center, y_center, width, height = normalize_coordinates(
                                x1, y1, x2, y2, 640, 640)
                            f.write(f"{cls} {x_center} {y_center} {width} {height}\n")
                    print(f"Saved labels to {label_file_path}")

                    update_data_yaml()

                    ready_image_path = os.path.join(ready_images_path, filename)
                    shutil.move(image_path, ready_image_path)
                    print(f"Moved image to {ready_image_path}")
                    break
                elif key == 27:
                    print("Skipped image")
                    break


            cv2.destroyAllWindows()

def network_learning(model, data_path, save_dir, epochs=6, batch=2, imgsz=640):
    results = model.train(data=data_path, epochs=epochs, batch=batch, imgsz=imgsz, name='red', device='cpu', project=save_dir)
    return results
