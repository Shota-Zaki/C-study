from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import shutil,http.server,json,hashlib
repo=Path('/Users/zaki/Documents/Codex/2026-10-02/task-6/cstudy-isolated');root=Path('/Users/zaki/Documents/Codex/2026-10-02/task-6/browser-fixture');root.mkdir(exist_ok=True)
files=set(repo.glob('*.html'))
for name in ['lessons','deep-dives','guides','projects']:files.update((repo/name).glob('*.html'))
for name in ['assets','samples/visual']:files.update(p for p in (repo/name).rglob('*') if p.is_file())
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for attr,value in attrs:
   if attr not in ['src','href'] or not value:continue
   url=urlsplit(value)
   if url.scheme or url.netloc or not url.path:continue
   target=(self.page.parent/unquote(url.path)).resolve()
   if url.path.endswith('/'):target/= 'index.html'
   assert repo in target.parents and target.is_file(),(self.page,value)
   files.add(target)
parser=Links()
for page in list(files):
 if page.suffix=='.html':parser.page=page;parser.feed(page.read_text())
for p in files:
 dst=root/'course'/p.relative_to(repo);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(root),**kwargs)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
report={'port':server.server_port,'root':str(root),'sourceSHA':'c50c2ae70634fa43edb41f8c57784148f5f06b5b','files':len(files),'hashes':{str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
(root/'fixture.json').write_text(json.dumps(report,indent=2)+'\n');print('Local origin http://127.0.0.1:'+str(server.server_port)+'/course/',flush=True)
server.serve_forever()
