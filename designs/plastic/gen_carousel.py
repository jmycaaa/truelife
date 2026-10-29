# Builds a 4-slide surgery carousel from the liposuction design + a JSON spec.
# Usage: python3 gen_carousel.py <slug>   (reads <slug>/spec.json, writes <slug>/carousel.html)
import json, re, sys, os
slug = sys.argv[1]
spec = json.load(open(f'{slug}/spec.json', encoding='utf-8'))
s = open('liposuction/carousel.html', encoding='utf-8').read()

def between(text, start, end, new):
    a = text.index(start) + len(start); b = text.index(end, a)
    return text[:a] + new + text[b:]

def ltr(t):  # keep number ranges left-to-right inside Arabic text
    return re.sub(r'(\d+–\d+)', r'<bdi class="ltr">\1</bdi>', t)

# slide 1
s = s.replace('src="model_cover.png"', 'src="model_cover.png"')
s = between(s, '<div class="ttl">', '</div>', spec['title'])
s = between(s, '<div class="sub">', '</div>', spec['hook'])
s = between(s, '<div class="pills">\n', '  </div>', ''.join(f'    <span class="pill"><i></i>{p}</span>\n' for p in spec['pills']))
if 'title_size' in spec:
    s = s.replace('right:60px;font-size:74px', f"right:60px;font-size:{spec['title_size']}px")

# slide 2
X0, Y0, W, H = 299, 360, 482, 640
px = lambda fx, fy: (round(X0 + fx * W), round(Y0 + fy * H))
s2 = s[s.index('<section class="slide s2"'):s.index('<section class="slide s3"')]
n2 = s2
n2 = between(n2, '<div class="ttl">', '</div>', spec['s2_title'])
n2 = between(n2, '<div class="sub">', '</div>', ltr(spec['s2_sub']))
marks = ['  <!-- generated markers -->']
outl = ''.join(f'<path d="{p}" fill="none" stroke="#0BB0A8" stroke-width="4" stroke-linecap="round"/>' for p in spec.get('outline', []))
circ = ''.join(f'<ellipse cx="{c[0]*W:.0f}" cy="{c[1]*H:.0f}" rx="{c[2]*W:.0f}" ry="{c[2]*W:.0f}" fill="none" stroke="#1278CC" stroke-width="7" stroke-linecap="round" stroke-dasharray="2 12"/>' for c in spec.get('circles', []))
paths = ''.join(f'<path d="{p}" fill="none" stroke="#1278CC" stroke-width="7" stroke-linecap="round" stroke-dasharray="2 12"/>' for p in spec.get('scars', []))
paths_all = True
if paths or outl or circ:
    marks.append(f'  <svg style="position:absolute;left:{X0}px;top:{Y0}px" width="{W}" height="{H}" viewBox="0 0 1 1" preserveAspectRatio="none">'
                 .replace('viewBox="0 0 1 1" preserveAspectRatio="none"', f'viewBox="0 0 {W} {H}"') +
                 re.sub(r'([\d.]+),([\d.]+)', lambda m: f'{float(m.group(1))*W:.0f},{float(m.group(2))*H:.0f}', outl + paths) + circ + '</svg>')
for fx, fy in spec.get('dots', []):
    x, y = px(fx, fy); marks.append(f'  <div class="mk" style="left:{x}px;top:{y}px"></div>')
for lb in spec['labels']:
    x, y = px(lb['fx'], lb['fy'])
    small = f'<br><small style="font-size:21px;font-weight:400">{lb["note"]}</small>' if lb.get('note') else ''
    if lb['side'] == 'r':
        marks.append(f'  <div class="lead" style="left:{x+15}px;top:{y-1}px;width:{770-x-15}px"></div><div class="lbl" style="left:780px;top:{y-21}px"><b>●</b> {lb["text"]}{small}</div>')
    else:
        marks.append(f'  <div class="lead" style="left:250px;top:{y-1}px;width:{x-15-250}px"></div><div class="lbl" style="left:30px;width:215px;white-space:normal;line-height:1.3;top:{y-21}px;text-align:right"><b>●</b> {lb["text"]}{small}</div>')
a = n2.index('  <!-- markers'); b = n2.index('  <div class="facts">')
n2 = n2[:a] + '\n'.join(marks) + '\n' + n2[b:]
n2 = between(n2, '<div class="facts">\n', '  </div>\n  <div class="num">',
             ''.join(f'    <div class="fact"><b>{ltr(f[0])}</b><span>{f[1]}</span></div>\n' for f in spec['facts']))
s = s.replace(s2, n2)

# slide 3
s3 = s[s.index('<section class="slide s3"'):s.index('<section class="slide s4"')]
n3 = between(s3, '<div class="tips">\n', '  </div>\n  <div class="num">',
             ''.join(f'    <div class="tip"><div class="n">{i}</div><p>{ltr(t)}<small>{ltr(d)}</small></p></div>\n' for i, (t, d) in enumerate(spec['tips'], 1)))
s = s.replace(s3, n3)
s = s.replace('src="body_illustration.png"', 'src="' + spec.get('illustration', '../liposuction/body_illustration.png') + '"')
if spec.get('gender') == 'm':
    s = s.replace('احجزي', 'احجز').replace('تناسب جسمك', 'تناسبك')
# face surgeries keep the original doctor photo; body & breast use dr_body.png
if slug in ('rhinoplasty', 'facelift', 'eyelid', 'brow_lift', 'otoplasty'):
    s = s.replace('../dr_body.png', '../dr_elsayed.png')
open(f'{slug}/carousel.html', 'w', encoding='utf-8').write(s)
print('written', slug)
