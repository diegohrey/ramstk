#!/usr/bin/env python
"""
####################################################
Survival Package Weibull Distribution Work Book View
####################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.survival.gui.gtk.Weibull.py is part of The RTK Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

# Import modules for mathematics.
from math import ceil, sqrt
import numpy as np
from scipy.stats import probplot
from statsmodels.distributions.empirical_distribution import ECDF

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

# Plotting package.
import matplotlib
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure
if 'linux' in sys.platform:
    import pkg_resources
    pkg_resources.require('matplotlib==1.4.3')

# Import other RTK modules.
try:
    import Configuration
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.gui.gtk.Widgets as Widgets

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

_ = gettext.gettext

matplotlib.use('GTK')


class Results(gtk.HPaned):                  # pylint: disable=R0902, R0904
    """
    The Work Book page to display all the attributes for an Weibull
    distribution.  The attributes of an Weibull Results page are:

    :ivar _model: the Survival :py:class:`rtk.survival.Survival.Model`
                  whose attributes are being displayed.

    :ivar gtk.Label lblFailureIntensity:
    :ivar gtk.Label lblModel:
    :ivar gtk.Entry txtNumSuspensions:
    :ivar gtk.Entry txtNumFailures:
    :ivar gtk.Entry txtMTBFLL:
    :ivar gtk.Entry txtMTBF:
    :ivar gtk.Entry txtMTBFUL:
    :ivar gtk.Entry txtHazardRateLL:
    :ivar gtk.Entry txtHazardRate:
    :ivar gtk.Entry txtHazardRateUL:
    :ivar gtk.Entry txtEtaLL:
    :ivar gtk.Entry txtEta:
    :ivar gtk.Entry txtEtaUL:
    :ivar gtk.Entry txtBetaLL:
    :ivar gtk.Entry txtBeta:
    :ivar gtk.Entry txtBetaUL:
    :ivar gtk.Entry txtEtaBeta:
    :ivar gtk.Entry txtEtaEta:
    :ivar gtk.Entry txtEtaBeta:
    :ivar gtk.Entry txtBetaEta:
    :ivar gtk.Entry txtBetaBeta:
    :ivar gtk.Entry txtAIC:
    :ivar gtk.Entry txtBIC:
    :ivar gtk.Entry txtMLE:
    :ivar gtk.Entry txtRho:
    """

    def __init__(self):
        """
        Initializes the Results page for the Weibull distribution.
        """

        gtk.HPaned.__init__(self)

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._model = None

        # Initialize public dict attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.lblPage = gtk.Label()
        self.lblFailureIntensity = Widgets.make_label("", height=-1, width=-1)
        self.lblModel = Widgets.make_label("", width=350)

        self.txtNumSuspensions = Widgets.make_entry(width=50, editable=False)
        self.txtNumFailures = Widgets.make_entry(width=50, editable=False)
        self.txtMTBFLL = Widgets.make_entry(width=100, editable=False)
        self.txtMTBF = Widgets.make_entry(width=100, editable=False)
        self.txtMTBFUL = Widgets.make_entry(width=100, editable=False)
        self.txtHazardRateLL = Widgets.make_entry(width=100, editable=False)
        self.txtHazardRate = Widgets.make_entry(width=100, editable=False)
        self.txtHazardRateUL = Widgets.make_entry(width=100, editable=False)
        self.txtEtaLL = Widgets.make_entry(width=100, editable=False)
        self.txtEta = Widgets.make_entry(width=100, editable=False)
        self.txtEtaUL = Widgets.make_entry(width=100, editable=False)
        self.txtBetaLL = Widgets.make_entry(width=100, editable=False)
        self.txtBeta = Widgets.make_entry(width=100, editable=False)
        self.txtBetaUL = Widgets.make_entry(width=100, editable=False)
        self.txtEtaEta = Widgets.make_entry(width=100, editable=False)
        self.txtEtaBeta = Widgets.make_entry(width=100, editable=False)
        self.txtBetaEta = Widgets.make_entry(width=100, editable=False)
        self.txtBetaBeta = Widgets.make_entry(width=100, editable=False)
        self.txtAIC = Widgets.make_entry(width=100, editable=False)
        self.txtBIC = Widgets.make_entry(width=100, editable=False)
        self.txtMLE = Widgets.make_entry(width=100, editable=False)
        self.txtRho = Widgets.make_entry(width=100, editable=False)

        self.tvwReliability = gtk.TreeView()

        # Create gtk.Widget() tooltips.
        self.txtNumSuspensions.set_tooltip_markup(_(u"Displays the number of "
                                                    u"suspensions in the "
                                                    u"dataset."))
        self.txtNumFailures.set_tooltip_markup(_(u"Displays the number of "
                                                 u"failures in the dataset."))
        self.txtMTBFLL.set_tooltip_markup(_(u"Displays the lower "
                                            u"<span>\u03B1</span>% bound "
                                            u"on the MTBF."))
        self.txtMTBF.set_tooltip_markup(_(u"Displays the point estimate "
                                          u"of the MTBF."))
        self.txtMTBFUL.set_tooltip_markup(_(u"Displays the upper "
                                            u"<span>\u03B1</span>% bound "
                                            u"on the MTBF."))
        self.txtHazardRateLL.set_tooltip_markup(_(u"Displays the lower "
                                                  u"<span>\u03B1</span>% "
                                                  u"bound on the hazard "
                                                  u"rate."))
        self.txtHazardRate.set_tooltip_markup(_(u"Displays the point "
                                                u"estimate of the hazard "
                                                u"rate."))
        self.txtHazardRateUL.set_tooltip_markup(_(u"Displays the upper "
                                                  u"<span>\u03B1</span>% "
                                                  u"bound on the hazard "
                                                  u"rate."))
        self.txtEtaLL.set_tooltip_markup(_(u"Displays the lower "
                                           u"<span>\u03B1</span>% bound on "
                                           u"the scale parameter."))
        self.txtEta.set_tooltip_markup(_(u"Displays the point estimate of the "
                                         u"scale parameter."))
        self.txtEtaUL.set_tooltip_markup(_(u"Displays the upper "
                                           u"<span>\u03B1</span>% bound on "
                                           u"the scale parameter."))
        self.txtBetaLL.set_tooltip_markup(_(u"Displays the lower "
                                            u"<span>\u03B1</span>% bound on "
                                            u"the shape parameter."))
        self.txtBeta.set_tooltip_markup(_(u"Displays the point estimate of "
                                          u"the shape parameter."))
        self.txtBetaUL.set_tooltip_markup(_(u"Displays the upper "
                                            u"<span>\u03B1</span>% bound on "
                                            u"the shape parameter."))
        self.txtEtaEta.set_tooltip_markup(_(u"Displays the variance of the "
                                            u"scale parameter."))
        self.txtEtaBeta.set_tooltip_markup(_(u"Displays the covariance of "
                                             u"the scale and shape "
                                             u"parameters."))
        self.txtBetaEta.set_tooltip_markup(_(u"Displays the covariance of the "
                                             u"shape and scale parameters."))
        self.txtBetaBeta.set_tooltip_markup(_(u"Displays the variance of the "
                                              u"shape parameter."))
        self.txtAIC.set_tooltip_markup(_(u"Displays the value of Aikike's "
                                         u"information criterion."))
        self.txtBIC.set_tooltip_markup(_(u"Displays the value of Bayes' "
                                         u"information criterion."))
        self.txtMLE.set_tooltip_markup(_(u"Displays the likelihood "
                                         u"value."))
        self.txtRho.set_tooltip_markup(_(u"Displays the correlation "
                                         u"coefficient."))

    def create_results_page(self):
        """
        Method to create the page for displaying numerical results of the
        analysis for the Weibull distribution.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _vpaned = gtk.VPaned()

        _frame = Widgets.make_frame(label=_(u"Summary of Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        _fxdSummary = gtk.Fixed()
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdSummary)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, True, True)

        _frame = Widgets.make_frame(label=_(u"Parameter Estimates"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        _fxdEstimates = gtk.Fixed()
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdEstimates)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, True, False)

        _frame = Widgets.make_frame(label=_(u"Reliability Table"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwReliability)
        _frame.add(_scrollwindow)

        self.pack1(_vpaned, True, True)
        self.pack2(_frame, True, False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display analysis results.           #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the summary of results widgets.
        _labels = [_(u"Number of Suspensions:"), _(u"Number of Failures:")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fxdSummary, 5, 5)
        _x_pos += 35

        _fxdSummary.put(self.txtNumSuspensions, _x_pos, _y_pos[0])
        _fxdSummary.put(self.txtNumFailures, _x_pos, _y_pos[1])

        _label = Widgets.make_label(_(u"LCL"), width=-1,
                                    justify=gtk.JUSTIFY_CENTER)
        _fxdSummary.put(_label, _x_pos + 35, _y_pos[1] + 35)
        _label = Widgets.make_label(_(u"Point\nEstimate"), height=-1,
                                    width=-1, justify=gtk.JUSTIFY_CENTER)
        _fxdSummary.put(_label, _x_pos + 125, _y_pos[1] + 35)
        _label = Widgets.make_label(_(u"UCL"), width=-1,
                                    justify=gtk.JUSTIFY_CENTER)
        _fxdSummary.put(_label, _x_pos + 240, _y_pos[1] + 35)

        _label = Widgets.make_label(_(u"MTBF:"))
        _fxdSummary.put(_label, 5, _y_pos[1] + 70)
        _fxdSummary.put(self.txtMTBFLL, _x_pos, _y_pos[1] + 70)
        _fxdSummary.put(self.txtMTBF, _x_pos + 105, _y_pos[1] + 70)
        _fxdSummary.put(self.txtMTBFUL, _x_pos + 210, _y_pos[1] + 70)
        _fxdSummary.put(self.lblModel, _x_pos + 315, _y_pos[1] + 70)

        _fxdSummary.put(self.lblFailureIntensity, 5, _y_pos[1] + 100)
        _fxdSummary.put(self.txtHazardRateLL, _x_pos, _y_pos[1] + 100)
        _fxdSummary.put(self.txtHazardRate, _x_pos + 105, _y_pos[1] + 100)
        _fxdSummary.put(self.txtHazardRateUL, _x_pos + 210, _y_pos[1] + 100)

        # Place the parameter estimates widgets.
        _labels = [_(u"Scale Parameter (<span>\u03B7</span>):"),
                   _(u"Shape Parameter (<span>\u03B2</span>):")]
        (__, _y_pos) = Widgets.make_labels(_labels, _fxdEstimates, 5, 45)

        _label = Widgets.make_label(_(u"LCL"), width=-1,
                                    justify=gtk.JUSTIFY_CENTER)
        _fxdEstimates.put(_label, _x_pos + 35, 5)
        _label = Widgets.make_label(_(u"Point\nEstimate"), height=-1,
                                    width=-1, justify=gtk.JUSTIFY_CENTER)
        _fxdEstimates.put(_label, _x_pos + 125, 5)
        _label = Widgets.make_label(_(u"UCL"), width=-1,
                                    justify=gtk.JUSTIFY_CENTER)
        _fxdEstimates.put(_label, _x_pos + 240, 5)

        _fxdEstimates.put(self.txtEtaLL, _x_pos, _y_pos[0])
        _fxdEstimates.put(self.txtEta, _x_pos + 105, _y_pos[0])
        _fxdEstimates.put(self.txtEtaUL, _x_pos + 210, _y_pos[0])

        _fxdEstimates.put(self.txtBetaLL, _x_pos, _y_pos[1])
        _fxdEstimates.put(self.txtBeta, _x_pos + 105, _y_pos[1])
        _fxdEstimates.put(self.txtBetaUL, _x_pos + 210, _y_pos[1])

        # Place the variance-covariance matrix.
        _label = Widgets.make_label(_(u"<u>Variance-Covariance Matrix</u>"),
                                    width=-1)
        _fxdEstimates.put(_label, 5, _y_pos[1] + 60)

        # Column labels.
        _label = Widgets.make_label(_(u"<span>\u03B7</span>"), width=100,
                                    justify=gtk.JUSTIFY_CENTER)
        _fxdEstimates.put(_label, 25, _y_pos[1] + 90)
        _label = Widgets.make_label(_(u"<span>\u03B2</span>"), width=100,
                                    justify=gtk.JUSTIFY_CENTER)
        _fxdEstimates.put(_label, 130, _y_pos[1] + 90)

        # Row labels.
        _label = Widgets.make_label(_(u"<span>\u03B7</span>"), width=10,
                                    justify=gtk.JUSTIFY_RIGHT)
        _fxdEstimates.put(_label, 5, _y_pos[1] + 120)
        _label = Widgets.make_label(_(u"<span>\u03B2</span>"), width=10,
                                    justify=gtk.JUSTIFY_RIGHT)
        _fxdEstimates.put(_label, 5, _y_pos[1] + 150)

        _fxdEstimates.put(self.txtEtaEta, 25, _y_pos[1] + 120)
        _fxdEstimates.put(self.txtEtaBeta, 130, _y_pos[1] + 120)
        _fxdEstimates.put(self.txtBetaEta, 25, _y_pos[1] + 150)
        _fxdEstimates.put(self.txtBetaBeta, 130, _y_pos[1] + 150)

        # Place the parametric goodness of fit statistics.
        _label = Widgets.make_label(_(u"<u>Goodness of Fit Statistics</u>"),
                                    width=-1)
        _fxdEstimates.put(_label, _x_pos + 210, _y_pos[1] + 60)
        _label = Widgets.make_label(_(u"Maximum Likelihood:"))
        _fxdEstimates.put(_label, _x_pos + 210, _y_pos[1] + 90)
        _label = Widgets.make_label(_(u"Aikake's Information:"))
        _fxdEstimates.put(_label, _x_pos + 210, _y_pos[1] + 120)
        _label = Widgets.make_label(_(u"Bayes Information:"))
        _fxdEstimates.put(_label, _x_pos + 210, _y_pos[1] + 150)
        _label = Widgets.make_label(_(u"Correlation Coefficient:"))
        _fxdEstimates.put(_label, _x_pos + 210, _y_pos[1] + 180)
        _fxdEstimates.put(self.txtMLE, _x_pos + 410, _y_pos[1] + 90)
        _fxdEstimates.put(self.txtAIC, _x_pos + 410, _y_pos[1] + 120)
        _fxdEstimates.put(self.txtBIC, _x_pos + 410, _y_pos[1] + 150)
        _fxdEstimates.put(self.txtRho, _x_pos + 410, _y_pos[1] + 180)

        # Place the reliability table.
        _model = gtk.ListStore(gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
        self.tvwReliability.set_model(_model)
        _headings = [_(u"Time\n(t)"), _(u"R(t)\nLower\nLimit"),
                     _(u"R(t)\nPoint\nEstimate"), _(u"R(t)\nUpper\nLimit")]
        for _index, _heading in enumerate(_headings):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _column = gtk.TreeViewColumn()
            _label = Widgets.make_column_heading(_heading)
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index)
            _column.set_clickable(True)
            _column.set_resizable(True)
            _column.set_sort_column_id(_index)
            self.tvwReliability.append_column(_column)

        # Insert the tab.
        self.lblPage.set_markup("<span weight='bold'>" +
                                _(u"Weibull\nResults") + "</span>")
        self.lblPage.set_alignment(xalign=0.5, yalign=0.5)
        self.lblPage.set_justify(gtk.JUSTIFY_CENTER)
        self.lblPage.show_all()
        self.lblPage.set_tooltip_text(_(u"Displays Weibull distribution "
                                        u"analysis results for the selected "
                                        u"dataset."))

        return False

    def load_results_page(self, model):
        """
        Method to load the gtk.Widgets() necessary for displaying the results
        of fitting a dataset to the Weibull distribution.

        :param model: the :py:class:`rtk.survival.Survival` data model to
                      display the results for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        self._model = model

        # Load the summary information.
        self.txtNumSuspensions.set_text(str(self._model.n_suspensions))
        self.txtNumFailures.set_text(str(self._model.n_failures))

        # Load the MTBF and hazard rate results.  Use the values from the last
        # record in the Survival data model mtbf and hazard rate dictionaries.
        try:
            _key = max(self._model.dicMTBF.iterkeys())
        except ValueError:
            _key = None
        if _key is not None:
            self.txtMTBFLL.set_text(str(fmt.format(self._model.dicMTBF[_key][0])))
            self.txtMTBF.set_text(str(fmt.format(self._model.dicMTBF[_key][1])))
            self.txtMTBFUL.set_text(str(fmt.format(self._model.dicMTBF[_key][2])))

        try:
            _key = max(self._model.dicHazard.iterkeys())
        except ValueError:
            _key = None
        if _key is not None:
            self.txtHazardRateLL.set_text(
                str(fmt.format(self._model.dicHazard[_key][2])))
            self.txtHazardRate.set_text(
                str(fmt.format(self._model.dicHazard[_key][1])))
            self.txtHazardRateUL.set_text(
                str(fmt.format(self._model.dicHazard[_key][0])))

        # Load the parameter estimates.
        self.lblFailureIntensity.set_text(_(u"Failure Intensity\n"
                                            u"at t={0:0.2f}:").format(
                                                self._model.rel_time))
        self.txtEtaLL.set_text(str(fmt.format(self._model.scale[0])))
        self.txtEta.set_text(str(fmt.format(self._model.scale[1])))
        self.txtEtaUL.set_text(str(fmt.format(self._model.scale[2])))
        self.txtBetaLL.set_text(str(fmt.format(self._model.shape[0])))
        self.txtBeta.set_text(str(fmt.format(self._model.shape[1])))
        self.txtBetaUL.set_text(str(fmt.format(self._model.shape[2])))

        # Display the model with the point estimates of the parameters.
        _model = _(u"<span>R(t) = exp(-(t / "
                   u"{0:0.4f})<sup>{1:0.4f}</sup>)"
                   u"</span>".format(self._model.scale[1],
                                     self._model.shape[1]))
        self.lblModel.set_markup(_model)

        # Load the variance-covariance matrix.
        # Scale variance.
        self.txtEtaEta.set_text(str(fmt.format(
            self._model.variance[0])))
        # Shape variance.
        self.txtBetaBeta.set_text(str(fmt.format(self._model.variance[1])))
        # Scale-shape covariance.
        self.txtEtaBeta.set_text(
            str(fmt.format(self._model.covariance[0])))
        # Shape-scale covariance.
        self.txtBetaEta.set_text(
            str(fmt.format(self._model.covariance[0])))

        # Load the GoF statistics.
        self.txtAIC.set_text(str(fmt.format(self._model.aic)))
        self.txtBIC.set_text(str(fmt.format(self._model.bic)))
        self.txtMLE.set_text(str(fmt.format(self._model.mle)))
        self.txtRho.set_text(str(fmt.format(self._model.rho**2.0)))

        # Load the reliability table.
        _model = self.tvwReliability.get_model()
        _model.clear()
        for _key in self._model.dicReliability.keys():
            _model.append([_key, self._model.dicReliability[_key][0],
                           self._model.dicReliability[_key][1],
                           self._model.dicReliability[_key][2]])

        return False


class Plots(gtk.HBox):                      # pylint: disable=R0902, R0904
    """
    The Work Book page to display plots for an Weibull distribution.  The
    attributes of an Weibull Plot page are:

    :ivar _model: the :py:class:`rtk.survival.Survival` data model whose
                  results are being displayed.
    :ivar matplotlib.backends.backend_gtkagg.FigureCanvasGTK pltPlot1: the plot
        in the upper left corner.
    :ivar matplotlib.axes.Axes axAxis1: the Axes in the upper left corner plot.
    :ivar matplotlib.backends.backend_gtkagg.FigureCanvasGTK pltPlot2: the plot
        in the lower left corner.
    :ivar matplotlib.axes.Axes axAxis2: the Axes in the lower left corner plot.
    :ivar matplotlib.backends.backend_gtkagg.FigureCanvasGTK pltPlot3: the plot
        in the upper right corner.
    :ivar matplotlib.axes.Axes axAxis3: the Axes in the upper right corner
                                        plot.
    :ivar matplotlib.backends.backend_gtkagg.FigureCanvasGTK pltPlot4: the plot
        in the lower right corner.
    :ivar matplotlib.axes.Axes axAxis4: the Axes in the lower right corner
                                        plot.
    """

    def __init__(self):
        """
        Initializes the Plot page for the Weibull distribution.
        """

        gtk.HBox.__init__(self)

        # Initialize private dict attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._model = None

        # Initialize public dict attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.lblPage = gtk.Label()

        _height = 100
        _width = 200
        _figure = Figure(figsize=(_width, _height))
        self.pltPlot1 = FigureCanvas(_figure)
        self.axAxis1 = _figure.add_subplot(111)
        _figure = Figure(figsize=(_width, _height))
        self.pltPlot2 = FigureCanvas(_figure)
        self.axAxis2 = _figure.add_subplot(111)
        _figure = Figure(figsize=(_width, _height))
        self.pltPlot3 = FigureCanvas(_figure)
        self.axAxis3 = _figure.add_subplot(111)
        _figure = Figure(figsize=(_width, _height))
        self.pltPlot4 = FigureCanvas(_figure)
        self.axAxis4 = _figure.add_subplot(111)

    def create_plot_page(self):
        """
        Method to create the page for displaying plots for the Weibull
        distribution.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _vbox = gtk.VBox()
        self.pack_start(_vbox, True, True)

        _frame = Widgets.make_frame(_(u"Histogram"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot1)
        _vbox.pack_start(_frame, True, True)

        _frame = Widgets.make_frame(_(u"Empirical CDF Plot"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot2)
        _vbox.pack_start(_frame, True, True)

        _vbox = gtk.VBox()
        self.pack_end(_vbox, True, True)

        _frame = Widgets.make_frame(_(u"Probability Plot"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot3)
        _vbox.pack_start(_frame, True, True)

        _frame = Widgets.make_frame(_(u"Reliability Plot"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot4)
        _vbox.pack_start(_frame, True, True)

        # Connect widgets to callback functions.
        self.pltPlot1.mpl_connect('button_press_event', Widgets.expand_plot)
        self.pltPlot2.mpl_connect('button_press_event', Widgets.expand_plot)
        self.pltPlot3.mpl_connect('button_press_event', Widgets.expand_plot)
        self.pltPlot4.mpl_connect('button_press_event', Widgets.expand_plot)

        # Insert the page.
        self.lblPage.set_markup("<span weight='bold'>Analysis\nPlots</span>")
        self.lblPage.set_alignment(xalign=0.5, yalign=0.5)
        self.lblPage.set_justify(gtk.JUSTIFY_CENTER)
        self.lblPage.show_all()
        self.lblPage.set_tooltip_text(_(u"Displays survival analyses plots."))

        return False

    def load_plots(self, model):
        """
        Method to load the plots for the Weibull distribution.

        :param model: the :py:class:`rtk.survival.Survival` data model to
                      display the plots for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._model = model

        _times = []
        for _record in self._model.dicRecords.values():
            if _record.status != 2 and _record.status != 'Right Censored':
                for __ in range(_record.n_failures):
                    _times.append(_record.right_interval)
        _times.sort()

        if len(_times) > 0:
            _theoretical = self._model.theoretical_distribution(_times)

            self._load_histogram(_times)
            self._load_ecdf(_times, _theoretical)
            self._load_probability_plot(_times)
            self._load_reliability_plot()

        return False

    def _load_histogram(self, times):
        """
        Method to load plot 1 with a histogram of failure times.

        :param list times: list of all failures times.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis1.cla()

        _q1 = int(ceil(0.25 * len(times)))
        _q3 = int(ceil(0.75 * len(times)))
        _iqr = times[_q3] - times[_q1]
        _h = 2.0 * _iqr / len(times)**(1.0 / 3.0)
        _k = int(ceil((max(times) - min(times)) / _h))
        if _k < 5:
            _k = int(ceil(sqrt(len(times))))

        _max = max(times) + (0.5 * (max(times) - min(times)) / (_k - 1))
        _hist, _bin_edges = np.histogram(times, _k, (0.0, _max))

        _title = _(u"Histogram of Failure Times "
                   u"for {0:s}").format(self._model.description)
        Widgets.load_plot(self.axAxis1, self.pltPlot1, times, y1=_bin_edges,
                          title=_title, xlab=_(u"Failure Times"),
                          ylab=_(u"Count of Failures"),
                          ltype=[3], marker=['g'])

        return False

    def _load_ecdf(self, times, theoretical):
        """
        Method to load plot 2 with an Empirical Cumulative Distribution
        Function (ECDF).

        :param list times: list of all failures times.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis2.cla()

        _ecdf = ECDF(times)

        _title = _(u"Weibull Empirical CDF of Failure Times "
                   u"for {0:s}").format(self._model.description)
        Widgets.load_plot(self.axAxis2, self.pltPlot2, _ecdf.x[1:],
                          y1=_ecdf.y[1:], y2=theoretical, title=_title,
                          xlab=_(u"t"), ylab=_(u"F(t) "), ltype=[1, 2],
                          marker=['b-', 'r:'])

        return False

    def _load_probability_plot(self, times):
        """
        Method to load plot 3 with a probability plot.

        :param list times: list of all failures times.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis3.cla()

        probplot(times, sparams=(self._model.scale[1], self._model.shape[1]),
                 dist='lognorm', plot=self.axAxis3)

        _title = _(u"Weibull Probability Plot of Failure Times "
                   u"for {0:s}").format(self._model.description)
        self.axAxis3.set_title(_title, {'fontsize': 16, 'fontweight': 'bold',
                                        'verticalalignment': 'baseline',
                                        'horizontalalignment': 'center'})
        self.axAxis3.set_xlabel(_(u"Quantile"))
        self.axAxis3.set_ylabel(_(u"Observed"))

        return False

    def _load_reliability_plot(self):
        """
        Method to load plot 4 with a plot of the reliability function given
        the estimated parameters.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.axAxis4.cla()

        _times = sorted(self._model.dicReliability.keys(), reverse=True)
        _r_ll = sorted([x[0] for x in self._model.dicReliability.values()])
        _r = sorted([x[1] for x in self._model.dicReliability.values()])
        _r_ul = sorted([x[2] for x in self._model.dicReliability.values()])

        _title = _(u"Estimated Reliability Function "
                   u"for {0:s} with "
                   u"{1:0.1f}% Bounds").format(self._model.description,
                                               self._model.confidence * 100.0)
        if _times:
            Widgets.load_plot(self.axAxis4, self.pltPlot4, _times, y1=_r_ll,
                              y2=_r, y3=_r_ul, title=_title, xlab=_(u"t"),
                              ylab=_(u"R(t) "), ltype=[2, 2, 2],
                              marker=['r:', 'g-', 'b:'])

        return False
