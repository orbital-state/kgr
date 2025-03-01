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