# -*- coding: utf-8 -*-
# test_plant_methods.py
from datetime import datetime as dt

from spruce import Plant


def test_plant_has_a_default_name():
    assert isinstance(Plant().name, str)


def test_plant_status_last_water_defaults_to_none():
    assert Plant().status('water')['last'] is None


def test_plant_status_next_water_defaults_to_today():
    assert Plant().status('water')['next'].day == dt.date(dt.utcnow())


def test_plant_status_last_fertilize_defaults_to_none():
    assert Plant().status('fertilize')['last'] is None


def test_plant_status_next_fertilize_defaults_to_today():
    assert Plant().status('fertilize')['next'].day == dt.date(dt.utcnow())
