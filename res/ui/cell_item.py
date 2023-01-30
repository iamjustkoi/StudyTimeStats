# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cell_item.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CellWidget(object):
    def setupUi(self, CellWidget):
        CellWidget.setObjectName("CellWidget")
        CellWidget.resize(421, 265)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CellWidget.sizePolicy().hasHeightForWidth())
        CellWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(CellWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 6)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addButton = HoverButton(CellWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy)
        self.addButton.setMinimumSize(QtCore.QSize(0, 64))
        self.addButton.setStyleSheet("#addButton {\n"
"    border: 1px solid rgba(134, 134, 134, 128);\n"
"    border-radius: 2px;\n"
"    background: transparent;\n"
"}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/add_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(icon)
        self.addButton.setIconSize(QtCore.QSize(20, 20))
        self.addButton.setObjectName("addButton")
        self.verticalLayout.addWidget(self.addButton)
        self.mainFrame = QtWidgets.QFrame(CellWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainFrame.sizePolicy().hasHeightForWidth())
        self.mainFrame.setSizePolicy(sizePolicy)
        self.mainFrame.setStyleSheet("#mainFrame {\n"
"    background: rgba(163, 163, 163, 5%);\n"
"    border-radius: 6px;\n"
"}")
        self.mainFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.mainFrame.setObjectName("mainFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.mainFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.mainFrame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.directionVerticalButton = QtWidgets.QPushButton(self.frame_2)
        self.directionVerticalButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.directionVerticalButton.sizePolicy().hasHeightForWidth())
        self.directionVerticalButton.setSizePolicy(sizePolicy)
        self.directionVerticalButton.setObjectName("directionVerticalButton")
        self.horizontalLayout_2.addWidget(self.directionVerticalButton)
        self.directionHorizontalButton = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.directionHorizontalButton.sizePolicy().hasHeightForWidth())
        self.directionHorizontalButton.setSizePolicy(sizePolicy)
        self.directionHorizontalButton.setObjectName("directionHorizontalButton")
        self.horizontalLayout_2.addWidget(self.directionHorizontalButton)
        self.gridLayout.addWidget(self.frame_2, 2, 1, 1, 1)
        self.frame = QtWidgets.QFrame(self.mainFrame)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rangeDropdown = QtWidgets.QComboBox(self.frame)
        self.rangeDropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.rangeDropdown.setObjectName("rangeDropdown")
        self.rangeDropdown.addItem("")
        self.rangeDropdown.addItem("")
        self.rangeDropdown.addItem("")
        self.rangeDropdown.addItem("")
        self.rangeDropdown.addItem("")
        self.rangeDropdown.addItem("")
        self.horizontalLayout.addWidget(self.rangeDropdown)
        self.calendarCheckbox = QtWidgets.QCheckBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendarCheckbox.sizePolicy().hasHeightForWidth())
        self.calendarCheckbox.setSizePolicy(sizePolicy)
        self.calendarCheckbox.setChecked(True)
        self.calendarCheckbox.setObjectName("calendarCheckbox")
        self.horizontalLayout.addWidget(self.calendarCheckbox)
        self.gridLayout.addWidget(self.frame, 3, 1, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.mainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.hourLabel = QtWidgets.QLabel(self.frame_3)
        self.hourLabel.setObjectName("hourLabel")
        self.horizontalLayout_3.addWidget(self.hourLabel)
        self.hourEdit = QtWidgets.QLineEdit(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hourEdit.sizePolicy().hasHeightForWidth())
        self.hourEdit.setSizePolicy(sizePolicy)
        self.hourEdit.setObjectName("hourEdit")
        self.horizontalLayout_3.addWidget(self.hourEdit)
        self.minuteLabel = QtWidgets.QLabel(self.frame_3)
        self.minuteLabel.setObjectName("minuteLabel")
        self.horizontalLayout_3.addWidget(self.minuteLabel)
        self.minEdit = QtWidgets.QLineEdit(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minEdit.sizePolicy().hasHeightForWidth())
        self.minEdit.setSizePolicy(sizePolicy)
        self.minEdit.setObjectName("minEdit")
        self.horizontalLayout_3.addWidget(self.minEdit)
        self.gridLayout.addWidget(self.frame_3, 5, 1, 1, 1)
        self.titleColorButton = QtWidgets.QToolButton(self.mainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleColorButton.sizePolicy().hasHeightForWidth())
        self.titleColorButton.setSizePolicy(sizePolicy)
        self.titleColorButton.setMaximumSize(QtCore.QSize(20, 20))
        self.titleColorButton.setStyleSheet("#titleColorButton {\n"
"    border-radius: 10px;\n"
"    background-color: #76bfb4;\n"
"    width: 20px;\n"
"}")
        self.titleColorButton.setObjectName("titleColorButton")
        self.gridLayout.addWidget(self.titleColorButton, 0, 2, 1, 1)
        self.outputColorButton = QtWidgets.QToolButton(self.mainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputColorButton.sizePolicy().hasHeightForWidth())
        self.outputColorButton.setSizePolicy(sizePolicy)
        self.outputColorButton.setMaximumSize(QtCore.QSize(20, 20))
        self.outputColorButton.setStyleSheet("#outputColorButton {\n"
"    border-radius: 10px;\n"
"    background-color: #FFF;\n"
"}")
        self.outputColorButton.setObjectName("outputColorButton")
        self.gridLayout.addWidget(self.outputColorButton, 1, 2, 1, 1)
        self.directionLabel = QtWidgets.QLabel(self.mainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.directionLabel.sizePolicy().hasHeightForWidth())
        self.directionLabel.setSizePolicy(sizePolicy)
        self.directionLabel.setObjectName("directionLabel")
        self.gridLayout.addWidget(self.directionLabel, 2, 0, 1, 1)
        self.codeButton = HoverButton(self.mainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.codeButton.sizePolicy().hasHeightForWidth())
        self.codeButton.setSizePolicy(sizePolicy)
        self.codeButton.setMinimumSize(QtCore.QSize(0, 0))
        self.codeButton.setMaximumSize(QtCore.QSize(20, 20))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../img/code_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.codeButton.setIcon(icon1)
        self.codeButton.setIconSize(QtCore.QSize(20, 20))
        self.codeButton.setObjectName("codeButton")
        self.gridLayout.addWidget(self.codeButton, 5, 4, 1, 1)
        self.removeButton = HoverButton(self.mainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeButton.sizePolicy().hasHeightForWidth())
        self.removeButton.setSizePolicy(sizePolicy)
        self.removeButton.setMinimumSize(QtCore.QSize(0, 0))
        self.removeButton.setMaximumSize(QtCore.QSize(20, 20))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../img/remove_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeButton.setIcon(icon2)
        self.removeButton.setIconSize(QtCore.QSize(20, 20))
        self.removeButton.setObjectName("removeButton")
        self.gridLayout.addWidget(self.removeButton, 0, 4, 1, 1)
        self.startDayDropdown = QtWidgets.QComboBox(self.mainFrame)
        self.startDayDropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.startDayDropdown.setObjectName("startDayDropdown")
        self.startDayDropdown.addItem("")
        self.startDayDropdown.addItem("")
        self.startDayDropdown.addItem("")
        self.startDayDropdown.addItem("")
        self.startDayDropdown.addItem("")
        self.startDayDropdown.addItem("")
        self.startDayDropdown.addItem("")
        self.gridLayout.addWidget(self.startDayDropdown, 4, 1, 1, 1)
        self.startDayLabel = QtWidgets.QLabel(self.mainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startDayLabel.sizePolicy().hasHeightForWidth())
        self.startDayLabel.setSizePolicy(sizePolicy)
        self.startDayLabel.setObjectName("startDayLabel")
        self.gridLayout.addWidget(self.startDayLabel, 4, 0, 1, 1)
        self.customRangeSpinbox = QtWidgets.QSpinBox(self.mainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customRangeSpinbox.sizePolicy().hasHeightForWidth())
        self.customRangeSpinbox.setSizePolicy(sizePolicy)
        self.customRangeSpinbox.setMaximum(5690)
        self.customRangeSpinbox.setProperty("value", 7)
        self.customRangeSpinbox.setObjectName("customRangeSpinbox")
        self.gridLayout.addWidget(self.customRangeSpinbox, 6, 1, 1, 1)
        self.titleLabel = QtWidgets.QLabel(self.mainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.outputLabel = QtWidgets.QLabel(self.mainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputLabel.sizePolicy().hasHeightForWidth())
        self.outputLabel.setSizePolicy(sizePolicy)
        self.outputLabel.setObjectName("outputLabel")
        self.gridLayout.addWidget(self.outputLabel, 1, 0, 1, 1)
        self.titleLineEdit = QtWidgets.QLineEdit(self.mainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLineEdit.sizePolicy().hasHeightForWidth())
        self.titleLineEdit.setSizePolicy(sizePolicy)
        self.titleLineEdit.setObjectName("titleLineEdit")
        self.gridLayout.addWidget(self.titleLineEdit, 0, 1, 1, 1)
        self.outputLineEdit = QtWidgets.QLineEdit(self.mainFrame)
        self.outputLineEdit.setObjectName("outputLineEdit")
        self.gridLayout.addWidget(self.outputLineEdit, 1, 1, 1, 1)
        self.rangeLabel = QtWidgets.QLabel(self.mainFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rangeLabel.sizePolicy().hasHeightForWidth())
        self.rangeLabel.setSizePolicy(sizePolicy)
        self.rangeLabel.setObjectName("rangeLabel")
        self.gridLayout.addWidget(self.rangeLabel, 3, 0, 1, 1)
        self.unitLabel = QtWidgets.QLabel(self.mainFrame)
        self.unitLabel.setObjectName("unitLabel")
        self.gridLayout.addWidget(self.unitLabel, 5, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(16, 0, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.verticalLayout.addWidget(self.mainFrame)

        self.retranslateUi(CellWidget)
        QtCore.QMetaObject.connectSlotsByName(CellWidget)

    def retranslateUi(self, CellWidget):
        _translate = QtCore.QCoreApplication.translate
        CellWidget.setWindowTitle(_translate("CellWidget", "Form"))
        self.directionVerticalButton.setText(_translate("CellWidget", "Vertical"))
        self.directionHorizontalButton.setText(_translate("CellWidget", "Horizontal"))
        self.rangeDropdown.setToolTip(_translate("CellWidget", "Time range to filter through for the ranged total stat."))
        self.rangeDropdown.setItemText(0, _translate("CellWidget", "Total"))
        self.rangeDropdown.setItemText(1, _translate("CellWidget", "Past Week"))
        self.rangeDropdown.setItemText(2, _translate("CellWidget", "Past 2 Weeks"))
        self.rangeDropdown.setItemText(3, _translate("CellWidget", "Past Month"))
        self.rangeDropdown.setItemText(4, _translate("CellWidget", "Past Year"))
        self.rangeDropdown.setItemText(5, _translate("CellWidget", "Custom"))
        self.calendarCheckbox.setToolTip(_translate("CellWidget", "Use the start of the selected range instead of using its timespan."))
        self.calendarCheckbox.setText(_translate("CellWidget", "Use Calendar Week"))
        self.hourLabel.setText(_translate("CellWidget", "Hour"))
        self.hourEdit.setText(_translate("CellWidget", "hrs"))
        self.minuteLabel.setText(_translate("CellWidget", "Minute"))
        self.minEdit.setText(_translate("CellWidget", "min"))
        self.directionLabel.setText(_translate("CellWidget", "Direction"))
        self.startDayDropdown.setToolTip(_translate("CellWidget", "The day a new week should start on."))
        self.startDayDropdown.setCurrentText(_translate("CellWidget", "Monday"))
        self.startDayDropdown.setItemText(0, _translate("CellWidget", "Monday"))
        self.startDayDropdown.setItemText(1, _translate("CellWidget", "Tuesday"))
        self.startDayDropdown.setItemText(2, _translate("CellWidget", "Wednesday"))
        self.startDayDropdown.setItemText(3, _translate("CellWidget", "Thursday"))
        self.startDayDropdown.setItemText(4, _translate("CellWidget", "Friday"))
        self.startDayDropdown.setItemText(5, _translate("CellWidget", "Saturday"))
        self.startDayDropdown.setItemText(6, _translate("CellWidget", "Sunday"))
        self.startDayLabel.setText(_translate("CellWidget", "Week-Start Day"))
        self.customRangeSpinbox.setToolTip(_translate("CellWidget", "Amount of days to filter the custom range."))
        self.customRangeSpinbox.setSuffix(_translate("CellWidget", " days"))
        self.titleLabel.setText(_translate("CellWidget", "Title"))
        self.outputLabel.setText(_translate("CellWidget", "Output"))
        self.rangeLabel.setText(_translate("CellWidget", "Selected Range"))
        self.unitLabel.setText(_translate("CellWidget", "Units"))
from .forms import HoverButton


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CellWidget = QtWidgets.QWidget()
    ui = Ui_CellWidget()
    ui.setupUi(CellWidget)
    CellWidget.show()
    sys.exit(app.exec_())
