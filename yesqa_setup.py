"""Script to check the configfile if the "per-file-ignores" codes can be removed."""
import glob
import os
import subprocess
import sys
import tempfile
from configparser import ConfigParser
from typing import Dict
from typing import Set
from typing import Tuple


def _run_flake8(  # noqa: WPS210
    glob_value: str,
    temp_config_file: str,
) -> Set[str]:
    """
    Run flake8 and return the codes per file.

    Args:
        glob_value: To run flake8 on
        temp_config_file: The path of the temporary configfile without the per-file-ignores section.

    Returns:
        The codes that are found by flake8.
    """
    cmd = _create_command(glob_value, temp_config_file)
    out, _ = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()
    retv: Set[str] = set()
    for line in out.decode().splitlines():
        try:
            _, code = line.split("\t")
        except ValueError:
            continue
        else:
            retv.add(code)
    return retv


def _create_command(
    glob_value: str,
    temp_config_file: str,
) -> Tuple[str, ...]:
    cmd: Tuple[str, ...] = (
        sys.executable,
        "-mflake8",
        f"--config={temp_config_file}",
        "--format=%(row)d\t%(code)s",  # noqa: WPS323
    )
    for result_glob in glob.glob(glob_value):
        cmd = cmd + (result_glob,)
    return cmd


def get_rules(
    file_path: str,
) -> Dict[str, Set[str]]:
    """
    Read the config file and return the data per ignore.

    Args:
        file_path: The path of the configfile to read.

    Returns:
        A dataset with the rules glob and ignore codes.
    """
    parser = ConfigParser()
    parser.read(file_path)
    per_file_ignores_data = parser.get("flake8", "per-file-ignores").split("\n")
    rtnv: Dict[str, Set[str]] = {}
    for ignore in per_file_ignores_data:
        _fill_ignore_dataset(ignore, rtnv)
    return rtnv


def _fill_ignore_dataset(ignore: str, rtnv: Dict[str, Set[str]]) -> None:
    if ignore:
        glob_entry, flake_values = ignore.split(":")
        flake_splitted_values = {
            flake_value.strip() for flake_value in flake_values.split(",")
        }
        rtnv[glob_entry] = flake_splitted_values


def create_tmp_configfile_no_ignores(
    file_path: str,
) -> str:
    """
    Create a temporary config file without the per-file-ignores section.

    Args:
        file_path: The path of the configfile to check.

    Returns:
        The path of the temporary configfile without the per-file-ignores section.
    """
    fd, path = tempfile.mkstemp(
        dir=os.path.dirname(file_path),
        prefix=os.path.basename(file_path),
        suffix=".cfg",
    )
    parser = ConfigParser()
    parser.read(file_path)
    parser.set("flake8", "per-file-ignores", "")
    with open(fd, "w") as configfile:
        parser.write(configfile)
    return path


def loop_globs(
    rules: Dict[str, Set[str]],
    temp_config_file: str,
) -> Dict[str, Set[str]]:
    """
    Print the resuls when they are found.

    Args:
        rules: A dataset with the rules glob and ignore codes.
        temp_config_file: The path of the temporary configfile without the per-file-ignores section.

    Returns:
        The flakes values while running flake without ignores.
    """

    return {
        glob_value: _run_flake8(glob_value, temp_config_file)
        for glob_value in rules.keys()
    }


def _print_removals(
    flake8_results: Dict[str, Set[str]],
    rules: Dict[str, Set[str]],
) -> None:
    for glob_value in rules.keys():
        compare = rules[glob_value] - flake8_results[glob_value]
        if compare:
            print(f"{glob_value}:{sorted(compare)}")  # noqa: WPS421, WPS237


def main() -> int:
    """
    Run the main function to run full functionality.

    Returns:
        The return value
    """
    root_dir = os.path.abspath(os.curdir)
    config_file_path: str = os.path.join(root_dir, "setup.cfg")
    temp_config_file = create_tmp_configfile_no_ignores(config_file_path)

    rules = get_rules(config_file_path)
    flake_run_result = loop_globs(rules, temp_config_file)
    _print_removals(flake_run_result, rules)
    os.remove(temp_config_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
