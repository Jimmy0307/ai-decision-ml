"""Search text files for 84/85-of-120 re-segmentation figure variants. Usage: python -I find_84_85.py OUT.tsv ROOT [ROOT...]"""
import os, re, sys, unicodedata
PAT = re.compile(r"(8[45]\s*(?:[-–—~～]\s*8[45])?\s*(?:/|／|of|格|個|之)\s*(?:the\s*)?120)|(84\s*[-–—~～、與和/]\s*85)|(84\s*(?:and|與|和|、)\s*85)|(84[^\n]{0,40}120)")
EXT = {'.md','.txt','.csv','.json','.jsonl','.py','.html','.tex','.tsv','.yaml','.yml','.xml','.js'}
out = open(sys.argv[1],'w',encoding='utf-8')
n=0
for root in sys.argv[2:]:
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ('.git','__pycache__')]
        for f in fn:
            p = os.path.join(dp,f)
            if os.path.splitext(f)[1].lower() not in EXT: continue
            if os.path.getsize(p) > 5_000_000: continue
            try: txt = open(p,encoding='utf-8',errors='replace').read()
            except Exception as e: print('ERR',p,e); continue
            for i,line in enumerate(txt.splitlines(),1):
                nl = unicodedata.normalize('NFKC',line)
                m = PAT.search(nl)
                if m:
                    s = max(0,m.start()-150); 
                    out.write(f"{p}\t{i}\t{nl[s:m.end()+150]}\n"); n+=1
print('hits',n)
