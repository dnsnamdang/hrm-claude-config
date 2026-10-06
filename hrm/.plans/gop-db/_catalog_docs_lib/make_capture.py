# -*- coding: utf-8 -*-
"""Sinh file JS chụp ảnh cho 1 màn từ capture_tpl.js. Ảnh ra .playwright-mcp/cat/<slug>/shots/, icon ra .../icons/.
Dùng: python3 make_capture.py <slug> '<json params>'  -> in đường dẫn file JS để chạy bằng browser_run_code_unsafe(filename=...)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
slug, params = sys.argv[1], json.loads(sys.argv[2])
base = os.path.join('.playwright-mcp', 'cat', slug)
os.makedirs(os.path.join(base, 'shots'), exist_ok=True)
os.makedirs(os.path.join(base, 'icons'), exist_ok=True)
params.setdefault('base', 'http://127.0.0.1:3002')
params['dir'] = base + '/shots/'
tpl = open(os.path.join(HERE, 'capture_tpl.js')).read().replace('__PARAMS__', json.dumps(params, ensure_ascii=False))
out = os.path.join('.playwright-mcp', 'cap_%s.js' % slug)
open(out, 'w').write(tpl)
print(out)
