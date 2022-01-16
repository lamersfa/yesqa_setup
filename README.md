yesqa_setup
===========

## Installation

`pip install yesqa_setup`


## As a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/falamers/yesqa
    rev: v0.0.1
    hooks:
    -   id: yesqa_setup
```
