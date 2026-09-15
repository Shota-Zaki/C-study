"""Authored educational SVGs and HTML components. No runtime simulation of C#."""
from __future__ import annotations
import html, json, unicodedata
from pathlib import Path
E=html.escape

def split_text(s: str, width: int = 29) -> list[str]:
    lines=[]; line=''; used=0
    for c in s:
        w=2 if unicodedata.east_asian_width(c) in 'WF' else 1
        if used+w>width:
            lines.append(line);line='';used=0
        line+=c;used+=w
    if line:lines.append(line)
    return lines or ['']

class SVG:
    def __init__(self, title:str, desc:str, height:int=350):
        self.height=height
        self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 {height}" role="img" aria-labelledby="title desc"><title id="title">{E(title)}</title><desc id="desc">{E(desc)}</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#5c6b82"/></marker></defs><style>text{{font-family:system-ui,-apple-system,\'Segoe UI\',\'Noto Sans CJK JP\',sans-serif;fill:#243248}}.small{{font-size:14px;fill:#53627a}}.label{{font-size:17px;font-weight:700}}.tag{{font-size:12px;font-weight:700;fill:#4f46e5}}.mono{{font-family:ui-monospace,Consolas,monospace}}</style><rect width="760" height="{height}" rx="14" fill="#f8fafc"/>']
    def text(self,x,y,text,cls='label',anchor='middle'):
        self.parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{E(str(text))}</text>')
    def path(self,d,arrow=True,dash=False):
        self.parts.append(f'<path d="{d}" fill="none" stroke="#5c6b82" stroke-width="2"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="6 5"' if dash else '')+'/>')
    def box(self,x,y,w,h,title,sub='',tint=False,tag=None):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="'+('#eef2ff' if tint else '#ffffff')+'" stroke="'+('#a5b4fc' if tint else '#cbd5e1')+'" stroke-width="1.5"/>')
        tl=split_text(title,max(16,int((w-28)/8.7)));sl=split_text(sub,max(18,int((w-25)/7.3)))
        total=len(tl)*23+(len(sl)*21+7 if sub else 0);sy=y+(h-total)/2+18
        for i,t in enumerate(tl):self.text(x+w/2,sy+23*i,t)
        if sub:
            for i,t in enumerate(sl):self.text(x+w/2,sy+len(tl)*23+7+21*i,t,'small')
        if tag:self.text(x+13,y+20,tag,'tag','start')
    def diamond(self,x,y,w,h,title,sub=''):
        self.parts.append(f'<path d="M{x+w/2} {y}L{x+w} {y+h/2}L{x+w/2} {y+h}L{x} {y+h/2}Z" fill="#eef2ff" stroke="#a5b4fc" stroke-width="1.5"/>')
        self.text(x+w/2,y+h/2-2,title);self.text(x+w/2,y+h/2+23,sub,'small')
    def finish(self):return ''.join(self.parts)+'</svg>\n'

