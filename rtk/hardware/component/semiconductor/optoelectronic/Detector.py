#!/usr/bin/env python
"""
########################################################################
Hardware.Component.Semiconductor.Optoelectronics Package Detector Module
########################################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.semiconductor.optoelectronics.Detector.py is
#       part of the RTK Project
#
# All rights reserved.

import gettext
import locale

try:
<<<<<<< HEAD
    import Configuration as _conf
    import Utilities as _util
    from hardware.component.semiconductor.Semiconductor import Model as \
        Semiconductor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    import rtk.Utilities as _util
=======
    import Configuration
    import Utilities
    from hardware.component.semiconductor.Semiconductor import Model as \
        Semiconductor
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    from rtk.hardware.component.semiconductor.Semiconductor import Model as \
        Semiconductor

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# Add localization support.
try:
<<<<<<< HEAD
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
=======
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Detector(Semiconductor):
    """
    The Optoelectronic Detector data model contains the attributes and methods
    of an Optoelectronic Detector component.  The attributes of an
    Optoelectronic Detector are:

<<<<<<< HEAD
    :cvar _lst_lambdab: list of base hazard rates
    :cvar _lst_piE: list of operating environment pi factors
    :cvar subcategory: default value: 22

    :ivar type: default value: 0
=======
    :cvar list _lst_lambdab: list of base hazard rates
    :cvar list _lst_piE: list of operating environment pi factors
    :cvar int subcategory: default value: 22

    :ivar int type: default value: 0
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

    Covers specification MIL-S-19500.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.11.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_lambdab = [0.0055, 0.0040, 0.0025, 0.013, 0.013, 0.0064, 0.0033,
                    0.017, 0.017, 0.0086, 0.0013, 0.00023]
    _lst_piE = [1.0, 2.0, 8.0, 5.0, 12.0, 4.0, 6.0, 6.0, 8.0, 17.0, 0.5, 9.0,
                24.0, 450.0]
    _lst_piQ_count = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lst_piQ_stress = [0.7, 1.0, 2.4, 5.5, 8.0]
    _lambda_count = [[0.01100, 0.0290, 0.0830, 0.0590, 0.1800, 0.0840, 0.1100,
                      0.2100, 0.3500, 0.3400, 0.00570, 0.1500, 0.510, 3.70],
                     [0.02700, 0.0700, 0.2000, 0.1400, 0.4300, 0.2000, 0.2500,
                      0.4900, 0.8300, 0.8000, 0.01300, 0.3500, 1.200, 8.70],
                     [0.00047, 0.0012, 0.0035, 0.0025, 0.0077, 0.0035, 0.0044,
                      0.0086, 0.0150, 0.0140, 0.00024, 0.0053, 0.021, 0.15]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 22

    def __init__(self):
        """
<<<<<<< HEAD
        Initialize a Optoelectronic Detector data model instance.
=======
        Method to initialize an Optoelectronic Detector data model instance.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        super(Detector, self).__init__()

        # Initialize private list attributes.
        self._lst_lambdab_count = []

        # Initialize public scalar attributes.
        self.type = 0                # Application index.

    def set_attributes(self, values):
        """
<<<<<<< HEAD
        Sets the Optoelectronic Detector data model attributes.
=======
        Method to set the Optoelectronic Detector data model attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Semiconductor.set_attributes(self, values)

        try:
            self.type = int(values[117])
        except IndexError as _err:
<<<<<<< HEAD
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _util.error_handler(_err.args)
=======
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = Utilities.error_handler(_err.args)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
<<<<<<< HEAD
        Retrieves the current values of the Optoelectronic Detector data model
        attributes.
=======
        Method to retrieve the current values of the Optoelectronic Detector
        data model attributes.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: (type, )
        :rtype: tuple
        """

        _values = Semiconductor.get_attributes(self)

        _values = _values + (self.type, )

        return _values

<<<<<<< HEAD
    def calculate(self):
        """
        Calculates the hazard rate for the Optoelectronic Detector data model.
=======
    def calculate_part(self):
        """
        Method to calculate the hazard rate for the Optoelectronic Detector
        data model.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            # Set the base hazard rate for the model.
            if self.type in [1, 2]:
                self._lst_lambdab_count = self._lambda_count[0]
            elif self.type in [3, 4, 5, 6, 7, 8, 9, 10]:
                self._lst_lambdab_count = self._lambda_count[1]
            else:
                self._lst_lambdab_count = self._lambda_count[2]

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piQ * piE'

            # Set the base hazard rate for the model.
            self.base_hr = self._lst_lambdab[self.type - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the temperature factor for the model.
<<<<<<< HEAD
            self.piT = exp(-2790.0 * ((1.0 / (self.junction_temperature + 273.0)) - (1.0 / 298.0)))
            self.hazard_rate_model['piT'] = self.piT

        return Semiconductor.calculate(self)

    def _overstressed(self):
        """
        Determines whether the Optoelectronic Detector is overstressed based on
        it's rated values and operating environment.
=======
            self.piT = exp(-2790.0 * ((1.0 / (self.junction_temperature +
                                              273.0)) - (1.0 / 298.0)))
            self.hazard_rate_model['piT'] = self.piT

        return Semiconductor.calculate_part(self)

    def _overstressed(self):
        """
        Method to determine whether the Optoelectronic Detector is overstressed
        based on it's rated values and operating environment.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _reason_num = 1
<<<<<<< HEAD
        _harsh = True

        self.overstress = False

        # If the active environment is Benign Ground, Fixed Ground,
        # Sheltered Naval, or Space Flight it is NOT harsh.
        if self.environment_active in [1, 2, 4, 11]:
            _harsh = False

        if self.operating_voltage > 0.70 * self.rated_voltage:
            self.overstress = True
            self.reason = self.reason + str(_reason_num) + \
                           ". Operating voltage > 70% rated voltage.\n"
            _reason_num += 1
        if self.junction_temperature > 125.0:
            self.overstress = True
            self.reason = self.reason + str(_reason_num) + \
                          ". Junction temperature > 125.0C.\n"
            _reason_num += 1

=======
        _reason = ''

        self.overstress = False

        if self.operating_voltage > 0.70 * self.rated_voltage:
            self.overstress = True
            _reason = _reason + str(_reason_num) + \
                      ". Operating voltage > 70% rated voltage.\n"
            _reason_num += 1
        if self.junction_temperature > 125.0:
            self.overstress = True
            _reason = _reason + str(_reason_num) + \
                      ". Junction temperature > 125.0C.\n"
            _reason_num += 1

        self.reason = _reason

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        return False
