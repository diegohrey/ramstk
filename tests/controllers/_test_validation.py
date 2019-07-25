# pylint: disable=protected-access
# -*- coding: utf-8 -*-
#
#       tests.modules.test_validation.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Validation module algorithms and models. """

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from treelib import Tree

# RAMSTK Package Imports
from ramstk.dao import DAO
from ramstk.dao.programdb import RAMSTKProgramStatus, RAMSTKValidation
from ramstk.modules.validation import dtcValidation, dtmValidation

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'revision_id': 1,
    'validation_id': 1,
    'acceptable_maximum': 0.0,
    'acceptable_mean': 0.0,
    'acceptable_minimum': 0.0,
    'acceptable_variance': 0.0,
    'confidence': 95.0,
    'cost_average': 0.0,
    'cost_ll': 0.0,
    'cost_maximum': 0.0,
    'cost_mean': 0.0,
    'cost_minimum': 0.0,
    'cost_ul': 0.0,
    'cost_variance': 0.0,
    'date_end': date.today() + timedelta(days=30),
    'date_start': date.today(),
    'description': '',
    'measurement_unit': '',
    'name': '',
    'status': 0.0,
    'task_type': '',
    'task_specification': '',
    'time_average': 0.0,
    'time_ll': 0.0,
    'time_maximum': 0.0,
    'time_mean': 0.0,
    'time_minimum': 0.0,
    'time_ul': 0.0,
    'time_variance': 0.0,
}


@pytest.mark.integration
def test_data_model_create(test_dao):
    """ __init__() should return a Validation model. """
    DUT = dtmValidation(test_dao, test=True)

    assert isinstance(DUT, dtmValidation)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.status_tree, Tree)
    assert isinstance(DUT.dao, DAO)
    assert DUT.status_tree.get_node(0).tag == 'Program Status'


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKValidation instances on success. """
    DUT = dtmValidation(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.tree.get_node(1).data, RAMSTKValidation)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKValidation data model on success. """
    DUT = dtmValidation(test_dao, test=True)
    DUT.do_select_all(revision_id=1)
    _validation = DUT.do_select(1)

    assert isinstance(_validation, RAMSTKValidation)
    assert _validation.validation_id == 1


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent Validation ID is requested. """
    DUT = dtmValidation(test_dao, test=True)
    _validation = DUT.do_select(100)

    assert _validation is None


@pytest.mark.integration
def test_request_do_delete_matrix_row(test_dao, test_configuration):
    """ request_do_delete_matrix() should return False on successfully deleting a row. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT._request_do_select_all_matrix(1, 'vldtn_hrdwr')
    DUT.request_do_insert_matrix('vldtn_hrdwr', 5, 'Validation task from test')

    assert not DUT._request_do_delete_matrix('vldtn_hrdwr', 5)


@pytest.mark.integration
def test_request_do_delete_matrix_non_existent_row(
        test_dao,
        test_configuration,
):
    """ request_do_delete_matrix() should return True when attempting to delete a non-existent row. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT._request_do_select_all_matrix(1, 'vldtn_hrdwr')

    assert DUT._request_do_delete_matrix('vldtn_hrdwr', 5)


@pytest.mark.integration
def test_request_do_delete_matrix_column(test_dao, test_configuration):
    """ request_do_delete_matrix() should return False on successfully deleting a column. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT._request_do_select_all_matrix(1, 'vldtn_hrdwr')
    DUT.request_do_insert_matrix('vldtn_hrdwr', 5, 'S1:SS1:A1', row=False)

    assert not DUT._request_do_delete_matrix('vldtn_hrdwr', 5, row=False)


