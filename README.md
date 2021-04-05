# Versescanner

## Introduction

The Elisio project is an attempt to teach computers to scan Latin verses, and to share the results publicly with those who are interested.
Scanning a Latin verse means, in this technical context, to analyze its structural variation of light and heavy syllables.
While this is an ancient art, practiced by the Romans themselves and almost ever since, this kind of data is hard to digitalize manually.

With this scanning engine, we want to allow users to do batch scans of Latin verses,
in hopes that they can eventually retrieve previously unknown information from this heavily stylized use of the Latin language.

## Technology

The Elisio engine is built using the programming language Python.
For everything except database access, the implementation should be as framework-agnostic as possible.
For the database itself, and for everything related to the front-end (web service and default client web application), Django is used.
You will need a Django version that supports database migrations (1.7 and up).

The project naturally requires a database connection (see [the BUILDING file](./BUILDING.md));
there are no inherent restrictions on which database to use
except those introduced by Django itself - and the availability of database connectors in Python 3.

## License

Elisio is released under the Affero General Public License (AGPL), a strong copyleft license which still gives third parties
considerable freedom to use the source code contained in this project.
If you are considering forking Elisio or using some of its algorithms,
please check [the license terms](./LICENSE.md) to make yourself acquainted with your rights and obligations.

**Ignorance is not a valid excuse.**

## Code of Conduct

This project includes a [code of conduct](./CODE_OF_CONDUCT.md)
and tries to adhere to it strictly.

## Further developments

If you're feeling Pythonic, you can look at [the CONTRIBUTING file](./CONTRIBUTING.md) for the contributor guide,
and read [the TODO file](./TODO.md) to see the high-level features we'd like to work on next.

## Building

Please refer to [the BUILDING file](./BUILDING.md) for instructions on how to import and build your own version of the project.

## Major contributors

This project was started by Benoit Lagae as a hobby assignment, coming from his background in Latin linguistics
and his Master's thesis research. The engine and the REST interface are his work.
