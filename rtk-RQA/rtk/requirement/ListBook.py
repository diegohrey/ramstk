#!/usr/bin/env python
"""
##################################
Requirement Package List Book View
##################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.requirement.ListBook.py is part of the RTK Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

# Modules required for the GUI.
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

# Import other RTK modules.
try:
    import Configuration
    import gui.gtk.Widgets as Widgets
    from gui.gtk.Matrix import Matrix as rtkMatrix
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.gui.gtk.Widgets as Widgets
    from rtk.gui.gtk.Matrix import Matrix as rtkMatrix

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ListView(gtk.VBox):
    """
    The List Book view displays all the matrices and lists associated with the
    Requirement Class.  The attributes of a List Book view are:

    :ivar _dtc_matrices: the :py:class:`rtk.datamodels.Matrix.Matrix` data
                         controller instance.
    :ivar _lst_handler_id: list containing the signal handler ID's for each of
                           the gtk.Widget()s who have a callback method.
    :ivar gtk.Button btnSaveRqmtHard: the gtk.Button() to save the Requirement/
                                      Hardware Matrix.
    :ivar gtk.Button btnSaveRqmtSoft: the gtk.Button() to save the Requirement/
                                      Software Matrix.
    :ivar gtk.Button btnSaveRqmtVal: the gtk.Button() to save the Requirement/
                                     Validation Matrix.
    :ivar mtxHardware: the :py:class:`rtk.gui.gtk.Matrix.Matrix` that displays
                       the Requirement/Hardware Matrix.
    :ivar mtxSoftware: the :py:class:`rtk.gui.gtk.Matrix.Matrix` that displays
                       the Requirement/Software Matrix.
    :ivar mtxValidation: the :py:class:`rtk.gui.gtk.Matrix.Matrix` that
                         displays the Requirement/Validation Matrix.
    :ivar gtk.TreeView tvwIncidentsList: the gtk.TreeView() that displates the
                                         list of Incidents against the selected
                                         Requirement.
    """

    def __init__(self, modulebook):
        """
        Initializes the List Book view for the Requirement package.

        :param modulebook: the :py:class:`rtk.requirement.ModuleBook` to
                           associate with this List Book.
        """

        gtk.VBox.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._dtc_matrices = modulebook.mdcRTK.dtcMatrices

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        # Hardware Matrix page widgets.
        self.btnSaveRqmtHard = Widgets.make_button(width=35, image='save')

        self.mtxHardware = rtkMatrix()
        self.mtxHardware.n_fixed_columns = 3

        # Software Matrix page widgets.
        self.btnSaveRqmtSoft = Widgets.make_button(width=35, image='save')

        self.mtxSoftware = rtkMatrix()
        self.mtxSoftware.n_fixed_columns = 3

        # Validation Matrix page widgets.
        self.btnSaveRqmtVal = Widgets.make_button(width=35, image='save')

        self.mtxValidation = rtkMatrix()
        self.mtxValidation.n_fixed_columns = 3

        # Incidents List page widgets.
        self.tvwIncidentsList = gtk.TreeView()

        # Put it all together.
        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_notebook(self):
        """
        Method to create the Requirement class List View gtk.Notebook().

        :return: _notebook
        :rtype: gtk.Notebook
        """

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if Configuration.TABPOS[1] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif Configuration.TABPOS[1] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif Configuration.TABPOS[1] == 'top':

            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_hardware_matrix_page(_notebook)
        self._create_software_matrix_page(_notebook)
        self._create_validation_matrix_page(_notebook)

        # Connect widget signals to callback methods.  We do this here rather
        # than in each method so the _lst_handler_id index is the same as the
        # dicMatrix key for each Matrix.
        self._lst_handler_id.append(
            self.mtxHardware.connect('changed', self._on_matrix_changed, 0))
        self._lst_handler_id.append(
            self.mtxSoftware.connect('changed', self._on_matrix_changed, 1))
        self._lst_handler_id.append(
            self.mtxValidation.connect('changed', self._on_matrix_changed, 2))
        self._lst_handler_id.append(
            self.btnSaveRqmtHard.connect('clicked',
                                         self._on_button_clicked, 3))
        self._lst_handler_id.append(
            self.btnSaveRqmtSoft.connect('clicked',
                                         self._on_button_clicked, 4))
        self._lst_handler_id.append(
            self.btnSaveRqmtVal.connect('clicked',
                                        self._on_button_clicked, 5))

        return _notebook

    def _create_hardware_matrix_page(self, notebook):
        """
        Method to create the Requirement/Hardware matrix page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Requirement/Hardware matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnSaveRqmtHard, False, False)

        _hbox.pack_start(_bbox, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.mtxHardware.treeview)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Set tooltips for the Requirement/Hardware Matrix.
        self.mtxHardware.treeview.set_tooltip_markup(_(u"Displays the "
                                                       u"relationship between "
                                                       u"system Requirements "
                                                       u"and system "
                                                       u"Hardware.  This "
                                                       u"matrix shows which "
                                                       u"Hardware item "
                                                       u"partially (P) or "
                                                       u"completely (C) "
                                                       u"implements a "
                                                       u"Requirement, if at "
                                                       u"all."))

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Hardware\nMatrix</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the matrix showing relationships "
                                  u"between system requirements and hardware "
                                  u"items."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_software_matrix_page(self, notebook):
        """
        Method to create the Requirement/Software matrix page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Requirement/Software matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnSaveRqmtSoft, False, False)

        _hbox.pack_start(_bbox, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.mtxSoftware.treeview)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Set tooltips for the Requirement/Software Matrix.
        self.mtxHardware.treeview.set_tooltip_markup(_(u"Displays the "
                                                       u"relationship between "
                                                       u"system Requirements "
                                                       u"and system "
                                                       u"Software.  This "
                                                       u"matrix shows which "
                                                       u"Software item "
                                                       u"partially (P) or "
                                                       u"completely (C) "
                                                       u"implements a "
                                                       u"Requirement, if at "
                                                       u"all."))

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Software\nMatrix</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the matrix showing relationships "
                                  u"between system requirements and system "
                                  u"software items."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_validation_matrix_page(self, notebook):
        """
        Method to create the Requirement/Validation matrix page in the List
        View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Requirement/Validation matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnSaveRqmtVal, False, False)

        _hbox.pack_start(_bbox, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.mtxValidation.treeview)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Set tooltips for the Requirement/Validation Matrix.
        self.mtxValidation.treeview.set_tooltip_markup(_(u"Displays the "
                                                         u"relationship "
                                                         u"between system "
                                                         u"Requirements and "
                                                         u"Validation tasks.  "
                                                         u"This matrix shows "
                                                         u"which Validation "
                                                         u"task partially (P) "
                                                         u"or completely (C) "
                                                         u"validates a "
                                                         u"Requirement, if at "
                                                         u"all."))

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Validation\nMatrix</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the matrix showing relationships "
                                  u"between system requirements and "
                                  u"validation tasks."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def load(self):
        """
        Method to load the Requirement List Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _matrix_ids = self._dtc_matrices.dicMatrices.keys()

        for _index, _matrix_id in enumerate(_matrix_ids):
            # Retrieve the next matrix in the list.
            _matrix = self._dtc_matrices.dicMatrices[_matrix_id]

            if _matrix.matrix_type == 3:
                self._load_hardware_matrix_page(_matrix)
            elif _matrix.matrix_type == 4:
                self._load_software_matrix_page(_matrix)
            elif _matrix.matrix_type == 5:
                self._load_validation_matrix_page(_matrix)

        return False

    def _load_hardware_matrix_page(self, matrix):
        """
        Method to load the Requirement/Hardware matrix page.

        :param matrix: the :py:class:`rtk.datamodels.matrix.Matrix.Model` data
                       model to load into the Matrix.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Get the list of all Requirements and the list of top-level
        # Requirements.
        _requirements = matrix.dicRows.values()
        _top_items = [_r for _r in _requirements if _r[0] == -1]

        # Load the Function/Hardware matrix data.
        _gobject_types = [gobject.TYPE_INT, gobject.TYPE_STRING,
                          gobject.TYPE_STRING] + \
                         [gtk.gdk.Pixbuf, gobject.TYPE_STRING] * (matrix.n_col)
        _model = gtk.TreeStore(*_gobject_types)
        self.mtxHardware.treeview.set_model(_model)

        # Create the columns for the Requirement/Hardware matrix.  First,
        # remove any existing columns in the Matrix.
        for _column in self.mtxHardware.treeview.get_columns():
            self.mtxHardware.treeview.remove_column(_column)

        _headings = [_(u"Requirement\nID"), _(u"Requirement\nCode"),
                     _(u"Requirement")] + matrix.lstColumnHeaders
        _editable = [False, False, False] + [True, True] * (matrix.n_col)
        for _index, _heading in enumerate(_headings):
            self.mtxHardware.add_column(_heading, _index,
                                        editable=_editable[_index])

        # Load the Requirement/Hardware matrix.
        self.mtxHardware.load_matrix(_top_items, _requirements, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.mtxHardware.treeview.expand_all()
        self.mtxHardware.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.mtxHardware.treeview.get_column(0)
            self.mtxHardware.treeview.row_activated(_path, _column)

        return False

    def _load_software_matrix_page(self, matrix):
        """
        Method to load the Requirement/Software matrix page.

        :param matrix: the :py:class:`rtk.datamodels.matrix.Matrix.Model` data
                       model to load into the Matrix.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Get the list of all Requirements and the list of top-level
        # Requirements.
        _requirements = matrix.dicRows.values()
        _top_items = [_r for _r in _requirements if _r[0] == -1]

        # Load the Function/Software matrix data.
        _gobject_types = [gobject.TYPE_INT, gobject.TYPE_STRING,
                          gobject.TYPE_STRING] + \
                         [gtk.gdk.Pixbuf, gobject.TYPE_STRING] * (matrix.n_col)
        _model = gtk.TreeStore(*_gobject_types)
        self.mtxSoftware.treeview.set_model(_model)

        # Create the columns for the Requirement/Software matrix.  First,
        # remove any existing columns in the Matrix.
        for _column in self.mtxSoftware.treeview.get_columns():
            self.mtxSoftware.treeview.remove_column(_column)

        _headings = [_(u"Requirement\nID"), _(u"Requirement\nCode"),
                     _(u"Requirement")] + matrix.lstColumnHeaders
        _editable = [False, False, False] + [True, True] * (matrix.n_col)
        for _index, _heading in enumerate(_headings):
            self.mtxSoftware.add_column(_heading, _index,
                                        editable=_editable[_index])

        # Load the Requirement/Software matrix.
        self.mtxSoftware.load_matrix(_top_items, _requirements, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.mtxSoftware.treeview.expand_all()
        self.mtxSoftware.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.mtxSoftware.treeview.get_column(0)
            self.mtxSoftware.treeview.row_activated(_path, _column)

        return False

    def _load_validation_matrix_page(self, matrix):
        """
        Method to load the Requirement/Validation matrix page.

        :param matrix: the :py:class:`rtk.datamodels.matrix.Matrix.Model` data
                       model to load into the Matrix.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Get the list of all Requirements and the list of top-level
        # Requirements.
        _requirements = matrix.dicRows.values()
        _top_items = [_r for _r in _requirements if _r[0] == -1]

        # Load the Requirement/Validation matrix data.
        _gobject_types = [gobject.TYPE_INT, gobject.TYPE_STRING,
                          gobject.TYPE_STRING] + \
                         [gtk.gdk.Pixbuf, gobject.TYPE_STRING] * (matrix.n_col)
        _model = gtk.TreeStore(*_gobject_types)
        self.mtxValidation.treeview.set_model(_model)

        # Create the columns for the Requirement/Validation matrix.  First,
        # remove any existing columns in the Matrix.
        for _column in self.mtxValidation.treeview.get_columns():
            self.mtxValidation.treeview.remove_column(_column)

        _headings = [_(u"Requirement\nID"), _(u"Requirement\nCode"),
                     _(u"Requirement")] + matrix.lstColumnHeaders
        _editable = [False, False, False] + [True, True] * (matrix.n_col)
        for _index, _heading in enumerate(_headings):
            self.mtxValidation.add_column(_heading, _index,
                                          editable=_editable[_index])

        # Load the Requirement/Validation matrix.
        self.mtxValidation.load_matrix(_top_items, _requirements, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.mtxValidation.treeview.expand_all()
        self.mtxValidation.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.mtxValidation.treeview.get_column(0)
            self.mtxValidation.treeview.row_activated(_path, _column)

        return False

    def _on_matrix_changed(self, matrix, treeview, new_value, col_position,
                           index):
        """
        Callback method to handle changes to a Matrix cell.

        :param Matrix: the :py:class:`rtk.gui.gtk.Matrix.Matrix` that called
                       this method.
        :param gtk.TreeView treeview: the gtk.TreeView() imbedded in the
                                      Matrix.
        :param new_value: the new value of the cell in the Matrix.
        :param int col_position: the position in the Matrix of the column the
                                 calling gtk.CellRenderer() is in.
        :param int index: the index in the signal handler list associated with
                          the Matrix calling this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        matrix.handler_block(self._lst_handler_id[index])

        # Retrieve the Matrix object.
        _matrix = self._dtc_matrices.dicMatrices[index + 3]

        # Retrieve the Matrix gtk.TreeView() gtk.TreeModel() and selected
        # gtk.TreeIter() (i.e., the selected row).
        (_model, _row) = treeview.get_selection().get_selected()

        # Get the key in the Matrix row dictionary corresponding to the
        # selected row.  This is done by selecting the Requirement ID from the
        # Matrix and using this to find the associated key.
        _requirement_id = _model.get_value(_row, 0)
        _row_num = next((_key for _key, _value in _matrix.dicRows.iteritems()
                         if _value[1] == _requirement_id), None)

        # Calculate the position in the Matrix row dictionary whose value needs
        # to be changed and then set it equal to the new_value.  The position
        # in the Matrix row dictionary value list that needs to be changed
        # depends on the number of non-x-reference columns at the beginning of
        # the Matrix.  Given the following row in the Matrix:
        #
        #    [(3), ('REL-0003'), ('Requirement #3'), (<Pixbuf>, '0'),
        #     (<Pixbuf>, '1')]
        #
        # And the corresponding value list in the Matrix row dictionary:
        #
        #    [-1, 3, u'REL-0003', u'Requirement #3', u'0', u'1']
        #
        # If the <Pixbuf> at position 3 is changed, the corresponding value
        # list position is 4.  If the <Pixbuf> at position 5 is changed, the
        # corresponding value list position is 5.
        #
        # The general function for translating the changed <Pixbuf> to list
        # position is:
        #
        #    _position = 0.5 * (col_postion + n_fixed_col + 2)
        #
        # For the two examples above:
        #
        #    _position = 0.5 * (3 + 3 + 2) = 4
        #    _position = 0.5 * (5 + 3 + 2) = 4
        _position = int(0.5 * (col_position + matrix.n_fixed_columns + 2))
        _matrix.dicRows[_row_num][_position] = str(new_value)

        matrix.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_button_clicked(self, button, index):
        """
        Callback method to respond to button clicks.

        :param gtk.Button button: the gtk.Button() that called this method.
        :param int index: the index in the gtk.Widget() signal list.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[index])

        self._dtc_matrices.save_matrix(index)

        button.handler_unblock(self._lst_handler_id[index])

        return False
