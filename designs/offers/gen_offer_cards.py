# Builds the per-offer carousel cards (cards 2..N + booking card) for each offer from offers.json + benefits.json.
import json, re
offers = json.load(open('offers.json', encoding='utf-8'))
ben = json.load(open('benefits.json', encoding='utf-8'))
CSS = open('offer.css', encoding='utf-8').read() + '''
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;background:#fff}
.c-model{position:absolute;left:-90px;bottom:0;width:740px;height:auto}
.c-product{position:absolute;left:-60px;bottom:220px;width:720px;height:auto}
.c-col{position:absolute;right:60px;top:300px;width:440px;text-align:right}
.c-tag{display:inline-block;background:var(--blue);color:#fff;font-weight:500;font-size:26px;padding:8px 24px;border-radius:24px}
.c-name{font-size:58px;font-weight:700;color:var(--blue);line-height:1.3;margin-top:22px}
.c-sub{font-size:28px;font-weight:400;color:var(--deepteal);margin-top:8px;line-height:1.5}
.c-ben{font-size:30px;font-weight:500;color:var(--charcoal);margin-top:28px;line-height:1.6;padding-right:18px;border-right:6px solid var(--teal)}
.c-price{display:inline-flex;align-items:center;gap:10px;direction:ltr;background:var(--blue);color:#fff;border-radius:22px;padding:10px 30px;margin-top:40px;border:6px solid #fff;box-shadow:0 6px 20px rgba(18,120,204,.22)}
.c-price b{font-size:84px;font-weight:700;line-height:1.1}
.c-price svg{width:34px;height:38px;margin-top:14px}
.c-cta{position:absolute;right:60px;bottom:70px;width:470px}
.num{position:absolute;top:70px;left:60px;font-size:24px;font-weight:600;color:var(--teal);direction:ltr}
.book{background:#0E3F6B}
.book .t{position:absolute;top:330px;width:100%;text-align:center;color:#fff;font-size:96px;font-weight:700;line-height:1.3}
.book .s{position:absolute;top:470px;width:100%;text-align:center;color:var(--ice);font-size:34px;line-height:1.5}
.book .list{position:absolute;top:560px;left:140px;right:140px;display:flex;flex-direction:column;gap:14px}
.book .li{display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,.08);border:2px solid rgba(198,234,246,.25);border-radius:16px;padding:9px 24px;color:#fff;font-size:26px}
.book .li b{direction:ltr;color:#fff;font-weight:700;font-size:32px}
.book .ft{position:absolute;left:140px;right:140px;bottom:70px;display:flex;flex-direction:column;gap:16px}
.book .chip.loc{background:transparent;border-color:rgba(198,234,246,.5);color:#fff}
'''
gen = __import__('gen_offer')  # reuse icons
BG_L = '''<svg class="bg" viewBox="0 0 1080 1350"><polygon points="1080,105 1010,150 1010,470 1080,425" fill="#C6EAF6" opacity=".55"/><polygon points="480,360 50,0 50,820 480,820" fill="#0BB0A8"/><polygon points="50,560 0,520 0,1100 50,1100" fill="#C6EAF6" opacity=".7"/></svg>'''
for o in offers:
    b = ben[o['slug']]; male = b['gender'] == 'm'
    total = len(o['rows']) + 2
    secs = []
    for i, (name, sub, price) in enumerate(o['rows']):
        img = f'<img class="c-product" src="{o["model"]}">' if o.get('product') else f'<img class="c-model" src="{o["model"]}">'
        cta = 'احجز الآن' if male else ('احجزوا الآن' if b['gender'] == 'p' else 'احجزي الآن')
        secs.append(f'''<section class="slide" id="c{i+2}">{BG_L}{img}
<img class="logo" style="left:auto;right:60px;transform:none;width:360px" src="../brand/TL_logo_primary_1024x237.png">
<div class="num" style="color:#fff;z-index:2">{i+2}/{total}</div>
<div class="c-col"><span class="c-tag">{b['tag']}</span><div class="c-name">{name}</div>{f'<div class="c-sub">{sub}</div>' if sub else ''}
<div class="c-ben">{b['b'][i]}</div><div class="c-price"><b>{price}</b>{gen.DIRHAM.replace('22 24','22 24')}</div></div>
<div class="c-cta"><div class="chip wa" style="direction:rtl;font-size:38px">{cta}</div></div></section>''')
    lis = ''.join(f'<div class="li"><span>{n}</span><b>{p} AED</b></div>' for n, s, p in o['rows'])
    secs.append(f'''<section class="slide book" id="c{total}">
<img class="logo" src="../brand/TL_logo_white_1024x237.png" style="top:110px">
<div class="num" style="color:var(--ice)">{total}/{total}</div>
<div class="t">{'احجز موعدك' if male else ('احجزوا موعدكم' if b['gender'] == 'p' else 'احجزي موعدك')}</div><div class="s">تواصل معنا على واتساب ونرتب لك الموعد المناسب</div>
<div class="list">{lis}</div>
<div class="ft"><div class="chip wa">{gen.WA}+971 7 204 4666</div><div class="chip loc">{gen.PIN.replace('#1278CC','#C6EAF6')}طريق الخور، رأس الخيمة</div></div></section>''')
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS} html,body{{height:auto;overflow:visible}}</style></head><body>{''.join(secs)}</body></html>'''
    open(f'{o["slug"]}_cards.html', 'w', encoding='utf-8').write(html)
    print('cards', o['slug'], total - 1)