def diagram_svg(number:str, data:dict)->str:
    d=data['diagram']; n=d['nodes']; kind=d['kind']
    s=SVG(d['title'],d['caption'],390 if number in ('05','13','24') else 350)
    if number=='05':
        s.box(30,25,220,62,'小計 4200円','会員 = true')
        s.path('M140 87V113');s.diamond(30,115,220,95,'5000円以上?','4200 >= 5000')
        s.path('M250 162H460');s.text(350,149,'true','tag');s.box(465,129,240,66,'送料 0円','5000円以上の注文')
        s.path('M140 210V237');s.text(171,230,'false','tag');s.diamond(30,238,220,94,'会員か?','true')
        s.path('M250 285H460');s.text(350,271,'true','tag');s.box(465,252,240,66,'送料 300円','今回選ばれる結果',True)
        s.path('M140 332V362H460');s.text(305,350,'false','tag');s.box(465,338,240,39,'非会員：送料600円')
    elif number=='13':
        s.text(40,34,'値型：代入した値は別々','label','start')
        s.box(40,58,220,78,'a = 3','変更後も 3');s.box(395,58,280,78,'b = a → b = 9','bの値だけが変わる',True)
        s.path('M260 95H390');s.text(325,82,'値をコピー','tag')
        s.text(40,180,'参照型：参照をコピーすると同じ実体を指す','label','start')
        s.box(40,207,200,60,'first');s.box(40,297,200,60,'second')
        s.box(405,235,290,95,'List オブジェクトA','[ノート, ペン]',True)
        s.path('M240 237H315V265H400');s.path('M240 327H315V302H400')
        s.text(448,366,'second.Addでfirstから見える要素も増える','small')
    elif number=='06':
        s.text(380,32,'配列の添字は 0 から始まる')
        for i,(value,total) in enumerate([(120,120),(90,210),(150,360)]):
            x=42+i*240;s.box(x,67,195,79,str(value)+' 分',f'index {i}',i==2)
            s.path(f'M{x+98} 146V210');s.box(x,214,195,66,f'total = {total}',f'{[0,120,210][i]} + {value}')
            if i<2:s.path(f'M{x+195} 247H{x+234}')
        s.text(380,322,'合計は 0 → 120 → 210 → 360 の順に更新される','small')
    elif number=='03':
        s.text(190,35,'整数同士の除算');s.text(570,35,'除算より前に型変換')
        s.box(38,60,302,83,'7 / 2','int / int');s.box(418,60,302,83,'(double)7 / 2','double / int',True)
        s.path('M190 143V187');s.path('M570 143V187')
        s.box(38,193,302,87,'結果 3','代入先をdoubleにしても3のまま');s.box(418,193,302,87,'結果 3.5','小数部分を含む結果',True)
        s.text(380,324,'演算に使う型によって、除算の結果が変わる','small')
    elif number=='24':
        s.text(30,33,'時間の流れ →','small','start');s.path('M200 29H708')
        s.text(35,100,'Task A','label','start');s.text(35,190,'Task B','label','start')
        s.box(190,65,340,65,'10を返す処理','完了まで待機');s.box(190,155,205,65,'20を返す処理','先に完了')
        s.path('M530 97H595V270');s.path('M395 187H565V270')
        s.box(365,277,340,65,'await Task.WhenAll(a, b)','結果は [10, 20]',True)
        s.text(380,373,'完了した順番ではなく、WhenAllに渡したTaskの順番','small')
    elif number=='18':
        s.text(380,30,'価格が200円以上の商品を抽出し、表示用に変換')
        for i,(a,b) in enumerate([('ノート','200'),('ペン','120'),('ファイル','500')]):
            s.box(28,50+i*90,186,69,a,b+'円',i!=1)
        s.box(271,105,198,98,'Where','price >= 200',True)
        s.path('M214 84H242V131H266');s.path('M214 264H242V174H266')
        s.path('M214 174H245',False,True);s.text(248,204,'除外','small')
        s.path('M469 154H510');s.box(515,58,220,75,'Select','名前と価格を文字列へ')
        s.path('M625 133V179');s.box(515,185,220,111,'ToArray','ノート: 200円 / ファイル: 500円',True)
    elif kind in ('compare','collections') or number=='20':
        for i,(a,b) in enumerate(n):s.box(32+(i%2)*380,36+(i//2)*147,316,112,a,b,i>=2)
    elif number=='11':
        s.box(230,22,300,68,'Notification 型','共通の Send(string) 呼び出し',True)
        s.path('M380 90V118H190V155');s.path('M380 118H570V155')
        s.box(30,161,315,91,'EmailNotification','override → メールを出力')
        s.box(415,161,315,91,'ScreenNotification','override → 画面へ出力')
        s.text(380,310,'実体の型に応じたoverrideが呼ばれる。','small')
    elif kind in ('objects','dispatch'):
        s.box(235,20,290,70,*n[0],True);s.path('M380 90V116');s.box(235,121,290,73,*n[1]);s.path('M380 194V214H188V238');s.path('M380 214H573V238')
        s.box(32,244,310,80,*n[2],True);s.box(417,244,310,80,*n[3],True)
    elif kind=='scope':
        for i,(a,b) in enumerate(n):
            s.parts.append(f'<rect x="{26+i*60}" y="{20+i*73}" width="{705-i*90}" height="{305-i*73}" rx="10" fill="'+(['#edf2ff','#f3f6ff','#fff','#f8fafc'][i])+'" stroke="#cbd5e1"/>')
            s.text(48+i*60,48+i*73,a,'label','start');s.text(235+i*60,48+i*73,b,'small','start')
    elif number=='19':
        s.box(30,27,300,90,'query = source.Where(...)','条件だけを定義');s.box(423,27,307,90,'snapshot = query.ToList()','この時点の結果 [2]',True)
        s.path('M330 72H418');s.path('M180 117V190');s.box(30,195,300,95,'source.Add(4)','元データに4を追加');s.path('M330 242H418');s.box(423,195,307,95,'query を列挙','変更後の元データ → [2, 4]',True)
        s.text(380,328,'snapshot の要素は [2] のまま。query は列挙する時点で評価。','small')
    elif kind in ('http','pipeline','boundary','resource','async','test','branch','timeline'):
        # Zigzag layout, readable labels rather than narrow mini boxes.
        s.box(28,37,315,102,*n[0]);s.box(417,37,315,102,*n[1],True)
        s.box(28,211,315,102,*n[3],True);s.box(417,211,315,102,*n[2])
        s.path('M343 88H411');s.path('M575 139V205');s.path('M417 262H350')
        for i,(x,y) in enumerate([(47,59),(436,59),(436,233),(47,233)],1):s.text(x,y,str(i),'tag')
    else:
        for i,(a,b) in enumerate(n):s.box(32+(i%2)*380,36+(i//2)*147,316,112,a,b,i>=2)
    return s.finish()

def codebox(raw:str,kind:str='csharp',label:str|None=None)->str:
    label=label or ('C# · Webプロジェクト' if kind=='csharp-web' else 'C# · Program.cs')
    return f'<div class="codebox" data-code-kind="{E(kind)}"><div class="codehead"><span>{E(label)}</span><button class="copy-btn" type="button" data-copy>コピー</button><button class="copy-btn" type="button" data-wrap-code aria-pressed="false">折り返し</button></div><pre tabindex="0"><code class="language-{E(kind)}">{E(raw)}</code></pre></div>'

def diagram_html(number:str,data:dict,base:str)->str:
    d=data['diagram']
    return f'<section class="visual-section" id="visual-model"><h2 id="visual-heading">図解：{E(d["title"])}</h2><figure class="lesson-diagram"><div class="diagram-scroll" role="region" aria-label="{E(d["title"])}" tabindex="0"><img src="{base}assets/diagrams/lesson-{number}.svg" width="760" height="{390 if number in ("05","13","24") else 350}" alt="{E(d["title"]+"。"+"。".join(a+"："+b for a,b in d["nodes"]))}" loading="lazy"/></div><figcaption>{E(d["caption"])}</figcaption></figure></section>'

def case_html(number:str,data:dict,base:str,detail=False)->str:
    c=data['detail' if detail else 'case'];which='detail' if detail else 'case'
    title=('境界・比較例：' if detail else '実例：')+c['title']
    intro=c.get('note','') if detail else c['context']
    walk=''
    if not detail:
        walk='<h3 id="case-steps">処理と値の変化</h3><ol class="value-walk">'+''.join(f'<li><b>{E(a)}</b><span>{E(b)}</span></li>' for a,b in c['walk'])+'</ol>'
        walk+=f'<div class="change-note"><strong>条件を変えた場合</strong><p>{E(c["change"])}</p></div>'
    return f'<section class="worked-example" id="worked-{which}"><div class="section-kicker">{E("境界値・比較" if detail else "実コード例")}</div><h2 id="worked-{which}-heading">{E(title)}</h2><p>{E(intro)}</p>{codebox(c["code"],c.get("kind","csharp"))}<div class="expected-result"><h3>想定出力{E("・HTTP応答" if c.get("kind")=="csharp-web" else "")}</h3><pre tabindex="0"><code>{E(c["output"])}</code></pre></div>{walk}<a class="sample-download" href="{base}samples/visual/{number}/{which}/example.zip" download>サンプル一式</a> <a class="sample-download" href="{base}samples/visual/{number}/{which}/Program.cs" download="Lesson{number}-{which}.cs">Program.cs</a></section>'
