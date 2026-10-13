"""Task C search: 完整資料來源 / Data Pack co-occurrence across W/01_ALL_OUTPUTS text, repo tracked files, V1.8 manuscript.
Usage: python -I task_c_search.py <W01_DIR> <REPO_DIR> <tracked_list.txt>"""
import sys, os, re, json, zipfile
sys.stdout.reconfigure(encoding='utf-8')
w01, repo, tracked = sys.argv[1:4]
P = re.compile(r'完整資料來源|Data[ _]?Pack', re.I)
TEXT = {'.md', '.txt', '.csv', '.json', '.py', '.tsv', '.yml', '.yaml', '.html', '.tex', '.log', '.ps1', '.sh', '.jsonl', '.xml', ''}
def scan_text(path, label, out):
    try:
        b = open(path, 'rb').read()
    except Exception as e:
        out.append(dict(file=label, line=0, text='READ_ERROR %s' % e)); return
    if b'\x00' in b[:4096]:
        return
    t = b.decode('utf-8', 'replace')
    for i, l in enumerate(t.split('\n'), 1):
        if P.search(l):
            out.append(dict(file=label, line=i, text=l.strip()[:400]))
def scan_office(path, label, out):
    try:
        z = zipfile.ZipFile(path)
    except Exception:
        return
    for n in z.namelist():
        if n.endswith('.xml'):
            x = z.read(n).decode('utf-8', 'replace')
            x2 = re.sub(r'<[^>]+>', '', x)
            for m in P.finditer(x2):
                out.append(dict(file=label + '::' + n, line=0, text=x2[max(0, m.start()-150):m.end()+150].replace('\n', ' ')))
res = {'W01': [], 'REPO': []}
for root, _, fs in os.walk(w01):
    for f in fs:
        p = os.path.join(root, f); ext = os.path.splitext(f)[1].lower()
        lab = os.path.relpath(p, w01)
        if ext in ('.docx', '.xlsx', '.pptx'):
            scan_office(p, lab, res['W01'])
        elif ext in TEXT:
            scan_text(p, lab, res['W01'])
for rel in open(tracked, encoding='utf-8').read().split('\n'):
    if not rel: continue
    p = os.path.join(repo, rel); ext = os.path.splitext(rel)[1].lower()
    if ext in ('.docx', '.xlsx', '.pptx'):
        scan_office(p, rel, res['REPO'])
    elif ext not in ('.png', '.jpg', '.pdf', '.zip', '.sqlite', '.db', '.gif'):
        scan_text(p, rel, res['REPO'])
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'task_c_out.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in res.items():
    print('==', k, len(v))
    for e in v:
        print(e['file'], e['line'], '|', e['text'][:300])
