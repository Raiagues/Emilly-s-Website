"""Inline, illustrative diagrams of the Flight Studio execution infrastructure.

Public API: hero(labels), board(labels), storage(labels).
Labels are plain text, escaped at every insertion. Technical names and addresses
are retained. No IDs or external assets are used, so diagrams can coexist safely.

Label keys (all optional, with short English fallbacks):
hero: signals, sensor, apps, cfs, linux, virtual_board
board: board, gpio, soc, memory, storage, sensor, console, bus
storage: host_files, kernel, dtb, initramfs, sd, boot, root, linux, loader, apps
"""
import html


PAPER = '#FBF8F1'
TEAL = '#1E3A3D'
SAGE = '#A9CBC5'
PEACH = '#F2CBAE'
LILAC = '#D8CCE0'


def _label(labels, key, fallback):
    return str(labels.get(key, fallback))


def _text(x, y, value, size=13, fill=PAPER, anchor='start', serif=False, weight=400, attrs=''):
    family = 'Newsreader, Georgia, serif' if serif else 'Space Mono, monospace'
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" {attrs}>'
            + html.escape(str(value), quote=True) + '</text>')


def _root(body, width, height, kind):
    return (f'<svg class="flight-infrastructure-drawing flight-infrastructure-{kind}" '
            f'xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" style="max-width:100%;height:auto" aria-hidden="true" focusable="false">'
            + ''.join(body) + '</svg>')


def _ground(width, height):
    pieces = [f'<rect width="{width}" height="{height}" rx="14" fill="{TEAL}"/>']
    for x in range(20, width, 28):
        for y in range(20, height, 28):
            pieces.append(f'<circle cx="{x}" cy="{y}" r=".65" fill="{SAGE}" opacity=".2"/>')
    return pieces


def _arrow(x, y, color=SAGE, direction='right'):
    if direction == 'right':
        path = f'M{x-6} {y-5} {x} {y} {x-6} {y+5}'
    elif direction == 'left':
        path = f'M{x+6} {y-5} {x} {y} {x+6} {y+5}'
    else:
        path = f'M{x-5} {y-6} {x} {y} {x+5} {y-6}'
    return f'<path d="{path}" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'


