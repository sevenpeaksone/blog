# -*- coding: utf-8 -*-
import glob, os, sys
from playwright.sync_api import sync_playwright

OUT = "/sessions/ecstatic-youthful-edison/mnt/ai-blog/output/news-산업IT/images"
TMP = "/tmp/imgbuild"
os.makedirs(TMP, exist_ok=True)

FONT = "'Noto Sans KR', sans-serif"

def launch(p):
    # try headless-shell channel, then glob, then full chromium
    try:
        return p.chromium.launch(channel='chromium-headless-shell', args=['--no-sandbox'])
    except Exception as e:
        print("hs channel fail:", str(e)[:80])
    bins = glob.glob('/sessions/ecstatic-youthful-edison/.cache/ms-playwright/chromium*/**/headless_shell', recursive=True)
    bins += glob.glob('/sessions/ecstatic-youthful-edison/.cache/ms-playwright/chromium*/**/chrome', recursive=True)
    for exe in bins:
        try:
            return p.chromium.launch(executable_path=exe, args=['--no-sandbox'])
        except Exception as e:
            print("exe fail", exe, str(e)[:80])
    try:
        return p.chromium.launch(channel='chromium', args=['--no-sandbox'])
    except Exception as e:
        print("chromium channel fail:", str(e)[:80])
    return p.chromium.launch(args=['--no-sandbox'])

def capture(name, html, w, h):
    path = os.path.join(TMP, name + ".html")
    out = os.path.join(OUT, name + ".png")
    full = "<!doctype html><html><head><meta charset='utf-8'><style>"+\
        "*{margin:0;padding:0;box-sizing:border-box;}"+\
        "body{font-family:"+FONT+";}"+ html["css"] +"</style></head><body>"+ html["body"] +"</body></html>"
    with open(path, "w") as f:
        f.write(full)
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        pg.goto("file://"+path)
        pg.wait_for_timeout(400)
        pg.locator("#card").screenshot(path=out)
        b.close()
    print("saved", out)

# ---------- THUMBNAIL (대표 이미지) 1200x630 가로형 ----------
thumb = {
"css": """
#card{width:1200px;height:630px;position:relative;overflow:hidden;
 background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);
 display:flex;flex-direction:column;align-items:center;justify-content:center;}
.cat{position:absolute;top:48px;left:60px;font-size:24px;letter-spacing:4px;
 color:#7aa2ff;font-weight:700;border:2px solid #3a4a7a;border-radius:30px;padding:8px 24px;}
.chips{position:absolute;top:54px;right:60px;display:flex;gap:14px;}
.chip{width:64px;height:64px;border-radius:16px;background:linear-gradient(135deg,#2a3a6a,#1d2a52);
 border:1px solid #4a5a9a;}
.chip.b{background:linear-gradient(135deg,#76c893,#2d6a4f);}
.title{font-size:74px;font-weight:900;color:#ffffff;text-align:center;line-height:1.18;
 letter-spacing:-1px;padding:0 60px;}
.title .accent{color:#7aa2ff;}
.sub{margin-top:34px;font-size:30px;color:#b8c0e0;font-weight:500;}
.stack{position:absolute;bottom:50px;left:60px;display:flex;flex-direction:column;gap:6px;}
.layer{width:150px;height:14px;border-radius:3px;background:linear-gradient(90deg,#7aa2ff,#76c893);}
.layer:nth-child(2){width:130px;opacity:.85;}
.layer:nth-child(3){width:110px;opacity:.7;}
.layer:nth-child(4){width:90px;opacity:.55;}
.bw{position:absolute;bottom:60px;right:70px;font-family:monospace;font-size:26px;color:#5a6a9a;}
""",
"body": """
<div id='card'>
 <div class='cat'>산업·IT 뉴스</div>
 <div class='chips'><div class='chip'></div><div class='chip b'></div></div>
 <div class='title'>HBM4 양산 시작<br><span class='accent'>삼성 · SK하이닉스</span> 메모리 대전</div>
 <div class='sub'>6세대 고대역폭메모리, AI 반도체의 진짜 병목</div>
 <div class='stack'><div class='layer'></div><div class='layer'></div><div class='layer'></div><div class='layer'></div></div>
 <div class='bw'>22 TB/s</div>
</div>
"""
}

