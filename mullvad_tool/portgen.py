import os
from json import dump, load

import click


def ensure_dir(path):
    """Creates the specified directory if it doesn't already exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def init_portgen(starting_port, run_name, state_file):
    ensure_dir(click.get_app_dir("mullvad"))
    with open(state_file, "w") as f:
        dump({run_name: starting_port}, f)
    return "Ready to generate ports with portgen run"


def run_portgen(run_name, state_file):
    with open(state_file, "r") as f:
        data = load(f)
    port = data[run_name]
    next_port = port + 1
    with open(state_file, "w") as f:
        dump({run_name: next_port}, f)
    return port
