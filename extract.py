#!/usr/bin/env python3

# run this command:
#   cat chasm.map | python3 extract.py
# TODO:
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
            if not (tokens[0] == 'classname' and tokens[1].startswith(prefix)): continue
            kind = tokens[1][len(prefix):]
            if not kind in ['start', 'next']: continue
            pos, target, radius, playerclasses, spawnflags = [], "", 50, set(), 0
            targetname = "no-target-{}".format(counter)
            counter += 1
            while True:
                tokens = read_tokens()
                if tokens[0] == 'origin': pos = tokens[1:]
                elif tokens[0] == 'target': target = tokens[1]
                elif tokens[0] == 'targetname': targetname = tokens[1]
                elif tokens[0] == 'size':
                    try: radius = float(tokens[1])
                    except ValueError: pass
                elif tokens[0] == 'playerclasses': playerclasses = tokens[1:]
                elif tokens[0] == 'spawnflags':
                    try: spawnflags = int(tokens[1])
                    except ValueError: pass
                else: break
            navcons[targetname] = dict(pos=pos, target=target, targetname=targetname, radius=radius, playerclasses=playerclasses, spawnflags=spawnflags, kind=kind, done=[])
    except Done: pass
    return navcons

teams = dict(humans=['human_naked', 'human_bsuit'], aliens=['builder', 'builderupg', 'level0', 'level1', 'level2', 'level2upg', 'level3', 'level3upg', 'level4'])

def main():
    navcons = read_navcon_ents()
    classnavcons, allclassnames = dict(), set()
    for teamname in teams:
        for classname in teams[teamname]:
            classnavcons[classname] = []
            allclassnames.add(classname)
    for currentname in navcons:
        start = navcons[currentname]
        classnames = set()
        for classname in start['playerclasses']:
            if not classname: continue
            if classname in teams: classnames = classnames.union(teams[classname])
            else: classnames.add(classname)
        if not classnames: classnames = allclassnames
        if start['kind'] == 'start':
            current = start
            while 'target' in current:
                targetname = current['target']
                if not targetname in navcons: break
                end = navcons[targetname]
                if currentname in end['done']: break
                spos, epos = current['pos'], end['pos']
                if spos and epos:
                    radius = start['radius']
                    twoway = int(start['spawnflags'] > 0)
                    line = '{} {} {} {} {} {} {} {} {} {}'.format(spos[0], spos[2], spos[1], epos[0], epos[2], epos[1], radius, 1, 63, twoway)
                    for classname in classnames: classnavcons[classname].append(line)
                end['done'].append(targetname)
                currentname = targetname
                current = end
    for requestedclassname in sys.argv[1:2]:
        print("navcon 3")
        if requestedclassname in classnavcons:
            for line in classnavcons[requestedclassname]: print(line)

if __name__ == '__main__': main()
