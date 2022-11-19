#!/usr/bin/env python3

import os
import glob
import tarfile
import argparse

import xml.etree.ElementTree as Etree


def filter_cc(data_dir: str,
              cc_min: int = 0,
              cc_max: int = 100,
              operation: str = 'extract',
              delete: bool = True):
    """Filter files based on their cloud coverage.

    :param data_dir: Path to the directory containing Venus data
    :param cc_min: Minimal desired cloud coverage in percents (inclusive)
    :param cc_max: Maximal desired cloud coverage in percents (inclusive)
    :param operation: What to do with the findings
        * report: Print suiting files on the standard output
        * extract: Extract the DBL archives for the suiting scenes
    :param delete: Whether to delete the ones that do not suit the desired
        cloud coverage
    """
    filtered_files = []
    xmlns = '{http://eop-cfi.esa.int/CFI}'

    metadata_files = glob.glob(os.path.join(data_dir, '*HDR'))

    for md_file in metadata_files:
        with open(os.path.join(data_dir, md_file)) as md:
            md_xml = Etree.ElementTree(Etree.fromstring(md.read()))

        root = md_xml.getroot()

        cc = root.find(
            xmlns + 'Variable_Header').find(
            xmlns + 'Specific_Product_Header').find(
            xmlns + 'Product_Information').find(
            xmlns + 'Cloud_Percentage')

        if cc_min <= int(cc.text) <= cc_max:
            if operation == 'report':
                print(md_file[:-3] + '*')
            if operation == 'extract':
                # extract DBL and remove the archive
                archive_path = os.path.join(data_dir, md_file[:-3] + 'DBL')
                with tarfile.open(archive_path) as tar:
                    def is_within_directory(directory, target):
                        
                        abs_directory = os.path.abspath(directory)
                        abs_target = os.path.abspath(target)
                    
                        prefix = os.path.commonprefix([abs_directory, abs_target])
                        
                        return prefix == abs_directory
                    
                    def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                    
                        for member in tar.getmembers():
                            member_path = os.path.join(path, member.name)
                            if not is_within_directory(path, member_path):
                                raise Exception("Attempted Path Traversal in Tar File")
                    
                        tar.extractall(path, members, numeric_owner=numeric_owner) 
                        
                    
                    safe_extract(tar, path=data_dir)
                os.remove(archive_path)
        elif delete is True:
            # remove metadata and the DBL archive of the scenes not meeting
            # the criteria
            for f in glob.glob(os.path.join(data_dir, md_file[:-3] + '*')):
                os.remove(f)

    return filtered_files


def _str2bool(string_val):
    """Transform a string looking like a boolean value to a boolean value.

    This is needed because using type=bool in argparse actually parses strings.
    Such an behaviour could result in `--extract False` being
    misinterpreted as True (bool('False') == True).

    :param string_val: a string looking like a boolean value
    :return: the corresponding boolean value
    """
    if isinstance(string_val, bool):
        return string_val
    elif string_val.lower() in ('true', 'yes', 't', 'y', '1'):
        return True
    elif string_val.lower() in ('false', 'no', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Print list of files with the desired cloud coverage '
                    'or cleanup the directory from the undesired ones')

    parser.add_argument(
        '--data_dir',
        type=str,
        dest='data_dir',
        required=True,
        help='Path to the directory containing Venus data')
    parser.add_argument(
        '--cloud_min',
        type=int,
        dest='cc_min',
        default=0,
        help='Minimal desired cloud coverage in percents (inclusive)')
    parser.add_argument(
        '--cloud_max',
        type=int,
        dest='cc_max',
        default=0,
        help='Maximal desired cloud coverage in percents (inclusive)')
    parser.add_argument(
        '--operation',
        type=str,
        dest='operation',
        default='report',
        choices=('report', 'extract'),
        help='An operation to perform: Either to print suiting files on the '
             'standard output or to extract the DBL archives for the suiting '
             'scenes')
    parser.add_argument(
        '--delete',
        type=_str2bool,
        dest='delete',
        default=True,
        help='Whether to delete the ones that do not suit the desired cloud '
             'coverage')

    args = parser.parse_args()

    filter_cc(args.data_dir, args.cc_min, args.cc_max, args.operation,
              args.delete)