# ---------- body-1: GPU=머리, HBM=혈관 비유 인포그래픽 ----------
body1 = {
"css":"""
#card{width:900px;background:#0f1530;padding:48px 56px;color:#e8ecff;}
.h{font-size:34px;font-weight:800;text-align:center;margin-bottom:8px;}
.h .a{color:#7aa2ff;}
.subh{text-align:center;color:#9aa6d0;font-size:18px;margin-bottom:40px;}
.row{display:flex;align-items:center;gap:28px;}
.box{flex:1;background:linear-gradient(135deg,#1c2550,#161d40);border:1px solid #34406e;
 border-radius:20px;padding:32px 28px;text-align:center;}
.box .ic{width:96px;height:96px;border-radius:50%;margin:0 auto 18px;display:flex;align-items:center;justify-content:center;}
.brain{background:radial-gradient(circle at 35% 30%,#9db4ff,#3a56c8);}
.brain .core{width:54px;height:54px;border-radius:14px;background:#0f1530;}
.vein{background:radial-gradient(circle at 35% 30%,#7ee0a8,#2d8a5a);}
.vein .core{width:18px;height:54px;border-radius:9px;background:#0f1530;}
.box .lab{font-size:26px;font-weight:800;margin-bottom:8px;}
.box .role{font-size:17px;color:#aab4dc;line-height:1.6;}
.conn{display:flex;flex-direction:column;align-items:center;gap:7px;color:#7aa2ff;}
.dot{width:11px;height:11px;border-radius:50%;background:#7aa2ff;}
.dot:nth-child(2){opacity:.7;}.dot:nth-child(3){opacity:.45;}
.note{margin-top:36px;background:#161d40;border-left:5px solid #7aa2ff;border-radius:0 12px 12px 0;
 padding:20px 24px;font-size:19px;line-height:1.65;color:#cdd5f5;}
.note b{color:#9ec9ff;}
""",
"body":"""
<div id='card'>
 <div class='h'>AI 반도체를 사람에 비유하면?</div>
 <div class='subh'>GPU는 머리, HBM은 그 머리에 정보를 나르는 혈관</div>
 <div class='row'>
  <div class='box'><div class='ic brain'><div class='core'></div></div><div class='lab'>GPU</div><div class='role'>'머리'<br>연산과 판단을 담당</div></div>
  <div class='conn'><div class='dot'></div><div class='dot'></div><div class='dot'></div></div>
  <div class='box'><div class='ic vein'><div class='core'></div></div><div class='lab'>HBM</div><div class='role'>'혈관'<br>데이터를 끊임없이 공급</div></div>
 </div>
 <div class='note'>혈관이 좁으면 아무리 <b>머리</b>가 좋아도 일을 빨리 처리하지 못합니다. 그래서 AI의 속도는 결국 <b>메모리의 속도</b>에서 갈립니다.</div>
</div>
"""
}

# ---------- body-2: 삼성 HBM4 성능 수치 핵심 카드 ----------
body2 = {
"css":"""
#card{width:900px;background:#0f1530;padding:48px 50px;color:#e8ecff;}
.h{font-size:32px;font-weight:800;text-align:center;margin-bottom:6px;}
.h .a{color:#76c893;}
.subh{text-align:center;color:#9aa6d0;font-size:17px;margin-bottom:36px;}
.grid{display:flex;gap:22px;}
.c{flex:1;background:linear-gradient(160deg,#1c2550,#141b3c);border:1px solid #34406e;
 border-radius:18px;padding:30px 22px;text-align:center;}
.c .big{font-size:46px;font-weight:900;color:#76c893;line-height:1.05;}
.c .unit{font-size:20px;color:#aab4dc;}
.c .cap{margin-top:14px;font-size:17px;color:#cdd5f5;font-weight:600;line-height:1.5;}
.c.blue .big{color:#7aa2ff;}
.foot{margin-top:30px;text-align:center;font-size:16px;color:#8893bd;}
""",
"body":"""
<div id='card'>
 <div class='h'>삼성전자 <span class='a'>HBM4</span> 성능 수치</div>
 <div class='subh'>업계 표준(JEDEC) 8.0Gbps를 크게 웃도는 스펙</div>
 <div class='grid'>
  <div class='c'><div class='big'>11.7</div><div class='unit'>Gbps</div><div class='cap'>동작 속도</div></div>
  <div class='c blue'><div class='big'>+46<span style='font-size:30px'>%</span></div><div class='unit'>vs 표준</div><div class='cap'>표준보다 빠름</div></div>
  <div class='c'><div class='big'>3.3</div><div class='unit'>TB/s</div><div class='cap'>스택당 대역폭<br>(직전 대비 약 2.7배)</div></div>
 </div>
 <div class='foot'>2026년 2월 세계 최초 양산 출하 · 엔비디아 '베라 루빈' 검증 통과</div>
</div>
"""
}

