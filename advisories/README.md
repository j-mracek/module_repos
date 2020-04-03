Advisory Issues
===============

All issues are related to advisories with multi collection per advisories.

    <pkglist>
      <collection short="named collection">
      </collection>
      <collection short="named collection">
      </collection>


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

------------------
Multiversion issue
------------------

Reproducer
----------

Use `multiversion` repository

`dnf install testpkg`

Install nonmodular `testpkg`

`dnf updateinfo`

Show correctly no advisory

`dnf check-update`

Show correctly no update

`dnf module enable perl-DBI`

Enable `perl:5.26` and `perl-DBI`

`dnf updateinfo`

Show incorrectly 1 advisory of enhancement type

`dnf update --enhancement`

`dnf check-update --enhancement`

Show correctly no update
