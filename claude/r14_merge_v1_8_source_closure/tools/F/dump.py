import sys
p=sys.argv[1]; out=sys.argv[2]; ls=[int(x) for x in sys.argv[3].split(',')]
L=open(p,encoding='utf-8').read().split('\n')
with open(out,'w',encoding='utf-8') as f:
    for n in ls:
        f.write(f'@@@ L{n}\n{L[n-1]}\n\n')
