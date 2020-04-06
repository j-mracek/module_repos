Advisory Issues
===============

All issues are related to advisories with multi collection per advisory.

```
<updates>
  <update from="secresponseteam@foo.bar" status="final" type="enhancement" version="3">
    <id>FEDORA-2019-0329090518</id>
    <title>glibc bug fix</title>
    <issued date="2019-03-29 00:00:00"/>
    <updated date="2019-03-29 00:00:00"/>
    <severity>none</severity>
    <summary>summary_1</summary>
    <description>Enhance some stuff</description>
    <references>
        <reference href="https://foobar/foobarupdate_2" id="2222" type="bugzilla" title="222"/>
        <reference href="https://foobar/foobarupdate_2" id="2222" type="cve" title="CVE-2999"/>
    </references>
    <pkglist>
      <collection short="named collection">
        <name>Foo component</name>
        <module name="perl-DBI" stream="master" version="2" context="iiiiiiiii" arch="x86_64"/>
        <package name="test-perl-DBI" version="1" release="2.module_el8+6745+9879ate3" epoch="0" arch="x86_64" src="http://www.foo.org">
          <filename>perl-DBI-1-2.module_el8+6745+9879ate3.spec</filename>
          <reboot_suggested/>
        </package>
      </collection>
      <collection short="named collection">
        <name>Foo component</name>
        <module name="perl-DBI" stream="master" version="2" context="hhhhhhhhhh" arch="x86_64"/>
        <package name="test-perl-DBI" version="1" release="2.module_el8+6587+9879afr5" epoch="0" arch="x86_64" src="http://www.foo.org">
          <filename>perl-DBI-1-2.module_el8+6587+9879afr5.spec</filename>
          <reboot_suggested/>
        </package>
      </collection>
    </pkglist>
  </update>
</updates>
```

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
