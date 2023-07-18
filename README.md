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

- Add a Bitcoin wallet address.
- Remove a Bitcoin wallet address.
- Get Bitcoin wallet address balance details.
- Get transactions of a Bitcoin wallet address.

## Requirements

- Python 3.8+
- Cassandra 4+

## Installation

### Setting up dependencies
- Clone the repository from github
- cd into the project directory.

Install Poetry (dependency manager)
```console
$ pip3 install poetry
```

Install all dependencies
```console
$ poetry install
```

### Cassandra
-Get the latest Cassandra docker image.
```console
$ docker pull cassandra
```

-Start Cassandra container
```console
$ docker run -p 9042:9042 -d cassandra:latest
```

- Open up a CQL shell
```console
$ docker exec -it <container_id> cqlsh
```

- Create a keyspace (database)
```console
$ CREATE KEYSPACE IF NOT EXISTS cointracker WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
```

- Create a test user
```console
$ INSERT INTO cointracker.user(id, first_name, last_name, email_id, created_at, updated_at,bucket_id) VALUES (uuid(), 'John', 'Doe', 'john.doe@example.com', toTimeStamp(now()), toTimeStamp(now()), 1);
```

## Usage

Start the back-end server
```console
poetry run uvicorn cointracker.app:app
```

From another console, send API requests

- Add a wallet address
```console
$ curl -v -X POST "http://localhost:8000/v1/users/john.doe@example.com/wallets/btc/<address>"
```

- Remove a wallet address
```console
$ curl -v -X DELETE "http://localhost:8000/v1/users/john.doe@example.com/wallets/btc/<address>"
```

- Get wallet details
```console
$ curl -v http://localhost:8000/v1/users/john.doe@example.com/wallets/btc/<address>
```

- Get transactions
```console
$ curl -v "http://localhost:8000/v1/wallets/btc/<address>/transactions?limit=200&token=<token>"
```
Initially token can be absent. In subsequent requests, use the token returned in the response headers(X-Token).

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
