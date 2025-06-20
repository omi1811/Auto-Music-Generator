"""
Base utility module for music and data processing.
Provides imports and environment checks for required packages.
"""

import collections
import datetime
import glob
import pathlib
from typing import Optional

from IPython import display
from matplotlib import pyplot as plt


def check_environment(packages=None):
    """Print versions of key packages to verify environment. If a package is missing, indicate so."""
    import sys
    print(f"Python: {sys.version}")
    default_packages = [
        ("numpy", "np"),
        ("pandas", "pd"),
        ("pretty_midi", None),
        ("seaborn", None),
        ("tensorflow", "tf"),
        ("fluidsynth", None)
    ]
    if packages is None:
        packages = default_packages
    for pkg, alias in packages:
        try:
            mod = __import__(pkg)
            version = getattr(mod, "__version__", "(no __version__)")
            print(f"{pkg}: {version}")
        except ImportError:
            print(f"{pkg}: NOT INSTALLED")
        except Exception as e:
            print(f"{pkg}: Error - {e}")


if __name__ == "__main__":
    check_environment()