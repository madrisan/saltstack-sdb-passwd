'''
SDB module for JSON
 
Like all sdb modules, the JSON module requires a configuration profile
to be configured in either the minion or, as in our implementation,
in the master configuration file (/etc/salt/master.d/passwords.conf).
This profile requires very little:
 
.. code-block:: yaml
 
     pwd:
       driver: json
       data: /srv/salt/common/pwd.json
 
The ``driver`` refers to the json module and ``data`` is the path
to the JSON file that contains the data.
 
This file should be saved as salt/_sdb/json.py
 
.. code-block:: yaml

     user: sdb://pwd/user1
 
CLI Example:
 
.. code-block:: bash
 
     salt-run sdb.delete sdb://pwd/user1
     salt-run sdb.get sdb://pwd/user1
     salt-run sdb.set sdb://pwd/user1 '$5$0DZt7BTf$gjNPsFCJDpwUhLervVkOhbzrmSxNnfJw46V.h7eEaE.'
'''
from __future__ import absolute_import
import salt.exceptions
import salt.utils.files
import json
 
__func_alias__ = {
    'set_': 'set'
}

def _read_json(profile):
    '''
    Return the content of a JSON file
    '''
    jsonfile = profile.get('data', None)
    if not jsonfile:
        raise salt.exceptions.CommandExecutionError(
            'No key data in the SDB profile')

    try:
        with salt.utils.files.fopen(jsonfile, 'r') as fp_:
            return json.load(fp_)
    except (IOError, OSError) as exc:
        raise salt.exceptions.CommandExecutionError(exc)
    except KeyError as exc:
        raise salt.exceptions.CommandExecutionError(
            '{0} needs to be configured'.format(exc))
    except ValueError as exc:   # includes json.decoder.JSONDecodeError
        raise salt.exceptions.CommandExecutionError((
            'Decoding JSON ({0}) has failed: {1}'
            .format(jsonfile, exc))) from None

def _write_json(profile, json_data):
    '''
    Write the JSON data to file
    '''
    try:
        with salt.utils.files.fopen(profile['data'], 'w') as fp_:
            json.dump(json_data, fp_, indent=2, sort_keys=True)
    except IOError as exc:
        raise CommandExecutionError(exc)

def delete(key, profile=None):
    '''
    Remove a key from a JSON file
    '''
    json_data = _read_json(profile)
    try:
        del json_data[key]
    except KeyError:
        return False

    _write_json(profile, json_data)
    return key
 
def get(key, profile=None):
    '''
    Get a value from a JSON file
    '''
    json_data = _read_json(profile)
    return json_data.get(key, {})

def set_(key, value, profile=None):
    '''
    Set a key/value pair in a JSON file
    '''
    json_data = _read_json(profile)
    json_data[key] = value

    _write_json(profile, json_data)
    return get(key, profile)
