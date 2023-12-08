from importlib import resources
try:
    import tomllib
except ModuleNotFoundError:
    # Third party imports
    import tomli as tomllib


__version__ = "2.5.0"
