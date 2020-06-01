#!/usr/bin/env python3

"""

Simple file to search an alien path for specified named file (default=root_archive.zip)
For each file found, check if it is on selected storage element. 

"""

import sys
if sys.version[0:3] < '3.0':
    print ("Python version 3.0 or greater required (found: %s)." % sys.version[0:5])
    sys.exit(-1)


import math, os, pprint, re, shlex, shutil, socket, stat, time
from shutil import copyfile
from datetime import datetime
from signal import alarm, signal, SIGALRM, SIGKILL, SIGTERM
from subprocess import Popen, PIPE, STDOUT
import argparse
#from ConfigParser import RawConfigParser
from process_commands import process_commands
import json

#---- Gobal defaults ---- Can be overwritten with commandline arguments 


#----------------------------------------

class find_data:
    """ application class """

    def __init__(self, args):
        self.args = args
        self.alien_path = args.alien_path
        self.se_name = args.se_name
        self.fname = args.filename
        self.testit = args.testit
        self.proc_c = process_commands(args.verbosity)

#------------------------
    def _unixT(self):
        return int(time.mktime((datetime.now()).timetuple()))

#-----------------------------------

#-----------------------------------

    def check_file(self,filename):

        cmd="alien_whereis %s" % (filename)
        self.proc_c.log("Running command = %s" % (cmd), 1)
        s, o, e = self.proc_c.comm(cmd)
        if s == 0:
            output=str(o,"utf-8")
            olist = output.splitlines()
            for aline in olist:
                if self.se_name in aline:
                    self.proc_c.log("will split line = %s" % (aline), 1)
                    pfnames = aline.split("pfn => ")
                    return pfnames[1]

        return None

#-----------------------------------

    def alienfind(self):

        cmd="alien_find %s %s" % (self.alien_path,self.fname)
        self.proc_c.log("Running command = %s" % (cmd), 1)

        s, o, e = self.proc_c.comm(cmd)
        if s == 0:
            output=str(o,"utf-8")
            olist = output.splitlines()
            for afile in olist:
                yield afile

#-----------------------------------
    def go(self):

#       A tally for keeping count of various stats
        tally = dict(pico_cp_tries=0, pico_cp_succ = 0, pico_cp_fail = 0, 
                    hpss_tries = 0, hpss_succ = 0, hpss_fail =0)
        self.proc_c.log("We will search = %s for all files=%s and print out any that are on SE=%s" % (self.alien_path,self.fname,self.se_name), 0)


        icount = 0
        for filename in self.alienfind():
            icount += 1
            if icount == 3 and self.testit:
                return -1
            pfn = self.check_file(filename)
            if pfn is not None:
                print ("File = %s PFN = %s" %(filename,pfn))



def main():
    """ Generic program structure to parse args, initialize and start application """
    desc = """ find files on given SE """
    
    p = argparse.ArgumentParser(description=desc, epilog="None")
    p.add_argument("--alien-path",dest="alien_path",default=None,help="base path to search for files")
    p.add_argument("--se-name",dest="se_name",default=None,help="storage element name to test")
    p.add_argument("--fname",dest="filename",default="root_archive.zip",help="filename to search for")

    p.add_argument("-t",action="store_true",dest="testit",default=False,help="testit with 2 loops and exit")
    p.add_argument("-v", "--verbose", action="count", dest="verbosity", default=0,                                                                                                 help="be verbose about actions, repeatable")
    p.add_argument("--config-file",dest="config_file",default="None",help="override any configs via a json config file")


    args = p.parse_args()
    if args.alien_path is None:
        print ("Required input, alien_path, is not specified")
        return -1
    if args.se_name is None:
        print ("Required input, se_name, is not specified")
        return -1

    isjalien = shutil.which("alien.py") is not None
    if not isjalien:
        print ("must be in jalien environment")
        return -1

#-------- parse config file to override input and defaults
    val=vars(args)
    if not args.config_file == "None":
        try:
            print ("opening ", args.config_file)
            with open(args.config_file) as config_file:
                configs=json.load(config_file)
            for key in configs:
                if key in val:
                    if isinstance(configs[key],unicode):
                        val[key]=configs[key].encode("ascii")
                    else:
                        val[key]=configs[key]
        except:
            p.error(" Could not open or parse the configfile ")
            return -1

    try:
        myapp = find_data(args)
        return(myapp.go())
    except (Exception, oops):
        if args.verbosity >= 2:
            import traceback
            traceback.print_exc()
        else:
            print (oops)
            return -1
                                                                                                                                                                
if __name__ == "__main__":                      
    sys.exit(main())


