# -*- coding: utf-8 -*-
# Copyright (c) Facebook, Inc. and its affiliates.

# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import absolute_import, division, print_function
import narwhals as nw
import datetime as dt

import numpy as np
import pandas as pd

import holidays


def get_country_holidays_class(country):
    """Get class for a supported country.

    Parameters
    ----------
    country: country code

    Returns
    -------
    A valid country holidays class
    """
    substitutions = {
        "TU": "TR",  # For compatibility with Turkey as 'TU' cases.
    }

    country = substitutions.get(country, country)
    if not hasattr(holidays, country):
        raise AttributeError(f"Holidays in {country} are not currently supported!")

    return getattr(holidays, country)


def get_holiday_names(country):
    """Return all possible holiday names of given country

    Parameters
    ----------
    country: country name

    Returns
    -------
    A set of all possible holiday names of given country
    """
    country_holidays = get_country_holidays_class(country)
    return set(country_holidays(language="en_US", years=np.arange(1995, 2045)).values())

def _convert_date_to_datetime(date: dt.date) -> dt.datetime:
    """Convert stlib date to stdlib datetime."""
    return dt.datetime(date.year, date.month, date.day)


def make_holidays_df(year_list, country, province=None, state=None):
    """Make dataframe of holidays for given years and countries

    Parameters
    ----------
    year_list: a list of years
    country: country name

    Returns
    -------
    Dataframe with 'ds' and 'holiday', which can directly feed
    to 'holidays' params in Prophet
    """
    country_holidays = get_country_holidays_class(country)
    holidays = country_holidays(expand=False, language="en_US", subdiv=province, years=year_list)

    ds_list: list[dt.datetime] = []
    holiday_list: list[str] = []
    for date in holidays:
        for holiday in holidays.get_list(date):
            ds_list.append(_convert_date_to_datetime(date))
            holiday_list.append(holiday)
    holidays_df = nw.from_dict({'ds': ds_list, 'holiday': holiday_list}, native_namespace=pd).to_native()
    return holidays_df
