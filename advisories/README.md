Advisory Issue
==============

------------------
Multicontext issue
------------------

Reproducer
----------

Reproducer is context specific therefore the issue appears only when perl:5.24 is enabled.

Use `multicontext` repository

`dnf enable perl:5.24`

`dnf install test-perl-DBI-0:1-1.module_el8+7554+8763afg8.x86_64`

Install older version of test-perl-DBI

`dnf updateinfo`

Show correctly 1 advisory of enhancement type

`dnf check-update --enhancement`

Show correctly 1 update

`dnf update --enhancement`

Install correctly update for `test-perl-DBI`

`dnf updateinfo`

Show incorrectly 1 advisory of enhancement type

`dnf check-update --enhancement`

Show correctly no update


