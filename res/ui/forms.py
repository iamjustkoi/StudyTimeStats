from aqt import Qt
from aqt.qt import (
    QToolButton,
    QColor,
    QShowEvent,
    QIcon,
    QTransform,
    QMouseEvent,
    QListWidget,
    QT_VERSION_STR,
)

ANKI_QT_VER = int(QT_VERSION_STR.split('.')[0])

if ANKI_QT_VER == 5:
    MaskOutColor = Qt.MaskMode.MaskOutColor
    ClosedHandCursor = Qt.CursorShape.ClosedHandCursor
    OpenHandCursor = Qt.CursorShape.OpenHandCursor
    SmoothTransformation = Qt.TransformationMode.SmoothTransformation
else:
    MaskOutColor = Qt.MaskMode.MaskOutColor
    ClosedHandCursor = Qt.CursorShape.ClosedHandCursor
    OpenHandCursor = Qt.CursorShape.OpenHandCursor
    SmoothTransformation = Qt.TransformationMode.SmoothTransformation


class HoverButton(QToolButton):
    """
    Custom button for handling button icon tinting during hover events with QPushButtons.
    """

    tint = "#FFFFFF"
    hover_tint = "#8a8a8a"
    mask_color = "black"
    raw_icon = None
    locked = False

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

    def _updateIcon(self, is_hovered: bool):
        """
        Updates the icon of the HoverButton to a tinted color if the mouse is currently hovering over it.

        :param is_hovered: whether the mouse is currently hovered over the HoverButton
        """

        pixmap = self.raw_icon.pixmap(self.size(), QIcon.Mode.Normal, QIcon.State.On)

        if is_hovered:
            mask = pixmap.createMaskFromColor(QColor(self.mask_color), MaskOutColor)
            pixmap.fill(QColor(self.hover_tint))
            pixmap.setMask(mask)
            self.setIcon(QIcon(pixmap))

        else:
            mask = pixmap.createMaskFromColor(QColor(self.mask_color), MaskOutColor)
            pixmap.fill(QColor(self.tint))
            pixmap.setMask(mask)
            self.setIcon(QIcon(pixmap))

        self.adjustSize()
        self.setMinimumSize(self.sizeHint())


class RotateButton(QToolButton):
    rotation = 0
    tint = "#FFFFFF"
    mask_color = "black"
    raw_icon = None

    def setRotation(self, degrees: float):
        self.rotation = degrees
        self._updateIcon()

    def setRawIcon(self, icon: QIcon) -> None:
        self.raw_icon = icon

    def showEvent(self, evt: QShowEvent) -> None:
        super().showEvent(evt)
        self._updateIcon()

    def setMaskColor(self, color: str):
        self.mask_color = color

    def setTint(self, tint: str):
        self.tint = tint

    def _updateIcon(self):
        """
        Updates the icon of the RotateButton to the tinted color, using the stored mask color.
        """
        pixmap = self.raw_icon.pixmap(self.size(), QIcon.Mode.Normal, QIcon.State.On)\
            .transformed(QTransform().rotate(self.rotation), SmoothTransformation)
        mask = pixmap.createMaskFromColor(QColor(self.mask_color), MaskOutColor)
        pixmap.fill(QColor(self.tint))
        pixmap.setMask(mask)

        self.setIcon(QIcon(pixmap))

        self.adjustSize()
        self.setMinimumSize(self.sizeHint())


class DragHandle(QToolButton):
    start_pos = None
    last_drag_global_pos = None
    list_widget: QListWidget = None
    is_dragging = False
    list_item = None
    icon_color = '#FFFFFF'
    last_target_idx = -1
    padding = 4

    def __init__(self, *args):
        super().__init__(*args)
        self.setCursor(OpenHandCursor)
        
    def setIcon(self, icon: QIcon) -> None:
        pixmap = icon.pixmap(self.size(), QIcon.Mode.Normal, QIcon.State.On)
        mask = pixmap.createMaskFromColor(QColor('black'), MaskOutColor)
        pixmap.fill(QColor(self.icon_color))
        pixmap.setMask(mask)
        super().setIcon(QIcon(pixmap))

        self.adjustSize()
        self.setMinimumSize(self.sizeHint())

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.start_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        offset = self.start_pos.y() - event.pos().y() if self.start_pos else 0

        if abs(offset) > 5:
            # Moved beyond range (enough to consider a drag check/updates)
            self.drag(offset)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.is_dragging = False
        self.start_pos = None
        self.setCursor(OpenHandCursor)

    def drag(self, offset: int):
        if not self.is_dragging:
            self.is_dragging = True
            self.setCursor(ClosedHandCursor)

        # Offset greater than half of the currently dragged cell item's height (plus padding)
        if self.list_widget and self.list_item and abs(offset) > ((self.parentWidget().height() / 2) + self.padding):
            drag_idx = self.list_widget.row(self.list_item)
            target_idx = drag_idx + (-1 if offset > 0 else 1)

            move_dir = target_idx - drag_idx

            if target_idx != self.list_widget.count() - 1:
                # Target index isn't the last cell item (empty cell)
                target_item = self.list_widget.item(target_idx)

                if target_item:
                    did_switch_dir = False
                    if self.last_drag_global_pos:
                        current_drag_global_pos = self.parentWidget().cursor().pos()
                        global_dir_y = current_drag_global_pos.y() - self.last_drag_global_pos.y()

                        # Moving in the opposite direction from the last drag event
                        did_switch_dir = (global_dir_y < 0 < -move_dir) or (global_dir_y > 0 > -move_dir)

                    # noinspection PyUnresolvedReferences
                    target_cell = target_item.cell_item

                    # Not the same target, or the same target and moving in the opposite direction
                    if target_cell.index != self.last_target_idx or did_switch_dir:
                        # Swap indices
                        self.list_item.cell_item.index = target_idx
                        target_cell.index = drag_idx

                        # Re-sort post index swap
                        self.list_widget.sortItems()

                        # Broadcast change
                        self.list_widget.currentRowChanged.emit(self.list_item.cell_item.index)

                        # Cache values
                        self.last_target_idx = drag_idx
                        self.last_drag_global_pos = self.parentWidget().cursor().pos()
