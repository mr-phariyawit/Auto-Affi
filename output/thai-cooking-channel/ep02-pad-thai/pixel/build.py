#!/usr/bin/env python3
"""Build index.html from template.html by inlining the data files."""
import os
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n)).read()
s = rd('template.html')
for tag, fn in (('IMGS', 'imgs.json'), ('UNDER', 'under.json'), ('REAL', 'real.json'), ('INSET_REAL', 'inset_real.json'), ('SND', 'snd.json')):
    marker = '/*__%s__*/{}' % tag
    assert marker in s, 'marker not found: ' + marker
    s = s.replace(marker, rd(fn))
out = os.path.join(here, 'index.html')
open(out, 'w').write(s)
print('index.html', len(s) // 1024, 'kB')
