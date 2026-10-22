import json
def flat(kids):
    out=[]
    for k in kids:
        if 'frag' in k: out+=flat(k['frag'])
        else:
            if 'kids' in k: k['kids']=flat(k['kids'])
            out.append(k)
    # merge adjacent text
    m=[]
    for k in out:
        if 't' in k and m and 't' in m[-1]: m[-1]={'t':m[-1]['t']+k['t']}
        else: m.append(k)
    return m
def sig(n):
    if 't' in n: return 'T'
    return n['tag']+'#'+str(n['tpl'])+'['+','.join(sig(k) for k in n['kids'])+']'
def load(S,key):
    d=json.load(open(f'{S}/extract/{key}.json'))
    for w in d: d[w]['sections']=flat(d[w]['sections'])
    return d
