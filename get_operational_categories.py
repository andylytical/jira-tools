import argparse
import csv
import io
import logging
import pathlib
import pprint
import tabulate
import textwrap
import time

from functools import wraps
from web_api import api_get


resources = {} # module level resources


def get_args( params=None ):
    key = 'args'
    if key not in resources:
        constructor_args = {
            'formatter_class': argparse.ArgumentDefaultsHelpFormatter,
            'description': textwrap.dedent( '''\
                Convenient listing of all parents and children 
                of the "operational categories" custom field.
                ''')
            }
        parser = argparse.ArgumentParser( **constructor_args )
        parser.add_argument( '-d', '--debug', action='store_true' )
        parser.add_argument( '-v', '--verbose', action='store_true' )
        parser.add_argument( '-f', '--format', default='pprint',
            help="One of 'print', 'csv', or a table format name for tabulate" )
        args = parser.parse_args( params )
        resources[key] = args
    return resources[key]

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


def operational_categories_as_csv( data ):
    # data = get_operational_categories()
    # outfile = pathlib.Path( 'operational_categories.csv' )
    # with outfile.open( mode='w' ) as csvfile:
    #     csvwriter = csv.writer( csvfile )
    #     for parent, children in data.items():
    #         for child in children:
    #             csvwriter.writerow( [ parent, child ] )
    output = io.StringIO()
    csvwriter = csv.writer( output )
    for parent, children in data.items():
        for child in children:
            csvwriter.writerow( [ parent, child ] )
    return output.getvalue()



def test_auth():
    path = 'issue/SVCPLAN-2741'
    r = api_get( path )
    print( r.text )



def run():
    starttime = time.time()

    args = get_args()
    data = get_operational_categories()
    if args.format == 'csv':
        print( operational_categories_as_csv( data ) )
    elif args.format == 'print':
        pprint.pprint( data )
    else:
        print( tabulate.tabulate( data, tablefmt=args.format ) )

    elapsed = time.time() - starttime
    logging.info( f'Finished in {elapsed} seconds!' )

    # Print summary of errors and warnings
    for e in get_errors():
        logging.error( e )
    for w in get_warnings():
        logging.warning( w )


if __name__ == '__main__':
    args = get_args()
    loglvl = logging.WARNING
    if args.verbose:
        loglvl = logging.INFO
    if args.debug:
        loglvl = logging.DEBUG
    logfmt = '%(levelname)s:%(funcName)s[%(lineno)d] %(message)s'
    logging.basicConfig( level=loglvl, format=logfmt )
    run()
