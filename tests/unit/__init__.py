#!/usr/bin/env python -O
"""
This is the test package for testing RTK.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.__init__.py is part of The RTK Project
#
# All rights reserved.
import sys
import os
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import create_database

import Configuration as Configuration
import Utilities as Utilities

# Import the RTK Common database table objects.
from dao.RTKUser import RTKUser
from dao.RTKGroup import RTKGroup
from dao.RTKEnviron import RTKEnviron
from dao.RTKModel import RTKModel
from dao.RTKType import RTKType
from dao.RTKCategory import RTKCategory
from dao.RTKSubCategory import RTKSubCategory
from dao.RTKPhase import RTKPhase
from dao.RTKDistribution import RTKDistribution
from dao.RTKManufacturer import RTKManufacturer
from dao.RTKUnit import RTKUnit
from dao.RTKMethod import RTKMethod
from dao.RTKCriticality import RTKCriticality
from dao.RTKRPN import RTKRPN
from dao.RTKLevel import RTKLevel
from dao.RTKApplication import RTKApplication
from dao.RTKHazards import RTKHazards
from dao.RTKStakeholders import RTKStakeholders
from dao.RTKStatus import RTKStatus
from dao.RTKCondition import RTKCondition
from dao.RTKFailureMode import RTKFailureMode
from dao.RTKMeasurement import RTKMeasurement
from dao.RTKLoadHistory import RTKLoadHistory

# Import the RTK Program database table objects.
from dao.RTKAction import RTKAction
from dao.RTKAllocation import RTKAllocation
from dao.RTKCause import RTKCause
from dao.RTKControl import RTKControl
from dao.RTKDesignElectric import RTKDesignElectric
from dao.RTKDesignMechanic import RTKDesignMechanic
from dao.RTKEnvironment import RTKEnvironment
from dao.RTKFailureDefinition import RTKFailureDefinition
from dao.RTKFunction import RTKFunction
from dao.RTKGrowthTest import RTKGrowthTest
from dao.RTKHardware import RTKHardware
from dao.RTKHazardAnalysis import RTKHazardAnalysis
from dao.RTKIncident import RTKIncident
from dao.RTKIncidentAction import RTKIncidentAction
from dao.RTKIncidentDetail import RTKIncidentDetail
from dao.RTKMatrix import RTKMatrix
from dao.RTKMechanism import RTKMechanism
from dao.RTKMilHdbkF import RTKMilHdbkF
from dao.RTKMission import RTKMission
from dao.RTKMissionPhase import RTKMissionPhase
from dao.RTKMode import RTKMode
from dao.RTKNSWC import RTKNSWC
from dao.RTKOpLoad import RTKOpLoad
from dao.RTKOpStress import RTKOpStress
from dao.RTKReliability import RTKReliability
from dao.RTKRequirement import RTKRequirement
from dao.RTKRevision import RTKRevision
from dao.RTKSimilarItem import RTKSimilarItem
from dao.RTKSoftware import RTKSoftware
from dao.RTKSoftwareDevelopment import RTKSoftwareDevelopment
from dao.RTKSoftwareReview import RTKSoftwareReview
from dao.RTKSoftwareTest import RTKSoftwareTest
from dao.RTKStakeholder import RTKStakeholder
from dao.RTKSurvival import RTKSurvival
from dao.RTKSurvivalData import RTKSurvivalData
from dao.RTKTest import RTKTest
from dao.RTKTestMethod import RTKTestMethod
from dao.RTKValidation import RTKValidation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2016 Andrew "weibullguy" Rowland'


def setUp():

    # Clean up from previous runs.
    if os.path.isfile('/tmp/rtk_debug.log'):
        os.remove('/tmp/rtk_debug.log')

    if os.path.isfile('/tmp/rtk_user.log'):
        os.remove('/tmp/rtk_user.log')

    if os.path.isfile('/tmp/TestDB.rtk'):
        os.remove('/tmp/TestDB.rtk')

    if os.path.isfile('/tmp/TestCommonDB.rtk'):
        os.remove('/tmp/TestCommonDB.rtk')

    # Create and populate the RTK Common test database.
    engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
    session = scoped_session(sessionmaker())

    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    RTKUser.__table__.create(bind=engine)
    RTKGroup.__table__.create(bind=engine)
    RTKEnviron.__table__.create(bind=engine)
    RTKModel.__table__.create(bind=engine)
    RTKType.__table__.create(bind=engine)
    RTKCategory.__table__.create(bind=engine)
    RTKSubCategory.__table__.create(bind=engine)
    RTKPhase.__table__.create(bind=engine)
    RTKDistribution.__table__.create(bind=engine)
    RTKManufacturer.__table__.create(bind=engine)
    RTKUnit.__table__.create(bind=engine)
    RTKMethod.__table__.create(bind=engine)
    RTKCriticality.__table__.create(bind=engine)
    RTKRPN.__table__.create(bind=engine)
    RTKLevel.__table__.create(bind=engine)
    RTKApplication.__table__.create(bind=engine)
    RTKHazards.__table__.create(bind=engine)
    RTKStakeholders.__table__.create(bind=engine)
    RTKStatus.__table__.create(bind=engine)
    RTKCondition.__table__.create(bind=engine)
    RTKFailureMode.__table__.create(bind=engine)
    RTKMeasurement.__table__.create(bind=engine)
    RTKLoadHistory.__table__.create(bind=engine)

    # Add an entry to each table.  These are used as the DUT in each test
    # file.
    session.add(RTKUser())
    session.add(RTKGroup())
    session.add(RTKEnviron())
    session.add(RTKModel())
    session.add(RTKType())
    session.add(RTKPhase())
    session.add(RTKDistribution())
    session.add(RTKManufacturer())
    session.add(RTKUnit())
    session.add(RTKMethod())
    session.add(RTKCriticality())
    session.add(RTKRPN())
    session.add(RTKLevel())
    session.add(RTKApplication())
    session.add(RTKHazards())
    session.add(RTKStakeholders())
    session.add(RTKStatus())
    session.add(RTKCondition())
    session.add(RTKMeasurement())
    session.add(RTKLoadHistory())
    session.commit()

    _category = RTKCategory()
    session.add(_category)
    session.commit()
    _subcategory = RTKSubCategory()
    _subcategory.category_id = _category.category_id
    session.add(_subcategory)
    session.commit()
    _failuremode = RTKFailureMode()
    _failuremode.category_id = _category.category_id
    _failuremode.subcategory_id = _subcategory.subcategory_id
    session.add(_failuremode)
    session.commit()

    # Create the RTK Program test database.
    create_database('sqlite:////tmp/TestDB.rtk')

    engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
    session = scoped_session(sessionmaker())

    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    # Create all the tables in the RTK Program test database.
    RTKRevision.__table__.create(bind=engine)
    RTKMission.__table__.create(bind=engine)
    RTKMissionPhase.__table__.create(bind=engine)
    RTKEnvironment.__table__.create(bind=engine)
    RTKFailureDefinition.__table__.create(bind=engine)
    RTKFunction.__table__.create(bind=engine)
    RTKRequirement.__table__.create(bind=engine)
    RTKStakeholder.__table__.create(bind=engine)
    RTKMatrix.__table__.create(bind=engine)
    RTKHardware.__table__.create(bind=engine)
    RTKAllocation.__table__.create(bind=engine)
    RTKHazardAnalysis.__table__.create(bind=engine)
    RTKSimilarItem.__table__.create(bind=engine)
    RTKReliability.__table__.create(bind=engine)
    RTKMilHdbkF.__table__.create(bind=engine)
    RTKNSWC.__table__.create(bind=engine)
    RTKDesignElectric.__table__.create(bind=engine)
    RTKDesignMechanic.__table__.create(bind=engine)
    RTKMode.__table__.create(bind=engine)
    RTKMechanism.__table__.create(bind=engine)
    RTKCause.__table__.create(bind=engine)
    RTKControl.__table__.create(bind=engine)
    RTKAction.__table__.create(bind=engine)
    RTKOpLoad.__table__.create(bind=engine)
    RTKOpStress.__table__.create(bind=engine)
    RTKTestMethod.__table__.create(bind=engine)
    RTKSoftware.__table__.create(bind=engine)
    RTKSoftwareDevelopment.__table__.create(bind=engine)
    RTKSoftwareReview.__table__.create(bind=engine)
    RTKSoftwareTest.__table__.create(bind=engine)
    RTKValidation.__table__.create(bind=engine)
    RTKIncident.__table__.create(bind=engine)
    RTKIncidentDetail.__table__.create(bind=engine)
    RTKIncidentAction.__table__.create(bind=engine)
    RTKTest.__table__.create(bind=engine)
    RTKGrowthTest.__table__.create(bind=engine)
    RTKSurvival.__table__.create(bind=engine)
    RTKSurvivalData.__table__.create(bind=engine)

    _revision = RTKRevision()
    session.add(_revision)
    session.commit()

    # Create tables that have Revision ID as a Foreign Key.
    _matrix = RTKMatrix()
    _matrix.revision_id = _revision.revision_id
    session.add(_matrix)

    _mission = RTKMission()
    _mission.revision_id = _revision.revision_id
    session.add(_mission)

    _failure_definition = RTKFailureDefinition()
    _failure_definition.revision_id = _revision.revision_id
    session.add(_failure_definition)

    _function = RTKFunction()
    _function.revision_id = _revision.revision_id
    session.add(_function)

    _requirement = RTKRequirement()
    _requirement.revision_id = _revision.revision_id
    session.add(_requirement)

    _stakeholder = RTKStakeholder()
    _stakeholder.revision_id = _revision.revision_id
    session.add(_stakeholder)

    _hardware = RTKHardware()
    _hardware.revision_id = _revision.revision_id
    session.add(_hardware)

    _incident = RTKIncident()
    _incident.revision_id = _revision.revision_id
    session.add(_incident)

    _software = RTKSoftware()
    _software.revision_id = _revision.revision_id
    session.add(_software)

    _test = RTKTest()
    _test.revision_id = _revision.revision_id
    session.add(_test)

    _survival = RTKSurvival()
    _survival.revision_id = _revision.revision_id
    session.add(_survival)

    _validation = RTKValidation()
    _validation.revision_id = _revision.revision_id
    session.add(_validation)

    session.commit()

    # Create tables that have Hardware ID as a Foreign Key.
    _allocation = RTKAllocation()
    _allocation.hardware_id = _hardware.hardware_id
    session.add(_allocation)

    _hazard_analysis = RTKHazardAnalysis()
    _hazard_analysis.hardware_id = _hardware.hardware_id
    session.add(_hazard_analysis)

    _similar_item = RTKSimilarItem()
    _similar_item.hardware_id = _hardware.hardware_id
    session.add(_similar_item)

    _mil_hdbk_f = RTKMilHdbkF()
    _mil_hdbk_f.hardware_id = _hardware.hardware_id
    session.add(_mil_hdbk_f)

    _nswc = RTKNSWC()
    _nswc.hardware_id = _hardware.hardware_id
    session.add(_nswc)

    _design_electric = RTKDesignElectric()
    _design_electric.hardware_id = _hardware.hardware_id
    session.add(_design_electric)

    _design_mechanic = RTKDesignMechanic()
    _design_mechanic.hardware_id = _hardware.hardware_id
    session.add(_design_mechanic)

    _reliability = RTKReliability()
    _reliability.hardware_id = _hardware.hardware_id
    session.add(_reliability)

    _mode = RTKMode()
    _mode.function_id = _function.function_id
    _mode.hardware_id = _hardware.hardware_id
    session.add(_mode)
    session.commit()

    # Create tables that have other than Revision ID or Hardware ID as a
    # Foreign Key or have o Foreign Key.
    _phase = RTKMissionPhase()
    _phase.mission_id = _mission.mission_id
    session.add(_phase)
    session.commit()

    _environment = RTKEnvironment()
    _environment.phase_id = _phase.phase_id
    session.add(_environment)
    session.commit()

    _mechanism = RTKMechanism()
    _mechanism.mode_id = _mode.mode_id
    session.add(_mechanism)
    session.commit()

    _cause = RTKCause()
    _cause.mechanism_id = _mechanism.mechanism_id
    session.add(_cause)
    session.commit()

    _control = RTKControl()
    _control.cause_id = _cause.cause_id
    session.add(_control)

    _action = RTKAction()
    _action.cause_id = _cause.cause_id
    session.add(_action)

    _op_load = RTKOpLoad()
    _op_load.mechanism_id = _mechanism.mechanism_id
    session.add(_op_load)

    _software_development = RTKSoftwareDevelopment()
    _software_development.software_id = _software.software_id
    session.add(_software_development)

    _software_review = RTKSoftwareReview()
    _software_review.software_id = _software.software_id
    session.add(_software_review)

    _software_test = RTKSoftwareTest()
    _software_test.software_id = _software.software_id
    session.add(_software_test)

    _incident_action = RTKIncidentAction()
    _incident_action.incident_id = _incident.incident_id
    session.add(_incident_action)

    _incident_detail = RTKIncidentDetail()
    _incident_detail.incident_id = _incident.incident_id
    session.add(_incident_detail)

    _growth_test = RTKGrowthTest()
    _growth_test.test_id = _test.test_id
    session.add(_growth_test)

    _survival_data = RTKSurvivalData()
    _survival_data.survival_id = _survival.survival_id
    session.add(_survival_data)

    session.commit()

    _op_stress = RTKOpStress()
    _op_stress.load_id = _op_load.load_id
    session.add(_op_stress)

    session.commit()

    _test_method = RTKTestMethod()
    _test_method.stress_id = _op_stress.stress_id
    session.add(_test_method)

    session.commit()

    Configuration.RTK_HR_MULTIPLIER = 1.0
    Configuration.RTK_DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/rtk_debug.log')
    Configuration.RTK_USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                         '/tmp/rtk_user.log')

def tearDown():

    if os.path.isfile('/tmp/TestDB.rtk'):
        os.remove('/tmp/TestDB.rtk')

    if os.path.isfile('/tmp/TestCommonDB.rtk'):
        os.remove('/tmp/TestCommonDB.rtk')