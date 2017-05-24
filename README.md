[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3fc99967c7d34805ba71de2e5b3c8f19)](https://www.codacy.com/app/madrisan/saltstack-sdb-passwd?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=madrisan/saltstack-sdb-passwd&amp;utm_campaign=Badge_Grade)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://spdx.org/licenses/Apache-2.0.html)

![](images/saltstack_horizontal_dark.png?raw=true)

# SDB interface for storing and retrieving passwords

The SaltStack SDB (Simple Data Base) interface is designed to store and retrieve data that, unlike pillars and grains, is not necessarily minion-specific. It is a generic database interface for SaltStack. 

We will show here how you can make use of SDB for storing and retrieving passwords in a centralized way.
This is usefull to avoid data duplication when the same users appear in multiple Salt configuration files.

## SDB Configuration

The SDB interface requires a profile to be set up in the master configuration file.
We can modularize the configuration by creating a file `/etc/salt/master.d/passwords.conf`.
The configuration stanza includes the name/ID that the profile will be referred to as, a driver setting (and when necessary any other arguments that are necessary for the SDB module that will be used.)

```
pwd:
    driver: json
    data: /srv/salt/common/pwd.json
```

## Writing SDB Modules

You will store the data in JSON format and make use of the SDB execution module to `get`, `set` and `delete` values from this file. 

There is currently one function that MUST exist in any SDB module (`get()`), one that SHOULD exist (`set_()`) and one that MAY exist (`delete()`). If using a (`set_()`) function, a `__func_alias__` dictionary MUST be declared in the module as well:

```python
__func_alias__ = {
    'set_': 'set',
}
```

These methods must be implemented in the python script `json.py` placed in a directory called `_sdb/` at the root of the Salt fileserver, usually `/srv/salt` (that is `/srv/salt/_sdb/json.py`).

See the complete driver code [here](json.py).

## Getting, Setting and Deleting SDB Values

You can now store the hashed passwords in the JSON data file

```json
{
  "user1": "$5$tEpxpTHeP...0128tglwMKE.X9b88fO4x0",
  "user2": "$5$n4XiZajqf...P3BrvFM5hYq.UazR4dHxl8"
}
```

Getting a value requires only the SDB URI to be specified. To retrieve a value from the pwd profile above, you would use:

```bash
$ sudo salt-run sdb.get sdb://pwd/user1
```

Setting a value uses the same URI as would be used to retrieve it, followed by the value as another argument. For the above pwd URI, you would set a new value using a command like:

```bash
$ sudo salt-run sdb.set sdb://pwd/user2 '$5$n4XiZajqf...P3BrvFM5hYq.UazR4dHxl8'
```

## Using SDB URIs in Files

If you would like to retrieve a key directly from SDB, you would call the sdb.get function directly, using the SDB URI. For instance, in a pillar file you can define the passwords as follows:

```yaml
users:
  user1:
    fullname: First User
    uid: 2000
    gid: 1000
    password: {{ salt['sdb.get']('sdb://pwd/user1') }}
```
