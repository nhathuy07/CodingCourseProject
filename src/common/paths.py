import pathlib

import sys
import os

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath("."))


DATA_PATH = pathlib.Path(f"{bundle_dir}/data")
ASSETS_PATH = pathlib.Path(f"{bundle_dir}/assets")
