#!/usr/bin/env python

from __future__ import print_function
from socket import timeout

import os
import sys
import codecs
import re

import markdown

try:
    # compatible for python2
    from urllib2 import urlopen
    from urllib2 import HTTPError
except ImportError:
    # compatible for python3
    from urllib.request import urlopen
    from urllib.error import HTTPError

def check_live_url(url):

    result = False
    try:
        ret = urlopen(url, timeout=5)
        result = (ret.code == 200)
    except HTTPError as e:
        print(e.code, file=sys.stderr)
    except timeout as e:
        print(e.code, file=sys.stderr)

    return result


def main(path):

    filenames = []
    for (dirpath, dnames, fnames) in os.walk(path):
        for fname in fnames:
            if fname.endswith('.md'):
                filenames.append(os.sep.join([dirpath, fname]))

    urls = []

    for filename in filenames:
        fd = codecs.open(filename, mode="r", encoding="utf-8")
        for line in fd.readlines():
            refs = re.findall(r'(?<=<a href=")[^"]*', markdown.markdown(line))
            for ref in refs:
                urls.append(ref)

    #print(urls)

    for url in urls:
        if check_live_url(url):
            print(url)
        else:
            print(url, file=sys.stderr)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Choose one path as argument one")
