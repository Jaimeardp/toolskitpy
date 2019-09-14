import sys, os
import subprocess
import logging

import argparse
from datetime import datetime
import configparser

def main(number, other_number, output):
    result = number * other_number
    print(f'[{datetime.utcnow().isoformat()}] The result is {result}',
    file=output)


kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes)                   # default: roughly a floppy

def split(fromfile, todir, chunksize=chunksize): 
    if not os.path.exists(todir):                  # caller handles errors
        os.mkdir(todir)                            # make dir, read/write parts
    else:
        for fname in os.listdir(todir):            # delete any existing files
            os.remove(os.path.join(todir, fname)) 
    partnum = 0
    input = open(fromfile, 'rb')                   # use binary mode on Windows
    _, typefile = os.path.splitext(fromfile)
    while 1:                                       # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum  = partnum+1
        filename = os.path.join(todir, ('part%04d.%s' % (partnum, typefile)))
        fileobj  = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()                            # or simply open(  ).write(  )
    input.close(  )
    assert partnum <= 9999                         # join sort fails if 5 digits
    return partnum

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-ffile', type=str, help='Archivo a particionar', required=True)

    parser.add_argument('-tdir', type=str, help='Ruta destino', default='./temp')

    parser.add_argument('-chunksz', type=str, help='Ruta destino', default=chunksize)

    parser.add_argument('--config', '-c', type=argparse.FileType('r'),
                            help='config file')
    parser.add_argument('-o', dest='output', type=argparse.FileType('a'),
                            help='output file',
                                default=sys.stdout)
    args = parser.parse_args()

    if args.config:
        config = configparser.ConfigParser()
        config.read_file(args.config)
        # Transforming values into integers
        args.n1 = int(config['DEFAULT']['fromfile'])
        args.n2 = int(config['DEFAULT']['todir'])

    split(args.ffile, args.tdir, args.chunksz)
    