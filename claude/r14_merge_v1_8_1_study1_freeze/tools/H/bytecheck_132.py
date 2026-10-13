import sys, re
a=open(sys.argv[1],'rb').read().decode('utf-8'); b=open(sys.argv[2],'rb').read().decode('utf-8')
b2=re.sub(r'〔VERIFIED_SOURCE: [^〕]*〕','〔2026-09-29 紀錄，待核〕',b)
print('BYTE_IDENTICAL_AFTER_REVERTING_FLAGS', a==b2, len(re.findall('VERIFIED_SOURCE',b)))
