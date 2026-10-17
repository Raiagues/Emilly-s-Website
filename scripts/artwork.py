"""Original, local SVG illustrations. These are conceptual drawings, not project photos."""
from pathlib import Path
import math

def generate(root):
    folder = root / 'img' / 'illustrations'
    folder.mkdir(parents=True, exist_ok=True)
    defs = '''<defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="currentColor" stroke-opacity=".07"/></pattern><pattern id="solar" width="26" height="26" patternUnits="userSpaceOnUse"><rect width="26" height="26" fill="#355960"/><path d="M0 0H26V26H0Z" fill="none" stroke="#b7d0c7" stroke-width=".8"/></pattern></defs>'''
    def svg(name, body, bg='#192e37', fg='#d7e6d6'):
        out=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" fill="none" color="{fg}">{defs}<path fill="{bg}" d="M0 0H800V500H0Z"/><path fill="url(#grid)" d="M0 0H800V500H0Z"/><g stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{body}</g><g fill="currentColor" opacity=".4"><circle cx="34" cy="34" r="2"/><circle cx="766" cy="466" r="2"/><path d="M750 34h16m-8-8v16M34 458v16m-8-8h16" stroke="currentColor"/></g></svg>'''
        (folder/f'{name}.svg').write_text(out)
    satellite='''<ellipse cx="400" cy="256" rx="330" ry="138" transform="rotate(-24 400 256)" stroke-dasharray="5 10" opacity=".4"/><circle cx="400" cy="250" r="170" opacity=".12"/><g transform="translate(400 240) rotate(-22)"><path d="M-70-65 15-105 90-60 5-18Z" fill="#efd1a0"/><path d="M-70-65 5-18V105L-70 57Z" fill="#c6a26d"/><path d="M5-18 90-60V65L5 105Z" fill="#e0bb7f"/><path d="M-70-25H-110M90 0h45"/><path d="M-290-85H-110V70H-290ZM135-75H315V80H135Z" fill="url(#solar)"/><path d="M5-105V-150m-24-10 24 10 24-10"/><circle cx="-25" cy="-12" r="12"/><path d="M25 17 72-5v48L25 66Z" fill="#263c43"/><path d="M25 35 72 13M48 5v49"/></g><path d="M560 105h80v-35M167 360H95v40" opacity=".5"/><circle cx="560" cy="105" r="5" fill="#d78362"/><circle cx="167" cy="360" r="5" fill="#d78362"/>'''
    svg('satellite',satellite)
    chip='''<g transform="translate(400 250) rotate(-25)"><rect x="-115" y="-115" width="230" height="230" rx="14" fill="#e4dac8"/><rect x="-83" y="-83" width="166" height="166" fill="#a76248"/><rect x="-60" y="-60" width="120" height="120" stroke="#edcfab"/><path d="M-60-25H60M-60 12H60M-12-60V60M23-60V60" stroke="#edcfab"/>'''
    for n in range(-90,100,20):
        chip+=f'<path d="M{n}-115v-40M{n} 115v40M-115 {n}h-40M115 {n}h40" stroke-width="6"/>'
    chip+='</g><path d="M96 115h120l45 45M705 372H580l-52-52M85 340h110l55-55M694 110H565l-35 35" opacity=".6"/><circle cx="96" cy="115" r="6"/><circle cx="705" cy="372" r="6"/>'
    svg('chip',chip,'#e9e0d1','#6e705c')
    platform='''<rect x="118" y="86" width="564" height="326" rx="14" fill="#1e353e"/><path d="M118 128h564M305 128v284"/><circle cx="141" cy="107" r="4" fill="#e09a7b"/><circle cx="158" cy="107" r="4" fill="#ddc796"/><circle cx="175" cy="107" r="4" fill="#b8d0b8"/><path d="M144 164h125M144 187h88M144 233h103M144 258h78M144 281h111M144 305h66" opacity=".45"/><path d="m148 345 10 10-10 10m22 0h28" stroke="#e09a7b" stroke-width="3"/><rect x="330" y="152" width="325" height="137" rx="5" fill="#2c444a"/><path d="M350 265h283M350 175v90" opacity=".3"/><path d="M350 246h25l15-33 25 44 30-65 28 50 22-20 26 15 25-50 21 48 23-15 22 8h20" stroke="#d9bd85" stroke-width="2.5"/><rect x="330" y="312" width="148" height="73" rx="5"/><rect x="500" y="312" width="155" height="73" rx="5"/><circle cx="359" cy="349" r="13" stroke="#c7cbb1"/><path d="M393 338h65M393 358h43M520 336h111M520 356h82"/><path d="M220 438h360" opacity=".4"/>'''
    svg('platform',platform,'#223d43','#a9c5ba')
    signal='<path d="M100 250H700M130 380V100" opacity=".4"/>'
    for a,col in [(0,'#d48b69'),(1,'#708a83')]:
        pts=' '.join(f'{x},{250+math.sin((x-130)/38)*80*(1 if a else .6)+ (math.sin(x*1.2)*35 if a else 0)}' for x in range(130,690,3))
        signal+=f'<polyline points="{pts}" stroke="{col}" stroke-width="{1 if a else 3}" opacity="{.5 if a else 1}"/>'
    signal+='<path d="M130 405h170m-170-8v16m170-16v16M595 125h95"/><circle cx="595" cy="125" r="4" fill="#d48b69"/>'
    svg('signal',signal,'#e9e5d9','#506858')
    fault='<g>'
    for row in range(5):
        for col in range(9):
            x,y=180+col*48,130+row*48
            fault+=f'<rect x="{x}" y="{y}" width="34" height="34" rx="3" fill="{"#cb785b" if (row,col)==(2,4) else "#354d56"}"/>'
    fault+='</g><path d="m489 50-50 104h40l-50 104" stroke="#ecb487" stroke-width="4"/><circle cx="389" cy="244" r="45" stroke="#ecb487" stroke-dasharray="4 8"/><path d="M180 403H600M180 395v16M600 395v16" opacity=".4"/>'
    svg('fault',fault)
    svg('radio','''<path d="M400 230v170M345 400h110" stroke-width="7"/><circle cx="400" cy="215" r="14" fill="#c47b5c"/><path d="M353 168a67 67 0 0 0 0 94M447 168a67 67 0 0 1 0 94M320 135a113 113 0 0 0 0 160M480 135a113 113 0 0 1 0 160M288 103a158 158 0 0 0 0 224M512 103a158 158 0 0 1 0 224" stroke-width="4"/><path d="M145 430h510" opacity=".4"/>''','#dde3d5','#638477')
    code='''<rect x="155" y="93" width="490" height="315" rx="10" fill="#2a333c"/><path d="M155 137h490"/><circle cx="180" cy="115" r="4" fill="#e49a75"/><circle cx="197" cy="115" r="4" fill="#e3d4ac"/><circle cx="214" cy="115" r="4" fill="#b5cbbc"/><path d="m215 210-28 28 28 28m73-56 28 28-28 28m-31-75-29 93" stroke="#e3b296" stroke-width="4"/><path d="M354 194h110M354 219h220M354 244h159M354 269h193M194 328h165M194 352h267M479 352h72" stroke-width="5" opacity=".5"/><path d="M280 443h240" opacity=".3"/>'''
    svg('code',code,'#c8c7ba','#b5c6ba')
    svg('aircraft','''<ellipse cx="400" cy="255" rx="280" ry="160" stroke-dasharray="5 9" opacity=".35"/><g transform="translate(400 250) rotate(-25)"><path d="M-17-150Q0-200 17-150L24-35 240 58v37L22 40l-6 105 65 45v20L0 185l-81 25v-20l65-45-6-105-218 55V58L-24-35Z" fill="#d7c6a8"/><path d="M0-150V185M-22-35l44 75M22-35l-44 75M-224 73H224M-65 193H65" stroke="#9b806a"/><path d="M-140 40v52M-80 15v62M80 15v62M140 40v52" stroke="#9b806a"/></g><path d="M75 410h650M75 402v16M725 402v16" opacity=".4"/>''','#dfe3d8','#6b8071')
    svg('rover','''<path d="M0 355C165 355 165 130 350 130S545 370 800 370" stroke="#536961" stroke-width="42"/><path d="M0 355C165 355 165 130 350 130S545 370 800 370" stroke="#c8ccac" stroke-dasharray="15 20" stroke-width="2"/><g transform="translate(405 222) rotate(35)"><rect x="-67" y="-75" width="134" height="155" rx="20" fill="#dbb68b"/><rect x="-84" y="-61" width="24" height="46" rx="7" fill="#243c38"/><rect x="60" y="-61" width="24" height="46" rx="7" fill="#243c38"/><rect x="-84" y="32" width="24" height="46" rx="7" fill="#243c38"/><rect x="60" y="32" width="24" height="46" rx="7" fill="#243c38"/><rect x="-38" y="-30" width="76" height="65" fill="#62736a"/><circle r="15"/><path d="M-50-87H50M0-87v-32m-65-30 65 30 65-30" stroke-dasharray="4 6"/></g>''','#d9dfc8','#9c9c7c')
    detector=''
    for r in [170,143,115,85,52]:
        detector+=f'<circle cx="400" cy="250" r="{r}" stroke-width="{12 if r==143 else 1}" opacity=".6"/>'
    for n in range(24):
        a=n*math.pi/12
        detector+=f'<path d="M{400+85*math.cos(a)} {250+85*math.sin(a)}L{400+170*math.cos(a)} {250+170*math.sin(a)}" opacity=".4"/>'
    for x,y in [(550,140),(260,150),(570,320),(270,345),(380,75)]:
        detector+=f'<path d="M400 250Q{(x+400)/2+20} {y} {x} {y}" stroke="#e7b17e" stroke-width="2"/>'
    detector+='<circle cx="400" cy="250" r="6" fill="#efcaa5"/><path d="M150 430H650" opacity=".3"/>'
    svg('detector',detector,'#302f3d','#c4b1bf')
    svg('rocket','''<circle cx="400" cy="245" r="163" fill="#d8c7aa" stroke="none"/><g transform="translate(400 235) rotate(25)"><path d="M-43-70Q-40-145 0-175 40-145 43-70V65H-43Z" fill="#f3ecdd"/><path d="M-43 10-90 70v65l47-45M43 10l47 60v65L43 90" fill="#a95d46"/><path d="M-22 80Q-45 140 0 195 45 140 22 80Z" fill="#dca364"/><circle cy="-65" r="24" fill="#4d6c69"/><path d="M-43 40h86M-33 65h66"/></g><path d="M165 130h26m-13-13v26M623 300h26m-13-13v26"/>''','#ede6d8','#8c7a61')
    svg('observatory','''<circle cx="605" cy="125" r="35" fill="#d8c8a5" stroke="none"/><path d="M0 405Q100 365 200 405T400 405T600 405T800 405V500H0" fill="#1b3036" stroke="none"/><g transform="translate(390 242)"><path d="M-100-40 80-130 112-66-68 24Z" fill="#c8c1a3"/><path d="M-115-32-100-40-68 24-83 32Z" fill="#8b9d90"/><path d="M80-130 97-138 129-74 112-66Z" fill="#8b9d90"/><circle cy="26" r="21" fill="#ac7962"/><path d="M0 47-75 170M0 47l75 123M0 47v123" stroke-width="7"/></g><path d="M200 95h20m-10-10v20M665 245h20m-10-10v20"/><circle cx="110" cy="225" r="3"/><circle cx="490" cy="60" r="2"/><circle cx="700" cy="70" r="3"/>''','#253d49','#b9cbb7')
    svg('outreach','''<circle cx="400" cy="220" r="135" stroke-dasharray="5 9"/><path d="M400 85v270M265 220h270" opacity=".3"/><circle cx="400" cy="220" r="63" fill="#c17858"/><path d="M374 222l18 18 35-40" stroke="#f4e7cd" stroke-width="4"/><g fill="#62796b"><circle cx="210" cy="305" r="30"/><circle cx="590" cy="305" r="30"/><circle cx="400" cy="70" r="30"/></g><path d="M150 404v-24a60 60 0 0 1 120 0v24M530 404v-24a60 60 0 0 1 120 0v24" fill="#62796b"/><path d="M240 290l95-45M465 245l95 45M400 100v55"/><path d="M100 435h600" opacity=".3"/>''','#eee3cf','#82917d')
    image='<rect x="150" y="120" width="200" height="260" rx="6"/><rect x="450" y="120" width="200" height="260" rx="6" fill="#d1bba0"/><path d="M375 250h50m-10-10 10 10-10 10"/>'
    for x in [250,550]:
        image+=f'<circle cx="{x}" cy="195" r="27" fill="{"#69867c" if x==250 else "#b87354"}"/><path d="M{x-58} 340v-65a58 58 0 0 1 116 0v65Z" fill="{"#69867c" if x==250 else "#b87354"}"/>'
    svg('image',image,'#e4e1d4','#879585')
    svg('suspension','''<path d="M235 95h330v65H235Z" fill="#819282"/><path d="M280 160v60h240v-60" stroke-width="6"/><path d="M300 170h200M300 183h200M300 196h200"/><circle cx="400" cy="300" r="42" fill="#c08161"/><path d="M350 238q-40 60 0 115M450 238q40 60 0 115M320 225q-65 90 0 145M480 225q65 90 0 145" stroke-dasharray="4 7"/><path d="M200 408h400M400 350v45"/><path d="M565 190h70v170h-70" opacity=".5"/>''','#e7e0d2','#6c8275')
    (root/'img'/'favicon.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#243c43"/><ellipse cx="32" cy="32" rx="26" ry="12" transform="rotate(-40 32 32)" fill="none" stroke="#d8c7aa" stroke-width="2"/><circle cx="32" cy="32" r="9" fill="#cc7855"/><circle cx="50" cy="17" r="4" fill="#f4eddf"/></svg>''')