def hero(labels):
    """Exploded virtual board, Linux, cFS and applications, plus synthetic signals."""
    out = _ground(640, 460)
    out += ['<ellipse cx="389" cy="404" rx="190" ry="25" fill="#10282C" opacity=".45"/>',
            '<path d="M276 91V337M479 76V337" stroke="#A9CBC5" stroke-dasharray="3 7" stroke-width="1" opacity=".3"/>']
    # Base plane: virtual Raspberry Pi. Pins, connector and chip are illustrative.
    out.append('''<g data-infrastructure-layer="board">
<path d="M192 301 360 374V394L192 320Z" fill="#4E7F7B" stroke="#A9CBC5"/>
<path d="M360 374 581 314V334L360 394Z" fill="#345C5B" stroke="#A9CBC5"/>
<path d="M192 301 413 241 581 314 360 374Z" fill="#7FA79B" stroke="#DDE8DF" stroke-width="1.4"/>
<path d="M219 307 345 361M428 255 549 308M382 355 544 312" fill="none" stroke="#DCE9E6" stroke-width="1" opacity=".5"/>
<path d="M246 305 310 288 324 294M421 326 473 312 505 326M324 341 366 329" fill="none" stroke="#C7DFCA" stroke-width="2"/>
<path d="M303 323 360 307 415 330 358 347Z" fill="#203C3F" stroke="#F2CBAE"/>
<path d="M303 323V337L358 361V347Z" fill="#102C30" stroke="#F2CBAE"/>
<path d="M358 347 415 330V344L358 361Z" fill="#315359" stroke="#F2CBAE"/>
</g>''')
    out.append(_text(359, 333, 'QEMU', 14, PEACH, 'middle', weight=600))
    for i in range(8):
        x = 460 + i * 9
        y = 281 + i * 3.9
        out.append(f'<path d="M{x:.1f} {y:.1f}  {x+3:.1f} {y-1:.1f}V{y+8:.1f}L{x:.1f} {y+9:.1f}Z" fill="#F2CBAE" stroke="#4E7F7B" stroke-width=".7"/>')
    for x, y in [(215, 300), (411, 252), (556, 313), (361, 364)]:
        out.append(f'<ellipse cx="{x}" cy="{y}" rx="5" ry="2.5" fill="#1E3A3D" stroke="#DDE8DF"/>')
    out.append('<path d="M478 352 530 338V353L478 367Z" fill="#D8CCE0" stroke="#FBF8F1"/><path d="M489 355 519 347" stroke="#746482" stroke-width="4"/>')
    # Linux plane floats above the board, with a file-system motif.
    out.append('''<g data-infrastructure-layer="linux">
<path d="M213 224 365 290V306L213 240Z" fill="#AFACB6" stroke="#D8CCE0"/>
<path d="M365 290 566 236V252L365 306Z" fill="#797587" stroke="#D8CCE0"/>
<path d="M213 224 414 169 566 236 365 290Z" fill="#D8CCE0" stroke="#FBF8F1" stroke-width="1.3"/>
<g transform="matrix(.83 -.225 .74 .32 269 212)">
<path d="M0 5H55L67 17H187V94H0Z" fill="#FBF8F1" stroke="#6D627A" stroke-width="2"/>
<path d="M17 38H168M17 54H153M17 70H130" stroke="#A9CBC5" stroke-width="5"/>
<rect x="132" y="27" width="44" height="52" rx="2" fill="#1E3A3D"/>
<path d="M142 42 149 48 142 54M155 57H167" fill="none" stroke="#F2CBAE" stroke-width="3"/>
</g></g>''')
    out.append(_text(227, 247, _label(labels, 'linux', 'Linux guest'), 14, TEAL, weight=500))
    # cFS services plane with bus and three small application modules above it.
    out.append('''<g data-infrastructure-layer="cfs">
<path d="M234 147 365 204V218L234 161Z" fill="#CEC5AF" stroke="#FBF8F1"/>
<path d="M365 204 550 155V169L365 218Z" fill="#9DAB9E" stroke="#FBF8F1"/>
<path d="M234 147 420 97 550 155 365 204Z" fill="#FBF8F1" stroke="#FBF8F1" stroke-width="1.4"/>
<path d="M272 149 405 113M294 159 427 123M317 169 450 133" stroke="#A9CBC5" stroke-width="4" stroke-linecap="round"/>
<g fill="#1E3A3D"><circle cx="289" cy="144" r="3"/><circle cx="344" cy="130" r="3"/><circle cx="398" cy="116" r="3"/></g>
</g>''')
    out.append(_text(271, 180, _label(labels, 'cfs', 'NASA cFS'), 16, TEAL, weight=500))
    for x, y, code, color in [(290, 99, 'CI', PEACH), (369, 78, 'APP', SAGE), (449, 57, 'TO', LILAC)]:
        out.append(f'''<g data-infrastructure-layer="app">
<path d="M{x} {y} {x+42} {y-11} {x+79} {y+5} {x+37} {y+16}Z" fill="{color}" stroke="#FBF8F1"/>
<path d="M{x} {y} {x+37} {y+16}V{y+32}L{x} {y+16}Z" fill="{color}" stroke="#FBF8F1"/>
<path d="M{x+37} {y+16} {x+79} {y+5}V{y+21}L{x+37} {y+32}Z" fill="#52746F" stroke="#FBF8F1"/>
</g>''')
        out.append(_text(x+37, y+7, code, 10, TEAL, 'middle', weight=700))
    out.append(_text(289, 50, _label(labels, 'apps', 'Flight applications'), 14, PAPER))
    # External signal definition and sensor injection, followed by the I²C route.
    out.append('''<g data-infrastructure-layer="signals">
<rect x="25" y="105" width="155" height="102" rx="7" fill="#FBF8F1"/>
<path d="M25 130H180" stroke="#D9CDB6"/>
<circle cx="37" cy="117" r="2.6" fill="#D9694E"/><circle cx="47" cy="117" r="2.6" fill="#A9CBC5"/><circle cx="57" cy="117" r="2.6" fill="#D8CCE0"/>
<path d="M40 174Q53 146 66 174T92 174 118 174 144 174 168 174" fill="none" stroke="#D9694E" stroke-width="2.5"/>
<path d="M40 188H168" stroke="#A9CBC5" stroke-width="1"/>
</g>''')
    out.append(_text(25, 91, _label(labels, 'signals', 'Python signals'), 14, PAPER))
    out.append(_text(165, 121, 'f(t)', 10, TEAL, 'end'))
    out.append('<path d="M103 208V248" fill="none" stroke="#F2CBAE" stroke-width="1.7"/>')
    out.append(_arrow(103, 248, PEACH, 'down'))
    out.append(_text(114, 233, 'QMP', 11, PEACH))
    out.append('''<g data-infrastructure-layer="sensor">
<rect x="47" y="258" width="112" height="79" rx="6" fill="#A9CBC5" stroke="#FBF8F1"/>
<rect x="57" y="271" width="34" height="43" rx="3" fill="#1E3A3D"/>
<path d="M69 279V295A6 6 0 1 0 79 295V279A5 5 0 0 0 69 279Z" fill="none" stroke="#F2CBAE" stroke-width="1.2"/>
<path d="M74 284V301" stroke="#F2CBAE" stroke-width="2"/>
<circle cx="74" cy="301" r="3" fill="#F2CBAE"/>
<path d="M101 282H145M101 292H132M101 302H139" stroke="#1E3A3D" stroke-width="2"/>
</g>''')
    out.append(_text(103, 355, _label(labels, 'sensor', 'Virtual sensor'), 13, SAGE, 'middle'))
    out.append('<path d="M159 285H180L216 275M159 302H181L233 288" fill="none" stroke="#F2CBAE" stroke-width="1.8"/>')
    out.append(_text(172, 266, 'I²C', 11, PEACH))
    out.append(_text(368, 431, _label(labels, 'virtual_board', 'Raspberry Pi 4B · virtual board'), 15, SAGE, 'middle', serif=True))
    return _root(out, 640, 460, 'hero')


