import os
import types
from copy import deepcopy
from pathlib import Path

import yesqa_setup

PY_WPS_WPS_ = types.MappingProxyType(
    {
        "**/__init__.py": {"D400", "D205", "D104"},
        "**/test_*.py": {
            "D403",
            "WPS431",
            "WPS237",
            "WPS515",
            "WPS221",
            "WPS210",
            "D210",
            "WPS317",
            "WPS433",
            "WPS440",
            "WPS326",
            "WPS437",
            "D400",
            "WPS226",
            "WPS204",
            "WPS110",
            "WPS342",
            "WPS352",
            "S101",
            "WPS211",
            "WPS115",
            "D103",
            "WPS235",
            "N802",
            "WPS218",
            "WPS432",
            "B904",
            "WPS441",
            "WPS602",
            "WPS421",
            "WPS318",
            "WPS213",
            "D102",
            "WPS323",
            "WPS202",
            "WPS319",
            "WPS201",
            "WPS118",
        },
    },
)


FAKE_FLAKE8_RESULTS = {
    "D403",
    "WPS431",
    "WPS237",
    "WPS515",
    "WPS221",
    "WPS210",
    "D210",
    "WPS317",
    "WPS433",
    "WPS440",
    "WPS326",
    "WPS437",
    "D400",
    "WPS226",
    "WPS204",
    "WPS110",
    "WPS342",
    "B904",
    "WPS441",
    "WPS602",
    "WPS421",
    "WPS318",
    "WPS213",
    "D102",
    "WPS323",
    "WPS202",
    "WPS319",
    "WPS201",
    "WPS118",
}


def test_read_per_file():
    test_result = yesqa_setup.get_rules("setup.cfg")

    assert test_result == PY_WPS_WPS_


def test_create_tmp_configfile_no_ignores():

    test_result = yesqa_setup.create_tmp_configfile_no_ignores("setup.cfg")

    assert Path(test_result).exists()

    os.remove(test_result)


def test_print_removals(capsys):
    flake8_input = deepcopy(dict(PY_WPS_WPS_))
    flake8_input["**/test_*.py"] = FAKE_FLAKE8_RESULTS
    yesqa_setup._print_removals(
        flake8_input,
        dict(PY_WPS_WPS_),
    )

    test_result = capsys.readouterr().out
    assert test_result == (
        "**/test_*.py:['D103', 'N802', 'S101', 'WPS115', 'WPS211', 'WPS218', "
        "'WPS235', 'WPS352', 'WPS432']\n"
    )


def test_print_removals_equal(capsys):
    yesqa_setup._print_removals(
        dict(PY_WPS_WPS_),
        dict(PY_WPS_WPS_),
    )

    test_result = capsys.readouterr().out
    assert test_result == ""
