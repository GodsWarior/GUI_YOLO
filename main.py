# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Kazakou Danil Viktorovich (GodsWarior)
# GUI_YOLO: Dataset Editor and Annotation Studio for YOLO

import GUI

if __name__ == "__main__":
    app = GUI.QApplication([])
    window = GUI.YOLO_GUI()
    window.show()
    app.exec()