def board(labels):
    """Virtual board with a two-wire I²C sensor link and a separate UART console.

    The sensor group has data-board-devicegroup="sensor". Update the address by
    assigning textContent to the single [data-board-address] text element.
    """
    out = _ground(900, 500)
    out.append(_text(30, 39, _label(labels, 'board', 'Raspberry Pi 4B · QEMU'), 22, PAPER, serif=True))
    # Beveled board, four mounting holes and abstract peripheral connectors.
    out.append('''<path d="M228 113 680 96 696 111V402L244 419 228 404Z" fill="#0F292E" opacity=".5"/>
<path d="M228 106 680 89 696 104 244 121Z" fill="#91B6A8" stroke="#C6DDD0"/>
<path d="M680 89 696 104V392L680 377Z" fill="#335D59" stroke="#91B6A8"/>
<path d="M228 106 680 89V377L228 394Z" fill="#58857B" stroke="#C6DDD0" stroke-width="1.5"/>
<path d="M250 164H351V192M504 183H650M478 306H526V350H640M261 306V360H340M360 144V172H475" fill="none" stroke="#B8D1BE" stroke-width="1" opacity=".5"/>
<path d="M492 169H590V155H660M261 272V322H295M490 320H516V361" fill="none" stroke="#B8D1BE" stroke-width="1" opacity=".35"/>
<g fill="#1E3A3D" stroke="#DCE9E6" stroke-width="3"><circle cx="245" cy="120" r="6"/><circle cx="662" cy="105" r="6"/><circle cx="245" cy="377" r="6"/><circle cx="662" cy="361" r="6"/></g>
<path d="M671 163 706 160V211L671 214Z" fill="#D8D6CA" stroke="#FBF8F1"/><path d="M682 172 699 171V202L682 203Z" fill="#1E3A3D"/>
<path d="M671 229 706 227V280L671 282Z" fill="#D8D6CA" stroke="#FBF8F1"/><path d="M682 239 699 238V270L682 271Z" fill="#1E3A3D"/>''')
    # Exactly 40 pins, represented in two rows.
    out.append('<rect x="278" y="112" width="296" height="39" rx="3" fill="#1E3A3D" stroke="#A9CBC5"/>')
    for row in range(2):
        for column in range(20):
            x, y = 287 + column * 14.4, 120 + row * 15
            out.append(f'<rect x="{x:.1f}" y="{y}" width="7" height="7" rx="1" fill="#F2CBAE" stroke="#E9D7AA" stroke-width=".5"/>')
    out.append(_text(423, 76, _label(labels, 'gpio', '40-pin GPIO'), 14, SAGE, 'middle'))
    out.append('<path d="M423 83V109" stroke="#A9CBC5" stroke-width="1"/>')
    # SoC package and edge pins.
    for i in range(8):
        y = 210 + i * 11
        out.append(f'<path d="M374 {y}H364M490 {y}H500" stroke="#E9D7AA" stroke-width="2.8"/>')
    for i in range(9):
        x = 387 + i * 11
        out.append(f'<path d="M{x} 199V189M{x} 305V315" stroke="#E9D7AA" stroke-width="2.8"/>')
    out.append('<rect x="373" y="198" width="119" height="108" rx="6" fill="#F2CBAE" stroke="#FBF8F1" stroke-width="1.5"/><rect x="383" y="208" width="99" height="88" rx="2" fill="#1E3A3D"/>')
    out.append(_text(433, 239, _label(labels, 'soc', 'SoC'), 23, PEACH, 'middle', serif=True))
    out.append(_text(433, 263, 'ARM64', 13, PAPER, 'middle'))
    out.append(_text(433, 282, 'I²C', 11, SAGE, 'middle'))
    # RAM package.
    out.append('<rect x="537" y="205" width="96" height="80" rx="4" fill="#D8CCE0" stroke="#FBF8F1"/><path d="M548 216V230M557 216V230M566 216V230M575 216V230M584 216V230M593 216V230M602 216V230M611 216V230M620 216V230" stroke="#867692" stroke-width="2"/>')
    out.append(_text(585, 251, _label(labels, 'memory', 'Memory'), 13, TEAL, 'middle'))
    out.append(_text(585, 271, 'RAM', 12, '#5E4F6B', 'middle'))
    # SD card lies at the base of the virtual board.
    out.append('''<path d="M283 348H335L349 363V408H283Z" fill="#1E3A3D" stroke="#D8CCE0" stroke-width="1.5"/>
<path d="M290 354V369M298 354V369M306 354V369M314 354V369M322 354V369" stroke="#F2CBAE" stroke-width="4"/>
<path d="M335 348V363H349" fill="none" stroke="#D8CCE0"/>''')
    out.append(_text(316, 394, 'SD', 18, PAPER, 'middle', serif=True))
    out.append(_text(316, 442, _label(labels, 'storage', 'SD image'), 14, SAGE, 'middle'))
    # The external sensor and its two separate wires form one highlightable group.
    out.append('''<g data-board-devicegroup="sensor">
<path d="M50 179H160L174 193V305H50Z" fill="#A9CBC5" stroke="#FBF8F1" stroke-width="1.5"/>
<path d="M160 179V193H174" fill="none" stroke="#1F4A4F"/>
<rect x="67" y="212" width="40" height="47" rx="3" fill="#1E3A3D"/>
<path d="M77 220V239A7 7 0 1 0 87 239V220A5 5 0 0 0 77 220Z" fill="none" stroke="#F2CBAE" stroke-width="1.4"/>
<path d="M82 227V246" stroke="#F2CBAE" stroke-width="2"/><circle cx="82" cy="246" r="3" fill="#F2CBAE"/>
<path d="M174 229H314Q326 229 326 241V250H362M174 261H304Q316 261 316 273V278H362" fill="none" stroke-width="2.4" stroke-linejoin="round" stroke="#F2CBAE"/>
<path d="M174 261H304Q316 261 316 273V278H362" fill="none" stroke="#D8CCE0" stroke-width="2.4"/>
<circle cx="174" cy="229" r="3.5" fill="#F2CBAE"/><circle cx="174" cy="261" r="3.5" fill="#D8CCE0"/>
</g>''')
    out.append(_text(50, 164, _label(labels, 'sensor', 'TMP105 sensor'), 14, PAPER))
    out.append(_text(112, 236, 'I²C', 13, TEAL))
    out.append(_text(64, 286, '0x48', 16, TEAL, attrs='data-board-address=""'))
    out.append(_text(201, 220, 'SDA', 12, PEACH))
    out.append(_text(201, 253, 'SCL', 12, LILAC))
    out.append(_text(118, 336, _label(labels, 'bus', 'Virtual I²C bus'), 13, SAGE, 'middle'))
    # UART is a distinct path; no connection from the sensor to this console.
    out.append('''<path d="M498 294H514V329H712Q726 329 726 341V351H746" fill="none" stroke="#A9CBC5" stroke-width="2"/>
<circle cx="514" cy="329" r="3" fill="#A9CBC5"/>
<rect x="746" y="298" width="130" height="104" rx="5" fill="#FBF8F1"/>
<rect x="755" y="319" width="112" height="68" rx="2" fill="#1E3A3D"/>
<circle cx="758" cy="308" r="2.5" fill="#D9694E"/><circle cx="768" cy="308" r="2.5" fill="#A9CBC5"/>
<path d="M765 333 771 338 765 343M780 340H845M765 354H825M765 367H839" fill="none" stroke="#A9CBC5" stroke-width="2" stroke-linecap="round"/>
<path d="M843 365H851" stroke="#F2CBAE" stroke-width="3"/>''')
    out.append(_text(624, 320, 'UART', 12, SAGE, 'middle'))
    out.append(_text(811, 427, _label(labels, 'console', 'Linux console'), 14, PAPER, 'middle'))
    out.append(_text(811, 449, 'ttyAMA1', 11, SAGE, 'middle'))
    return _root(out, 900, 500, 'board')


