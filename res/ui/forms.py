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
        """
        Updates the icon of the HoverButton to a tinted color if the mouse is currently hovering over it.

        :param is_hovered: whether the mouse is currently hovered over the HoverButton
        """
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
        """
        Set the color of the icon when the mouse is hovering over the button.
        :param tint: a string representation of the color
        """
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
