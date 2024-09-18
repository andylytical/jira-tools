import csv
import json
import logging
import pathlib
import time

import pprint

from functools import wraps

import web_api


# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1

logfmt = '%(levelname)s:%(funcName)s[%(lineno)d] %(message)s'
loglvl = logging.INFO
#loglvl = logging.DEBUG
logging.basicConfig( level=loglvl, format=logfmt )

# requests_log = logging.getLogger("urllib3")
# requests_log.setLevel(loglvl)
# requests_log.propagate = True

resources = {} # module level resources


def get_warnings():
    key = 'errs'
    if key not in resources:
        resources[key] = []
    return resources[key]


def warn( msg ):
    ''' Log an warning to the screen and,
        Also save it in an array for later retrieval of all warnings.
    '''
    key = 'errs'
    if key not in resources:
        resources[key] = []
    resources[key].append( msg )
    logging.warning( msg )


def get_errors():
    key = 'errs'
    if key not in resources:
        resources[key] = []
    return resources[key]


def err( msg ):
    ''' Log an error to the screen and,
        Also save it in an array for later retrieval of all errors.
    '''
    key = 'errs'
    if key not in resources:
        resources[key] = []
    resources[key].append( msg )
    logging.error( msg )


# https://stackoverflow.com/questions/1622943/timeit-versus-timing-decorator#27737385
def timing( f ):
    @wraps( f )
    def wrap( *args, **kw ):
        starttime = time.time()
        result = f( *args, **kw )
        endtime = time.time()
        elapsed = endtime - starttime
        logging.info( f'func:{f.__name__} args:[{args}, {kw}] took: {elapsed} sec' )
        return result
    return wrap


# def get_custom_fields():
#     path = 'customFields'



# def add_application_access_groups():
#     jira_groups = get_config().options( 'Application Access Jira' )
#     path = 'applicationrole'
#     # r = api_get( path )
#     data = {
#         'key': 'jira-software',
#         'groups': jira_groups[:2],
#         }
#     r = api_put( path, data )
#     print( r.text )


# def get_project_roles( pid ):
#     r = api_get( f'project/{pid}/role' )
#     data = r.json()
#     role_names = list( data.keys() )
#     roles = {}
#     for role in role_names:
#         rid = get_role_id( role )
#         role_data = get_project_role_details( pid, rid )
#         # print( f"Project:{pid} Role:'{role}'" )
#         # pprint.pprint( role_data )
#         actors = [ f"{r['name']} ({r['displayName']})" for r in role_data['actors'] ]
#         roles[role] = actors
#     return roles


# def get_project_role_details( pid, role_id ):
#     path = f'project/{pid}/role/{role_id}'
#     r = api_get( path )
#     data = r.json()
#     return data


# def project_roles_as_csv():
#     r = api_get( 'project' )
#     data = r.json()
#     project_keys = { p['key'] : p['name'] for p in data }
#     # projects = {}
#     csv_rows = [ ['Project', 'Role', 'Members'] ]
#     for pid,p_name in project_keys.items():
#         roles = get_project_roles( pid )
#         # projects[pid] = {
#         #     'name': p_name,
#         #     'roles': roles,
#         #     }
#         for role, members in roles.items():
#             csv_rows.append( [ pid, role] + members )
#     # pprint.pprint( projects )
#     output = pathlib.Path( 'perms.csv' )
#     with output.open(mode='w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerows( csv_rows )
#     # return projects




def test_auth():
    path = 'issue/SVCPLAN-2741'
    r = api_get( path )
    # print( r.text )



def run():
    starttime = time.time()

    test_auth()

    # set_banner()

    # set_general_config()

    # add_application_access_groups() #returns error 400

    # project_roles_as_csv()
    # get_project_roles( 'SVCPLAN', 10002 )

    elapsed = time.time() - starttime
    logging.info( f'Finished in {elapsed} seconds!' )

    # Print summary of errors and warnings
    for e in get_errors():
        logging.error( e )
    for w in get_warnings():
        logging.warning( w )


if __name__ == '__main__':
    run()
