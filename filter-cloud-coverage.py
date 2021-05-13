#!/usr/bin/env python3

import os
import glob
import argparse

import xml.etree.ElementTree as Etree


def filter_cc(data_dir: str,
              cc_min: int = 0,
              cc_max: int = 100,
              operation: str = 'report'):
    """Filter files based on their cloud coverage.

    :param data_dir: Path to the directory containing Venus data
    :param cc_min: Minimal desired cloud coverage in percents (inclusive)
    :param cc_max: Maximal desired cloud coverage in percents (inclusive)
    :param operation: What to do with the findings
        * report: Print suiting files on the standard output
        * delete: Delete the ones that do not suit the desired cloud coverage
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
        elif operation == 'delete':
            for f in glob.glob(os.path.join(data_dir, md_file[:-3] + '*')):
                os.remove(f)

    return filtered_files


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
        choices=('report', 'delete'),
        help='An operation to perform: Either to print suiting files on the '
             'standard output or to delete the ones that do not suit the '
             'desired cloud coverage')

    args = parser.parse_args()

    filter_cc(args.data_dir, args.cc_min, args.cc_max, args.operation)
