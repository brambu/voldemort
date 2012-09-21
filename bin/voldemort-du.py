#!/usr/bin/env python2.6
'''
A simple script that calculates disk usage for voldemort directory.
usage: voldemort_du.py /path/to/data/bdb/store /path/to/data/bdb/store2
author="szielinski@linkedin.com"
'''

import os
import sys
from collections import defaultdict
from argparse import ArgumentParser
import simplejson as json

def verifydirectory(path):
  try:
    os.stat(path)
  except:
    sys.stderr.write("Path %s invalid.\n") % (path)
    sys.exit(1)
  return path

def get_du(path):
  result=defaultdict(int)
  for d, n, files in os.walk(path):
    for f in files:
      ext=f.split(".")[-1]
      fullpath=os.path.join(d, f)
      size=os.path.getsize(fullpath)
      result[ext]+=size
  return result

def printout(rdict,oformat):
  if oformat=="json":
    print json.dumps(rdict)
  else:
    sep_dict={'plain': ' ', 'csv': ',', 'psv': '|'}
    sep=sep_dict[oformat]
    print sep.join(["store","type","size"])
    for k,v in rdict.iteritems():
      for ext,size in v.iteritems():
        print sep.join([k,ext,str(size)])
  return

def main():
  parser=ArgumentParser(description='A simple script that calculates disk usage for voldemort data location.')
  outputmap=['json','plain','csv','psv']
  parser.add_argument('-o','--output',\
                      help='Set output format (%s)' % (",".join(outputmap)),\
                      required=False, default='json')
  parser.add_argument('paths',nargs='+')
  
  args=parser.parse_args()
  
  if args.output not in outputmap:
    sys.stderr.write("Valid options for output format are %s.\n" % (",".join(outputmap)))
    sys.exit(1)
  
  outputformat=args.output
  paths=args.paths
  
  pathresult=defaultdict()
  allresult=defaultdict()
  
  for path in paths:
    path=verifydirectory(path)
    storename=path.split("/")[-1]
    pathresult=get_du(path)
    allresult[storename]=pathresult

  printout(allresult,outputformat)
  
if __name__ == '__main__':
  sys.exit(main())

