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
            prefix = 'pos_navcon_'
            if not (tokens[0] == 'classname' and tokens[1].startswith(prefix)):
                continue
            prefixlen = len(prefix)
            if not tokens[1][prefixlen:] in ['start', 'next']:
                continue
            kind = tokens[1][prefixlen:]
            pos, target, spawnflags = False, False, False
            targetname = "no-target-{}".format(counter)
            radius = 50
            playerclasses = []
            counter += 1
            while True:
                tokens = read_tokens()
                if tokens[0] == 'origin': pos = tokens[1:]
                elif tokens[0] == 'target': target = tokens[1]
                elif tokens[0] == 'targetname': targetname = tokens[1]
                elif tokens[0] == 'size': radius = tokens[1]
                elif tokens[0] == 'playerclasses': playerclasses = tokens[1:]
                elif tokens[0] == 'spawnflags': spawnflags = tokens[1]
                else: break
            navcons[targetname] = dict(pos=pos, target=target, targetname=targetname, radius=radius, playerclasses=playerclasses, spawnflags=spawnflags, kind=kind, done=[])
    except Done: pass
    return navcons

def main():
    navcons = read_navcon_ents()
    print("navcon 3")
    for currentname in navcons:
        start = navcons[currentname]
        if start['kind'] == 'start':
            current = start
            while 'target' in current:
                targetname = current['target']
                if not targetname in navcons:
                    break
                end = navcons[targetname]
                if currentname in end['done']:
                    break
                spos = current['pos']
                epos = end['pos']
                radius = int(start['radius'])
                twoway = int(int(start['spawnflags']) > 0)
                print(spos[0], spos[2], spos[1], epos[0], epos[2], epos[1], radius, 1, 63, twoway)
                end['done'].append(targetname)
                currentname = targetname
                current = end

if __name__ == '__main__': main()
