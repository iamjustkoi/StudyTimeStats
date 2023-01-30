from aqt import Qt
from aqt.qt import (
    QToolButton,
    QColor,
    QShowEvent,
    QIcon,
)


class HoverButton(QToolButton):
    """
    Custom button for handling button icon tinting during hover events with QPushButtons.
    """

    tint = "#FFFFFF"
    hover_tint = "#8a8a8a"
    mask_color = "black"
    raw_icon = None

    def _updateIcon(self, is_hovered: bool):
        """
        Updates the icon of the HoverButton to a tinted color if the mouse is currently hovering over it.

        :param is_hovered: whether the mouse is currently hovered over the HoverButton
        """

        pixmap = self.raw_icon.pixmap(self.size(), QIcon.Normal, QIcon.On)

        if is_hovered:
            mask = pixmap.createMaskFromColor(QColor(self.mask_color), Qt.MaskOutColor)
            pixmap.fill(QColor(self.hover_tint))
            pixmap.setMask(mask)
            self.setIcon(QIcon(pixmap))

        else:
            mask = pixmap.createMaskFromColor(QColor(self.mask_color), Qt.MaskOutColor)
            pixmap.fill(QColor(self.tint))
            pixmap.setMask(mask)
            self.setIcon(QIcon(pixmap))

    def setMaskColor(self, color: str):
        self.mask_color = color

    def setTint(self, tint: str):
        self.tint = tint

    def setHoverTint(self, tint: str):
        """
        Set the color of the icon when the mouse is hovering over the button.
        :param tint: a string representation of the color
        """
        self.hover_tint = tint

    def setRawIcon(self, icon: QIcon) -> None:
        self.raw_icon = icon

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self._updateIcon(False)

    def enterEvent(self, *args, **kwargs):
        super().enterEvent(*args, *kwargs)
        self._updateIcon(True)

    def leaveEvent(self, *args, **kwargs):
        super().leaveEvent(*args, *kwargs)
        self._updateIcon(False)
