import aqt
import aqt.qt
from aqt import Qt
from aqt.qt import (
    QPushButton,
    QPixmap,
    QColor,
    QIcon,
)


class HoverButton(QPushButton):
    """
    Custom button for handling button icon tinting during hover events with QPushButtons.
    """

    tint_color = "#FFFFFF"
    mask_color = "black"
    raw_icon = None

    def _updateIcon(self, is_hovered: bool):
        if is_hovered:
            pixmap = self.raw_icon.pixmap(self.size(), QIcon.Normal, QIcon.On)
            mask = pixmap.createMaskFromColor(QColor(self.mask_color), Qt.MaskOutColor)
            pixmap.fill(QColor(self.tint_color))
            pixmap.setMask(mask)
            self.setIcon(QIcon(pixmap))
        else:
            pixmap = self.raw_icon.pixmap(self.size(), QIcon.Normal, QIcon.On)
            mask = pixmap.createMaskFromColor(QColor(self.tint_color), Qt.MaskOutColor)
            pixmap.fill(QColor(self.mask_color))
            pixmap.setMask(mask)
            self.setIcon(QIcon(pixmap))

    def setMaskColor(self, color: str):
        self.mask_color = color

    def setTint(self, tint: str):
        self.tint_color = tint

    def setIcon(self, icon: QIcon) -> None:
        super().setIcon(icon)
        self.raw_icon = icon

    def enterEvent(self, *args, **kwargs):
        super().enterEvent(*args, *kwargs)
        self._updateIcon(True)

    def leaveEvent(self, *args, **kwargs):
        super().leaveEvent(*args, *kwargs)
        self._updateIcon(False)
