import cv2


def load_camera(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Ошибка: не удалось открыть веб-камеру.")
        return None
    return cap

def process_frame(frame, model):
    """
    Обрабатывает один кадр с использованием модели YOLO и возвращает кадр с отрисованными объектами.

    :param frame: Входной кадр (BGR).
    :param model: Объект модели YOLO.
    :return: Обработанный кадр (BGR).
    """
    # Преобразование в RGB для модели
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(rgb_frame)

    # Отображение результатов
    for result in results[0].boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0])
        confidence = result.conf[0]
        class_id = int(result.cls[0])

        # Рисуем прямоугольник и текст
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"Hole {class_id}: {confidence:.2f}"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return frame


def process_video(video_path, model):
    """
    Запускает обработку видео с использованием модели YOLO.

    :param video_path: Путь к видеофайлу.
    :param model: Объект модели YOLO.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Ошибка открытия видео: {video_path}")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Обработка кадра
        processed_frame = process_frame(frame, model)

        # Отображение обработанного кадра
        cv2.imshow("Обнаруженные объекты", processed_frame)

        # Останавливаем при нажатии клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def process_image(image_path, model):
    """
    Запускает обработку изображения с использованием модели YOLO.

    :param image_path: Путь к изображению.
    :param model: Объект модели YOLO.
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"Ошибка загрузки изображения: {image_path}")
        return

    # Обработка кадра
    processed_image = process_frame(image, model)

    # Отображение обработанного изображения
    cv2.imshow("Обнаруженные объекты", processed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()