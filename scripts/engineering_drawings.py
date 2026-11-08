"""Illustrative engineering SVGs for the Flight Studio and kernel case studies.

Labels are plain text. Every ID is scoped to the caller's prefix. These drawings
explain architecture; they are not screenshots or depictions of built hardware.
"""
import html
import re


COLORS = {
    'paper': '#F4EEE2', 'light': '#FBF8F1', 'ink': '#1E3A3D',
    'teal': '#1F4A4F', 'coral': '#D9694E', 'peach': '#F2CBAE',
    'sage': '#A9CBC5', 'lilac': '#D8CCE0', 'sand': '#D9CDB6',
}


def _scope(prefix):
    return 'eng-' + (re.sub(r'[^a-zA-Z0-9_-]', '-', str(prefix)) or 'diagram')


def _text(x, y, value, size=12, color='#F4EEE2', anchor='start', serif=False, weight=400, spacing=0):
    family = 'Newsreader, Georgia, serif' if serif else 'Space Mono, monospace'
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}" '
            f'text-anchor="{anchor}">{html.escape(str(value), quote=True)}</text>')


def _label(labels, key, default):
    return str(labels.get(key, default))


def _defs(prefix, dark=True):
    return f'''<defs>
<pattern id="{prefix}-grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#A9CBC5" opacity=".2"/></pattern>
<linearGradient id="{prefix}-ground" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#173A3E"/><stop offset="1" stop-color="#28595B"/></linearGradient>
<linearGradient id="{prefix}-screen" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#1F4A4F"/><stop offset="1" stop-color="#102B30"/></linearGradient>
<marker id="{prefix}-coral-arrow" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto"><path d="M0 0 6 3.5 0 7" fill="none" stroke="#D9694E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
<marker id="{prefix}-sage-arrow" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto"><path d="M0 0 6 3.5 0 7" fill="none" stroke="#A9CBC5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
<marker id="{prefix}-teal-arrow" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto"><path d="M0 0 6 3.5 0 7" fill="none" stroke="#1F4A4F" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>'''


def _root(body, width, height, kind):
    return (f'<svg class="engineering-drawing engineering-{kind}" xmlns="http://www.w3.org/2000/svg" '
            f'width="{width}" height="{height}" viewBox="0 0 {width} {height}" aria-hidden="true" focusable="false">'
            + body + '</svg>')


