# kgr

KanGaRoo is an IaC DSL: declarative, agnostic, logical and distributed.

## Installation

with pip:

    pip install kangaroo

with poetry:

    poetry add git+https://orbital-state/kgr.git

## Publish

    poetry publish --build


## License

Licensed under Apache License Version 2.0. See LICENSE for details.


## Developer

### Running yep

As developer you can run yep locally with poetry:

    poetry run kgr --help

But you also have an option to fallback to `pip install --editable .` to simplify local development process.

### Versioning

We adopt [semantic versioning style](https://semver.org/).

Releases are versioned via git tags. We use [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning) to automate this.

This lets us generate the version from your VCS tags (or other configuration). Info is pulled from git tags that were done with commands like `git tag v0.1.0 -m "New release"`.  The tool is installed via `poetry self add poetry-dynamic-versioning`.
