from aqt import Qt
from aqt.qt import (
    QToolButton,
    QColor,
    QShowEvent,
    QIcon,
)

from aqt.qt import (
    QMouseEvent,
    QListWidget,
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
        if not self.locked:
            self._updateIcon(False)

    def lockHoverTint(self, locked: bool = True):
        self.locked = locked


class DragHandle(QToolButton):
    start_pos = None
    list_widget: QListWidget = None
    is_dragging = False
    list_item = None
    icon_color = '#FFFFFF'

    def __init__(self, *args):
        super().__init__(*args)
        self.setCursor(Qt.OpenHandCursor)
        
    def setIcon(self, icon: QIcon) -> None:
        pixmap = icon.pixmap(self.size(), QIcon.Normal, QIcon.On)
        mask = pixmap.createMaskFromColor(QColor('black'), Qt.MaskOutColor)
        pixmap.fill(QColor(self.icon_color))
        pixmap.setMask(mask)
        super().setIcon(QIcon(pixmap))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.start_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        offset = self.start_pos.y() - event.pos().y() if self.start_pos else 0

        if abs(offset) > 5:
            # moved beyond range (enough to consider a drag check/updates)
            self.drag(offset)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.is_dragging = False
        self.start_pos = None
        self.setCursor(Qt.OpenHandCursor)

    def drag(self, offset: int, padding=4):
        if not self.is_dragging:
            self.is_dragging = True
            self.setCursor(Qt.ClosedHandCursor)

        if self.list_widget and self.list_item and abs(offset) > ((self.parentWidget().height() / 2) + padding):
            drag_idx = self.list_widget.row(self.list_item)
            target_idx = drag_idx + (1 if offset < 0 else -1)

            if target_idx != self.list_widget.count() - 1:
                # target index isn't the last cell item (empty cell)
                target_item = self.list_widget.item(target_idx)

                if target_item:
                    self.list_item.cell_item.index = target_idx
                    target_item.cell_item.index = drag_idx

                self.list_widget.sortItems()
                # Broadcast change
                self.list_widget.currentRowChanged.emit(self.list_item.cell_item.index)