def flight_hero(labels, prefix='flight'):
    """Three connected isometric architecture planes with selectable node groups."""
    p = _scope(prefix)
    body = [_defs(p), f'<rect width="560" height="440" rx="16" fill="url(#{p}-ground)"/>',
            f'<rect width="560" height="440" rx="16" fill="url(#{p}-grid)"/>',
            '<ellipse cx="305" cy="394" rx="172" ry="23" fill="#102B30" opacity=".35"/>',
            '<path d="M246 54 246 350M363 60 363 354" stroke="#A9CBC5" stroke-width="1" stroke-dasharray="3 6" opacity=".32"/>']
    # A small satellite anchors the conceptual ground-to-flight scene.
    body.append('''<g transform="translate(424 25)">
<path d="M32 13 48 5 64 13 48 22Z" fill="#F2CBAE" stroke="#FBF8F1"/>
<path d="M32 13 48 22 48 43 32 34Z" fill="#D9694E" stroke="#FBF8F1"/>
<path d="M48 22 64 13 64 34 48 43Z" fill="#E6B395" stroke="#FBF8F1"/>
<path d="M3 19 28 12 28 31 3 39ZM68 10 92 3 92 24 68 31Z" fill="#527B80" stroke="#A9CBC5"/>
<path d="M11 17 11 36M20 14 20 34M3 29 28 21M76 8 76 28M84 5 84 26M68 20 92 13" stroke="#A9CBC5" stroke-width=".7"/>
<path d="M36 9 28 2M48 43 50 51" stroke="#F4EEE2" stroke-linecap="round"/>
<circle cx="50" cy="53" r="2" fill="#F2CBAE"/>
</g>''')
    # The rear routes connect all three planes. They use distinct directions/colors.
    body.append(f'''<path d="M455 119H499Q507 119 507 127V339Q507 347 499 347H459" fill="none" stroke="#D9694E" stroke-width="2" marker-end="url(#{p}-coral-arrow)"/>
<path d="M463 363H521Q531 363 531 353V111Q531 102 521 102H460" fill="none" stroke="#A9CBC5" stroke-width="2" stroke-dasharray="5 5" marker-end="url(#{p}-sage-arrow)"/>
<circle cx="507" cy="191" r="4" fill="#F2CBAE"/><circle cx="531" cy="275" r="4" fill="#A9CBC5"/>''')
    for key, y, top, front, side, name in [
        ('flight', 302, '#A9CBC5', '#527E7C', '#6E9891', _label(labels, 'flight', 'cFS · Linux')),
        ('backend', 194, '#D8CCE0', '#8B7C99', '#B1A1BC', _label(labels, 'backend', 'Python service')),
        ('web', 86, '#F4EEE2', '#B8B7A5', '#D8D2BE', _label(labels, 'web', 'Web interface')),
    ]:
        body.append(f'<g data-arch-node="{key}" class="engineering-plane">')
        body.append(f'''<path d="M157 {y+14} 355 {y-33} 461 {y+17} 263 {y+64}Z" fill="#102B30" opacity=".22" transform="translate(0 17)"/>
<path d="M157 {y} 263 {y+50}V{y+69}L157 {y+19}Z" fill="{side}" stroke="#1E3A3D" stroke-width="1.2"/>
<path d="M263 {y+50} 461 {y+3}V{y+22}L263 {y+69}Z" fill="{front}" stroke="#1E3A3D" stroke-width="1.2"/>
<path d="M157 {y} 355 {y-47} 461 {y+3} 263 {y+50}Z" fill="{top}" stroke="#FBF8F1" stroke-width="1.2"/>
<path d="M282 {y+56} 302 {y+51}M309 {y+49} 320 {y+46}" stroke="#F4EEE2" stroke-width="2" opacity=".65"/>
<circle cx="445" cy="{y+13}" r="2.5" fill="#F2CBAE"/>''')
        # Draw the functional surface in the same isometric coordinate frame.
        body.append(f'<g transform="matrix(.86 -.204 .70 .33 185 {y-5})">')
        if key == 'web':
            body.append('''<rect x="0" y="0" width="230" height="108" rx="5" fill="#FBF8F1" stroke="#1F4A4F" stroke-width="2"/>
<path d="M0 19H230" stroke="#1F4A4F" stroke-width="2"/>
<circle cx="10" cy="10" r="3" fill="#D9694E"/><circle cx="21" cy="10" r="3" fill="#A9CBC5"/><circle cx="32" cy="10" r="3" fill="#D8CCE0"/>
<rect x="12" y="31" width="48" height="62" rx="2" fill="#1F4A4F"/>
<path d="M20 43H49M20 55H42M20 67H48M20 79H37" stroke="#A9CBC5" stroke-width="4"/>
<rect x="72" y="31" width="144" height="62" rx="2" fill="#E2EAE3"/>
<path d="M82 77H204M82 45V77" stroke="#9AB6AD"/>
<path d="M84 69 102 64 118 70 136 51 154 55 174 41 204 46" fill="none" stroke="#D9694E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>''')
        elif key == 'backend':
            body.append('''<rect x="22" y="10" width="114" height="80" rx="8" fill="#1E3A3D" stroke="#FBF8F1" stroke-width="2"/>
<path d="M50 32 37 50 50 68M108 32 121 50 108 68M88 28 70 73" fill="none" stroke="#F2CBAE" stroke-width="4" stroke-linecap="round"/>
<rect x="157" y="17" width="51" height="16" rx="3" fill="#FBF8F1" stroke="#1F4A4F"/>
<rect x="157" y="42" width="51" height="16" rx="3" fill="#FBF8F1" stroke="#1F4A4F"/>
<rect x="157" y="67" width="51" height="16" rx="3" fill="#FBF8F1" stroke="#1F4A4F"/>
<path d="M136 50H151V25H157M151 50H157M151 50V75H157" fill="none" stroke="#1F4A4F" stroke-width="2"/>''')
        else:
            for row in range(2):
                for col in range(4):
                    color = '#F2CBAE' if (row, col) in [(0, 1), (1, 2)] else '#FBF8F1'
                    body.append(f'<rect x="{10+col*54}" y="{8+row*40}" width="44" height="28" rx="3" fill="{color}" stroke="#1F4A4F" stroke-width="1.5"/>')
            body.append('<path d="M9 97H216" stroke="#1F4A4F" stroke-width="4"/>')
            body.append(_text(112, 101, 'cFE', 16, '#1F4A4F', 'middle', weight=700))
        body.append('</g>')
        label_y = y + 31
        body.append(f'<path d="M31 {label_y+12}H134L157 {y+10}" fill="none" stroke="{top}" stroke-width="1.2" opacity=".65"/>')
        body.append(_text(29, label_y, name, 13, '#F4EEE2', weight=500))
        body.append(f'<circle cx="157" cy="{y+10}" r="3" fill="{top}"/>')
        body.append('</g>')
    body.append(_text(471, 207, 'REST', 9, '#D8CCE0', 'middle'))
    body.append(_text(472, 316, 'UDP', 9, '#A9CBC5', 'middle'))
    body.append('<path d="M45 410H70" stroke="#D9694E" stroke-width="2"/><path d="M296 410H321" stroke="#A9CBC5" stroke-width="2" stroke-dasharray="4 4"/>')
    body.append(_text(80, 414, _label(labels, 'commands', 'Commands'), 11, '#F2CBAE'))
    body.append(_text(331, 414, _label(labels, 'telemetry', 'Telemetry'), 11, '#A9CBC5'))
    return _root(''.join(body), 560, 440, 'flight')


