#!/usr/bin/env python
"""
###########################
FMEA Package Work Book View
###########################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.gui.gtk.WorkBook.py is part of The RTK Project
#
# All rights reserved.

import sys

# Modules required for the GUI.
import pango
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    import utilities as _util
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.utilities as _util
    import rtk.widgets as _widg
from Assistants import AddControlAction

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def get_mode_id(mode):
    """
    Helper function to return the mode id of the passed mode object.  Used to
    sort the list of failure mode objects before loading into the
    gtk.TreeView().

    :param rtk.analyses.fmea.Mode.model mode: the failure mode object to return
                                              the mode id for.
    :return mode_id: the mode id of the passed mode object.
    :rtype: int
    """

    return mode.mode_id

class WorkView(gtk.HBox):                   # pylint: disable=R0902
    """
    The Work Book view displays all the attributes for the selected
    Failure Mode and Effects Analysis.  The attributes of a Failure Mode and
    Effects Analysis Work Book view are:

    :ivar _lst_control_type: default value: [_(u"Prevention"), _(u"Detection")]
    :ivar _lst_handler_id: default value: []

    :ivar _hardware_id: default value: None
    :ivar _item_hr: default value: 0.0

    :ivar dtcFMECA: the FMECA data controller.
    :ivar btnAddSibling: gtk.Button() used to add a "sibling" element.
    :ivar btnAddChild: gtk.Button() used to add a "child" element.
    :ivar btnRemove: gtk.Button() used to remove the selected element.
    :ivar btnCalculate: gtk.Button() used to calculate the criticality.
    :ivar btnSaveFMECA: gkt.Button() used to save the selected FMEA.
    :ivar cmbFMECAMethod: gtk.Combo() used to select the criticality method.
    :ivar tvwFMECA: gtk.TreeView() used to display the FMEA/FMECA.
    """

    def __init__(self, controller):
        """
        Initializes the Work Book view for the Failure Mode and Effects
        Analysis module.

        :param rtk.analyses.fmea.FMEA controller: the FMEA data controller.
        """

        gtk.HBox.__init__(self)

        # Initialize private dictionary attributes.
        self._dic_phases = {}

        # Initialize private list attributes.
        self._lst_control_type = [_(u"Prevention"), _(u"Detection")]
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._hardware_id = None
        self._item_hr = 0.0

        # Initialize public scalar attributes.
        self.dtcFMECA = controller

        self.btnAddSibling = _widg.make_button(width=35,
                                               image='insert_sibling')
        self.btnAddChild = _widg.make_button(width=35, image='insert_child')
        self.btnRemove = _widg.make_button(width=35, image='remove')
        self.btnCalculate = _widg.make_button(width=35, image='calculate')
        self.btnSaveFMECA = _widg.make_button(width=35, image='save')

        self.cmbFMECAMethod = _widg.make_combo()

        self.tvwFMECA = gtk.TreeView()

    def create_page(self):                  # pylint: disable=R0912,R0914,R0915
        """
        Create the Failure Mode and Effects Analysis gtk.Notebook() page for
        displaying the FMEA/FMECA for the selected Hardware.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the FMEA/FMECA gtk.TreeView().                         #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self.tvwFMECA.set_tooltip_text(_(u"Displays the failure mode and "
                                         u"effects analysis for the currently "
                                         u"selected hardware item."))
        _model = gtk.TreeStore(gtk.gdk.Pixbuf, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_INT,
                               gobject.TYPE_INT)
        self.tvwFMECA.set_model(_model)

        _headings = [_(u"Mode ID"), _(u"Description"), _(u"Control\nType"),
                     _(u"Action\nCategory"), _(u"Mission"),
                     _(u"Mission\nPhase"), _(u"Local\nEffect"),
                     _(u"Next\nEffect"), _(u"End\nEffect"),
                     _(u"Detection\nMethod"), _(u"Other\nIndications"),
                     _(u"Isolation\nMethod"), _(u"Design\nProvisions"),
                     _(u"Operator\nActions"), _(u"Severity\nClassification"),
                     _(u"Hazard Rate\nData Source"),
                     _(u"Failure\nProbability"), _(u"Effect\nProbability"),
                     _(u"Mode Ratio"), _(u"Mode\nHazard\nRate"),
                     _(u"Mode\nOperating\nTime"), _(u"Mode\nCriticality"),
                     _(u"Severity\n(RPN)"), _(u"Occurrence\n(RPN)"),
                     _(u"Detection\n(RPN)"), _(u"RPN"),
                     _(u"Severity\nNew (RPN)"), _(u"Occurrence\nNew (RPN)"),
                     _(u"Detection\nNew (RPN)"), _(u"RPN New"),
                     _(u"Include\nin PoF"), _(u"Action\nOwner"),
                     _(u"Action\nDue Date"), _(u"Action\nStatus"),
                     _(u"Action\nTaken"), _(u"Action\nApproved"),
                     _(u"Approval\nDate"), _(u"Action\nClosed"),
                     _(u"Closure\nDate"), _(u"Critical\nItem"), _(u"SPV"),
                     _(u"Remarks"), "", ""]

        for i in range(44):
            _column = gtk.TreeViewColumn()
            if i == 0:
                _cell = gtk.CellRendererPixbuf()
                _cell.set_property('visible', 1)
                _cell.set_property('xalign', 0.5)
                _column.pack_start(_cell, False)
                _column.set_attributes(_cell, pixbuf=0)

                _cell = gtk.CellRendererText()
                _cell.set_property('background', 'light gray')
                _cell.set_property('editable', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('visible', 1)
                _cell.set_property('yalign', 0.1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=1)

            elif i == 1:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('visible', 1)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, 2)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=2)

            elif i == 2:
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                _cellmodel.append([""])
                _cell = gtk.CellRendererCombo()
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('has-entry', False)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, 3)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=3, background=52,
                                       editable=43)
                for j in range(len(_conf.RTK_CONTROL_TYPES)):
                    _cellmodel.append([_conf.RTK_CONTROL_TYPES[j]])

            elif i == 3:
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                _cellmodel.append([""])
                _cell = gtk.CellRendererCombo()
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, 4)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=4, background=53,
                                       editable=44)
                for j in range(len(_conf.RTK_ACTION_CATEGORY)):
                    _cellmodel.append([_conf.RTK_ACTION_CATEGORY[j]])

            elif i in [4, 5, 14]:
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                _cellmodel.append([""])
                _cell = gtk.CellRendererCombo()
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, i + 1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1, background=54,
                                       editable=45)
                if i == 4:                  # Mission
                    _results = []
                elif i == 5:                # Mission phase
                    _results = []
                elif i == 14:               # Severity classification
                    _results = [_s[1] for _s in _conf.RTK_SEVERITY]

                for j in range(len(_results)):
                    _cellmodel.append([_results[j]])

            elif i in [6, 7, 8, 9, 10, 11, 12, 13, 41]:
                _cell = gtk.CellRendererText()
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('visible', 1)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, i + 1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1, background=54,
                                       editable=45)

            elif i in [15, 19, 20, 21]:
                _cell = gtk.CellRendererText()
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('visible', 1)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, i + 1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1, background=55,
                                       editable=46)

            elif i == 16:                   # Failure probability.
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                _cellmodel.append([""])
                _cell = gtk.CellRendererCombo()
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, i + 1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1, background=55,
                                       editable=46)
                for j in range(len(_conf.RTK_FAILURE_PROBABILITY)):
                    _cellmodel.append([_conf.RTK_FAILURE_PROBABILITY[j][1]])

            elif i in [17, 18]:             # Effect probability and mode ratio
                _cell = gtk.CellRendererSpin()
                _adjustment = gtk.Adjustment(upper=1.0, step_incr=0.01)
                _cell.set_property('adjustment', _adjustment)
                _cell.set_property('digits', 2)
                _cell.connect('edited', self._on_cell_edit, i + 1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1, background=55,
                                       editable=46)
            elif i in [22, 26]:             # RPN severity and new severity.
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                _cellmodel.append([""])
                _cell = gtk.CellRendererCombo()
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, i + 1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1, background=55,
                                       editable=47)
                for j in range(len(_conf.RTK_RPN_SEVERITY)):
                    _cellmodel.append([_conf.RTK_RPN_SEVERITY[j][1]])

            elif i in [25, 29]:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', False)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, i + 1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1, background=56)

            elif i in [23, 24, 27, 28]:
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                _cellmodel.append([""])
                _cell = gtk.CellRendererCombo()
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, i + 1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1, background=56,
                                       editable=48)
                if i == 23 or i == 27:
                    _results = _conf.RTK_RPN_OCCURRENCE
                else:
                    _results = _conf.RTK_RPN_DETECTION
                for j in range(len(_results)):
                    _cellmodel.append([_results[j][1]])

            elif i == 30:
                _cell = gtk.CellRendererToggle()
                _cell.connect('toggled', self._on_cell_edit, None, i + 1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, active=i + 1, activatable=49)

            elif i in [31, 33]:             # Action owner and action status.
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                _cellmodel.append([""])
                _cell = gtk.CellRendererCombo()
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, i + 1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1, background=58,
                                       editable=50)
                if i == 31:
                    _results = [_s[0] + ', ' + _s[1] for _s in _conf.RTK_USERS]
                elif i == 33:
                    _results = [_s[0] for _s in _conf.RTK_STATUS]
                for j in range(len(_results)):
                    _cellmodel.append([_results[j]])

            elif i in [32, 34, 36, 38]:
                _cell = gtk.CellRendererText()
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('visible', 1)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, i + 1)
                _cell.connect('editing-started', self._on_start_edit, i)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1, background=58,
                                       editable=50)

            elif i in [35, 37]:
                _cell = gtk.CellRendererToggle()
                _cell.set_property('activatable', 1)
                _cell.connect('toggled', self._on_cell_edit, None, i + 1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, active=i + 1, activatable=50)
                _column.add_attribute(_cell, 'cell-background', 58)

            elif i in [39, 40]:
                _cell = gtk.CellRendererToggle()
                _cell.set_property('activatable', 1)
                _cell.connect('toggled', self._on_cell_edit, None, i + 1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, active=i + 1, activatable=45)
                _column.add_attribute(_cell, 'cell-background', 54)

            elif i == 42:
                for j in range(17):
                    _cell = gtk.CellRendererText()
                    _cell.set_property('editable', 0)
                    _column.pack_start(_cell, True)
                    _column.set_attributes(_cell, text=j + 43)
                    _column.set_visible(False)

            elif i == 43:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=60)
                _column.set_visible(False)

            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" + _headings[i] +
                              "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column.set_widget(_label)
            _column.set_alignment(0.5)

            _column.set_expand(True)
            _column.set_resizable(True)
            _column.set_min_width(1)

            self.tvwFMECA.append_column(_column)

        self.tvwFMECA.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        self.pack_start(_bbox, False, True)

        _vbox = gtk.VBox()

        self.pack_end(_vbox, True, True)

        _fixed = gtk.Fixed()
        _vbox.pack_start(_fixed, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwFMECA)

        _frame = _widg.make_frame(label=_(u"Failure Mode and Effects "
                                          u"Analysis"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vbox.pack_end(_frame, True, True)

        _bbox.pack_start(self.btnAddSibling, False, False)
        _bbox.pack_start(self.btnAddChild, False, False)
        _bbox.pack_start(self.btnRemove, False, False)
        _bbox.pack_start(self.btnCalculate, False, False)
        _bbox.pack_start(self.btnSaveFMECA, False, False)

        self.btnAddSibling.set_tooltip_text(_(u"Add a failure mode to the "
                                              u"selected hardware item."))
        self.btnAddChild.set_tooltip_text(_(u"Add a failure mechanism to the "
                                            u"selected hardware item."))
        self.btnRemove.set_tooltip_text(_(u"Remove the selected failure "
                                          u"mode from the selected "
                                          u"hardware item."))
        self.btnCalculate.set_tooltip_text(_(u"Calculate the criticality "
                                             u"analysis for the selected "
                                             u"FMECA."))
        self.btnSaveFMECA.set_tooltip_text(_(u"Saves the FMECA to the open "
                                             u"RTK Project database."))

        # Connect to callback functions.
        self._lst_handler_id.append(
            self.btnAddSibling.connect('clicked',
                                       self._on_button_clicked, 0))
        self._lst_handler_id.append(
            self.btnAddChild.connect('clicked',
                                     self._on_button_clicked, 1))
        self._lst_handler_id.append(
            self.btnRemove.connect('clicked',
                                   self._on_button_clicked, 2))
        self._lst_handler_id.append(
            self.btnCalculate.connect('clicked',
                                      self._on_button_clicked, 3))
        self._lst_handler_id.append(
            self.btnSaveFMECA.connect('clicked',
                                      self._on_button_clicked, 4))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display the FMEA/FMECA.             #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.Combo()
        _results = [[_(u"Criticality Analysis"), 0],
                    [_(u"Risk Priority Number (RPN)"), 1]]
        _widg.load_combo(self.cmbFMECAMethod, _results)

        _labels = [_(u"Risk Evaluation Method:")]

        # Widgets to display FMEA/FMECA results.
        self.cmbFMECAMethod.set_tooltip_text(_(u"Selects the risk ranking "
                                               u"method for the selected "
                                               u"hardware item."))

        _x_pos = 5
        _label = _widg.make_label(_labels[0], width=-1)
        _fixed.put(_label, _x_pos, 5)
        _x_pos = _x_pos + _label.size_request()[0] + 35
        _fixed.put(self.cmbFMECAMethod, _x_pos, 5)

        self._lst_handler_id.append(
            self.cmbFMECAMethod.connect('changed', self._on_combo_changed, 5))

        self._lst_handler_id.append(
            self.tvwFMECA.connect('cursor_changed', self._on_row_changed))

        return False

    def load_page(self, hardware_id, item_hr, path=None):   # pylint: disable=R0914
        """
        Function to load the widgets on the FMEA/FMECA page.

        :param `rtk.hardware.Hardware.Hardware` controller: the Hardware data
                                                            controller instance
                                                            being used by RTK.
        :param int hardware_id: the Hardware ID to load the FMEA/FMECA for.
        :param float item_hr: the hazard rate of the hardware item associated
                              with the FMEA/FMECA being loaded.
        :keyword str path: the path of the parent hardware item in the
                           FMEA/FMECA gtk.TreeView().
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """

        self._hardware_id = hardware_id
        self._item_hr = item_hr

        _column = self.tvwFMECA.get_column(4)
        _model = _column.get_cell_renderers()[0].get_property('model')
        _model.clear()
        for __, _mission in self.dtcFMECA.dicMissions.iteritems():
            _model.append([_mission[3]])

        _model = self.tvwFMECA.get_model()
        _model.clear()

        # Find all the FMEA/FMECA for the selected Hardware Item.
        _modes = self.dtcFMECA.dicDFMEA[hardware_id].dicModes.values()
        _modes = sorted(_modes, key=get_mode_id)
        _criticality = 1
        _severity = ['', '']
        _occurrence = ['', '']
        _detection = ['', '']
        _rpn = ['', '']
        _piter = [None, None, None]
        for _mode in _modes:
            _icon = _conf.ICON_DIR + '32x32/mode.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            _attributes = _mode.get_attributes()
            _severity[0] = _conf.RTK_RPN_SEVERITY[_attributes[22] - 1][1]
            _severity[1] = _conf.RTK_RPN_SEVERITY[_attributes[23] - 1][1]
            for _key, _value in self.dtcFMECA.dicMissions.iteritems():
                if _value[3] == _attributes[4]:
                    self._load_mission_phases(self.dtcFMECA.dicPhases[_key])
            _data = (_icon, _attributes[2], _attributes[3], '', '',
                     _util.none_to_string(_attributes[4]),
                     _util.none_to_string(_attributes[5]),
                     _util.none_to_string(_attributes[6]),
                     _util.none_to_string(_attributes[7]),
                     _util.none_to_string(_attributes[8]),
                     _util.none_to_string(_attributes[9]),
                     _util.none_to_string(_attributes[10]),
                     _util.none_to_string(_attributes[11]),
                     _util.none_to_string(_attributes[12]),
                     _util.none_to_string(_attributes[13]),
                     _util.none_to_string(_attributes[14]),
                     _util.none_to_string(_attributes[15]),
                     _util.none_to_string(_attributes[16]), _attributes[17],
                     str(_attributes[18]), str(_attributes[19]),
                     str(_attributes[20]), str(_attributes[21]), _severity[0],
                     '', '', '', _severity[1], '', '', '', 0, '', '', '', '',
                     0, '', 0, '', _attributes[24], _attributes[25],
                     _attributes[26], 0, 0, 1, 1, 1, 0, 0, 0, 0, 'light gray',
                     'light gray', 'white', 'white', 'light gray',
                     'light gray', 'light gray', 0, 1)
            _piter[0] = _model.append(None, _data)

            for _mechanism in _mode.dicMechanisms.values():
                _icon = _conf.ICON_DIR + '32x32/mechanism.png'
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
                _attributes = _mechanism.get_attributes()
                _occurrence[0] = _conf.RTK_RPN_OCCURRENCE[_attributes[3]][1]
                _occurrence[1] = _conf.RTK_RPN_OCCURRENCE[_attributes[6]][1]
                _detection[0] = _conf.RTK_RPN_DETECTION[_attributes[4]][1]
                _detection[1] = _conf.RTK_RPN_DETECTION[_attributes[7]][1]
                _data = (_icon, _attributes[1], _attributes[2], '', '', '', '',
                         '', '', '', '', '', '', '', '', '', '', '', '', '',
                         '', '', '', '', _occurrence[0], _detection[0],
                         str(_attributes[5]), '', _occurrence[1],
                         _detection[1], str(_attributes[8]), _attributes[9],
                         '', '', '', '', 0, '', 0, '', 0, 0, '', 0, 0, 0, 0, 0,
                         1, 1, 0, 0, 'light gray', 'light gray', 'light gray',
                         'light gray', 'white', 'white', 'light gray', 0, 2)
                _piter[1] = _model.append(_piter[0], _data)

                for _cause in _mechanism.dicCauses.values():
                    _icon = _conf.ICON_DIR + '32x32/cause.png'
                    _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
                    _attributes = _cause.get_attributes()
                    if _conf.RTK_RPN_FORMAT == 0:
                        _occurrence = ['', '']
                        _detection = ['', '']
                        _rpn = ['', '']
                    else:
                        _occurrence[0] = _conf.RTK_RPN_OCCURRENCE[_attributes[4]][1]
                        _occurrence[1] = _conf.RTK_RPN_OCCURRENCE[_attributes[7]][1]
                        _detection[0] = _conf.RTK_RPN_DETECTION[_attributes[5]][1]
                        _detection[1] = _conf.RTK_RPN_DETECTION[_attributes[8]][1]
                        _rpn[0] = _attributes[6]
                        _rpn[1] = _attributes[9]
                    _data = (_icon, _attributes[2], _attributes[3], '', '', '',
                             '', '', '', '', '', '', '', '', '', '', '', '',
                             '', '', '', '', '', '', _occurrence[0],
                             _detection[0], _rpn[0], '', _occurrence[1],
                             _detection[1], _rpn[1], 0, '', '', '', '', 0,
                             '', 0, '', 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             'light gray', 'light gray', 'light gray',
                             'light gray', 'light gray', 'white', 'light gray',
                             1, 3)
                    _piter[2] = _model.append(_piter[1], _data)

                    for _control in _cause.dicControls.values():
                        _icon = _conf.ICON_DIR + '32x32/control.png'
                        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22,
                                                                     22)
                        _attributes = _control.get_attributes()
                        _type = self._lst_control_type[_attributes[5]]
                        _data = (_icon, _attributes[3], _attributes[4],
                                 _type, '', '', '', '', '', '', '', '', '', '',
                                 '', '', '', '', '', '', '', '', '', '', '',
                                 '', '', '', '', '', '', 0, '', '', '', '', 0,
                                 '', 0, '', 0, 0, '', 1, 0, 0, 0, 0, 0, 0, 0,
                                 0, 'white', 'light gray', 'light gray',
                                 'light gray', 'light gray', 'light gray',
                                 'light gray', 0, 4)
                        _model.append(_piter[2], _data)
                    for _action in _cause.dicActions.values():
                        _icon = _conf.ICON_DIR + '32x32/action.png'
                        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon,
                                                                     22, 22)
                        _attributes = _action.get_attributes()
                        _owner = _conf.RTK_USERS[_attributes[6]]
                        _owner = _owner[0] + ", " + _owner[1]
                        _category = _conf.RTK_ACTION_CATEGORY[_attributes[5]]
                        _due_date = _util.ordinal_to_date(_attributes[7])
                        _status = _conf.RTK_STATUS[_attributes[8]][0]
                        _approve_date = _util.ordinal_to_date(_attributes[11])
                        _close_date = _util.ordinal_to_date(_attributes[13])
                        _data = (_icon, _attributes[3], _attributes[4], '',
                                 _category, '', '', '', '', '', '', '',
                                 '', '', '', '', '', '', '', '', '', '', '',
                                 '', '', '', '', '', '', '', '', 0,
                                 _owner, _due_date, _status,
                                 _attributes[9], _attributes[10],
                                 _approve_date, _attributes[12], _close_date,
                                 0, 0, '', 0, 1, 0, 0, 0, 0, 0, 1, 0,
                                 'light gray', 'white', 'light gray',
                                 'light gray', 'light gray', 'light gray',
                                 'white', 0, 5)
                        _model.append(_piter[2], _data)

        if path is None:
            _root = _model.get_iter_root()
            try:
                path = _model.get_path(_root)
            except TypeError:
                return False
        _column = self.tvwFMECA.get_column(0)
        self.tvwFMECA.set_cursor(path, None, False)
        self.tvwFMECA.row_activated(path, _column)
        self.tvwFMECA.expand_all()

        self.cmbFMECAMethod.set_active(_conf.RTK_FMECA_METHOD)
        self._show_risk_analysis()

        return False

    def _show_risk_analysis(self):
        """
        Method to show or hide the criticality analysis columns and the RPN
        columns in the FMECA gtk.TreeView() depending on the risk analysis
        method selected.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if _conf.RTK_FMECA_METHOD == 1:     # Task 102
            _criticality = True
            _rpn = False
        elif _conf.RTK_FMECA_METHOD == 2:   # RPN
            _criticality = False
            _rpn = True

        _columns = self.tvwFMECA.get_columns()

        for i in [15, 16, 17, 18, 19, 20, 21]:
            _columns[i].set_visible(_criticality)
        for i in [22, 23, 24, 25, 26, 27, 28, 29]:
            _columns[i].set_visible(_rpn)

        return False

    def _on_button_clicked(self, __button, index):  # pylint: disable=R0912,R0914
        """
        Responds to gtk.Button() clicked signals and calls the correct function
        or method, passing any parameters as needed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _fmeca = self.dtcFMECA.dicDFMEA[self._hardware_id]

        (_model, _row) = self.tvwFMECA.get_selection().get_selected()
        _id = _model.get_value(_row, 1)
        _level = _model.get_value(_row, 60)

        if index == 0:                      # Add sibling
            if _level == 1:                 # Failure Mode
                (_results,
                 _error_code,
                 _last_id) = self.dtcFMECA.add_mode(self._hardware_id, None)

            elif _level == 2:               # Failure Mechanism
                _piter = _model.iter_parent(_row)
                _mode_id = _model.get_value(_piter, 1)

                (_results,
                 _error_code,
                 _last_id) = self.dtcFMECA.add_mechanism(self._hardware_id,
                                                         _mode_id)

            elif _level == 3:               # Failure Cause
                _piter = _model.iter_parent(_row)
                _mechanism_id = _model.get_value(_piter, 1)
                _piter = _model.iter_parent(_piter)
                _mode_id = _model.get_value(_piter, 1)

                (_results,
                 _error_code,
                 _last_id) = self.dtcFMECA.add_cause(self._hardware_id,
                                                     _mode_id, _mechanism_id)

            elif _level == 4:               # Control
                _piter = _model.iter_parent(_row)
                _cause_id = _model.get_value(_piter, 1)
                _piter = _model.iter_parent(_piter)
                _mechanism_id = _model.get_value(_piter, 1)
                _piter = _model.iter_parent(_piter)
                _mode_id = _model.get_value(_piter, 1)

                (_results,
                 _error_code,
                 _last_id) = self.dtcFMECA.add_control(self._hardware_id,
                                                       _mode_id, _mechanism_id,
                                                       _cause_id)

            elif _level == 5:               # Action
                _piter = _model.iter_parent(_row)
                _cause_id = _model.get_value(_piter, 1)
                _piter = _model.iter_parent(_piter)
                _mechanism_id = _model.get_value(_piter, 1)
                _piter = _model.iter_parent(_piter)
                _mode_id = _model.get_value(_piter, 1)

                (_results,
                 _error_code,
                 _last_id) = self.dtcFMECA.add_action(self._hardware_id,
                                                      _mode_id, _mechanism_id,
                                                      _cause_id)

            if _results:
                try:
                    _path = _model.get_path(_model.iter_next(_row))
                except TypeError:
                    _path = None
                self.load_page(self._hardware_id, _path)

        elif index == 1:                    # Add child
            if _level == 1:                 # Failure Mode
                (_results,
                 _error_code,
                 _last_id) = self.dtcFMECA.add_mechanism(self._hardware_id,
                                                         _id)
            elif _level == 2:               # Failure Mechanism
                _piter = _model.iter_parent(_row)
                _mode_id = _model.get_value(_piter, 1)

                (_results,
                 _error_code,
                 _last_id) = self.dtcFMECA.add_cause(self._hardware_id,
                                                     _mode_id, _id)

            elif _level == 3:               # Failure Cause
                _piter = _model.iter_parent(_row)
                _mechanism_id = _model.get_value(_piter, 1)
                _piter = _model.iter_parent(_piter)
                _mode_id = _model.get_value(_piter, 1)

                _dialog = AddControlAction()
                if _dialog.run() == gtk.RESPONSE_ACCEPT:
                    if _dialog.rdoControl.get_active():
                        (_results,
                         _error_code,
                         _last_id) = self.dtcFMECA.add_control(self._hardware_id,
                                                               _mode_id,
                                                               _mechanism_id,
                                                               _id)
                    elif _dialog.rdoAction.get_active():
                        (_results,
                         _error_code,
                         _last_id) = self.dtcFMECA.add_action(self._hardware_id,
                                                              _mode_id,
                                                              _mechanism_id,
                                                              _id)
                else:
                    _results = False

                _dialog.destroy()

            if _results:
                try:
                    _path = _model.get_path(_model.iter_next(_row))
                except TypeError:
                    _path = None
                self.load_page(self._hardware_id, _path)

        elif index == 2:                    # Delete selected
            if _level == 1:                 # Failure Mode
                (_results,
                 _error_code) = self.dtcFMECA.delete_mode(_id,
                                                          self._hardware_id)

            elif _level == 2:               # Failure Mechanism
                _prow = _model.iter_parent(_row)
                _mode_id = _model.get_value(_prow, 1)
                (_results, _error_code) = self.dtcFMECA.delete_mechanism(
                    self._hardware_id, _mode_id, _id)

            elif _level == 3:               # Failure Cause
                _prow = _model.iter_parent(_row)
                _mechanism_id = _model.get_value(_prow, 1)
                _prow = _model.iter_parent(_prow)
                _mode_id = _model.get_value(_prow, 1)
                (_results,
                 _error_code) = self.dtcFMECA.delete_cause(self._hardware_id,
                                                           _mode_id,
                                                           _mechanism_id, _id)

            elif _level == 4:               # Control
                _prow = _model.iter_parent(_row)
                _cause_id = _model.get_value(_prow, 1)
                _prow = _model.iter_parent(_prow)
                _mechanism_id = _model.get_value(_prow, 1)
                _prow = _model.iter_parent(_prow)
                _mode_id = _model.get_value(_prow, 1)
                (_results,
                 _error_code) = self.dtcFMECA.delete_control(self._hardware_id,
                                                             _mode_id,
                                                             _mechanism_id,
                                                             _cause_id, _id)

            elif _level == 5:               # Action
                _prow = _model.iter_parent(_row)
                _cause_id = _model.get_value(_prow, 1)
                _prow = _model.iter_parent(_prow)
                _mechanism_id = _model.get_value(_prow, 1)
                _prow = _model.iter_parent(_prow)
                _mode_id = _model.get_value(_prow, 1)
                (_results,
                 _error_code) = self.dtcFMECA.delete_action(self._hardware_id,
                                                            _mode_id,
                                                            _mechanism_id,
                                                            _cause_id, _id)
            if _results:
                try:
                    _path = _model.get_path(_model.iter_next(_row))
                except TypeError:
                    _path = None
                self.load_page(self._hardware_id, _path)

        elif index == 3:                    # Calculate criticality
            _row = _model.get_iter_root()
            while _row is not None:
                _id = _model.get_value(_row, 1)
                if _model.get_value(_row, 60) == 1:
                    _mode = _fmeca.dicModes[_id]

                    if _conf.RTK_FMECA_METHOD == 2:     # RPN
                        _severity = int([x[0] for x in _conf.RTK_RPN_SEVERITY
                                         if x[1] == _model.get_value(_row, 23)][0])
                        _severity_new = int([x[0] for x in _conf.RTK_RPN_SEVERITY
                                             if x[1] == _model.get_value(_row, 27)][0])
                        _child_row = _model.iter_children(_row)
                        while _child_row is not None:
                            if _model.get_value(_child_row, 60) == 2:
                                _mechanism_id = _model.get_value(_child_row, 1)
                                _mechanism = _mode.dicMechanisms[_mechanism_id]
                                _occurrence = int([x[0] for x in _conf.RTK_RPN_OCCURRENCE
                                                   if x[1] == _model.get_value(_child_row, 24)][0])
                                _detection = int([x[0] for x in _conf.RTK_RPN_DETECTION
                                                  if x[1] == _model.get_value(_child_row, 25)][0])
                                _occurrence_new = int([x[0] for x in _conf.RTK_RPN_OCCURRENCE
                                                       if x[1] == _model.get_value(_child_row, 28)][0])
                                _detection_new = int([x[0] for x in _conf.RTK_RPN_DETECTION
                                                      if x[1] == _model.get_value(_child_row, 29)][0])
                                _rpn = _severity * _occurrence * _detection
                                _rpn_new = _severity_new * _occurrence_new * _detection_new
                                _model.set_value(_child_row, 26, _rpn)
                                _model.set_value(_child_row, 30, _rpn_new)
                                _mechanism.rpn = int(_rpn)
                                _mechanism.rpn_new = int(_rpn_new)
                            _child_row = _model.iter_next(_child_row)

                    elif _conf.RTK_FMECA_METHOD == 1:   # Task 102
                        _effect_prob = float(_model.get_value(_row, 19))
                        _ratio = float(_model.get_value(_row, 19))
                        _op_time = float(_model.get_value(_row, 21))
                        (_mode_hr, _mode_crit) = _mode.calculate(self._item_hr,
                                                                 _ratio,
                                                                 _op_time,
                                                                 _effect_prob)
                        _mode.mode_hazard_rate = _mode_hr
                        _mode.mode_criticality = _mode_crit
                        _model.set_value(_row, 20, _mode_hr)
                        _model.set_value(_row, 22, _mode_crit)

                _row = _model.iter_next(_row)

        elif index == 4:                    # Save FMECA
            self.dtcFMECA.save_fmea(self._hardware_id, None)

        return False

    def _on_cell_edit(self, cell, path, new_text, index):   # pylint: disable=R0912,R0914
        """
        Responds to edited signals from the FMECA gtk.TreeView().

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that called this
                                      method.
        :param str path: the path of the selected gtk.TreeIter().
        :param str new_text: the new text in the gtk.CellRenderer() that called
                             this method.
        :param int index: the position of the gtk.CellRenderer() in the
                          gtk.TreeModel().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _fmeca = self.dtcFMECA.dicDFMEA[self._hardware_id]

        (_model, _row) = self.tvwFMECA.get_selection().get_selected()
        _id = _model.get_value(_row, 1)
        _level = _model.get_value(_row, 60)

        _convert = gobject.type_name(_model.get_column_type(index))

        if new_text is None:
            _model[path][index] = not cell.get_active()
        elif _convert == 'gchararray':
            _model[path][index] = str(new_text)
        elif _convert == 'gint':
            _model[path][index] = int(new_text)
        elif _convert == 'gfloat':
            _model[path][index] = float(new_text)

        if _level == 1:                 # Failure Mode
            _mode = _fmeca.dicModes[_id]

            if index == 2:              # Description
                _mode.description = new_text
            elif index == 5:            # Mission
                for _key, _value in self.dtcFMECA.dicMissions.iteritems():
                    if _value[3] == new_text:
                        self._load_mission_phases(self.dtcFMECA.dicPhases[_key])
                _mode.mission = new_text
            elif index == 6:            # Mission phase
                _mode.mission_phase = new_text
                _mode.mode_op_time = float(self._dic_phases[new_text][1]) - \
                                     float(self._dic_phases[new_text][0])
                _model[path][21] = _mode.mode_op_time
            elif index == 7:            # Local effect
                _mode.local_effect = new_text
            elif index == 8:            # Next effect
                _mode.next_effect = new_text
            elif index == 9:            # End effect
                _mode.end_effect = new_text
            elif index == 10:
                _mode.detection_method = new_text
            elif index == 11:
                _mode.other_indications = new_text
            elif index == 12:
                _mode.isolation_method = new_text
            elif index == 13:
                _mode.design_provisions = new_text
            elif index == 14:
                _mode.operator_actions = new_text
            elif index == 15:
                _mode.severity_class = new_text
            elif index == 16:
                _mode.hazard_rate_source = new_text
            elif index == 17:
                _mode.mode_probability = new_text
            elif index == 18:
                _mode.effect_probability = float(new_text)
            elif index == 19:
                _mode.mode_ratio = float(new_text)
            elif index == 20:
                _mode.mode_hazard_rate = float(new_text)
            elif index == 21:
                _mode.mode_op_time = float(new_text)
            elif index == 22:
                _mode.mode_criticality = float(new_text)
            elif index == 23:
                _mode.rpn_severity = [i[0] for i in _conf.RTK_RPN_SEVERITY
                                      if i[1] == new_text][0]
            elif index == 27:
                _mode.rpn_severity_new = [i[0] for i in _conf.RTK_RPN_SEVERITY
                                          if i[1] == new_text][0]
            elif index == 40:
                _mode.critical_item = not cell.get_active()
            elif index == 41:
                _mode.single_point = not cell.get_active()
            elif index == 42:
                _mode.remarks = new_text

        elif _level == 2:               # Failure Mechanism
            _prow = _model.iter_parent(_row)
            _mode_id = _model.get_value(_prow, 1)
            _mode = _fmeca.dicModes[_mode_id]
            _mechanism = _mode.dicMechanisms[_id]

            if index == 2:
                _mechanism.description = new_text
            elif index == 24:
                _mechanism.rpn_occurrence = [i[0] for i in
                                             _conf.RTK_RPN_OCCURRENCE
                                             if i[1] == new_text][0]
            elif index == 25:
                _mechanism.rpn_detection = [i[0] for i in
                                            _conf.RTK_RPN_DETECTION
                                            if i[1] == new_text][0]
            elif index == 26:
                _mechanism.rpn = int(new_text)
            elif index == 28:
                _mechanism.rpn_occurrence_new = [i[0] for i in
                                                 _conf.RTK_RPN_OCCURRENCE
                                                 if i[1] == new_text][0]
            elif index == 29:
                _mechanism.rpn_detection_new = [i[0] for i in
                                                _conf.RTK_RPN_DETECTION
                                                if i[1] == new_text][0]
            elif index == 30:
                _mechanism.rpn_new = int(new_text)
            elif index == 31:
                _mechanism.include_pof = not cell.get_active()

        elif _level == 3:               # Failure Cause
            _prow = _model.iter_parent(_row)
            _mechanism_id = _model.get_value(_prow, 1)
            _prow = _model.iter_parent(_prow)
            _mode_id = _model.get_value(_prow, 1)
            _mode = _fmeca.dicModes[_mode_id]
            _mechanism = _mode.dicMechanisms[_mechanism_id]
            _cause = _mechanism.dicCauses[_id]

            if index == 2:
                _cause.description = new_text
            elif index == 24:
                _cause.rpn_occurrence = [i[0] for i in
                                         _conf.RTK_RPN_OCCURRENCE
                                         if i[1] == new_text][0]
            elif index == 25:
                _cause.rpn_detection = [i[0] for i in
                                        _conf.RTK_RPN_DETECTION
                                        if i[1] == new_text][0]
            elif index == 26:
                _cause.rpn = int(new_text)
            elif index == 28:
                _cause.rpn_occurrence_new = [i[0] for i in
                                             _conf.RTK_RPN_OCCURRENCE
                                             if i[1] == new_text][0]
            elif index == 29:
                _cause.rpn_detection_new = [i[0] for i in
                                            _conf.RTK_RPN_DETECTION
                                            if i[1] == new_text][0]
            elif index == 30:
                _cause.rpn_new = int(new_text)

        elif _level == 4:               # Control
            _prow = _model.iter_parent(_row)
            _cause_id = _model.get_value(_prow, 1)
            _prow = _model.iter_parent(_prow)
            _mechanism_id = _model.get_value(_prow, 1)
            _prow = _model.iter_parent(_prow)
            _mode_id = _model.get_value(_prow, 1)
            _mode = _fmeca.dicModes[_mode_id]
            _mechanism = _mode.dicMechanisms[_mechanism_id]
            _cause = _mechanism.dicCauses[_cause_id]
            _control = _cause.dicControls[_id]

            if index == 2:
                _control.description = new_text
            elif index == 3:
                _control.control_type = self._lst_control_type.index(new_text)

        elif _level == 5:               # Action
            _prow = _model.iter_parent(_row)
            _cause_id = _model.get_value(_prow, 1)
            _prow = _model.iter_parent(_prow)
            _mechanism_id = _model.get_value(_prow, 1)
            _prow = _model.iter_parent(_prow)
            _mode_id = _model.get_value(_prow, 1)
            _mode = _fmeca.dicModes[_mode_id]
            _mechanism = _mode.dicMechanisms[_mechanism_id]
            _cause = _mechanism.dicCauses[_cause_id]
            _action = _cause.dicActions[_id]

            if index == 2:
                _action.action_recommended = new_text
            elif index == 4:
                _action.action_category = _conf.RTK_ACTION_CATEGORY.index(new_text)
            elif index == 32:
                _owner = tuple([x.strip()
                                for x in new_text.decode('utf-8').split(',')])
                _action.action_owner = _conf.RTK_USERS.index(_owner)
            elif index == 33:
                _action.action_due_date = _util.date_to_ordinal(new_text)
            elif index == 34:
                _status = (new_text.decode('utf-8'),)
                _action.action_status = _conf.RTK_STATUS.index(_status)
            elif index == 35:
                _action.action_taken = new_text
            elif index == 36:
                _action.action_approved = not cell.get_active()
            elif index == 37:
                _action.action_approved_date = _util.date_to_ordinal(new_text)
            elif index == 38:
                _action.action_closed = not cell.get_active()
            elif index == 39:
                _action.action_closed_date = _util.date_to_ordinal(new_text)

        return False

    def _load_mission_phases(self, phases):
        """
        Loads the mission phase gtk.CellRendererCombo() whenever a new mission
        is selected.

        :param list phase: the list of phases to load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._dic_phases.clear()

        _column = self.tvwFMECA.get_column(5)
        _model = _column.get_cell_renderers()[0].get_property('model')
        _model.clear()

        _model.append([""])
        for i in range(len(phases)):
            _model.append([phases[i][5]])
            self._dic_phases[phases[i][5]] = phases[i][3:5]

        return False

    def _on_start_edit(self, cell, editable, __path, index):
        """
        Responds to editing-started signals from the FMECA gtk.TreeView().

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that called this
                                      method.
        :param gtk.CellEditable editable: the gtk.CellEditable() that is
                                          associated with the calling
                                          gtk.CellRenderer().
        :param str __path: the path of the selected gtk.TreeIter().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if isinstance(editable, gtk.Entry):
            if index in [32, 36, 38]:
                _date = _util.date_select(cell, None, editable)

        return False

    def _on_combo_changed(self, combo, index):
        """
        Responds to gtk.ComboBox() changed signals and calls the correct
        function or method, passing any parameters as needed.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        combo.handler_block(self._lst_handler_id[index])

        if index == 5:                      # FMECA Risk Method
            _conf.RTK_FMECA_METHOD = combo.get_active()
            self._show_risk_analysis()

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_row_changed(self, treeview):
        """
        Callback function to handle events for the FMECA package Work Book
        gtk.TreeView().  It is called whenever a FMECA Work Book gtk.TreeView()
        row is activated.

        :param gtk.TreeView treeview: the FMECA class gtk.TreeView().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = treeview.get_selection().get_selected()
        _level = _model.get_value(_row, 60)

        if _level == 1:                     # Failure mode.
            self.btnAddSibling.set_tooltip_text(_(u"Add a failure mode to the "
                                                  u"selected hardware item."))
            self.btnAddChild.set_tooltip_text(_(u"Add a failure mechanism to "
                                                u"the selected failure mode."))
            self.btnAddChild.set_sensitive(True)
            self.btnRemove.set_tooltip_text(_(u"Remove the selected failure "
                                              u"mode from the selected "
                                              u"hardware item."))
        elif _level == 2:                   # Failure mechanism.
            self.btnAddSibling.set_tooltip_text(_(u"Add a failure mechanism "
                                                  u"to the selected failure "
                                                  u"mode."))
            self.btnAddChild.set_tooltip_text(_(u"Add a failure cause to "
                                                u"the selected failure "
                                                u"mechanism."))
            self.btnAddChild.set_sensitive(True)
            self.btnRemove.set_tooltip_text(_(u"Remove the selected failure "
                                              u"mechanism from the selected "
                                              u"failure mode."))
        elif _level == 3:                   # Failure cause.
            self.btnAddSibling.set_tooltip_text(_(u"Add a failure cause "
                                                  u"to the selected failure "
                                                  u"mechanism."))
            self.btnAddChild.set_tooltip_text(_(u"Add a control or action to "
                                                u"the selected failure "
                                                u"cause."))
            self.btnAddChild.set_sensitive(True)
            self.btnRemove.set_tooltip_text(_(u"Remove the selected failure "
                                              u"cause from the selected "
                                              u"failure mechanism."))
        elif _level == 4:                   # Control.
            self.btnAddSibling.set_tooltip_text(_(u"Add a control to the "
                                                  u"selected failure cause."))
            self.btnAddChild.set_sensitive(False)
            self.btnRemove.set_tooltip_text(_(u"Remove the selected control "
                                              u"from the selected failure "
                                              u"cause."))
        elif _level == 5:                   # Action.
            self.btnAddSibling.set_tooltip_text(_(u"Add an action to the "
                                                  u"selected failure cause."))
            self.btnAddChild.set_sensitive(False)
            self.btnRemove.set_tooltip_text(_(u"Remove the selected action "
                                              u"from the selected failure "
                                              u"cause."))

        return False
