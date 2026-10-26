# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Kazakou Danil Viktorovich (GodsWarior)
# GUI_YOLO: Dataset Editor and Annotation Studio for YOLO

import cv2 as cv
import numpy as np
import time

def load_camera(camera_index=0):
    cap = cv.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Ошибка: не удалось открыть веб-камеру.")
        return None
    return cap

def load_video(video_path):
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        print("Ошибка: не удалось открыть видео.")
        return None
    return cap

def frameHandlerCanny(frame):
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_frame = cv.bilateralFilter(gray_frame, 11, 15, 15)
    edges = cv.Canny(gray_frame, 140, 150)
    return edges

def process_frame(frame):
    # Новый пустой черный кадр
    new_frame = np.zeros(frame.shape, dtype='uint8')

    # Применение фильтра Гаусса для сглаживания
    frame = cv.GaussianBlur(frame, (11, 11), 0)  # Уменьшен размер окна для ускорения

    # Применение детектора Canny для обнаружения границ
    frame = frameHandlerCanny(frame)

    # Применение метода Хафа для поиска линий
    lines = cv.HoughLinesP(frame, 1, np.pi / 180, threshold=30, minLineLength=30, maxLineGap=20)

    # Рисуем найденные линии на новом кадре
    if lines is not None:
        for line in lines[:20]:
            x1, y1, x2, y2 = line[0]
            cv.line(new_frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

    return frame

def display_from_camera(camera_index=0):
    cap = load_camera(camera_index)
    if cap is None:
        return

    prev_time = time.time()
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Не удалось прочитать кадр.")
            break

        processed_frame = process_frame(frame)
        cv.imshow('Processed Video (Camera)', processed_frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
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
    cv.destroyAllWindows()

def display_from_video(video_path):
    cap = load_video(video_path)
    if cap is None:
        return

    prev_time = time.time()
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Видео закончилось или не удалось прочитать кадр.")
            break

        processed_frame = process_frame(frame)
        cv.imshow('Processed Video (File)', processed_frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
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
    cv.destroyAllWindows()


# Для веб-камеры
# display_from_camera()

# Для видеофайла
display_from_video('vid/video_2024-10-28_14-39-47.mp4')# видео с дырками
display_from_video('vid/video_2024-10-28_14-46-04.mp4')