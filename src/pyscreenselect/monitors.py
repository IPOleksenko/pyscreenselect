import screeninfo
from PyQt5.QtGui import QCursor


class Monitor:
    def get_monitors(self) -> list:
        return screeninfo.get_monitors()

    def get_main_monitor(self):
        return next((monitor for monitor in self.get_monitors() if monitor.is_primary), None)

    def count(self) -> int:
        return len(self.get_monitors())

    def virtual_bounds(self) -> tuple:
        monitors = self.get_monitors()
        if not monitors:
            return 0, 0, 0, 0
        return (
            min(m.x for m in monitors),
            min(m.y for m in monitors),
            max(m.x + m.width for m in monitors),
            max(m.y + m.height for m in monitors),
        )

    def is_multimonitor(self) -> bool:
        return self.count() > 1

    def largest(self):
        return max(self.get_monitors(), key=lambda m: m.width * m.height, default=None)

    def smallest(self):
        return min(self.get_monitors(), key=lambda m: m.width * m.height, default=None)

    def center(self, monitor) -> tuple:
        return monitor.x + monitor.width // 2, monitor.y + monitor.height // 2

    def is_primary(self, monitor) -> bool:
        return monitor.is_primary

    def get_monitor_at_cursor(self):
        cursor_pos = QCursor.pos()
        for monitor in self.get_monitors():
            if (
                monitor.x <= cursor_pos.x() <= monitor.x + monitor.width
                and monitor.y <= cursor_pos.y() <= monitor.y + monitor.height
            ):
                return monitor
        return None
