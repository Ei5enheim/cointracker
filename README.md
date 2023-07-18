# Cointracker

[![Status](https://img.shields.io/pypi/status/cointracker.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/cointracker)][python version]
[![License](https://img.shields.io/pypi/l/cointracker)][license]

[![Read the documentation at https://cointracker.readthedocs.io/](https://img.shields.io/readthedocs/cointracker/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/Ei5enheim/cointracker/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/Ei5enheim/cointracker/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/cointracker/
[status]: https://pypi.org/project/cointracker/
[python version]: https://pypi.org/project/cointracker
[read the docs]: https://cointracker.readthedocs.io/
[tests]: https://github.com/Ei5enheim/cointracker/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/Ei5enheim/cointracker
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

-

## Requirements

- Python 3.8+
- Cassandra 4+

## Installation

### Setting up dependencies
- Clone the repository from github
- cd into the project directory.
```console
$ pip3 install poetry
```

```console
$ poetry install
```
### Cassandra
```console
$ docker pull cassandra
```

```console
$ docker run -p 9042:9042 -d cassandra:latest
```

```console
$ docker exec -it <container_id> cqlsh
```

```console
$ CREATE KEYSPACE IF NOT EXISTS cointracker WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
```

```console
$ INSERT INTO cointracker.user(id, first_name, last_name, email_id, created_at, updated_at,bucket_id) VALUES (uuid(), 'John', 'Doe', 'john.doe@example.com', toTimeStamp(now()), toTimeStamp(now()), 1);
```

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Cointracker_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/Ei5enheim/cointracker/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/Ei5enheim/cointracker/blob/main/LICENSE
[contributor guide]: https://github.com/Ei5enheim/cointracker/blob/main/CONTRIBUTING.md
[command-line reference]: https://cointracker.readthedocs.io/en/latest/usage.html
