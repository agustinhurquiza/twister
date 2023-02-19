#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------
# Description A script for generate random password for
# encrypt the tookens.
# Autohor: Agustin Urquiza
# Email: agustin.h.urquiza@gmail.com
# --------------------------------------------------------

from cryptography.fernet import Fernet
import argparse


def parser() -> argparse.Namespace:
    ''' This function recolect the input arguments.
        Return:
            <class 'argparse.Namespace'>: Users atguments
    '''

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--output', type=str, required=True,
    help='Directs the output to a name of your choice')

    args = parser.parse_args()

    return args


def main() -> None:
    args = parser()

    key = Fernet.generate_key()

    with open(args.output, 'wb') as mykey:
        mykey.write(key)


if __name__ == '__main__':
    main()
