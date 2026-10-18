import sys,re,json
sys.stdout.reconfigure(encoding='utf-8')
t=open(sys.argv[1],encoding='utf-8').read().split('\n')
TERMS={'企業決策介面':'企業決策介面','企業決策過程':'企業決策過程','企業決策機制':'企業決策機制','組織決策安排':'組織決策安排',
'最小充分/minimal sufficient':r'最小充分|minimal(ly)? sufficien','完整/complete':r'完整|完備|窮盡|[Cc]omplete\b|exhaustive',
'非冗餘/non-redundant':r'非冗餘|non-redundan','必要/necessary':r'必要|[Nn]ecessary','充分/sufficient':r'充分|[Ss]ufficien',
'若且唯若/iff':r'若且唯若|充要|\biff\b','定理/theorem':r'定理|Thm |[Tt]heorem','驗證/validated':r'已驗證|驗證完成|[Vv]alidated',
'構念效度/construct validity':r'構念效度|[Cc]onstruct valid','實證/empirical':r'實證|[Ee]mpirical','AI 特有/AI-specific':r'AI 特有|AI 特定|AI 所獨有|AI-specific',
'最適/optimal':r'最適|最佳|[Oo]ptimal','可推廣/generalizable':r'可推廣|可外推|[Gg]eneraliz|外部效度'}
out=[];cnt={}
for k,p in TERMS.items():
    n=0
    for i,l in enumerate(t,1):
        for m in re.finditer(p,l):
            n+=1; out.append(f"{k}\tL{i}\t{l[max(0,m.start()-50):m.end()+50]}")
    cnt[k]=n
open(sys.argv[2],'w',encoding='utf-8').write('\n'.join(out))
print(json.dumps(cnt,ensure_ascii=False,indent=0))
