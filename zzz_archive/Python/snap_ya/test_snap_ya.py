#!/usr/bin/python3
## Tests snap_ya.py

import subprocess

import hypothesis
import pytest
import snap_ya


def test_package_list():
    package_list = subprocess.check_output(["trizen", "-Q"])
    package_number = package_list.count(b"\n")
    assert len(snap_ya.get_installed_packages()) == package_number
