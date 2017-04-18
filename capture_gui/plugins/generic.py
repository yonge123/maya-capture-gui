import maya.cmds as mc
from capture_gui.vendor.Qt import QtCore, QtWidgets

import capture_gui.plugin
import capture_gui.lib


class GenericPlugin(capture_gui.plugin.Plugin):
    """Widget for generic options"""
    id = "Generic"
    label = "Generic"
    section = "config"
    order = 100

    def __init__(self, parent=None):
        super(GenericPlugin, self).__init__(parent=parent)

        layout  = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        isolate_view = QtWidgets.QCheckBox("Use isolate view from active panel")
        off_screen = QtWidgets.QCheckBox("Render offscreen")

        layout.addWidget(isolate_view)
        layout.addWidget(off_screen)

        isolate_view.stateChanged.connect(self.options_changed)
        off_screen.stateChanged.connect(self.options_changed)

        self.widgets = {
            "off_screen": off_screen,
            "isolate_view": isolate_view
        }

        self.apply_inputs(self.get_defaults())

    def get_defaults(self):
        return {
            "off_screen": True,
            "isolate_view": False
        }

    def get_inputs(self):
        """
        Return the widget options
        :return: dictionary with all the settings of the widgets 
        """

        inputs = dict()
        for key, widget in self.widgets.items():
            state = widget.isChecked()
            inputs[key] = state

        return inputs

    def apply_inputs(self, inputs):
        """
        Apply the settings which can be adjust by the user or presets
        :param inputs: a collection of settings
        :type inputs: dict

        :return: None
        """

        for key, widget in self.widgets.items():
            state = inputs.get(key, None)
            if state is not None:
                widget.setChecked(state)

        return inputs

    def get_outputs(self):
        """
        Retrieve all settings of each available sub widgets
        :return: 
        """

        inputs = self.get_inputs()
        outputs = dict()
        outputs['off_screen'] = inputs['off_screen']

        import capture_gui.lib

        # Get isolate view members of the active panel
        if inputs['isolate_view']:
            panel = capture_gui.lib.get_active_editor()
            filter_set = mc.modelEditor(panel, query=True, viewObjects=True)
            isolate = mc.sets(filter_set, q=1) if filter_set else None
            outputs['isolate'] = isolate

        return outputs


