#!/usr/bin/env python
import argparse
import glob
import os.path
import csv
import shutil

def parse_dirnames():
    parser = argparse.ArgumentParser(description='Correlates steering with images')
    parser.add_argument('dirnames', metavar='dirname', nargs='+', help='a directory with saved session')
    return parser.parse_args().dirnames

def read_data(logfile):
    log_line = logfile.readline()
    return map(int, log_line.strip().split('/')) if log_line else None

def save_data(writer, image_timestamp, data):
    steer_timestamp, direction = data
    writer.writerow([image_timestamp, steer_timestamp, direction, 'images/%d.jpg' % image_timestamp])

def process_session(dirname):
    image_names = map(os.path.basename, glob.glob('%s/images/*.jpg' % dirname))
    image_timestamps = sorted([int(os.path.splitext(name)[0]) for name in image_names])
    with open('%s/log' % dirname, 'r') as log:
        with open('%s/data.csv' % dirname, 'wb') as csv_log:
            writer = csv.writer(csv_log, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            for image_timestamp in image_timestamps:
                data = read_data(log)
                while data and data[0] < image_timestamp:
                    data = read_data(log)
                if not data:
                    break
                save_data(writer, image_timestamp, data)
    compress_output(dirname)
 
def compress_output(dirname):
    shutil.make_archive(dirname, 'zip', root_dir=dirname)

def main():
    dirnames = parse_dirnames()
    for dirname in dirnames:
        process_session(dirname)
 
if __name__ == '__main__':
    main()
