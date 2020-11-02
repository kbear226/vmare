#!/usr/bin/env python3.9

"""
VMare donothings

dothings [OPTION] [PARAMS]
DESCRIPTION

dothings does some things:
-p Takes an input file name with text and phone numbers and
extracts all the phone numbers then outputs a file containing
a list of the phone numbers only, e.g. -p inputfile.txt
outputfile.txt

-b Takes an input file name for a binary file, copies and saves a
binary file to a new location (Note, should not be implemented
with built in functions like copyfile(3) or shutil.copy), e.g.
-b inputfile outputfile

-w Downloads the contents of
https://www.carbonblack.com/contact-us/ and extracts all of
the office locations of Carbon Black to
a file, e.g. -w outputfile.txt

-u Takes a comma separated list of integers and returns the
number of unique ones to the command line, e.g.
-u 1,2,2,3,4,5,4 returns "3" (1, 3, and 5 occur
exactly once)

-m Returns the amount of memory (RAM) currently used and
available on the system in a table showing GB, rounded to one
decimal place:
| Used | Unused |
| 3.3GB | 4.4GB |

-c Takes two file names as input and prints “true” if the contents
are identical or “false” if not, e.g. -c fileA fileB
"""
import psutil
import sys
import re
import json
import requests
import filecmp
import collections
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--p" ,dest="p",default="",
                    help="String list separated by a comma input,output" )
parser.add_argument(
    "-b", "--b" ,dest="b",default="",
    help="String list separated by a comma input,output binary files" )
parser.add_argument("-w", "--w" ,dest="w",default="",
                    help="String rep name of output file" )
parser.add_argument("-m", "--m" ,dest="m",default=False)
parser.add_argument("-c", "--c" ,dest="c",default="",
                    help="String list separated by a comma fileA,fileb" )
parser.add_argument("-u", "--u" ,dest="u",default="")

args = parser.parse_args()

class Error(Exception):
    pass

class CheckError(Error):
    """CheckError: """

    def __init__(self, error):
        self.message = error


class DoNothings():
    """VMare DoNothings Scripts."""

    def run(self):

        def _GetError(value):
            return "ERROR: %s requires 2 files, 1 received \n" % value

        if args.p:
            pfiles = args.p.split(',')
            try:
                self.ExtractPhoneNumbers(pfiles[0], pfiles[1])
            except IndexError:
                sys.stderr.write(_GetError("ExtractPhoneNumbers"))
        if args.b:
            bfiles = args.b.split(',')
            try:
                self.CopyBinaryFile(bfiles[0], bfiles[1])
            except IndexError:
                sys.stderr.write(_GetError("CopyBinaryFile"))
        if args.c:
            cfiles = args.c.split(',')
            try:
                self.AreFilesIdentical(cfiles[0], cfiles[1])
            except IndexError as Error:
                sys.stderr.write(_GetError("AreFilesIdentical"))
        if args.w:
            self.ExtractCarbonBlackSiteLocations(args.w)
        if args.m:
            self.GetMemory()
        if args.u:
            self.ExtractUniqueNumberCount(args.u)


    def ExtractPhoneNumbers(self, input, output):
        """Pulls and saves phone numbers to an output file(s).

        args:
            input:  Full path to inputfile.
            output: Full path to outputfile.
        """
        # TODO exception FileNotFoundError
        p0 = "\d{3}-\d{3}-\d{4}"
        p1 = "\(\d{0,}\)\d{3}-\d{4}"
        p2 = "\d{3}-\d{8}|\d{4}-\d{7}"
        p3 = "\(\d{0,}\)\d{0,}"
        p4 = "\+\d{0,}"
        p5 = "\d{10}$"
        patterns = [p0,p1,p2,p3,p4, p5]
        data = open(input, 'r')
        f = open(output, "a")
        for row in data:
            m = re.search(str.join("|", patterns), row.replace(" ", ""))
            if m:
                f.write(m[0] + "\n")
            else: sys.stderr.write("ERROR: Row not matched ==>" + row)
        f.close()

    def CopyBinaryFile(self, input, output):
        # TODO: Add a binary check
        with open(input,'rb') as f1, open(output,'wb') as f2:
            while True:
                b=f1.read(1)
                if b:
                    n=f2.write(b)
                else: break
        if not (self.AreFilesIdentical(input, output)):
            raise(CheckError("ERROR: Files not identical"))

    def ExtractCarbonBlackSiteLocations(self, outputfile):
        """Scraps the returned contents matching
            VMware Carbon Black Office Location xxxxx
        """
        # Saving to a eliminates duplication
        locations = set()
        url = "https://www.carbonblack.com/contact-us/"
        x = requests.get(url)
        for le in x.iter_lines():
            m = re.search(r"VMWCB-Location-\w{0,}", str(le))
            if m:
                locations.add(m[0].split("-")[-1])
        if locations:
            with open(outputfile,'w+') as f:
                for loc in sorted(locations):
                    f.write(loc + "\n")

    def ExtractUniqueNumberCount(self, lst):
        unq = 0
        cnt = collections.Counter(lst)
        for n in lst:
            if isinstance(n, int):
                if cnt[n]==1:
                    unq+=1
            else:
                raise ValueError("List excepts int values only")
        return unq

    def AreFilesIdentical(self, f1, f2):
        filecmp.clear_cache()
        return filecmp.cmp(f1, f2, shallow=True)

    def GetMemory(self):
        usage = psutil.virtual_memory().used/1024**3
        free = psutil.virtual_memory().free/1024**3
        usage_f = re.search("\d{0,}.\d{2}", str(usage))
        free_f = re.search("\d{0,}.\d{2}", str(free))
        print(f'| {"Used":4} | {"Unused":6} |')
        print(f'| {usage_f[0]:4} | {free_f[0]:6} |')



if __name__ == "__main__":
    DoNothings().run()
    print("Complete")