def kernel_hero(labels, prefix='kernel'):
    """Conceptual QEMU CEP drawing: RV64, console, VRAM, UART and timer."""
    p = _scope(prefix)
    body = [_defs(p), f'<rect width="560" height="440" rx="16" fill="url(#{p}-ground)"/>',
            f'<rect width="560" height="440" rx="16" fill="url(#{p}-grid)"/>',
            '<ellipse cx="280" cy="225" rx="210" ry="169" fill="none" stroke="#A9CBC5" opacity=".12"/>',
            '<ellipse cx="280" cy="225" rx="167" ry="126" fill="none" stroke="#A9CBC5" stroke-dasharray="2 9" opacity=".23"/>',
            _text(28, 32, 'QEMU / CEP', 11, '#A9CBC5', spacing=1.4),
            _text(531, 32, 'RV64', 11, '#F2CBAE', 'end')]
    # Copper-like paths are illustrative buses, not a physical board schematic.
    body.append('''<g fill="none" stroke-linecap="round" stroke-linejoin="round">
<path d="M234 192H180V154H128" stroke="#F2CBAE" stroke-width="2.5"/>
<path d="M234 207H165V283H132" stroke="#A9CBC5" stroke-width="2.5"/>
<path d="M327 192H363V131H398" stroke="#D8CCE0" stroke-width="2.5"/>
<path d="M327 224H383V295H405" stroke="#D9694E" stroke-width="2.5"/>
<path d="M245 249V342H281V382" stroke="#A9CBC5" stroke-width="1" opacity=".35"/>
<path d="M314 165V70H286V51" stroke="#A9CBC5" stroke-width="1" opacity=".35"/>
</g>''')
    for x, y, color in [(180, 192, '#F2CBAE'), (165, 246, '#A9CBC5'), (363, 166, '#D8CCE0'), (383, 265, '#D9694E')]:
        body.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{color}" stroke="#1E3A3D" stroke-width="2"/>')
    # Serial console, with abstract rows rather than fabricated program output.
    body.append(f'''<g data-kernel-node="console">
<path d="M44 81 205 66 216 78 216 161 55 176 44 165Z" fill="#102B30" opacity=".35"/>
<path d="M44 76 205 61 216 73 55 88Z" fill="#A9CBC5" stroke="#DCE9E6"/>
<path d="M205 61 216 73V158L205 146Z" fill="#4E7F7B" stroke="#A9CBC5"/>
<path d="M44 76 205 61V146L44 161Z" fill="#F4EEE2" stroke="#FBF8F1"/>
<path d="M53 88 195 75V135L53 148Z" fill="url(#{p}-screen)"/>
<path d="M64 103 69 106 64 110M77 103 131 98M65 119 172 110M65 132 147 124" fill="none" stroke="#A9CBC5" stroke-width="2.5" stroke-linecap="round"/>
<path d="M145 121 151 120" stroke="#F2CBAE" stroke-width="3"/>
<path d="M114 154V169L92 178M114 169 145 173" stroke="#F4EEE2" stroke-width="3" stroke-linecap="round"/>
</g>''')
    body.append(_text(44, 199, _label(labels, 'console', 'Console'), 13, '#F4EEE2'))
    # CPU pins, substrate and die.
    body.append('<g data-kernel-node="cpu"><rect x="221" y="156" width="119" height="105" rx="9" fill="#102B30" opacity=".3"/>')
    for i in range(7):
        x, y = 242 + i * 13, 172 + i * 12
        body.append(f'<path d="M{x} 164V153M{x} 248V260M236 {y}H225M326 {y}H337" stroke="#D9CDB6" stroke-width="3"/>')
    body.append('''<rect x="234" y="160" width="94" height="91" rx="5" fill="#F2CBAE" stroke="#F4EEE2" stroke-width="1.5"/>
<rect x="243" y="169" width="76" height="73" rx="2" fill="#1E3A3D" stroke="#D9694E"/>
<path d="M248 176H261M248 176V187M314 235H301M314 235V224" fill="none" stroke="#A9CBC5"/>
<circle cx="239" cy="165" r="1.5" fill="#1E3A3D"/>''')
    body.append(_text(281, 192, _label(labels, 'cpu', 'CPU'), 11, '#F4EEE2', 'middle'))
    body.append(_text(281, 217, 'RV64', 25, '#F2CBAE', 'middle', serif=True))
    body.append(_text(281, 233, 'RISC-V', 9, '#A9CBC5', 'middle'))
    body.append('</g>')
    # VRAM: address and pixel-cell visual establish memory-to-screen relation.
    body.append('''<g data-kernel-node="memory">
<path d="M45 283 209 271 221 280 57 293Z" fill="#C4D9CE" stroke="#E5EEE7"/>
<path d="M209 271 221 280V365L209 356Z" fill="#6B928C" stroke="#A9CBC5"/>
<path d="M45 283 209 271V356L45 368Z" fill="#1E3A3D" stroke="#A9CBC5"/>
</g>''')
    body.append(_text(60, 303, 'VRAM', 12, '#F4EEE2', weight=700))
    body.append(_text(60, 323, '0x80000000', 11, '#A9CBC5'))
    for row in range(2):
        for col in range(12):
            fill = '#F2CBAE' if (row+col) % 4 == 0 else '#4E7F7B'
            body.append(f'<rect x="{60+col*11}" y="{337+row*9}" width="7" height="5" rx=".8" fill="{fill}"/>')
    body.append(_text(46, 394, _label(labels, 'memory', 'Memory'), 13, '#A9CBC5'))
    # UART waveform: repeated pulses, not a recorded trace.
    body.append('''<g data-kernel-node="uart">
<rect x="382" y="78" width="145" height="95" rx="6" fill="#D8CCE0"/>
<path d="M394 133H408V117H423V133H437V117H452V133H467V117H482V133H515" fill="none" stroke="#4E3D62" stroke-width="2" stroke-linecap="round"/>
<path d="M394 140H515" stroke="#9D8BAC" stroke-width=".7"/>
</g>''')
    body.append(_text(396, 103, _label(labels, 'uart', 'UART'), 13, '#1E3A3D', weight=500))
    body.append(_text(396, 159, '0x10013000', 11, '#4E3D62'))
    # Timer and compare event.
    body.append('''<g data-kernel-node="timer">
<rect x="381" y="278" width="147" height="112" rx="6" fill="#F2CBAE"/>
<circle cx="499" cy="309" r="16" fill="none" stroke="#1E3A3D" stroke-width="1.5"/>
<path d="M499 296V309L507 314M496 288H502M511 293 515 289" stroke="#1E3A3D" stroke-width="1.5" fill="none" stroke-linecap="round"/>
<path d="M395 344H414V331H422V344H441V331H449V344H470V331H478V344H514" fill="none" stroke="#B04A32" stroke-width="2"/>
</g>''')
    # The localized label sits above the instrument, leaving room for long words.
    body.append(_text(382, 267, _label(labels, 'timer', 'Timer'), 13, '#F4EEE2'))
    body.append(_text(395, 307, 'CLINT', 11, '#1E3A3D', weight=500))
    body.append(_text(395, 370, '0x0200BFF8', 11, '#1E3A3D'))
    body.append('<path d="M267 394H293M280 381V407" stroke="#A9CBC5" stroke-width="1" opacity=".5"/><circle cx="280" cy="394" r="8" stroke="#A9CBC5" stroke-width="1" fill="none" opacity=".5"/>')
    return _root(''.join(body), 560, 440, 'kernel')


