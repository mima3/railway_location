# -*- coding: utf-8 -*-
import railway_db
import sys


def main(argvs, argc):
    if argc != 3:
        print ("Usage #python %s db_path xml_path" % argvs[0])
        return 1
    railway_db.setup(argvs[1])           # 'railway.sqlite'
    railway_db.import_railway(argvs[2])  # './kokudo/N02-13/N02-13.xml'


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
