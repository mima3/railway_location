#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os

def main(argvs, argc):
    """
    index.cgiの作成
    """
    if(argc != 3):
        print ('Usage #python %s "/usr/local/python" "./serif.ini"' % argvs[0])
        return -1

    python_path = argvs[1]
    ini_path = argvs[2]
    original = os.path.abspath(os.path.dirname(__file__)) + '/index.cgi.original'
    f = open(original)
    contents = f.read()
    f.close()
    contents = contents.replace('[python_path]', python_path)
    contents = contents.replace('[ini_path]', ini_path)
    print (contents)
    return 0

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
