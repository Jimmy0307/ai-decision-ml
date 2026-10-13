import sys, difflib, re, io
a=open(sys.argv[1],encoding='utf-8').read().splitlines(); b=open(sys.argv[2],encoding='utf-8').read().splitlines()
out=io.StringIO()
print("# Changed-line segment diff (v1.7 -> v1.8)\n",file=out)
for i,(x,y) in enumerate(zip(a,b),1):
    if x==y: continue
    sm=difflib.SequenceMatcher(None,x,y,autojunk=False)
    segs=[(x[i1:i2],y[j1:j2]) for t,i1,i2,j1,j2 in sm.get_opcodes() if t!='equal']
    print(f"## L{i}",file=out)
    for o,n in segs: print(f"- OLD: {o[:300]!r}\n  NEW: {n[:300]!r}",file=out)
open(sys.argv[3],'w',encoding='utf-8').write(out.getvalue())
# phase10
pats=["32 pairs were confirmed by human validation","human validation confirmed the robust core","structural hole","enterprise ROI demonstrated","empirically validated enterprise model","optimal enterprise AI configuration identified","V7 complete","human construct validity complete","結構洞","人工驗證確認","人工驗證證實","V7 已完成","企業 ROI","最適企業"]
res=[]
for p in pats:
    hits=[(i,l) for i,l in enumerate(b,1) if p.lower() in l.lower()]
    res.append((p,hits))
w=open(sys.argv[4],'w',encoding='utf-8')
for p,h in res:
    w.write(f"=== {p} : {len(h)}\n")
    for i,l in h:
        k=l.lower().find(p.lower()); w.write(f"L{i}: ...{l[max(0,k-80):k+len(p)+80]}...\n")
