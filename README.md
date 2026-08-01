# pyscreenselect

pyscreenselect is a small Python library for interactive screen-region selection using PyQt5. It lets you create an overlay on one of the connected monitors, draw a selection rectangle or freeform path, and receive the resulting geometry as a Python object.

## Features

- Select a region on the primary or current monitor
- Support for rectangular selection
- Support for freeform selection with mouse drawing
- Receive the selected area through a Qt signal
- Customize overlay colors, text, and border styling
- Detect the monitor under the current mouse cursor

## Installation

```bash
pip install pyscreenselect
```

## Quick start

The simplest example shows how to launch the overlay and print the selection result:

```python
import sys
from PyQt5.QtWidgets import QApplication
from pyscreenselect.monitors import Monitor
from pyscreenselect.overlay import RectangleSelectionOverlay


def main() -> int:
    app = QApplication(sys.argv)

    monitor = Monitor()
    main_monitor = monitor.get_main_monitor()
    if main_monitor is None:
        return 1

    overlay = RectangleSelectionOverlay(main_monitor, text="Select area")
    overlay.selectionFinished.connect(print)
    overlay.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
```

## API overview

### Monitor helpers

The Monitor class provides access to screen information:

```python
from pyscreenselect.monitors import Monitor

monitor = Monitor()

print(monitor.count())
print(monitor.get_main_monitor())
print(monitor.get_monitor_at_cursor())
print(monitor.virtual_bounds())
```

### Overlay classes

- Overlay — base class for all overlays
- RectangleSelectionOverlay — draws a rectangular selection
- FreeformSelectionOverlay — draws a freeform path selection

### Example: rectangle selection

```python
import sys
from PyQt5.QtWidgets import QApplication
from pyscreenselect.monitors import Monitor
from pyscreenselect.overlay import RectangleSelectionOverlay


app = QApplication(sys.argv)
monitor = Monitor().get_main_monitor()

overlay = RectangleSelectionOverlay(
    monitor,
    text="Drag to select",
    color=(0, 0, 0, 80),
    selection_color=(255, 0, 0, 150),
    selection_border_color=(255, 0, 0),
    selection_border_width=3,
)


def on_selection_finished(rect):
    print("Selected rectangle:", rect)


overlay.selectionFinished.connect(on_selection_finished)
overlay.show()
app.exec_()
```

### Example: freeform selection

```python
import sys
from PyQt5.QtWidgets import QApplication
from pyscreenselect.monitors import Monitor
from pyscreenselect.overlay import FreeformSelectionOverlay


app = QApplication(sys.argv)
monitor = Monitor().get_main_monitor()

overlay = FreeformSelectionOverlay(
    monitor,
    text="Click and draw",
    selection_color=(0, 180, 255, 160),
    selection_border_color=(0, 120, 255),
    selection_border_width=2,
)


def on_selection_finished(points):
    print("Selected points:", points)


overlay.selectionFinished.connect(on_selection_finished)
overlay.show()
app.exec_()
```

### Example: use the monitor under the cursor

```python
from pyscreenselect.monitors import Monitor

monitor = Monitor()
current_monitor = monitor.get_monitor_at_cursor()
if current_monitor is not None:
    print(current_monitor.width, current_monitor.height)
```

## Selection result format

- RectangleSelectionOverlay returns a QRect object
- FreeformSelectionOverlay returns a list of points

## Customization

You can customize the overlay appearance using parameters such as:

- color — background overlay color
- text — text shown over the overlay
- text_color — text color
- selection_color — fill color of the selection
- selection_border_color — border color
- selection_border_width — border thickness
- font / font_size — text styling

## Authors

- [IPOleksenko](https://github.com/IPOleksenko) (owner) — Developer

## License

This project is licensed under the [MIT License][license].

[license]: ./LICENSE
