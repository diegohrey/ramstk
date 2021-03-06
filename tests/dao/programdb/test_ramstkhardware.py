# -*- coding: utf-8 -*-
#
#       tests.dao.programmdb.test_ramstkhardware.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKHardware module algorithms and models. """

from datetime import date

import pytest

from ramstk.dao.programdb.RAMSTKHardware import RAMSTKHardware

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'revision_id': 1,
    'hardware_id': 1,
    'alt_part_num': '',
    'attachments': '',
    'cage_code': '',
    'category_id': 0,
    'comp_ref_des': 'S1',
    'cost': 0.0,
    'cost_failure': 0.0,
    'cost_hour': 0.0,
    'cost_type_id': 0,
    'description': 'Test System',
    'duty_cycle': 100.0,
    'figure_number': '',
    'lcn': '',
    'level': 0,
    'manufacturer_id': 0,
    'mission_time': 100.0,
    'name': '',
    'nsn': '',
    'page_number': '',
    'parent_id': 0,
    'part': 0,
    'part_number': '',
    'quantity': 1,
    'ref_des': 'S1',
    'remarks': '',
    'repairable': 0,
    'specification_number': '',
    'subcategory_id': 0,
    'tagged_part': 0,
    'total_cost': 0.0,
    'total_part_count': 0,
    'total_power_dissipation': 0,
    'year_of_manufacture': date.today().year
}


@pytest.mark.integration
def test_ramstkhardware_create(test_dao):
    """ __init__() should create an RAMSTKHardware model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKHardware).first()

    assert isinstance(DUT, RAMSTKHardware)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_hardware'
    assert DUT.revision_id == 1
    assert DUT.hardware_id == 1
    assert DUT.alt_part_number == ''
    assert DUT.attachments == ''
    assert DUT.cage_code == ''
    assert DUT.comp_ref_des == 'S1'
    assert DUT.category_id == 0
    assert DUT.cost == 0.0
    assert DUT.cost_failure == 0.0
    assert DUT.cost_hour == 0.0
    assert DUT.cost_type_id == 0
    assert DUT.description == 'Test System'
    assert DUT.duty_cycle == 100.0
    assert DUT.figure_number == ''
    assert DUT.lcn == ''
    assert DUT.level == 0
    assert DUT.manufacturer_id == 0
    assert DUT.mission_time == 100.0
    assert DUT.name == ''
    assert DUT.nsn == ''
    assert DUT.page_number == ''
    assert DUT.parent_id == 0
    assert DUT.part == 0
    assert DUT.part_number == ''
    assert DUT.quantity == 1
    assert DUT.ref_des == 'S1'
    assert DUT.remarks == ''
    assert DUT.repairable == 0
    assert DUT.specification_number == ''
    assert DUT.subcategory_id == 0
    assert DUT.tagged_part == 0
    assert DUT.total_part_count == 0
    assert DUT.total_power_dissipation == 0.0
    assert DUT.year_of_manufacture == date.today().year


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKHardware).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKHardware).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKHardware {0:d} "
                    "attributes.".format(DUT.hardware_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKHardware).first()

    ATTRIBUTES.pop('name')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'name' in attribute "
                    "dictionary passed to RAMSTKHardware.set_attributes().")

    ATTRIBUTES['name'] = ''
