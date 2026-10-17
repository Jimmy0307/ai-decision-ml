import re,sys,io,difflib
base=open(sys.argv[1],encoding='utf-8').read().split('\n')
new=open(sys.argv[2],encoding='utf-8').read().split('\n')
sm=difflib.SequenceMatcher(None,base,new,autojunk=False)
changed=set()
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag!='equal': changed.update(range(j1,j2))
terms={'minimal sufficient':r'最小充分|minimal suffic','complete':r'完整|完備|窮盡|complete','all enterprise':r'所有企業|all enterprise','construct validity':r'構念效度|construct validity','validated':r'驗證完成|已驗證|validated','proved':r'證明|proved|proven','theorem':r'定理|[Tt]heorem|Thm','optimal':r'最適|最佳|optimal','causal':r'因果|causal','generalizable':r'可推廣|一般化|一般形式|generaliz|任何共用平台','enterprise evidence':r'企業證據|實證|enterprise evidence','AI-specific':r'AI 特有|AI 所獨有|AI 特定|AI-specific','robust':r'穩健|robust|ROBUST','necessary':r'必要','sufficient':r'充分','iff':r'若且唯若|當且僅當|充要|iff|⇔'}
out=io.open('hits.tsv','w',encoding='utf-8')
for k,p in terms.items():
    ls=[j+1 for j in sorted(changed) if re.search(p,new[j])]
    n=sum(len(re.findall(p,new[j])) for j in changed)
    out.write(f"{k}\t{n}\t{','.join(map(str,ls))}\n")
out.close()
print(len(changed))
