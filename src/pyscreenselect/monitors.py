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

    def get_monitor_at(self, x: int, y: int):
        return next(
            (m for m in self.get_monitors() if self.contains(m, x, y)),
            None,
        )

    def get_monitor_at_cursor(self):
        pos = QCursor.pos()
        return self.get_monitor_at(pos.x(), pos.y())
    
    def get(self, index: int):
        monitors = self.get_monitors()
        return monitors[index] if 0 <= index < len(monitors) else None

    def contains(self, monitor, x: int, y: int) -> bool:
        return (
            monitor.x <= x < monitor.x + monitor.width
            and monitor.y <= y < monitor.y + monitor.height
        )

    def size(self, monitor) -> tuple[int, int]:
        return monitor.width, monitor.height