import http.server,json,os
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n=int(self.headers['Content-Length']); d=json.loads(self.rfile.read(n))
        open(os.path.join('raw',d['name']),'w').write(d['text'])
        self.send_response(200); self.send_header('Access-Control-Allow-Origin','*'); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self,*a): pass
http.server.HTTPServer(('127.0.0.1',8767),H).serve_forever()
