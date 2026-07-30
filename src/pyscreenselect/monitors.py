import screeninfo

class Monitor:
    def get_monitors(self):
        return screeninfo.get_monitors()

    def get_main_monitor(self):
        for monitor in self.get_monitors():
            if monitor.is_primary:
                return monitor
        return None

    def count(self):
        return len(self.get_monitors())

    def virtual_bounds(self):
        monitors = self.get_monitors()

        left = min(m.x for m in monitors)
        top = min(m.y for m in monitors)
        right = max(m.x + m.width for m in monitors)
        bottom = max(m.y + m.height for m in monitors)

        return left, top, right, bottom
    
    def is_multimonitor(self):
        return len(self.get_monitors()) > 1

    def largest(self):
        return max(
            self.get_monitors(),
            key=lambda m: m.width * m.height
        )
    
    def smallest(self):
        return min(
            self.get_monitors(),
            key=lambda m: m.width * m.height
        )

    def center(self, monitor):
        return (
            monitor.x + monitor.width // 2,
            monitor.y + monitor.height // 2,
        )

    def is_primary(self, monitor):
        return monitor.is_primary