def storage(labels):
    """External boot files and an SD root filesystem feed a Linux/cFE guest.

    BOOT is drawn separately from rootfs and has no arrow implying execution of
    applications there. The /cf directory contains modules read by the cFE loader.
    """
    out = _ground(960, 430)
    # Host-provided boot inputs, not files read by firmware from BOOT in this run.
    out.append(_text(25, 38, _label(labels, 'host_files', 'Host boot files'), 20, PAPER, serif=True))
    out.append('<rect x="25" y="58" width="275" height="147" rx="6" fill="#FBF8F1"/>')
    file_rows = [(87, 'kernel', 'Kernel', 'kernel8.img'), (131, 'dtb', 'Device tree', 'bcm2711-rpi-4-b.dtb'), (175, 'initramfs', 'Initramfs', 'initramfs8')]
    for y, key, fallback, name in file_rows:
        out.append(f'<path d="M39 {y-15}H53L59 {y-9}V{y+8}H39Z" fill="#D8CCE0" stroke="#84738F"/><path d="M53 {y-15}V{y-9}H59" fill="none" stroke="#84738F"/>')
        out.append(_text(70, y-3, _label(labels, key, fallback), 12, TEAL))
        out.append(_text(70, y+13, name, 10, '#526A66'))
    # Guest domain is explicitly distinct from host files and the virtual SD.
    out.append('''<rect x="373" y="58" width="561" height="335" rx="10" fill="#294E51" stroke="#A9CBC5" stroke-width="1.2"/>
<path d="M373 110H934" stroke="#577C77"/>
<path d="M301 130H353Q363 130 363 140V159H391" fill="none" stroke="#D8CCE0" stroke-width="1.8"/>
<path d="M300 345H352Q362 345 362 355H392" fill="none" stroke="#F2CBAE" stroke-width="1.8"/>''')
    out.append(_arrow(391, 159, LILAC))
    out.append(_arrow(392, 355, PEACH))
    out.append(_text(394, 91, _label(labels, 'linux', 'Linux guest'), 23, PAPER, serif=True))
    out.append(_text(913, 89, 'QEMU · ARM64', 12, SAGE, 'end'))
    # SD partitions are shown as two storage regions; only rootfs is mounted at /.
    out.append(_text(25, 237, _label(labels, 'sd', 'Virtual SD image'), 20, PAPER, serif=True))
    out.append('''<path d="M25 255H276L300 279V393H25Z" fill="#1E3A3D" stroke="#A9CBC5" stroke-width="1.5"/>
<path d="M276 255V279H300" fill="none" stroke="#A9CBC5"/>
<rect data-storage-region="0" x="39" y="270" width="220" height="46" rx="3" fill="#D8CCE0"/>
<rect data-storage-region="1" x="39" y="326" width="247" height="52" rx="3" fill="#F2CBAE"/>''')
    out.append(_text(51, 288, _label(labels, 'boot', 'Boot partition'), 12, TEAL))
    out.append(_text(51, 306, 'p1 · bootfs · FAT32', 10, '#584F64'))
    out.append(_text(51, 346, _label(labels, 'root', 'Root filesystem'), 12, TEAL))
    out.append(_text(51, 366, 'p2 · rootfs · ext4', 10, '#6A4E40'))
    # Guest process and cFE loader. Modules are files loaded into this process.
    out.append('''<rect x="395" y="135" width="204" height="183" rx="6" fill="#FBF8F1"/>
<rect data-storage-region="2" x="412" y="199" width="170" height="100" rx="5" fill="#A9CBC5"/>
<path d="M425 277H439V264H455V277H471V264H487V277H503V264H519V277H535V264H551V277H569" fill="none" stroke="#37635D" stroke-width="1.5"/>
<path d="M412 185H582" stroke="#D9CDB6"/>''')
    out.append(_text(497, 165, 'Linux', 25, TEAL, 'middle', serif=True))
    out.append(_text(497, 232, 'cFE', 25, TEAL, 'middle', serif=True))
    out.append(_text(497, 252, _label(labels, 'loader', 'Module loader'), 11, TEAL, 'middle'))
    # /cf content on the guest filesystem. No app is drawn in the boot partition.
    out.append('''<path d="M687 147H746L761 160H910V318H687Z" fill="#E4DED0" stroke="#FBF8F1"/>
<path d="M687 147V135H741L752 147" fill="#F2CBAE" stroke="#FBF8F1"/>
<rect x="702" y="208" width="192" height="26" rx="3" fill="#FBF8F1"/>
<rect x="702" y="242" width="192" height="26" rx="3" fill="#FBF8F1"/>
<rect x="702" y="276" width="192" height="26" rx="3" fill="#FBF8F1"/>
<path d="M679 247H608" fill="none" stroke="#F2CBAE" stroke-width="1.8"/>''')
    out.append(_arrow(608, 247, PEACH, 'left'))
    out.append(_text(705, 183, '/cf', 25, TEAL, serif=True))
    out.append(_text(894, 182, _label(labels, 'apps', 'cFS apps'), 12, TEAL, 'end'))
    for y, name, color in [(225, 'sample_app.so', '#D9694E'), (259, 'ci_lab.so', '#4E7F7B'), (293, 'to_lab.so', '#867392')]:
        out.append(f'<rect x="713" y="{y-10}" width="8" height="8" rx="1" fill="{color}"/>')
        out.append(_text(732, y, name, 12, TEAL))
    out.append(_text(643, 230, '.so', 11, PEACH, 'middle'))
    out.append(_text(705, 339, 'cfe_es_startup.scr', 11, SAGE))
    out.append(_text(395, 359, 'root=/dev/mmcblk1p2', 12, PEACH))
    out.append(_text(395, 379, '/', 12, PAPER))
    return _root(out, 960, 430, 'storage')
