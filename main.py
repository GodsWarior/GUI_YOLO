import GUI

if __name__ == "__main__":
    app = GUI.QApplication([])
    window = GUI.YOLO_GUI()
    window.show()
    app.exec()

