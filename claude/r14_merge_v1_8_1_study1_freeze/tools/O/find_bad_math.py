"""Convert each math span separately with pandoc to locate TeX that pandoc cannot turn into OMML."""
import sys, re, subprocess, pypandoc
md = open(sys.argv[1], encoding='utf-8').read()
pandoc = pypandoc.get_pandoc_path()
spans = []
for m in re.finditer(r'\$\$(.+?)\$\$', md, flags=re.S): spans.append(('display', m.start(), m.group(0)))
nod = re.sub(r'\$\$.+?\$\$', lambda m: ' ' * len(m.group(0)), md, flags=re.S)
for m in re.finditer(r'(?<![\$])\$(?!\s)[^$\n]+?(?<!\s)\$(?!\d)', nod): spans.append(('inline', m.start(), m.group(0)))
for m in re.finditer(r'\\[(.+?)\\]', md, flags=re.S): spans.append(('bracket', m.start(), m.group(0)))
for kind, pos, s in spans:
    p = subprocess.run([pandoc, '-f', 'markdown+tex_math_dollars+tex_math_single_backslash', '-t', 'docx', '-o', 'NUL', '--verbose'],
                       input=s, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if 'Could not convert TeX math' in p.stderr:
        line = md.count('\n', 0, pos) + 1
        print(kind, 'L%d' % line, repr(s[:400])); print('  ', [l for l in p.stderr.splitlines() if 'TeX' in l or 'unexpected' in l.lower()][:4])
