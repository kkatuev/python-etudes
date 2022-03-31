#!/bin/env python
#
# Construct contextRoot/portNumbers list from haproxy.cfg
# Accepts haproxy.cfg as stdin and outputs formatted json to stdout
# KK 2020-01-30
# v2 KK 2020-03-04
import sys
import json

keywords = [ "acl", "use_backend", "backend", "default_backend" ]
crConfig = {}
acls = {}
backends = {}
defaultEnv = "masterPort"
secondEnv = "featurePort"
waitForKeyword = True

if len(sys.argv) <= 1:
    print("Usage: hap2json.py feature-file.cfg [master-file.cfg] > output.json")
    sys.exit(1)

f = open(sys.argv[1],'r')
cfgContent = f.readlines()

if len(sys.argv) > 2:
    f = open(sys.argv[2],'r')
    cfgContent.extend(f.readlines())
    defaultEnv = "featurePort"

for line in cfgContent:
    lexems = [ w.strip() for w in line.strip().split(' ') if w ]
    if len(lexems) <= 0: continue
    try:
        lnum = keywords.index(lexems[0])
    except ValueError:
        lnum = -1
    if waitForKeyword:
        if lnum == 0:
            if lexems[2] == "url_beg":
                context = lexems[3].strip('/').replace('/','$')
                if not context: context = '$default'
                acls[lexems[1]] = context
                if context not in crConfig.keys(): crConfig[context] = { }
        elif lnum == 1:
            env = defaultEnv if len(lexems) == 4 else secondEnv
            if lexems[3] in acls.keys(): backends[lexems[1]] = [ env, lexems[3] ]
        elif lnum == 2:
            backendName = lexems[1]
            if backendName in backends.keys(): waitForKeyword = False
            if len(keywords) < 5: keywords.append('frontend')
        elif lnum == 3:
            if '$default' not in crConfig.keys(): crConfig['$default'] = {}
            acls['$default'] = '$default'
            backends[lexems[1]] = [ defaultEnv, '$default' ]
        elif lnum == 4:
            defaultEnv = "masterPort"
            secondEnv = "featurePort"
    else:
        if lexems[0] == "server":
            portNum = lexems[2].split(':')[1]
            crConfig[acls[backends[backendName][1]]][backends[backendName][0]] = int(portNum)
            crConfig[acls[backends[backendName][1]]]["ssl"] = "ssl" in lexems
            crConfig[acls[backends[backendName][1]]]["sticky"] = "cookie" in lexems
            waitForKeyword = True

print(json.dumps(crConfig, indent=2, sort_keys=True))