@pytest.mark.integration
def test_do_insert(test_dao):
    """ do_insert() should return False on success. """
    DUT = dtmValidation(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(revision_id=1)

    assert _error_code == 0
    assert _msg == (
        'RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program '
        'database.'
    )
    assert DUT.last_id == 2


@pytest.mark.integration
def test_request_do_insert_matrix_row(test_dao, test_configuration):
    """ request_do_insert_matrix() should return False on successfully inserting a row. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT._request_do_select_all_matrix(
        1, 'vldtn_hrdwr',
    )

    assert not DUT.request_do_insert_matrix(
        'vldtn_hrdwr', 5,
        'Validation task from test',
    )
    assert DUT._dmx_vldtn_hw_matrix.dic_row_hdrs[
        5
    ] == 'Validation task from test'


@pytest.mark.integration
def test_request_do_insert_matrix_duplicate_row(test_dao, test_configuration):
    """ request_do_insert_matrix() should return True when attempting to insert a duplicate row. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT._request_do_select_all_matrix(
        1, 'vldtn_hrdwr',
    )

    assert DUT.request_do_insert_matrix(
        'vldtn_hrdwr', 1,
        'Validation task from test',
    )


@pytest.mark.integration
def test_request_do_insert_matrix_column(test_dao, test_configuration):
    """ request_do_insert_matrix() should return False on successfully inserting a column. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT._request_do_select_all_matrix(
        5, 'vldtn_hrdwr',
    )

    assert not DUT.request_do_insert_matrix(
        'vldtn_hrdwr', 9, 'S1:SS1:A11', row=False,
    )
    assert DUT._dmx_vldtn_hw_matrix.dic_column_hdrs[9] == 'S1:SS1:A11'


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmValidation(test_dao, test=True)
    DUT.do_select_all(revision_id=1)
    DUT.do_insert(revision_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == (
        'RAMSTK SUCCESS: Deleting an item from the RAMSTK Program '
        'database.'
    )


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Validation ID that doesn't exist. """
    DUT = dtmValidation(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == (
        '  RAMSTK ERROR: Attempted to delete non-existent '
        'Validation ID 300.'
    )


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmValidation(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _validation = DUT.do_select(DUT.last_id)
    _validation.availability_logistics = 0.9832

    _error_code, _msg = DUT.do_update(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Updating the RAMSTK Program database.')


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a Validation ID that doesn't exist. """
    DUT = dtmValidation(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2005
    assert _msg == (
        'RAMSTK ERROR: Attempted to save non-existent Validation ID '
        '100.'
    )


@pytest.mark.integration
def test_do_update_status(test_dao):
    """ do_update_status() should return a zero error code on success. """
    DUT = dtmValidation(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update_status()

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Updating the RAMSTK Program database.')


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmValidation(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Updating all records in the validation "
        "table."
    )


@pytest.mark.integration
def test_do_calculate_cost(test_dao):
    """ do_calculate() returns False on successfully calculating tasks costs. """
    DUT = dtmValidation(test_dao, test=True)
    DUT.do_select_all(revision_id=1)
    _validation = DUT.do_select(1)
    _validation.cost_minimum = 252.00
    _validation.cost_average = 368.00
    _validation.cost_maximum = 441.00
    _validation.confidence = 0.95

    assert not DUT.do_calculate(1, metric='cost')
    assert _validation.cost_mean == pytest.approx(360.83333333)
    assert _validation.cost_variance == pytest.approx(992.25)


@pytest.mark.integration
def test_do_calculate_time(test_dao):
    """ do_calculate() returns False on successfully calculating tasks times. """
    DUT = dtmValidation(test_dao, test=True)
    DUT.do_select_all(revision_id=1)
    _validation = DUT.do_select(1)
    _validation.time_minimum = 25.2
    _validation.time_average = 36.8
    _validation.time_maximum = 44.1
    _validation.confidence = 0.95

    assert not DUT.do_calculate(1, metric='time')
    assert _validation.time_mean == pytest.approx(36.08333333)
    assert _validation.time_variance == pytest.approx(9.9225)


@pytest.mark.integration
def test_do_calculate_all(test_dao):
    """ do_calculate_all() returns False on successfully calculating tasks times. """
    DUT = dtmValidation(test_dao, test=True)
    DUT.do_select_all(revision_id=1)
    _validation = DUT.do_select(1)
    _validation.cost_minimum = 252.00
    _validation.cost_average = 368.00
    _validation.cost_maximum = 441.00
    _validation.time_minimum = 25.2
    _validation.time_average = 36.8
    _validation.time_maximum = 44.1
    _validation.confidence = 0.95

    _attributes = DUT.do_calculate_all()
    assert _attributes['cost_ll'] == pytest.approx(299.0944678203216)
    assert _attributes['cost_mean'] == pytest.approx(360.833)
    assert _attributes['cost_ul'] == pytest.approx(422.572)
    assert _attributes['cost_variance'] == pytest.approx(0.0)
    assert _attributes['time_ll'] == pytest.approx(29.909446782032155)
    assert _attributes['time_mean'] == pytest.approx(36.08333333333333)
    assert _attributes['time_ul'] == pytest.approx(42.2572198846345)
    assert _attributes['time_variance'] == pytest.approx(992.25)
    assert _attributes['time_remaining'] == pytest.approx(36.8)
    assert isinstance(_attributes['status'], RAMSTKProgramStatus)


@pytest.mark.integration
def test_data_controller_create(test_dao, test_configuration):
    """ __init__() should return a Validation Data Controller. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcValidation)
    assert isinstance(DUT._dtm_data_model, dtmValidation)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_configuration):
    """ request_do_select_all() should return a Tree of RAMSTKValidation models. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert isinstance(
        DUT._dtm_data_model.tree.get_node(1).data, RAMSTKValidation,
    )


@pytest.mark.integration
def test_request_do_select(test_dao, test_configuration):
    """ request_do_select() should return an RAMSTKValidation model. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert isinstance(DUT.request_do_select(1), RAMSTKValidation)


@pytest.mark.integration
def test_request_do_create_matrix(test_dao, test_configuration):
    """ request_do_create_matrix should return None. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT._request_do_create_matrix(1, 'vldtn_hrdwr') is None


@pytest.mark.integration
def test_request_do_select_non_existent_id(test_dao, test_configuration):
    """ request_do_select() should return None when requesting a Validation that doesn't exist. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)

    assert DUT.request_do_select(100) is None


@pytest.mark.integration
def test_request_do_insert(test_dao, test_configuration):
    """ request_do_insert() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_insert(revision_id=1)


@pytest.mark.integration
def test_request_do_delete(test_dao, test_configuration):
    """ request_do_delete() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_delete(2)


@pytest.mark.integration
def test_request_do_delete_non_existent_id(test_dao, test_configuration):
    """ request_do_delete() should return True when attempting to delete a non-existent Validation. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_delete(100)


@pytest.mark.integration
def test_request_do_update(test_dao, test_configuration):
    """ request_do_update() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update(1)


@pytest.mark.integration
def test_request_do_update_non_existent_id(test_dao, test_configuration):
    """ request_do_update() should return True when attempting to save a non-existent Validation. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_update(100)


@pytest.mark.integration
def test_request_do_update_matrix(test_dao, test_configuration):
    """ request_do_update_matrix() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT._request_do_select_all_matrix(
        1, 'vldtn_hrdwr',
    )

    assert not DUT._request_do_update_matrix(1, 'vldtn_hrdwr')


@pytest.mark.integration
def test_request_do_update_non_existent_matrix(test_dao, test_configuration):
    """ request_do_update_matrix() should return True when attempting to update a non-existent matrix. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    (_matrix, _column_hdrs, _row_hdrs) = DUT._request_do_select_all_matrix(
        1, 'vldtn_hrdwr',
    )

    assert DUT._request_do_update_matrix(1, 'vldtn_rvsn')

@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update_all()


@pytest.mark.integration
def test_request_do_calculate_cost(test_dao, test_configuration):
    """ request_do_calculate() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)
    _validation = DUT.request_do_select(1)
    _validation.cost_minimum = 252.00
    _validation.cost_average = 368.00
    _validation.cost_maximum = 441.00
    _validation.confidence = 0.95

    assert not DUT.request_do_calculate(1, metric='cost')
    assert _validation.cost_mean == pytest.approx(360.83333333)
    assert _validation.cost_variance == pytest.approx(992.25)


@pytest.mark.integration
def test_request_do_calculate_time(test_dao, test_configuration):
    """ request_do_calculate() should return False on success. """
    DUT = dtcValidation(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)
    _validation = DUT.request_do_select(1)
    _validation.time_minimum = 25.2
    _validation.time_average = 36.8
    _validation.time_maximum = 44.1
    _validation.confidence = 0.95

    assert not DUT.request_do_calculate(1, metric='time')
    assert _validation.time_mean == pytest.approx(36.08333333)
    assert _validation.time_variance == pytest.approx(9.9225)