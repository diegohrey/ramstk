#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.fmea.TestFMEA.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This is the test class for testing the FMEA class.
"""

import unittest
from nose.plugins.attrib import attr

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

from analyses.fmea.FMEA import Model, FMEA, ParentError

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestFMEAModel(unittest.TestCase):
    """
    Class for testing the FMEA model class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the FMEA model class.
        """

        self.FDUT = Model(None, 0)
        self.HDUT = Model(0, None)

    @attr(all=True, unit=True)
    def test_function_FMEA_create(self):
        """
        (TestFMEA) __init__ should return instance of Function FMEA data model
        """

        DUT = Model(None, 0)

        self.assertTrue(isinstance(DUT, Model))
        self.assertEqual(DUT.dicModes, {})
        self.assertEqual(DUT.assembly_id, None)
        self.assertEqual(DUT.function_id, 0)

    @attr(all=True, unit=True)
    def test_hardware_FMEA_create(self):
        """
        (TestFMEA) __init__ should return instance of Hardware FMEA data model
        """

        DUT = Model(0, None)

        self.assertTrue(isinstance(DUT, Model))
        self.assertEqual(DUT.dicModes, {})
        self.assertEqual(DUT.assembly_id, 0)
        self.assertEqual(DUT.function_id, None)

    @attr(all=True, unit=True)
    def test_FMEA_create_parent_problem(self):
        """
        (TestFMEA) __init__ raises ParentError for None, None or int, int input
        """

        self.assertRaises(ParentError, Model, None, None)
        self.assertRaises(ParentError, Model, 2, 10)

    #@attr(all=True, unit=True)
    #def test_rpn(self):
    #    """
    #    (TestFMEA) calculate always returns a value between 1 - 1000
    #    """

    #    for severity in range(1, 11):
    #        for occurrence in range(1, 11):
    #            for detection in range(1, 11):
    #                self.assertIn(self.DUT.calculate(severity,
    #                                                 occurrence,
    #                                                 detection),
    #                              range(1, 1001))

    #@attr(all=True, unit=True)
    #def test_rpn_out_of_range_inputs(self):
    #    """
    #    (TestFMEA) calculate raises OutOfRangeError for 10 < input < 1
    #    """

    #    self.assertRaises(OutOfRangeError, self.DUT.calculate, 0, 1, 1)
    #    self.assertRaises(OutOfRangeError, self.DUT.calculate, 11, 1, 1)
    #    self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 0, 1)
    #    self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 11, 1)
    #    self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 1, 0)
    #    self.assertRaises(OutOfRangeError, self.DUT.calculate, 1, 1, 11)


class TestFMEAController(unittest.TestCase):
    """
    Class for testing the FMEA data controller class.
    """

    def setUp(self):

        self.DUT = FMEA()

    @attr(all=True, unit=True)
    def test_create_controller(self):
        """
        (TestFMEA) __init__ should return instance of FMEA data controller
        """

        self.assertEqual(self.DUT.dicDFMEA, {})
        self.assertEqual(self.DUT.dicFFMEA, {})
