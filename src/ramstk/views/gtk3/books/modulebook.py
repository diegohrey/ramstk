# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.mwi.ModuleBook.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Module Book Module."""

# Standard Library Imports
from typing import List

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.revision import mvwRevision
from ramstk.views.gtk3.widgets import RAMSTKBaseBook


class RAMSTKModuleBook(RAMSTKBaseBook):
    """
    Display Module Views for the RAMSTK modules.

    Attributes of the Module Book are:

    :ivar dict _dic_module_views: dictionary containing the Module View to
        load into the RAMSTK Module Book for each RAMSTK module.  Key is the
        RAMSTK module name; value is the View associated with that RAMSTK
        module.
    """

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize an instance of the Module Book class.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        RAMSTKBaseBook.__init__(self, configuration)

        # Initialize private dictionary attributes.
        self._dic_module_views = {
            'revision': mvwRevision(configuration, logger),
            #    'requirement': mvwRequirement(configuration),
            #    'function': mvwFunction(configuration),
            #    'hardware': mvwHardware(configuration),
            #    'validation': mvwValidation(configuration),
        }

        # Initialize private list attributes.
        self._lst_handler_id: List[int] = []

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.icoStatus = Gtk.StatusIcon()

        self._set_properties('modulebook')
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_open, 'succeed_retrieve_revisions')
        pub.subscribe(self._on_close, 'succeed_closed_program')

    def __make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.insert_page(
            self._dic_module_views['revision'],
            tab_label=self._dic_module_views['revision'].hbx_tab_label,
            position=0)

        self.show_all()
        self.set_current_page(0)

    def __set_callbacks(self) -> None:
        """
        Set the callback functions/methods for the RAMSTKListBook and widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.connect('select-page', self._on_switch_page))
        self._lst_handler_id.append(
            self.connect('switch-page', self._on_switch_page))

    def _on_close(self) -> None:
        """
        Update the Module View when a RAMSTK Program database is closed.

        :return: None
        :rtype: None
        """
        # Remove all the non-Revision pages.
        _n_pages = self.get_n_pages()
        for _page in range(_n_pages - 1):
            self.remove_page(-1)

        # Clear the Revision page treeview.
        _model = self._dic_module_views['revision'].treeview.get_model()
        _model.clear()

    def _on_open(self, tree: Tree) -> None:  # pylint: disable=unused-argument
        """
        Update the status bar and clear the progress bar.

        :return: None
        :rtype: None
        """
        # Insert a page for each of the active RAMSTK Modules.
        for _key in self.RAMSTK_USER_CONFIGURATION.RAMSTK_PAGE_NUMBER:
            _mkey = self.RAMSTK_USER_CONFIGURATION.RAMSTK_PAGE_NUMBER[_key]
            _module = self._dic_module_views[_mkey]

            self.insert_page(_module,
                             tab_label=_module.hbx_tab_label,
                             position=_key)

        pub.sendMessage('mvwSwitchedPage', module='revision')

    def _on_switch_page(self, __notebook: Gtk.Notebook, __page: Gtk.Widget,
                        page_num: int) -> None:
        """
        Handle page changes in the Module Book Gtk.Notebook().

        :param __notebook: the Tree Book notebook widget.
        :type __notebook: :class:`Gtk.Notebook`
        :param __page: the newly selected page's child widget.
        :type __page: :class:`Gtk.Widget`
        :param int page_num: the newly selected page number.
            0 = Revision Tree
            1 = Requirements Tree
            2 = Function Tree
            3 = Hardware Tree
            4 = Software Tree (future)
            5 = Testing Tree (future)
            6 = Validation Tree
            7 = Incident Tree (future)
            8 = Survival Analyses Tree (future)

        :return: None
        :rtype: None
        """
        # Key errors occur when no RAMSTK Program database has been loaded.  In
        # that case, select the Revision page to load.
        try:
            _module = self.RAMSTK_USER_CONFIGURATION.RAMSTK_PAGE_NUMBER[
                page_num]
        except KeyError:
            _module = 'revision'

        pub.sendMessage('mvwSwitchedPage', module=_module)