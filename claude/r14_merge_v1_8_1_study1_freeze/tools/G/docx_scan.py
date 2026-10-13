"""Scan docx text for re-segmentation figures. Usage: python -I docx_scan.py file.docx [...]"""
import sys, zipfile, re, hashlib, unicodedata
PATS = ['84/120','85/120','84 與 85','84–85','3,112','重切分','29/32','30/32','邊界敏感','句與子句','R14','R7','R9']
for p in sys.argv[1:]:
    h = hashlib.sha256(open(p,'rb').read()).hexdigest()
    z = zipfile.ZipFile(p)
    xml = z.read('word/document.xml').decode('utf-8')
    txt = unicodedata.normalize('NFKC', re.sub(r'<w:p[ >].*?</w:p>', lambda m: re.sub(r'<[^>]+>','',m.group(0))+'\n', xml, flags=re.S))
    txt = re.sub(r'<[^>]+>','',txt)
    core = z.read('docProps/core.xml').decode('utf-8') if 'docProps/core.xml' in z.namelist() else ''
    dates = re.findall(r'<dcterms:(created|modified)[^>]*>([^<]+)<', core)
    print('==', p, h[:16], dates)
    for k in PATS:
        print('  ', k, txt.count(unicodedata.normalize('NFKC',k)))
    for m in re.finditer(r'[^\n]{0,80}8[45]\s*/\s*120[^\n]{0,80}', txt):
        print('   CTX:', m.group(0))
