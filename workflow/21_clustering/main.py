

# scipy.spatial.distance.cdist

# pyclust

import argparse


import args

from c_dbscan import do_dbscan

args.init()


if args.args.method == 'dbscan':
    do_dbscan();

