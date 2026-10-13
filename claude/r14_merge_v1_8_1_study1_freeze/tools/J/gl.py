import re,sys
L=open(sys.argv[1],encoding='utf-8').read().split('\n')
G=re.compile(r'G(0[1-9]|1[0-6])\b')
for n in map(int,sys.argv[2].split(',')):
    print(n, bool(G.search(L[n-1])), G.findall(L[n-1])[:5])
