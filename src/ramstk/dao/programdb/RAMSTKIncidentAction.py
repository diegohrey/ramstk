# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKIncidentAction.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RAMSTKIncidentAction Table
===============================================================================
"""

from datetime import date, timedelta

from sqlalchemy import BLOB, Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import error_handler, none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKIncidentAction(RAMSTK_BASE):
    """
    Class to represent the table ramstk_incident_action in the RAMSTK Program
    database.

    This table shares a Many-to-One relationship with ramstk_incident.
    """

    __tablename__ = 'ramstk_incident_action'
    __table_args__ = {'extend_existing': True}

    incident_id = Column(
        'fld_incident_id',
        Integer,
        ForeignKey('ramstk_incident.fld_incident_id'),
        nullable=False)
    action_id = Column(
        'fld_action_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    action_owner = Column('fld_action_owner', Integer, default=0)
    action_prescribed = Column('fld_action_prescribed', BLOB, default=b'')
    action_taken = Column('fld_action_taken', BLOB, default=b'')
    approved = Column('fld_approved', Integer, default=0)
    approved_by = Column('fld_approved_by', Integer, default=0)
    approved_date = Column(
        'fld_approved_date', Date, default=date.today() + timedelta(days=30))
    closed = Column('fld_closed', Integer, default=0)
    closed_by = Column('fld_closed_by', Integer, default=0)
    closed_date = Column(
        'fld_closed_date', Date, default=date.today() + timedelta(days=30))
    due_date = Column(
        'fld_due_date', Date, default=date.today() + timedelta(days=30))
    status_id = Column('fld_status_id', Integer, default=0)

    # Define the relationships to other tables in the RAMSTK Program database.
    incident = relationship('RAMSTKIncident', back_populates='incident_action')

    def get_attributes(self):
        """
        Retrieves the current values of the RAMSTKIncidentAction data model
        attributes.

        :return: (incident_id, action_id, action_id, action_owner,
                  action_prescribed, action_taken, approved, approved_by,
                  approved_date, closed, closed_by, closed_date, due_date,
                  status_id)
        :rtype: tuple
        """

        _values = (self.incident_id, self.action_id, self.action_owner,
                   self.action_prescribed, self.action_taken, self.approved,
                   self.approved_by, self.approved_date, self.closed,
                   self.closed_by, self.closed_date, self.due_date,
                   self.status_id)

        return _values

    def set_attributes(self, values):
        """
        Method to set the RAMSTKIncidentAction data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKIncidentAction {0:d} attributes.". \
               format(self.action_id)

        try:
            self.action_owner = int(none_to_default(values[0], 0))
            self.action_prescribed = none_to_default(values[1], b'')
            self.action_taken = none_to_default(values[2], b'')
            self.approved = int(none_to_default(values[3], 0))
            self.approved_by = int(none_to_default(values[4], 0))
            self.approved_date = none_to_default(
                values[5], date.today() + timedelta(days=30))
            self.closed = int(none_to_default(values[6], 0))
            self.closed_by = int(none_to_default(values[7], 0))
            self.closed_date = none_to_default(
                values[8], date.today() + timedelta(days=30))
            self.due_date = none_to_default(
                values[9], date.today() + timedelta(days=30))
            self.status_id = int(none_to_default(values[10], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Insufficient number of input values to " \
                   "RAMSTKIncidentAction.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Incorrect data type when converting one or " \
                   "more RAMSTKIncidentAction attributes."

        return _error_code, _msg
