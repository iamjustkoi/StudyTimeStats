# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets


class Ui_MacroDialog(object):
    def setupUi(self, MacroDialog):
        MacroDialog.setObjectName("MacroDialog")
        MacroDialog.resize(528, 362)
        self.verticalLayout = QtWidgets.QVBoxLayout(MacroDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.macroGroupBox = QtWidgets.QGroupBox(MacroDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.macroGroupBox.sizePolicy().hasHeightForWidth())
        self.macroGroupBox.setSizePolicy(sizePolicy)
        self.macroGroupBox.setObjectName("macroGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.macroGroupBox)
        self.verticalLayout_2.setContentsMargins(6, 0, 6, 6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.filterLineEdit = QtWidgets.QLineEdit(self.macroGroupBox)
        self.filterLineEdit.setClearButtonEnabled(True)
        self.filterLineEdit.setObjectName("filterLineEdit")
        self.verticalLayout_2.addWidget(self.filterLineEdit)
        self.listView = QtWidgets.QListView(self.macroGroupBox)
        self.listView.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.listView.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.listView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.listView.setTabKeyNavigation(True)
        self.listView.setProperty("showDropIndicator", False)
        self.listView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.listView.setObjectName("listView")
        self.verticalLayout_2.addWidget(self.listView)
        self.verticalLayout.addWidget(self.macroGroupBox)
        self.previewGroupBox = QtWidgets.QGroupBox(MacroDialog)
        self.previewGroupBox.setMinimumSize(QtCore.QSize(0, 42))
        self.previewGroupBox.setObjectName("previewGroupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.previewGroupBox)
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.previewLabel = QtWidgets.QLabel(self.previewGroupBox)
        self.previewLabel.setObjectName("previewLabel")
        self.verticalLayout_3.addWidget(self.previewLabel)
        self.verticalLayout.addWidget(self.previewGroupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(MacroDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok
            )
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MacroDialog)
        self.buttonBox.accepted.connect(MacroDialog.accept)  # type: ignore
        self.buttonBox.rejected.connect(MacroDialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MacroDialog)

    def retranslateUi(self, MacroDialog):
        _translate = QtCore.QCoreApplication.translate
        MacroDialog.setWindowTitle(_translate("MacroDialog", "Macros"))
        self.macroGroupBox.setTitle(_translate("MacroDialog", "Macros"))
        self.filterLineEdit.setPlaceholderText(_translate("MacroDialog", "Filter..."))
        self.previewGroupBox.setTitle(_translate("MacroDialog", "Preview"))
        self.previewLabel.setText(_translate("MacroDialog", "test"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MacroDialog = QtWidgets.QDialog()
    ui = Ui_MacroDialog()
    ui.setupUi(MacroDialog)
    MacroDialog.show()
    sys.exit(app.exec_())
