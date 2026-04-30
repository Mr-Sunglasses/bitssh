## Description

Briefly describe what this PR does and why.

Fixes #(issue)

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Refactor (code restructuring without changing behavior)
- [ ] Documentation update
- [ ] CI/Build improvement

## Affected Area

- [ ] TUI (Terminal User Interface)
- [ ] SSH Connection Handling
- [ ] SSH Config Parsing
- [ ] CLI Arguments / Options
- [ ] Installation / Packaging
- [ ] Tests
- [ ] Documentation

## Testing

Describe how you tested your changes.

- [ ] I tested manually by running `bitssh` and connecting to a host
- [ ] I ran the existing test suite (`pytest`)
- [ ] I added new tests for my changes

**Python version tested**: 
**OS tested on**: 

## SSH Config Tested (if applicable)

If your change affects SSH config parsing or connection behavior, please describe the config entries used for testing (redact sensitive info):

```
Host example
    Hostname x.x.x.x
    User test
    Port 22
```

## Checklist

- [ ] My code follows the project's style guidelines (`ruff` and `black`)
- [ ] I have performed a self-review of my code
- [ ] My changes generate no new warnings
- [ ] I have updated the documentation if needed