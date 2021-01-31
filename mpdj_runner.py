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
parser.add_argument('-f', help="The MPDJ to run",required=True)
parser.add_argument('-A', help="The HOST IP address to connect to")
#parser.add_argument('-A', '--HOST-address')
parser.add_argument('-p', help="The port to connect to")
#parser.add_argument('-p', '--port')


if __name__ == '__main__':
    args = parser.parse_args()
    host = 'localhost'
    if args.A:
        HOST = args.A

    port = '6600'
    if args.p:
        port = '6600'

    file = args.f
    if not os.path.isfile(file):
        print ('{} does not exist.'.format(file))
        sys.exit(1)

    mpdjRunner = MPDJRunnerV2(HOST,port)
    with open(file, 'r') as loadFile:
        mpdjRunner.mpdj_data = jsonpickle.decode(loadFile.read())
    mpdjRunner.run()
    