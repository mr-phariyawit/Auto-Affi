#!/usr/bin/env python3
"""Build index.html from template.html by inlining the data files. Run from this folder: python3 build.py"""
import os
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n)).read()
s = rd('template.html')
for tag, f in (('IMGS', 'imgs.json'), ('UNDER', 'under.json'), ('REAL', 'real.json'), ('INSET_REAL', 'inset_real.json'), ('SND', 'snd.json')):
    marker = '/*__%s__*/{}' % tag
    assert marker in s, marker
    s = s.replace(marker, rd(f))
open(os.path.join(here, 'index.html'), 'w').write(s); print('index.html', len(s), 'bytes')
