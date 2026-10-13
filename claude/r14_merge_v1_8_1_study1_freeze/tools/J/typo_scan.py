import re,sys
L=open(sys.argv[1],encoding='utf-8').read().split('\n')
out=open(sys.argv[2],'w',encoding='utf-8')
pats=[r'([一-鿿])\1(?!\1)', r'[，。；、：]{2,}', r'（（|））|〔〔|〕〕', r'\b(the the|a a|of of|to to|and and)\b', r'[一-鿿] {2,}[一-鿿]',r'[，。；][，。；]']
ok2=set('們個常漸每步重往層談看慢天年月日人時處種項輕稍偶點一明分剛紛隱略僅久頻屢再層多多常刻')
for i,x in enumerate(L,1):
    if x.startswith('|') and set(x)<=set('|-: '): continue
    for p in pats:
        for m in re.finditer(p,x):
            if p.startswith('([') and m.group(1) in ok2: continue
            s=max(0,m.start()-25); out.write(f"L{i} {p[:12]} :: {x[s:m.end()+25]}\n")
    # bracket balance
    for a,b in ['（）','〔〕','「」','『』','()','[]']:
        if x.count(a)!=x.count(b): out.write(f"L{i} UNBAL {a}{b} {x.count(a)}/{x.count(b)} :: {x[:80]}\n")
