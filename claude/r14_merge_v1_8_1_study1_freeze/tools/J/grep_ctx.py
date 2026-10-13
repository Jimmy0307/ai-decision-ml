import re, sys
L=open(sys.argv[1],encoding='utf-8').read().split('\n')
pats=sys.argv[3].split('|')
out=open(sys.argv[2],'w',encoding='utf-8')
for i,x in enumerate(L,1):
    for p in pats:
        for m in re.finditer(re.escape(p),x):
            s=max(0,m.start()-150); out.write(f"L{i} [{p}] ...{x[s:m.end()+150]}...\n")
