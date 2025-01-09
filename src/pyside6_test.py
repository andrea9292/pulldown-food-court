from PySide6.QtWidgets import QApplication, QMainWindow

app = QApplication([])
window = QMainWindow()
window.setWindowTitle("PySide6 Installation Test")
window.setGeometry(100, 100, 800, 600)
window.show()
app.exec()