from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont, QPainterPath, QPen
import sys

class Overlay(QWidget):
    selectionFinished = pyqtSignal(object)

    def __init__(self, monitor, color=QColor(0, 0, 0, 100), text=None,
                 text_color=QColor(255, 255, 255), font=None, font_size=24,
                 text_position=None, draw_text_after_background=False,
                 selection_color=QColor(0, 0, 0, 100),
                 selection_border_color=QColor(0, 0, 0, 100),
                 selection_border_width=2):

        if self.__class__ is Overlay:
            raise TypeError(
                "Overlay is an abstract class and cannot be instantiated directly."
            )

        self.app = QApplication.instance() or QApplication(sys.argv)

        super().__init__()
        
        self.monitor = monitor
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font or QFont("Arial", font_size)
        self.text_position = text_position
        self.draw_text_after_background = draw_text_after_background
        self.selection_color = selection_color
        self.selection_border_color = selection_border_color
        self.selection_border_width = selection_border_width

        self.start = self.end = QPoint()
        self.selecting = False
        self.selection_points = []
        self.selection_closed = False

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(monitor.x, monitor.y, monitor.width, monitor.height)
        self.setMouseTracking(True)
        self.setCursor(Qt.CrossCursor)
        self.show()
        self.activateWindow()
        self.raise_()

    def _draw_shape(self, painter, draw_fn):
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.selection_color)
        draw_fn(painter)

    def _draw_shape_border(self, painter, draw_fn):
        painter.setPen(QPen(self.selection_border_color, self.selection_border_width,
                           cap=Qt.RoundCap, join=Qt.RoundJoin))
        painter.setBrush(Qt.NoBrush)
        draw_fn(painter)

    def draw_text(self, painter):
        if self.text:
            painter.setPen(self.text_color)
            painter.setFont(self.font)
            if self.text_position:
                painter.drawText(*self.text_position, self.text)
            else:
                painter.drawText(self.rect(), Qt.AlignCenter, self.text)

    def draw_overlay(self, painter):
        painter.fillRect(self.rect(), self.color)

    def draw_selection(self, painter):
        raise NotImplementedError

    def draw_selection_border(self, painter):
        raise NotImplementedError

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.draw_text_after_background:
            self.draw_overlay(painter)
            self.draw_text(painter)
        else:
            self.draw_text(painter)
            self.draw_overlay(painter)
        self.draw_selection(painter)
        self.draw_selection_border(painter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = self.end = event.pos()
            self.selecting = True
            self.selection_closed = False
            self.update()

    def mouseMoveEvent(self, event):
        if self.selecting:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end = event.pos()
            self.selecting = False
            self.update()
            self.selectionFinished.emit(self.get_selection_result())
            self.close()

    def closeEvent(self, event):
        QApplication.quit()
        event.accept()

    def get_selection_result(self):
        return None


class RectangleSelectionOverlay(Overlay):
    def _get_rect(self):
        start_x = self.start.x()
        start_y = self.start.y()
        end_x = self.end.x()
        end_y = self.end.y()

        left = min(start_x, end_x)
        top = min(start_y, end_y)
        width = abs(end_x - start_x)
        height = abs(end_y - start_y)

        if width <= 0 and height <= 0:
            return QRect()
        return QRect(left, top, width, height)

    def draw_selection(self, painter):
        rect = self._get_rect()
        if not rect.isNull():
            self._draw_shape(painter, lambda p: p.drawRect(rect))

    def draw_selection_border(self, painter):
        rect = self._get_rect()
        if not rect.isNull():
            self._draw_shape_border(painter, lambda p: p.drawRect(rect))

    def get_selection_result(self):
        return self._get_rect()

class FreeformSelectionOverlay(Overlay):
    def _build_path(self, close=False):
        if len(self.selection_points) < 2:
            return None
        path = QPainterPath()
        path.moveTo(self.selection_points[0])
        for point in self.selection_points[1:]:
            path.lineTo(point)
        if close:
            path.closeSubpath()
        return path

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        if not self.selecting:
            self.selecting = True
            self.selection_points = [event.pos()]
            self.selection_closed = False
        else:
            self.selection_points.append(event.pos())
        self.update()

    def mouseMoveEvent(self, event):
        if self.selecting and event.buttons() & Qt.LeftButton:
            if not self.selection_points or self.selection_points[-1] != event.pos():
                self.selection_points.append(event.pos())
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selecting = False
            self.update()
            self.selectionFinished.emit(self.selection_points.copy())
            self.close()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and self.selection_points:
            self.selection_closed = True
            self.update()

    def draw_selection(self, painter):
        path = self._build_path(close=self.selection_closed)
        if path:
            self._draw_shape(painter, lambda p: p.drawPath(path))

    def draw_selection_border(self, painter):
        path = self._build_path(close=self.selection_closed)
        if path:
            self._draw_shape_border(painter, lambda p: p.drawPath(path))

    def get_selection_result(self):
        return self.selection_points.copy()