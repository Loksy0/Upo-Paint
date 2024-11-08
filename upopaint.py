import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QColorDialog, QToolBar, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint

class RysuRysu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UPO PAINT")
        self.setGeometry(100, 100, 800, 600)
        self.last_point = QPoint()
        self.drawing = False
        self.lines = [] 
        self.pen_color = QColor(Qt.black)  
        self.pen_size = 3 
        self.initUI()

    def initUI(self):
        toolbar = QToolBar("Toolbar", self)
        self.addToolBar(toolbar)

        size_label = QLabel("Size:", self)
        toolbar.addWidget(size_label)

        self.size_input = QLineEdit(self)
        self.size_input.setText(str(self.pen_size)) 
        self.size_input.setFixedWidth(40)
        self.size_input.returnPressed.connect(self.change_size) 
        toolbar.addWidget(self.size_input)

        color_label = QLabel("Color:", self)
        toolbar.addWidget(color_label)

        self.color_button = QPushButton(self)
        self.color_button.setFixedSize(30, 30)
        self.color_button.setStyleSheet(f"background-color: {self.pen_color.name()};")  
        self.color_button.clicked.connect(self.change_color)  
        toolbar.addWidget(self.color_button)

    def change_size(self):
        try:
            new_size = int(self.size_input.text())
            if new_size > 0:
                self.pen_size = new_size
        except ValueError:
            pass  

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.pen_color = color
            self.color_button.setStyleSheet(f"background-color: {self.pen_color.name()};")  

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            current_point = event.pos()
            self.lines.append((self.last_point, current_point, self.pen_color, self.pen_size))  
            self.last_point = current_point
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        for line in self.lines:  
            pen = QPen(line[2], line[3], Qt.SolidLine)  
            painter.setPen(pen)
            painter.drawLine(line[0], line[1])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RysuRysu()
    window.show()
    sys.exit(app.exec_())
