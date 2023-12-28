#!/usr/bin/python

#  bruteforce.py - try random numbers to login to sector 0
#
#  Adam Laurie <adam@algroup.co.uk>
#  http://rfidiot.org/
#
#  This code is copyright (c) Adam Laurie, 2006, All rights reserved.
#  For non-commercial use only, the following terms apply - for all other
#  uses, please contact the author:
#
#    This code is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#

import random
import sys
import os
import rfidiot

def main():
    try:
        card= rfidiot.card
    except:
        print("Couldn't open reader!")
        os._exit(True)

    args= rfidiot.args

    card.info('bruteforce v0.1i')
    card.select()
    print('Card ID: ' + card.uid)

    finished = 0
    tries = 0
    print(f' Tries: {tries}')
    sys.stdout.flush()

    while not finished:

        tries += 1
        if tries % 10 == 0:
            print(f' Tries: {tries}')
            sys.stdout.flush()

        if len(args) == 1:
            key= args[0]
            if len(key) != 12:
                print('  Static Key must be 12 HEX characters!')
                os._exit(True)
            print('Trying static key: ' + key)
        else:
            key = '%012x' % random.getrandbits(48)

        for card_type in ['AA', 'BB']:
            card.select()
            if card.login(0,card_type,key):
                print(f'\nlogin succeeded after {tries} tries!')
                print('key: ' + card_type + ' ' + key)
                finished = 1
                break
            if card.errorcode not in ('X', '6982','6200'):
                print('\nerror!')
                print('key: ' + card_type +  ' ' + key)
                print('error code: ' + card.errorcode)
                finished = 1
                break
        if finished:
            break
    os._exit(False)

if __name__ == '__main__':
    main()