def mission_diagram(labels, prefix='mission'):
    """Mission objective → application → command → telemetry, with a return loop."""
    p = _scope(prefix)
    body = [_defs(p, dark=False), '<rect width="900" height="250" rx="10" fill="#F4EEE2"/>']
    fields = [('objective', 'Objective', '#F2CBAE'), ('application', 'Application', '#A9CBC5'),
              ('command', 'Command', '#D8CCE0'), ('telemetry', 'Telemetry', '#F1E2B2')]
    for i, (key, default, color) in enumerate(fields):
        x = 28 + i * 220
        body.append(f'<g data-mission-node="{key}">')
        body.append(f'''<rect x="{x+4}" y="52" width="180" height="135" rx="6" fill="#D9CDB6" opacity=".5"/>
<rect x="{x}" y="47" width="180" height="135" rx="6" fill="#FBF8F1" stroke="#D9CDB6"/>
<path d="M{x+6} 47H{x+174}Q{x+180} 47 {x+180} 53V84H{x}V53Q{x} 47 {x+6} 47" fill="{color}"/>
<circle cx="{x+18}" cy="28" r="12" fill="#1F4A4F"/>''')
        body.append(_text(x+18, 31, f'{i+1:02}', 8, '#F4EEE2', 'middle'))
        body.append(_text(x+90, 70, _label(labels, key, default), 14, '#1E3A3D', 'middle', serif=True, weight=500))
        cx = x + 90
        if key == 'objective':
            body.append(f'''<g fill="none" stroke="#1F4A4F" stroke-width="1.5">
<circle cx="{cx-11}" cy="129" r="25"/><circle cx="{cx-11}" cy="129" r="14"/>
<path d="M{cx-11} 129 {cx+33} 101M{cx+21} 100 {cx+33} 101 {cx+30} 113" stroke="#B04A32" stroke-width="2"/>
<path d="M{cx-46} 129H{cx-37}M{cx-11} 94V103M{cx-11} 155V164"/>
</g><circle cx="{cx-11}" cy="129" r="3" fill="#B04A32"/>
<path d="M{cx+47} 123V143A8 8 0 1 0 {cx+57} 143V123A5 5 0 0 0 {cx+47} 123Z" fill="none" stroke="#1F4A4F" stroke-width="1.5"/>
<path d="M{cx+52} 132V149" stroke="#B04A32" stroke-width="2.5" stroke-linecap="round"/>
<circle cx="{cx+52}" cy="150" r="3.5" fill="#B04A32"/>''')
        elif key == 'application':
            body.append(f'''<rect x="{cx-36}" y="103" width="72" height="48" rx="4" fill="#1F4A4F"/>
<path d="M{cx-22} 115H{cx-5}M{cx-22} 126H{cx+23}M{cx-22} 137H{cx+10}" stroke="#A9CBC5" stroke-width="3" stroke-linecap="round"/>
<path d="M{cx-16} 99V92M{cx} 99V92M{cx+16} 99V92M{cx-16} 155V162M{cx} 155V162M{cx+16} 155V162" stroke="#1F4A4F" stroke-width="2"/>
<circle cx="{cx+28}" cy="110" r="3" fill="#F2CBAE"/>''')
        elif key == 'command':
            body.append(f'''<path d="M{cx-45} 111H{cx+35}V146H{cx-45}Z" fill="#E6DDEA" stroke="#5D4A6D" stroke-width="1.5"/>
<path d="M{cx-23} 111V146M{cx-8} 111V146" stroke="#9D8BAC"/>
<path d="M{cx+1} 127H{cx+26}M{cx+20} 121 {cx+27} 127 {cx+20} 133" fill="none" stroke="#5D4A6D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M{cx-44} 154H{cx+35}" stroke="#D9CDB6"/>''')
        else:
            body.append(f'''<rect x="{cx-45}" y="103" width="90" height="51" rx="3" fill="#1F4A4F"/>
<path d="M{cx-35} 144H{cx+35}M{cx-35} 115V144" stroke="#70998E"/>
<path d="M{cx-34} 138 {cx-21} 136 {cx-10} 123 {cx+1} 129 {cx+14} 116 {cx+24} 123 {cx+35} 119" fill="none" stroke="#F1E2B2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="{cx+35}" cy="119" r="2.5" fill="#F2CBAE"/>
<path d="M{cx-11} 161H{cx+11}" stroke="#1F4A4F" stroke-width="2"/>''')
        body.append('</g>')
        if i < 3:
            body.append(f'<path d="M{x+188} 119H{x+211}" fill="none" stroke="#1F4A4F" stroke-width="1.6" marker-end="url(#{p}-teal-arrow)"/>')
    body.append(f'''<path d="M778 195V210Q778 220 768 220H128Q118 220 118 210V195" fill="none" stroke="#4E7F7B" stroke-width="1.5" stroke-dasharray="4 5" marker-end="url(#{p}-teal-arrow)"/>
<circle cx="448" cy="220" r="12" fill="#F4EEE2"/>
<path d="M443 217A6 6 0 1 1 444 225M443 212V217H448" fill="none" stroke="#4E7F7B" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>''')
    return _root(''.join(body), 900, 250, 'mission')
