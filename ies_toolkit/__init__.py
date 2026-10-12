"""Telicent IES Toolkit."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("telicent-ies-toolkit")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"
