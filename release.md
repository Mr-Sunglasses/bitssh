## bitssh v3.6.0 Release Notes

### New Feature: `bitssh add`

A new `add` subcommand to add SSH hosts directly from the command line -- no need to manually edit `~/.ssh/config` anymore.

#### Interactive Mode

```bash
bitssh add
```

Launches a step-by-step guided prompt asking for:
- **Host** -- alias for the connection (e.g. `myserver`)
- **HostName** -- IP address or domain (e.g. `192.168.1.1`)
- **User** -- login username (optional)
- **Port** -- defaults to 22 (optional)
- **IdentityFile** -- path to private key (optional)

Includes input validation, a summary preview, and a confirmation step before writing.

#### Non-Interactive Mode

```bash
bitssh add --host myserver --hostname 192.168.1.1
bitssh add --host myserver --hostname 192.168.1.1 --user root --port 2222
bitssh add --host myserver --hostname 192.168.1.1 --identity-file ~/.ssh/id_ed25519
```

Add hosts directly via CLI flags -- perfect for scripting and automation. Requires at minimum `--host` and `--hostname`.

### Improvements

- **Duplicate host detection** -- prevents accidentally overwriting existing entries in the SSH config
- **Auto-creation of config** -- if `~/.ssh/` or `~/.ssh/config` doesn't exist, `bitssh add` creates them automatically with correct permissions (`0700` for directory, `0644` for file)
- **Better error messaging** -- when no config file exists, the error now guides users to run `bitssh add` to get started

### Full Changelog

**Files changed:** `argument_parser.py`, `cli.py`, `prompt.py`, `utils.py`, `__init__.py`, `pyproject.toml`
