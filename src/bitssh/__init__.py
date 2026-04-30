try:
    from importlib.metadata import version

    __version__ = version("bitssh")
except Exception:  # pragma: no cover
    __version__ = "0.0.0"
