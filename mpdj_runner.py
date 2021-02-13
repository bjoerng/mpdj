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
parser.add_argument('-f', help="The MPDJ file to run",required=True)
parser.add_argument('-A', help="The HOST IP address to connect to")
#parser.add_argument('-A', '--HOST-address')
parser.add_argument('-p', help="The PORT to connect to")
#parser.add_argument('-p', '--PORT')

if __name__ == '__main__':
    args = parser.parse_args()

    if args.A:
        HOST = args.A
    else:
        HOST = 'localhost'

    if args.p:
        PORT = args.p
    else:
        PORT = '6600'

    file = args.f
    if not os.path.isfile(file):
        print ('{} does not exist.'.format(file))
        sys.exit(1)

    mpdjRunner = MPDJRunnerV2(HOST,PORT)
    with open(file, 'r') as loadFile:
        mpdjRunner.mpdj_data = jsonpickle.decode(loadFile.read())
    try:
        mpdjRunner.run()
    except KeyboardInterrupt:
        print('leaving....')
