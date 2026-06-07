import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

# Maya version specific imports
maya_version = int(cmds.about(apiVersion=True))

if maya_version >= 20250000:
    from PySide6.QtWidgets import (
        QDialog, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QLineEdit, QPushButton, QMessageBox
    )
    from PySide6.QtCore import Qt
    import shiboken6 as shiboken
    import maya.OpenMayaUI as omui
    import maya.OpenMaya as om
else:
    from PySide2.QtWidgets import (
        QDialog, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QLineEdit, QPushButton, QMessageBox
    )
    from PySide2.QtCore import Qt
    import shiboken2 as shiboken



def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(int(main_window_ptr), QWidget)


class ObjectIdTool(QDialog):
    def __init__(self, parent=maya_main_window()):
        super(ObjectIdTool, self).__init__(parent)

        self.setWindowFlags(
            Qt.Window |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowCloseButtonHint
        )
        self.setModal(False)
        self.setWindowTitle("Add ObjectId Attribute")
        self.resize(320, 150)

        self.init_ui()
        self.show()

    def init_ui(self):
        layout = QVBoxLayout(self)

        input_layout = QHBoxLayout()
        label = QLabel("Start ObjectId:")
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("ex: 10, 25, 32...")

        input_layout.addWidget(label)
        input_layout.addWidget(self.line_edit)
        layout.addLayout(input_layout)

        self.add_btn = QPushButton("Add ObjectId to Shapes")
        self.add_btn.clicked.connect(self.add_object_id)
        layout.addWidget(self.add_btn)

    def add_object_id(self):
        val_text = self.line_edit.text().strip()
        if not val_text.isdigit():
            QMessageBox.warning(self, "Error", "Please enter a valid integer.")
            return

        start_id = float(val_text)
        current_id = start_id

        selected_objs = cmds.ls(selection=True, long=True)
        if not selected_objs:
            QMessageBox.warning(self, "Error", "No objects selected!")
            return

        # Collect leaf transforms (no child transforms)
        transforms_to_process = []
        for obj in selected_objs:
            if not cmds.objectType(obj, isType="transform"):
                continue

            children = cmds.listRelatives(
                obj,
                allDescendents=True,
                type="transform",
                fullPath=True
            ) or []

            all_transforms = [obj] + children

            for t in all_transforms:
                child_transforms = cmds.listRelatives(
                    t,
                    children=True,
                    type="transform"
                )
                if not child_transforms:
                    transforms_to_process.append(t)

        # Remove duplicates, preserve order
        transforms_to_process = list(dict.fromkeys(transforms_to_process))

        if not transforms_to_process:
            om.MGlobal.displayWarning("No valid objects found.")
            return

        overwrite_all = None

        for transform in transforms_to_process:
            shapes = cmds.listRelatives(
                transform,
                shapes=True,
                noIntermediate=True,
                fullPath=True
            ) or []

            if not shapes:
                continue

            for shape in shapes:
                if cmds.attributeQuery("ObjectId", node=shape, exists=True):
                    if overwrite_all is None:
                        msg = QMessageBox()
                        msg.setText("Some shapes already have ObjectId.")
                        msg.setInformativeText(
                            "Do you want to overwrite existing ObjectId attributes?"
                        )
                        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        msg.setDefaultButton(QMessageBox.No)
                        ret = msg.exec_()
                        overwrite_all = (ret == QMessageBox.Yes)

                    if not overwrite_all:
                        continue

                if not cmds.attributeQuery("ObjectId", node=shape, exists=True):
                    cmds.addAttr(
                        shape,
                        longName="ObjectId",
                        attributeType="float"
                    )
                    cmds.setAttr(
                        f"{shape}.ObjectId",
                        e=True,
                        channelBox=True
                    )

                cmds.setAttr(f"{shape}.ObjectId", current_id)

            current_id += 1

        om.MGlobal.displayInfo(
            f"Success: ObjectId applied to shapes "
            f"from {start_id} to {current_id - 1}"
        )


# Show tool
ObjectIdTool()