#!/usr/bin/env python3
'''
Created on 07.11.2020

@author: Bjoern Graebe
'''

import os.path
import sys
import argparse
import jsonpickle
from control.mpdj_runner_v2 import MPDJRunnerV2
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help="The MPDJ file to run",required=True)
parser.add_argument('-A', '--address', help="The HOST IP address to connect to")
#parser.add_argument('-A', '--HOST-address')
parser.add_argument('-p', '--port', help="The PORT to connect to")
parser.add_argument('-k', '--keep-current-playlist', help="Keep current playlist and append if necessary.", action="store_true")
#parser.add_argument('-p', '--PORT')


if __name__ == '__main__':
    args = parser.parse_args()
    if args.address:
        HOST = args.address
    else:
        HOST = 'localhost'

    if args.port:
        PORT = args.port
    else:
        PORT = '6600'

    file = args.file
    if not os.path.isfile(file):
        print ('{} does not exist.'.format(file))
        sys.exit(1)

    mpdjRunner = MPDJRunnerV2(HOST,PORT)
    
    with open(file, 'r') as loadFile:
        mpdjRunner.mpdj_data = jsonpickle.decode(loadFile.read())
    try:
        if not args.keep_current_playlist:
            mpdjRunner.clear_playlist()
        mpdjRunner.run()
    except KeyboardInterrupt:
        print('leaving....')
