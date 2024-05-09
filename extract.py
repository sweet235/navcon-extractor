#!/usr/bin/env python3

# run this command:
#   cat chasm.map | python3 extract.py
# TODO in .map:
#   specify radius
# TODO in this file:
#   consider twoway information
#   output different files for different classes

import sys

class Done(Exception): pass

def read_tokens():
    line = sys.stdin.readline()
    if not line: raise Done()
    else: return line.strip().replace('"', '').split(' ')

def read_navcon_ents():
    navcons = {}
    try:
        counter = 0
        while True:
            tokens = read_tokens()
            if tokens[0] != '{': continue
            tokens = read_tokens()
            if not (tokens[0] == 'classname' and tokens[1].startswith('pos_navcon')):
                continue
            if not tokens[1][len('pos_navcon'):] in ['_start', '_next']:
                continue
            type = tokens[1][len('pos_navcon_'):]
            pos, target, spawnflags = False, False, False
            targetname = "no-target-{}".format(counter)
            playerclasses = []
            counter += 1
            while True:
                tokens = read_tokens()
                if tokens[0] == 'origin': pos = tokens[1:]
                elif tokens[0] == 'target': target = tokens[1]
                elif tokens[0] == 'targetname': targetname = tokens[1]
                elif tokens[0] == 'playerclasses': classes = tokens[1:]
                elif tokens[0] == 'spawnflags': spawnflags = tokens[1]
                else: break
            navcons[targetname] = dict(pos=pos, target=target, targetname=targetname, type=type, playerclasses=classes, spawnflags=spawnflags)
    except Done: pass
    return navcons

def main():
    navcons = read_navcon_ents()
    print("navcon 3")
    for key in navcons:
        start = navcons[key]
        try:
            end = navcons[start['target']]
        except KeyError:
            end = False
        if end:
            spos = start['pos']
            epos = end['pos']
            radius = 50
            twoway = int(int(start['spawnflags']) > 0)
            print(spos[0], spos[2], spos[1], epos[0], epos[2], epos[1], radius, 1, 63, twoway)

if __name__ == '__main__': main()
