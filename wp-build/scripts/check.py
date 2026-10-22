import sys; sys.path.insert(0,sys.argv[1]+'/scripts')
from common import *
S=sys.argv[1]
for key in 'about design repairs ewp load loader forklift telehandler crane'.split():
    d=load(S,key)
    base=[sig(s) for s in d['1440']['sections']]
    bad=[]
    for w in d:
        cur=[sig(s) for s in d[w]['sections']]
        for i,(a,b) in enumerate(zip(base,cur)):
            if a!=b: bad.append((w,d['1440']['sections'][i].get('label')))
        if len(cur)!=len(base): bad.append((w,'count'))
    print(key, 'hov',len(d['1440']['hov']), 'MISMATCH' if bad else 'ok', bad)
