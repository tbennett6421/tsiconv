#from __future__ import (print_function, unicode_literals, division, absolute_import)
__metaclass__ = type
__package_name__ = 'tsiconv'

## Standard Libraries
import os
import sys
import argparse
import logging
from pprint import pprint

## Third Party libraries
import pkg_resources
import pytz
from dateutil.parser import isoparse

## Modules
# try:
#     from .classes import CustomExceptions
# except ImportError:
#     # If we can't import modules, probably running from VSCODE
#     # attempt to hack in modules
#     import importlib
#     SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
#     sys.path.append(os.path.dirname(SCRIPT_DIR))
#     CustomExceptions = importlib.import_module(__package_name__+'.classes.CustomExceptions')

## Load up some metadata
try:
    __code_name__  = __package_name__
    # spacing is deliberate
    __code_desc__ = """ program description to be displayed by argparse \n    ex: python {name}
        """.format(name=str(__package_name__)+'.py')
    _distro = pkg_resources.get_distribution(__package_name__)
    __code_version__ = _distro.version
    __code_meta__ = vars(_distro)
    __code_debug__ = False
except pkg_resources.DistributionNotFound:
    # when debugging with vscode
    __code_debug__ = True
    stubs = [ '__code_version__', '__code_meta__']
    for s in stubs:
        globals()[s] = 'Not Available'

## Functions
def __print_dunders__():
    blacklist = ['__builtins__', '__print_dunders__']
    for k, v in list(globals().items()):
        if k.startswith('__'):
            if k in blacklist:
                pass
            else:
                pprint("%s => %s" % (k, v))

def isNaive(t):
    if t.tzinfo is None or t.tzinfo.utcoffset(t) is None:
        return True
    else:
        return False

def isAware(t):
    if t.tzinfo is not None and t.tzinfo.utcoffset(t) is not None:
        return True
    else:
        return False

def demo():
    __print_dunders__()
    sys.exit(1)

def usage_list():
    for i in pytz.all_timezones:
        print(i)
    sys.exit(1)

def begin_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            style="{",
            fmt="[{name}:{filename}] {levelname} - {message}"
        )
    )
    log = logging.getLogger(__package_name__)
    log.setLevel(logging.INFO)
    log.addHandler(handler)
    return log

def collect_args():
    parser = argparse.ArgumentParser(description=__code_desc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-V', '--version', action='version', version=__code_version__)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-t', '--time', action='store', required=True, help="A datetime to convert. This should be in ISO-8601 format")
    parser.add_argument('-l', '--list', action='store_true', help="List out the timezones supported by this application")
    args = parser.parse_args()
    return parser, args

def handle_args():
    # collect parser if needed to conditionally call usage: parser.print_help()
    parser, args = collect_args()
    return args

def main():
    log = begin_logging()
    args = handle_args()

    try:

        # print out timezones?
        if args.list:
            usage_list()
    except Exception as e:
        pprint(e)
        raise e
    finally:
        pass

if __name__=="__main__":
    main()
