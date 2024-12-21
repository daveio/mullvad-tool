import os
from typing import Final

import click

default_state_file: Final[str] = os.path.join(
    click.get_app_dir("mullvad-tool"), "state.json"
)
