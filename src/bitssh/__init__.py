from ._version import __version__

try:
    from importlib.metadata import version

    __version__ = version("bitssh")
except Exception:  # pragma: no cover
    pass
