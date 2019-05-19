Ansible Bitbucket_Backup Role
=============================

[![Build Status](https://travis-ci.org/computerlyrik/ansible-bitbucket_backup.svg?branch=master)](https://travis-ci.org/computerlyrik/ansible-bitbucket_backup)


Backup all public and/or private repositories of a specific account.

This role makes use of the included module bitbucket_repositories (see below) and adds functionality to fetch all reachable bitbucket repositories.

Requirements
------------

All requirements will be installed automatically on an Ubuntu 18.04 target.


Role Variables
--------------

**Mandatory Variables**


| Variable Name | Mandatory | Default | Description |
| --------------|-----------|---------|-------------|
| bitbucket_backup__search_user | x |         | user to search repositories for |
| bitbucket_backup__workdir     |   | /backup | target backup root |
| bitbucket_backup__user        |   |         | Bitbucket Username to auth with |
| bitbucket_backup__app_password|   |         | Bitbucket APP Password to auth with |
| bitbucket_backup__prune|      |   | False   | Prune existing repo refs |


Example Playbook
----------------

See `molecule/default/playbook.yml`

Testing
-------

See `molecule/INSTALL.rst`

Run `molecule test`

Module
======

Development Requirements
------------------------
`
pip install requests ~2
`

Testing
---------
`
./library/bitbucket_repositories.py ./library/params-[anon|nulls].json
`

License
=======

Apache 2

Author Information
==================

An optional section for the role authors to include contact information, or a
website (HTML is not allowed).
