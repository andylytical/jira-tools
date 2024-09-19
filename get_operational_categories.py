import csv
import logging
import pathlib
import time

import pprint

from functools import wraps
from web_api import api_get

logfmt = '%(levelname)s:%(funcName)s[%(lineno)d] %(message)s'
loglvl = logging.INFO
#loglvl = logging.DEBUG
logging.basicConfig( level=loglvl, format=logfmt )

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


def get_custom_field_id( cf_name ):
    cf_id = None
    r = api_get( 'customFields' )
    data = r.json()
    # pprint.pprint( { k:data[k] for k in ( 'maxResults', 'total' ) } )
    params = { 'maxResults':data['total'] }
    r = api_get( 'customFields', params=params )
    data = r.json()
    # pprint.pprint( { k:data[k] for k in ( 'maxResults', 'total' ) } )
    # pprint.pprint( data )
    for field in data['values']:
        if field['name'] == cf_name:
            cf_id = field['numericId']
            break
    return cf_id


def get_operational_categories():
    cf_id = get_custom_field_id( 'Operational Categories' )
    r = api_get( f'customFields/{cf_id}/options' )
    options = r.json()[ 'options' ]
    names = {}
    parents = {}
    data = {}
    for o in options:
        f_id = o[ 'id' ]
        f_children = o[ 'childrenIds' ]
        f_name = o[ 'value' ]
        names[ f_id ] = f_name
        if len( f_children ) > 0:
            parents[ f_id ] = f_children
    for parent_id, child_ids in parents.items():
        parent = names[ parent_id ]
        children = [ names[x] for x in child_ids ]
        data[ parent ] = children
    # pprint.pprint( data )
    return data


def operational_categories_as_csv():
    data = get_operational_categories()
    outfile = pathlib.Path( 'operational_categories.csv' )
    with outfile.open( mode='w' ) as csvfile:
        csvwriter = csv.writer( csvfile )
        for parent, children in data.items():
            for child in children:
                csvwriter.writerow( [ parent, child ] )



def test_auth():
    path = 'issue/SVCPLAN-2741'
    r = api_get( path )
    print( r.text )



def run():
    starttime = time.time()

    # test_auth()

    operational_categories_as_csv()

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