# ---------- body-3: 2026 HBM4 시장 점유율 도넛 차트 ----------
# conic-gradient donut: SK 54.5, 삼성 28.5, 마이크론 17
body3 = {
"css":"""
#card{width:900px;background:#0f1530;padding:48px 56px;color:#e8ecff;}
.h{font-size:32px;font-weight:800;text-align:center;margin-bottom:6px;}
.subh{text-align:center;color:#9aa6d0;font-size:17px;margin-bottom:34px;}
.wrap{display:flex;align-items:center;gap:54px;justify-content:center;}
.donut{width:300px;height:300px;border-radius:50%;
 background:conic-gradient(#7aa2ff 0 54.5%,#76c893 54.5% 83%,#e0a458 83% 100%);
 display:flex;align-items:center;justify-content:center;position:relative;}
.donut .hole{width:170px;height:170px;border-radius:50%;background:#0f1530;
 display:flex;flex-direction:column;align-items:center;justify-content:center;}
.hole .t{font-size:18px;color:#9aa6d0;}.hole .y{font-size:34px;font-weight:900;color:#fff;}
.leg{display:flex;flex-direction:column;gap:20px;}
.li{display:flex;align-items:center;gap:16px;}
.sw{width:26px;height:26px;border-radius:7px;}
.li .nm{font-size:23px;font-weight:700;width:150px;}
.li .pc{font-size:26px;font-weight:900;}
.b1{background:#7aa2ff;}.b2{background:#76c893;}.b3{background:#e0a458;}
.foot{margin-top:30px;text-align:center;font-size:15px;color:#8893bd;}
""",
"body":"""
<div id='card'>
 <div class='h'>2026년 HBM4 시장 점유율 전망</div>
 <div class='subh'>'세계 최초 양산'과 '시장 1위'는 다르다</div>
 <div class='wrap'>
  <div class='donut'><div class='hole'><div class='t'>2026</div><div class='y'>HBM4</div></div></div>
  <div class='leg'>
   <div class='li'><div class='sw b1'></div><div class='nm'>SK하이닉스</div><div class='pc' style='color:#7aa2ff'>54~55%</div></div>
   <div class='li'><div class='sw b2'></div><div class='nm'>삼성전자</div><div class='pc' style='color:#76c893'>28~29%</div></div>
   <div class='li'><div class='sw b3'></div><div class='nm'>마이크론</div><div class='pc' style='color:#e0a458'>17~18%</div></div>
  </div>
 </div>
 <div class='foot'>자료: 카운터포인트리서치 등 · 측정 대상에 따라 수치는 달라질 수 있음</div>
</div>
"""
}

# ---------- body-4: HBM 적층 12단->16단 단면 일러스트 ----------
def layers(n, color):
    s=""
    for i in range(n):
        s+="<div class='lyr' style='background:%s'></div>"%color
    return s
body4 = {
"css":"""
#card{width:900px;background:#0f1530;padding:48px 56px;color:#e8ecff;}
.h{font-size:32px;font-weight:800;text-align:center;margin-bottom:6px;}
.h .a{color:#7aa2ff;}
.subh{text-align:center;color:#9aa6d0;font-size:17px;margin-bottom:40px;}
.row{display:flex;align-items:flex-end;justify-content:center;gap:90px;}
.col{display:flex;flex-direction:column;align-items:center;}
.stk{display:flex;flex-direction:column-reverse;gap:4px;margin-bottom:18px;}
.lyr{width:170px;height:15px;border-radius:3px;}
.base{width:200px;height:22px;border-radius:5px;background:#3a4670;margin-bottom:4px;}
.cap{font-size:24px;font-weight:800;}
.cap .a{color:#7aa2ff;}
.arrow{display:flex;flex-direction:column;align-items:center;color:#76c893;font-weight:800;font-size:18px;align-self:center;margin-bottom:60px;}
.arrow .ln{width:70px;height:4px;background:#76c893;margin:8px 0;position:relative;}
.arrow .ln:after{content:'';position:absolute;right:-2px;top:-6px;border-left:14px solid #76c893;border-top:8px solid transparent;border-bottom:8px solid transparent;}
.note{margin-top:38px;background:#161d40;border-left:5px solid #76c893;border-radius:0 12px 12px 0;padding:18px 24px;font-size:18px;line-height:1.6;color:#cdd5f5;}
""",
"body":"""
<div id='card'>
 <div class='h'>다음 분수령, <span class='a'>16단</span> 적층 경쟁</div>
 <div class='subh'>메모리를 더 높이 쌓는 기술이 다음 승부처</div>
 <div class='row'>
  <div class='col'><div class='stk'>"""+layers(12,"linear-gradient(90deg,#5a78d8,#7aa2ff)")+"""<div class='base'></div></div><div class='cap'>12단 (12-Hi)</div></div>
  <div class='arrow'>2026 하반기<div class='ln'></div></div>
  <div class='col'><div class='stk'>"""+layers(16,"linear-gradient(90deg,#3da06a,#76c893)")+"""<div class='base'></div></div><div class='cap'><span class='a'>16단 (16-Hi)</span></div></div>
 </div>
 <div class='note'>엔비디아가 SK하이닉스·삼성·마이크론에 4분기까지 16단 제품 공급을 요청했습니다. 최상위급 HBM4 납품 향배는 연말께 가려질 전망입니다.</div>
</div>
"""
}

jobs = [
 ("thumbnail", thumb, 1200, 700),
 ("body-1", body1, 1000, 800),
 ("body-2", body2, 1000, 700),
 ("body-3", body3, 1000, 700),
 ("body-4", body4, 1000, 900),
]

only = sys.argv[1:] if len(sys.argv)>1 else None
for name, h, w, vh in jobs:
    if only and name not in only:
        continue
    capture(name, h, w, vh)
print("DONE")
