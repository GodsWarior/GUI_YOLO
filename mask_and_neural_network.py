# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Kazakou Danil Viktorovich (GodsWarior)
# GUI_YOLO: Dataset Editor and Annotation Studio for YOLO

import neural_network
import cv2
import time

def process_frame(frame, model):
    nn_frame = neural_network.process_frame(frame, model)
    return nn_frame


def process_video(video_path, model):
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

def display_from_camera(camera_index=0, model=None):
    cap = neural_network.load_camera(camera_index)
    if cap is None:
        return

    prev_time = time.time()
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Не удалось прочитать кадр.")
            break

        processed_frame = process_frame(frame, model)
        cv2.imshow('Processed Video (Camera)', processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - prev_time
        if elapsed_time >= 1.0:
            fps = frame_count / elapsed_time
            print(f"FPS: {fps:.2f}")
            frame_count = 0
            prev_time = current_time

    cap.release()
    cv2.destroyAllWindows()
