import math
def rnd(seed):
    while True:
        seed=(seed*1103515245+12345)&0x7FFFFFFF; yield (seed%10000)/10000
R=rnd(11); N=520
grains=[(next(R),(next(R)+next(R)+next(R))/3-0.5,next(R)) for _ in range(N)]
cols=["#c4a7e7","#9ccfd8","#ebbcba","#31748f"]; rim=100
paths={}; seen=set(); k=0
for j,c in enumerate(cols):
    for a,ac,ar in grains:
        r=rim*(0.1+0.9*a)+ac*rim*0.12*(0.4+a)
        t=j*2*math.pi/len(cols)+a*2.4*math.pi+(ar-0.5)*0.25
        x=round(r*math.cos(t)); y=round(r*math.sin(t))
        if (x,y) in seen: continue
        seen.add((x,y)); k+=1
        key=(c,(k*7)%8,min(2,int(a*3)))
        paths.setdefault(key,[]).append(f"M{x-.35:g} {y-.35:g}h.7v.7h-.7z")
op=[.9,.65,.4]
body="".join(f'<path class="f{b}" fill="{c}" fill-opacity="{op[o]}" d="{"".join(v)}"/>' for (c,b,o),v in paths.items())
# bulge: grains scattered around the centre, densest in the middle, slightly barred, gold fading into rose
C=rnd(5); cb={}
for _ in range(420):
    u=(next(C)+next(C)+next(C)-1.5)*15; v=(next(C)+next(C)+next(C)-1.5)*9
    x=round(u); y=round(v); d=(u/15)**2+(v/9)**2
    if (x,y) in seen: continue
    seen.add((x,y)); col="#f6c177" if d<.35 and next(C)<.7 else "#ebbcba"
    o=round(max(.15,.55-d*.25)*10)/10
    cb.setdefault((col,o),[]).append(f"M{x-.35:g} {y-.35:g}h.7v.7h-.7z")
body+="".join(f'<path fill="{c}" fill-opacity="{o}" d="{"".join(v)}"/>' for (c,o),v in cb.items())
S=rnd(7); stars={0:[],1:[],2:[],3:[]}
for i in range(260):
    x=int(next(S)*1600); y=int(next(S)*1000); s=1.5 if next(S)<.8 else 2.5
    stars[i%4].append(f"M{x} {y}h{s}v{s}h-{s}z")
sc=["#e0def4","#c4a7e7","#9ccfd8","#ebbcba"]
st="".join(f'<path class="s{i}" fill="{sc[i]}" d="{"".join(v)}"/>' for i,v in stars.items())
met="".join(f'<g class="m m{i}" transform="translate({x} {y}) rotate(25)"><rect x="-140" y="-1" width="140" height="2" fill="url(#tail)"/><rect x="-2" y="-1.5" width="3" height="3" fill="#e0def4"/></g>' for i,(x,y) in enumerate([(300,120),(900,80),(500,380)]))
blink="".join(f".f{b}{{animation:blink 16s ease-in-out {b*2}s infinite}}" for b in range(8))
css=(".s0,.s1,.s2,.s3{opacity:.25;animation:tw 12s ease-in-out infinite}.s1{animation-delay:3s}.s2{animation-delay:6s}.s3{animation-delay:9s}"
 "@keyframes tw{50%{opacity:.75}}"+blink+"@keyframes blink{0%,100%{opacity:1}45%,60%{opacity:.08}}"
 ".g{animation:turn 600s linear infinite}@keyframes turn{to{transform:rotate(-360deg)}}"
 ".m{opacity:0;animation:shoot 37s linear infinite}.m1{animation-delay:14s;animation-duration:53s}.m2{animation-delay:29s;animation-duration:71s}"
 "@keyframes shoot{0%{opacity:0;translate:0 0}1%{opacity:1}4%{opacity:0;translate:420px 196px}100%{opacity:0;translate:420px 196px}}"
 "@media (prefers-reduced-motion:reduce){*{animation:none!important}.m{display:none}}")
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="tail"><stop offset="0" stop-color="#e0def4" stop-opacity="0"/><stop offset="1" stop-color="#e0def4" stop-opacity=".8"/></linearGradient></defs><style>{css}</style>{st}{met}'
 f'<svg width="1600" height="1000" viewBox="-130 -130 260 260" preserveAspectRatio="xMidYMid meet" opacity="0.45"><g transform="rotate(-17) scale(1 0.5)"><g class="g">{body}</g></g></svg></svg>')
assert len(svg)<131072, len(svg)
open("hooks/scene.ts","w").write("export const SCENE = `"+svg+"`\n")
pass
print(len(svg),k)
