"""Extract paragraph text of a docx to UTF-8 file. Usage: python -I docx_text.py in.docx out.txt"""
import sys, zipfile, re, html
xml = zipfile.ZipFile(sys.argv[1]).read('word/document.xml').decode('utf-8')
paras = re.findall(r'<w:p[ >].*?</w:p>', xml, flags=re.S)
with open(sys.argv[2],'w',encoding='utf-8') as f:
    for p in paras:
        t = html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p)))
        if t.strip(): f.write(t+'\n')
