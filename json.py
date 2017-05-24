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
 
        sudo salt-run sdb.get sdb://pwd/user1
'''
from __future__ import absolute_import
from salt.exceptions import CommandExecutionError
import salt.utils
import json
 
__func_alias__ = {
    'set_': 'set'
}
 
def _read_json(profile):
    '''
    Return the content of a JSON file
    '''
    try:
        with salt.utils.fopen(profile['data'], 'r') as fp_:
            return json.load(fp_)
        except IOError as exc:
            raise CommandExecutionError(exc)
        except KeyError as exc:
            raise CommandExecutionError(
                '{0} needs to be configured'.format(exc))
        except ValueError as exc:
            raise CommandExecutionError(
                'There was an error with the JSON data: {0}'.format(exc))
 
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
 
    try:
        with salt.utils.fopen(profile['data'], 'w') as fp_:
            json.dump(json_data, fp_, indent=2, sort_keys=True)
    except IOError as exc:
        raise CommandExecutionError(exc)
 
    return get(key, profile)
