#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: bitbucket_repositories

short_description: Gets all your repositories for further processing

version_added: "2.8"

description:
    - "Reads the bitbucket API and sends back a json with all repository data. See call in role for an example"

options:

    search_user:
        description: The user / group for whom the repositories are listet
        required: true
    bitbucket_user:
        description: The user to login agains bitbucket API
        required: false
    bitbucket_app_password:
        description: The **APP**-password to login against bitbucket API
        required: false
    paging:
        description: If you like to have paged output or all-at-once
        required: false
extends_documentation_fragment:
    - azure

author:
    - Christian Fischer (@computerlyrik)
'''

EXAMPLES = '''
# Backup with anonymous auth
- name: get public repositories of user myuser
  bitbucket_repositories:
    search_user: myuser

# Backup all repos including private
- name: get all repositories of user myuser - including private
  bitbucket_repositories:
    search_user: myuser
    bitbucket_user: myloginuser
    bitbucket_app_password: mygeneratedapppassword

'''

RETURN = '''
A complex bitbucket API json object
'''

from ansible.module_utils.basic import AnsibleModule
import requests

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        paging=dict(type='bool', required=False, default=True),
        search_user=dict(type='str', required=True),
        bitbucket_user=dict(type='str', required=False),
        bitbucket_app_password=dict(type='str', required=False, no_log=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        repositories=None
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    server_base_uri = "https://api.bitbucket.org/2.0"
    url = server_base_uri + '/repositories/' + module.params['search_user']

    results = []

    if (module.params['bitbucket_user'] != None
       and module.params['bitbucket_app_password'] != None):
      auth = (module.params['bitbucket_user'], module.params['bitbucket_app_password'])
    else:
      auth = None 

    while True:
      current_page = requests.get(url, auth=auth)
      if (current_page.status_code != requests.codes.ok):
        module.fail_json(msg='Request to bitbucket API call '+url+' failed, try set user and app_password', **result)
      results.extend(current_page.json()['values'])
      if (module.params['paging']):
        break
      try:
        url = current_page.json()['next']
      except KeyError:
        break

    # manipulate or modify the state as needed
    result['repositories'] = results

    # Due to this is a readonly module, we do not do any changes
    # and can send back the acquired information directly to the caller
    #if module.check_mode:
    #    return result

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()

