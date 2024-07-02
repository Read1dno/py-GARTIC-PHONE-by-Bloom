import sys
from PySide6.QtWidgets import QApplication, QLabel, QFileDialog, QLineEdit, QVBoxLayout, QPushButton, QWidget
from PySide6.QtGui import QPixmap, QImage, QColor, QIcon
from PySide6.QtCore import Qt, QPoint

class TransparentImageWindow(QWidget):
    def __init__(self, pixmap):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.label.resize(pixmap.size())
        self.resize(pixmap.size())

        self.dragging = False
        self.drag_offset = QPoint()
        self.interactive = True

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.interactive:
            self.dragging = True
            self.drag_offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging and self.interactive:
            self.move(self.pos() + event.pos() - self.drag_offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def wheelEvent(self, event):
        if self.interactive:
            angle = event.angleDelta().y() / 8
            steps = angle / 15
            factor = 1 + steps * 0.1
            self.resize(self.size() * factor)
            self.label.resize(self.label.size() * factor)

    def updateOpacity(self, value):
        opacity = value / 100.0
        image = self.label.pixmap().toImage()
        image = image.convertToFormat(QImage.Format_ARGB32)

        for y in range(image.height()):
            for x in range(image.width()):
                pixel = image.pixel(x, y)
                alpha = QColor(pixel).alpha() * opacity
                color = QColor(pixel)
                color.setAlpha(int(alpha))
                image.setPixelColor(x, y, color)

        self.label.setPixmap(QPixmap.fromImage(image))

    def setNonInteractive(self):
        self.interactive = False
        self.setWindowFlags(self.windowFlags() | Qt.WindowTransparentForInput)
        self.show()

    def setInteractive(self):
        self.interactive = True
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowTransparentForInput)
        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_T or event.key() == Qt.Key_E:
            self.setNonInteractive()
        elif event.key() == Qt.Key_Y or event.key() == Qt.Key_N:
            self.setInteractive()

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel('Выберите изображение и настройте параметры:', self)

        self.button = QPushButton('Выбрать изображение', self)
        self.button.clicked.connect(self.loadImage)

        self.opacity_input = QLineEdit(self)
        self.opacity_input.setPlaceholderText('Введите прозрачность (%)')
        self.opacity_input.setEnabled(False)
        self.opacity_input.returnPressed.connect(self.changeOpacity)

        self.fix_button = QPushButton('Закрепить изображение (T)', self)  
        self.fix_button.clicked.connect(self.fixImage)
        self.fix_button.setEnabled(False)

        self.unfix_button = QPushButton('Открепить изображение (Y)', self)  
        self.unfix_button.clicked.connect(self.unfixImage)
        self.unfix_button.setEnabled(False)

        self.description_label = QLabel('Колесико мышки - менять размер\nЗажатой левой кнопкой мышки - перемещение\nT - закрепить картинку\nY - открепить картинку', self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.opacity_input)
        layout.addWidget(self.fix_button)
        layout.addWidget(self.unfix_button)
        layout.addWidget(self.description_label)
        self.setLayout(layout)

        self.image_window = None

    def loadImage(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)", options=options)
        if filePath:
            pixmap = QPixmap(filePath)
            if self.image_window is None:
                self.image_window = TransparentImageWindow(pixmap)
            else:
                self.image_window.label.setPixmap(pixmap)
                self.image_window.label.resize(pixmap.size())
                self.image_window.resize(pixmap.size())

            self.image_window.updateOpacity(35)
            self.image_window.show()
            self.opacity_input.setEnabled(True)
            self.fix_button.setEnabled(True)
            self.unfix_button.setEnabled(True)

    def changeOpacity(self):
        if self.image_window:
            try:
                value = int(self.opacity_input.text())
                if 0 <= value <= 100:
                    self.image_window.updateOpacity(value)
                else:
                    self.opacity_input.setText('')
            except ValueError:
                self.opacity_input.setText('')

    def fixImage(self):
        if self.image_window:
            self.image_window.setNonInteractive()
            self.fix_button.setEnabled(False)
            self.unfix_button.setEnabled(True)

    def unfixImage(self):
        if self.image_window:
            self.image_window.setInteractive()
            self.fix_button.setEnabled(True)
            self.unfix_button.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    
    app.setApplicationName("ImageOverlayApp")
    app.setApplicationDisplayName("Image Overlay Application")
    app.setWindowIcon(QIcon('icon.png'))

    settings_window = SettingsWindow()
    settings_window.show()

    def quitApp():
        if settings_window.image_window:
            settings_window.image_window.close()
        app.quit()
    
    def keyPressEvent(event):
        if event.key() == Qt.Key_Q or event.key() == Qt.Key_CyrillicShortI:
            quitApp()
    
    app.aboutToQuit.connect(quitApp)
    app.keyPressEvent = keyPressEvent

    app.exec()

if __name__ == '__main__':
    main()
