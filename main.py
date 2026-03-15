import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap


class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Screen Draw")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().size()
        self.resize(screen)

        self.pixmap = QPixmap(self.size())
        self.pixmap.fill(Qt.transparent)

        self.last_point = QPoint()
        self.drawing = False
        self.eraser = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.pixmap)

            if self.eraser:
                pen = QPen(Qt.transparent, 20)
                painter.setCompositionMode(QPainter.CompositionMode_Clear)
            else:
                pen = QPen(QColor(255, 0, 0), 4)

            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()

            self.update()

    def mouseReleaseEvent(self, event):
        self.drawing = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.eraser = not self.eraser


class ControlPanel(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Control")

        layout = QVBoxLayout()

        self.canvas = None

        start_btn = QPushButton("필기 시작")
        stop_btn = QPushButton("종료")

        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMinimum(20)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(80)

        layout.addWidget(start_btn)
        layout.addWidget(stop_btn)
        layout.addWidget(self.opacity_slider)

        self.setLayout(layout)

        start_btn.clicked.connect(self.start_draw)
        stop_btn.clicked.connect(self.close_app)
        self.opacity_slider.valueChanged.connect(self.change_opacity)

    def start_draw(self):
        self.canvas = Canvas()
        self.canvas.showFullScreen()

    def change_opacity(self, value):
        if self.canvas:
            self.canvas.setWindowOpacity(value / 100)

    def close_app(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    panel = ControlPanel()
    panel.show()
    sys.exit(app.exec_())
