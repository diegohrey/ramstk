# -*- coding: utf-8 -*-
#
#       ramstk.modules.function.Controller.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Package Data Controller."""

# Import third party modules.
from pubsub import pub

# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataController
from ramstk.modules import RAMSTKDataMatrix
from ramstk.dao import RAMSTKFunction, RAMSTKHardware, RAMSTKSoftware
from . import dtmFunction


class FunctionDataController(RAMSTKDataController):
    """
    Provide interface between Function data model and RAMSTK view model.

    A single Function controller can manage one or more Function data
    models.  The attributes of a Function data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Function data controller instance.

        :param dao: the RAMSTK Program DAO instance to pass to the
                    Function Data Model.
        :type dao: :class:`ramstk.dao.DAO`
        :param configuration: the Configuration instance associated with
                              the current instance of the RAMSTK
                              application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmFunction(dao, **kwargs),
            ramstk_module='function',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dmx_fctn_hw_matrix = RAMSTKDataMatrix(dao, RAMSTKFunction,
                                                    RAMSTKHardware)
        self._dmx_fctn_sw_matrix = RAMSTKDataMatrix(dao, RAMSTKFunction,
                                                    RAMSTKSoftware)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.request_do_select_all, 'selected_revision')
        pub.subscribe(self.request_do_delete, 'request_delete_function')
        pub.subscribe(self.request_do_insert, 'request_insert_function')
        pub.subscribe(self.request_do_update, 'request_update_function')
        pub.subscribe(self.request_do_update_all,
                      'request_update_all_functions')
        pub.subscribe(self.request_set_attributes, 'editing_function')

    def request_do_create(self, revision_id, matrix_type):
        """
        Request to create or refresh a Function matrix.

        :param int revision_id: the ID of the Revision the desired Matrix is
                                associated with.
        :param str matrix_type: the type of the Matrix to select all rows and
        """
        if matrix_type == 'fnctn_hrdwr':
            self._dmx_fctn_hw_matrix.do_create(
                revision_id,
                matrix_type,
                rkey='function_id',
                ckey='hardware_id')

        return

    def request_do_select_all(self, revision_id):
        """
        Retrieve the treelib Tree() from the Function Data Model.

        :return: tree; the treelib Tree() of RAMSTKFunction models in the
                 Function tree.
        :rtype: :class:`treelib.Tree`
        """
        return self._dtm_data_model.do_select_all(revision_id=revision_id)

    def request_do_select_all_matrix(self, revision_id, matrix_type):
        """
        Retrieve all the Matrices associated with the Function.

        :param int revision_id: the Revision ID to select the matrices for.
        :param int matrix_type: the type of the Matrix to retrieve.  Current
                                Function matrix types are:

                                fnctn_hrdwr = Function:Hardware
                                fnctn_sftwr = Function:Software
                                fnctn_vldtn = Function:Validation

        :return: (_matrix, _column_hdrs, _row_hdrs); the Pandas Dataframe,
                 noun names to use for column headings, noun names to use for
                 row headings.
        :rtype: (:class:`pandas.DataFrame`, dict, dict)
        """
        _matrix = None
        _column_hdrs = []
        _row_hdrs = []

        if matrix_type == 'fnctn_hrdwr':
            self._dmx_fctn_hw_matrix.do_select_all(
                revision_id,
                matrix_type,
                rkey='function_id',
                ckey='hardware_id',
                rheader='function_code',
                cheader='comp_ref_des')
            _matrix = self._dmx_fctn_hw_matrix.dtf_matrix
            _column_hdrs = self._dmx_fctn_hw_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_fctn_hw_matrix.dic_row_hdrs

        return (_matrix, _column_hdrs, _row_hdrs)

    def request_do_insert(self, revision_id, parent_id, **kwargs):  # pylint: disable=unused-argument
        """
        Request to add an RAMSTKFunction table record.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_insert(
            revision_id=revision_id, parent_id=parent_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_insert_matrix(self, matrix_type, item_id, heading,
                                 row=True):
        """
        Request the to add a new row or column to the Data Matrix.

        :param str matrix_type: the type of the Matrix to retrieve.  Current
                                Function matrix types are:

                                fnctn_hrdwr = Function:Hardware
                                fnctn_sftwr = Function:Software
                                fnctn_vldtn = Function:Validation

        :param int item_id: the ID of the row or column item to insert into the
                            Matrix.
        :param str heading: the heading for the new row or column.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if matrix_type == 'fnctn_hrdwr':
            _error_code, _msg = self._dmx_fctn_hw_matrix.do_insert(
                item_id, heading, row=row)

        if _error_code == 0 and not self._test:
            pub.sendMessage(
                'insertedMatrix',
                matrix_type=matrix_type,
                item_id=item_id,
                row=row)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_delete(self, node_id):
        """
        Request to delete an RAMSTKFunction table record.

        :param int node_id: the PyPubSub Tree() ID of the Function to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_delete(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_delete_matrix(self, matrix_type, item_id, row=True):
        """
        Request to remove a row or column from the selected Data Matrix.

        :param str matrix_type: the type of the Matrix to retrieve.  Current
                                Function matrix types are:

                                fnctn_hrdwr = Function:Hardware
                                fnctn_sftwr = Function:Software
                                fnctn_vldtn = Function:Validation

        :param int item_id: the ID of the row or column item to remove from the
                            Matrix.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if matrix_type == 'fnctn_hrdwr':
            _error_code, _msg = self._dmx_fctn_hw_matrix.do_delete(
                item_id, row=row)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      'deletedMatrix')

    def request_do_update(self, node_id):
        """
        Request to update an RAMSTKFunction table record.

        :param int node_id: the PyPubSub Tree() ID of the Function to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_update_matrix(self, revision_id, matrix_type):
        """
        Request to update the selected Data Matrix.

        :param int revision_id: the ID of the Revision is the matrix to update
                                is associated with.
        :param int matrix_type: the type of the Matrix to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if matrix_type == 'fnctn_hrdwr':
            _error_code, _msg = self._dmx_fctn_hw_matrix.do_update(
                revision_id, matrix_type)
        else:
            _error_code = 6
            _msg = 'RAMSTK ERROR: Attempted to update non-existent matrix ' \
                   '{0:s}.'.format(matrix_type)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      'savedMatrix')

    def request_do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Request to update all records in the RAMSTKFunction table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_update_all()

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_set_attributes(self, module_id, key, value):
        """
        Request to set a Function attribute.

        :param int module_id: the ID of the entity who's attribute is to
                              be set.
        :param str key: the key of the attributes to set.
        :param value: the value to set the attribute identified by the
                      key.
        :return:
        :rtype:
        """
        _entity = self.request_do_select(module_id)
        _attributes = _entity.get_attributes()

        _attributes[key] = value

        return _entity.set_attributes(_attributes)
