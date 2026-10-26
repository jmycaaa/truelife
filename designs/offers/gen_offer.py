# Builds single-image offer posts (1080x1350) in the facial-offer layout from offers.json.
import json
DIRHAM = '<svg viewBox="0 0 22 24"><path d="M4 2v20h6a10 10 0 0 0 0-20H4z" fill="none" stroke="#fff" stroke-width="3.2"/><path d="M0 9h20M0 15h20" stroke="#fff" stroke-width="2.4"/></svg>'
WA = '<svg viewBox="0 0 32 32"><path fill="#fff" d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.9 2 6.9L3 29l6.5-2c1.9 1 4.1 1.6 6.5 1.6 7.2 0 13-5.7 13-12.8S23.2 3 16 3zm0 23.3c-2.1 0-4.1-.6-5.8-1.7l-.4-.2-3.9 1.2 1.2-3.7-.3-.4a10.4 10.4 0 0 1-1.7-5.7C5.1 10 10 5.3 16 5.3S26.9 10 26.9 15.8 22 26.3 16 26.3zm6-7.8c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.8 8.8 0 0 1-4.4-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.7s1.2 3.2 1.4 3.4c.2.2 2.4 3.6 5.8 5 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>'
PIN = '<svg viewBox="0 0 32 32"><path fill="#1278CC" d="M16 2a10 10 0 0 0-10 10c0 7.5 10 18 10 18s10-10.5 10-18A10 10 0 0 0 16 2zm0 13.6A3.6 3.6 0 1 1 16 8.4a3.6 3.6 0 0 1 0 7.2z"/></svg>'
CSS = open('offer.css', encoding='utf-8').read()
def build():
  for o in json.load(open('offers.json', encoding='utf-8')):
      n = len(o['rows'])
      top = 560 if o.get('tagline') else 525
      h = min(140, (1125 - top - 14 * (n - 1)) // n)
      used = n * h + 14 * (n - 1)
      top += max(0, (1125 - top - used) // 2 - 20)
      name_fs = 30 if h >= 96 else 27
      rows = ''.join(
          f'<div class="row" style="min-height:{h}px"><div class="name" style="font-size:{name_fs}px">{name}</div>'
          + (f'<div class="sub">{sub}</div>' if sub else '')
          + f'<div class="pill"><b>{price}</b>{DIRHAM}</div></div>' for name, sub, price in o['rows'])
      tag = f'<div class="tagline">{o["tagline"]}</div>' if o.get('tagline') else ''
      model_cls = 'product' if o.get('product') else 'model'
      html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
  <link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>{CSS}</style></head><body>
  <svg class="bg" viewBox="0 0 1080 1350">
  <polygon points="440,330 50,0 50,700 440,700" fill="#0BB0A8"/>
  <polygon points="50,560 0,520 0,1100 50,1100" fill="#C6EAF6" opacity=".7"/>
</svg>
  <img class="{model_cls}" src="{o['model']}" alt="">
  <img class="logo" style="left:auto;right:60px;transform:none;width:380px" src="../brand/TL_logo_primary_1024x237.png" alt="True Life Medical Center">
  <div class="title"><div class="pre">{o['pre']}</div><div class="main" style="font-size:{o.get('main_size',76)}px">{o['main']}</div>{tag}</div>
  <div class="panel"></div>
  <div class="rows" style="top:{top}px">{rows}</div>
  <div class="footer">
    <div class="chip wa">{WA}+971 7 204 4666</div>
    <div class="chip loc">{PIN}طريق الخور، رأس الخيمة</div>
  </div></body></html>'''
      open(f'{o["slug"]}.html', 'w', encoding='utf-8').write(html)
      print('written', o['slug'], n, 'rows, row h', h)

if __name__=='__main__':
  build()
