"""Infrastructure tour: one interactive data path, board, storage and drivers."""
import html
import json
import math
import runpy

E=html.escape

class Infrastructure:
    def __init__(self,case):
        self.c=case
        self.copy=runpy.run_path(str(case.b['ROOT']/'content/flight_infrastructure.py'))['COPY']
        case.strings.update(self.copy)
        self.t=case.text
        self.draw=runpy.run_path(str(case.b['ROOT']/'scripts/flight_infrastructure_drawings.py'))
        self.evidence=json.loads((case.b['ROOT']/'content/flight-studio/infrastructure-evidence.json').read_text())
        self.commit=self.evidence['commit']
        self.repo='https://github.com/Raiagues/cfs_emulator'

    def labels(self,**keys):
        return {name:self.c.strings[key][self.c.lang] for name,key in keys.items()}

    def link(self,path,label=None):
        return self.c.source_link(f'{self.repo}/blob/{self.commit}/{path}',E(label or path))

    def location(self,key):
        return f'<p class="fs-edit-location"><span>{self.t("edit_signal")}</span><code>{self.t(key)}</code></p>'

    def node(self,index,title,key,value=None):
        value_html=f'<output data-fs-node-value="{value}">{"27.830" if value=="sample" else "27.5"} °C</output>' if value else ''
        return f'<button type="button" class="fs-flow-node fs-node-{index}" data-fs-node="{index}" aria-controls="fs-explain-{index}" aria-pressed="false" disabled><span class="fs-node-index">0{index+1}</span><span class="fs-node-purpose">{self.t(key)}</span><strong>{E(title)}</strong>{value_html}</button>'

    def signal(self):
        t=self.t
        points=' '.join(f'{45+i*8:.1f},{165-3*(23.5+5*math.sin(2*math.pi*i/30)):.1f}' for i in [n/4 for n in range(241)])
        controls=''
        for key,value,minimum,maximum,step,unit in [('initial',23.5,10,35,.5,'°C'),('amplitude',5,0,10,.5,'°C'),('period',30,10,60,1,'s')]:
            controls+=f'<label for="fs-{key}"><span>{t(key)} <output data-fs-readout="{key}">{value} {unit}</output></span><input type="range" id="fs-{key}" data-fs-param="{key}" min="{minimum}" max="{maximum}" step="{step}" value="{value}"></label>'
        plot=f'''<div class="fs-wave"><div class="fs-panel-bar"><span>sensors/tmp105.py</span><span>sample(t)</span></div><svg viewBox="0 0 560 205" role="img" aria-label="{t('signal_title')}"><g class="fs-chart-grid"><path d="M45 30H525M45 75H525M45 120H525M45 165H525M45 30V165M285 30V165M525 30V165"/></g><g class="fs-chart-labels"><text x="10" y="35">45°</text><text x="10" y="80">30°</text><text x="10" y="125">15°</text><text x="14" y="170">0°</text><text x="45" y="192">0 s</text><text x="270" y="192">30 s</text><text x="500" y="192">60 s</text></g><polyline data-fs-wave points="{points}"/><path data-fs-wave-guide d="M85 30V165"/><circle data-fs-wave-dot cx="85" cy="81.5" r="6"/></svg><div class="fs-time-control" data-fs-controls hidden><label for="fs-time">{t('time')} <output data-fs-time>5.00 s</output></label><input type="range" id="fs-time" data-fs-param="time" min="0" max="60" step=".25" value="5"></div><div class="fs-measurements"><div><span>{t('source_value')}</span><output data-fs-source-value>27.830 <small>°C</small></output></div><span aria-hidden="true">→</span><div><span>{t('read_value')}</span><output data-fs-read-value>27.5 <small>°C</small></output></div></div><p class="fs-resolution">{t('resolution')}</p></div>'''
        settings=f'''<div class="fs-signal-settings"><p class="eyebrow">01 / PYTHON</p><h3>{t('signal_title')}</h3><p>{t('signal_copy')}</p><div class="fs-signal-inputs" data-fs-controls hidden><label for="fs-mode"><span>{t('waveform')}</span><select id="fs-mode" data-fs-param="mode"><option value="sine">{t('sine')}</option><option value="constant">{t('constant')}</option></select></label>{controls}</div><pre class="fs-function" aria-label="sample"><code>def sample(seconds, initial_c):
    return initial_c + <b data-fs-code-amplitude>5</b> * sin(
        2 * pi * seconds / <b data-fs-code-period>30</b>
    )</code></pre>{self.location('signal_location')}</div>'''
        return f'<div class="fs-signal-lab">{settings}{plot}</div>'

    def flow(self):
        t=self.t
        diagram=f'''<div class="fs-route" data-fs-route><svg class="fs-route-wires" data-fs-wires aria-hidden="true"><defs><marker id="fs-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M1 1 9 5 1 9"/></marker></defs><g data-fs-paths></g><g data-fs-traveller hidden><circle r="5"/><rect x="10" y="-23" width="85" height="22" rx="4"/><text x="16" y="-8">27.830 °C</text></g></svg>
<section class="fs-host"><h3>{t('host')}</h3>{self.node(0,'Python · sample()', 'source','sample')}{self.node(1,'QMP · qom-set','control')}</section>
<section class="fs-machine"><h3>{t('board_runtime')}</h3>{self.node(2,'TMP105 · I²C 0x48','sensor','sample')}<section class="fs-guest"><h4>{t('guest')}</h4><div class="fs-guest-nodes">{self.node(3,'/dev/i2c-1','linux_driver')}{self.node(4,'linux_i2c_lib + tmp105_lib','libraries','read')}{self.node(5,'thermal_app','mission','read')}{self.node(6,'Software Bus → TO_LAB','bus','read')}</div></section></section>
<section class="fs-return"><h3>GROUND STATION</h3>{self.node(7,'Flight Studio','ground','read')}<p class="fs-return-channel">UDP → Python → HTTP</p></section></div>'''
        explain=''.join(f'<article id="fs-explain-{i}" data-fs-explain="{i}"><span class="fs-explain-number">0{i+1}</span><div><h3>{t(key)}</h3><p>{t("flow_"+str(i))}</p></div></article>' for i,key in enumerate(['source','control','sensor','linux_driver','libraries','mission','bus','ground']))
        action=f'<div class="fs-flow-toolbar" data-fs-controls hidden><div><span class="eyebrow">{t("model")}</span><p data-fs-status role="status">{t("sample_status")} 5.00 s · 27.830 °C</p></div><div class="fs-flow-buttons"><button type="button" class="fs-action" data-fs-follow data-start-label="{t("follow")}" data-pause-label="{t("pause")}">▶ {t("follow")}</button><button type="button" data-fs-next>{t("next_step")} →</button><button type="button" data-fs-reset aria-label="{t("reset")}">↺</button></div></div>'
        return self.signal()+f'<div class="fs-flow-lab">{action}{diagram}<div class="fs-flow-explanations">{explain}</div><p class="fs-model-note">{t("flow_note")}</p></div>'

    def board(self):
        t=self.t
        drawing=self.draw['board'](self.labels(board='board_runtime',sensor='sensor_short',gpio='gpio_short',bus='i2c_short',console='console_short',memory='ram_short',storage='sd_short'))
        settings=f'''<div class="fs-board-settings"><p class="eyebrow">project/config.json</p><h3>{t('board_settings')}</h3>{self.location('board_location')}<div class="fs-device-controls" data-fs-controls hidden><label><input type="checkbox" data-fs-device="tmp105" checked><span><strong>TMP105</strong>{t('temperature_sensor')}</span></label><label><input type="checkbox" data-fs-device="mag" checked><span><strong>LSM303DLHC</strong>{t('magnetic_sensor')}</span></label><label class="fs-address-label" for="fs-address">{t('i2c_address')}<select id="fs-address" data-fs-address><option>0x48</option><option>0x49</option><option>0x4a</option><option>0x4b</option></select></label></div><p class="fs-board-note">{t('board_note')}</p></div>'''
        boot='<div class="fs-boot-parts">'+''.join(f'<article><span class="fs-file-icon" aria-hidden="true">↳</span><div><h4>{E(name)}</h4><code>{E(path)}</code><p>{t(key)}</p></div></article>' for name,path,key in [('KERNEL','board/kernel8.img','boot_kernel'),('DEVICE TREE','board/bcm2711-rpi-4-b.dtb','boot_dtb'),('INITRAMFS','board/initramfs8','boot_init')])+'</div>'
        args='-M raspi4b\n-device tmp105,id=tmp105,bus=i2c-bus.1,address=0x48\n-device lsm303dlhc_mag,id=lsm303dlhc_mag,bus=i2c-bus.1,address=0x1e'
        return f'<div class="fs-board-lab"><div class="fs-board-art" tabindex="0" role="group" aria-label="{t('board_short')}">{drawing}<span class="fs-magnet-label" data-fs-magnet>LSM303DLHC · I²C 0x1e</span></div>{settings}</div><div class="fs-boot-output"><h3>{t("qemu_args")}</h3><pre tabindex="0" aria-label="QEMU"><code data-fs-qemu-args>{E(args)}</code></pre></div>{boot}'

    def storage(self):
        t=self.t
        diagram=self.draw['storage'](self.labels(host_files='host_boot_short',linux='guest',sd='sd_short',boot='boot_partition',root='root_partition',loader='loader_short',apps='apps_short',dtb='dtb_short'))
        choices=''.join(f'<button type="button" data-fs-part="{i}" aria-controls="fs-part-{i}" aria-pressed="{str(i==1).lower()}"><span>0{i+1}</span><strong>{t(key)}</strong><code>{path}</code></button>' for i,(key,path) in enumerate([('boot_partition','bootfs / FAT32'),('root_partition','rootfs / ext4'),('running_apps','core-cpu1 / cFE')]))
        descriptions=''.join(f'<div id="fs-part-{i}" data-fs-part-detail="{i}"><h3>{t(key)}</h3><p>{t(body)}</p></div>' for i,(key,body) in enumerate([('boot_partition','part_boot'),('root_partition','part_root'),('running_apps','part_apps')]))
        stages=[('source_stage','HOST','cFS/apps/thermal_app/fsw/src/thermal_app_user.c'),('build_stage','HOST','cFS/build-flight/exe/cpu1/cf/thermal_app.so'),('install_stage','LINUX / ROOTFS','/opt/cFS/build-rpi_linux/exe/cpu1/cf/'),('load_stage','cFE / RAM','/cf/cfe_es_startup.scr → thermal_app.so')]
        trail='<ol class="fs-app-trail">'+''.join(f'<li><span class="eyebrow">0{i+1} / {label}</span><h4>{t(key)}</h4><code>{E(path)}</code></li>' for i,(key,label,path) in enumerate(stages))+'</ol>'
        return f'<div class="fs-storage-art" tabindex="0" role="group" aria-label="{t('disk_short')}">{diagram}</div><div class="fs-partitions" data-fs-controls hidden>{choices}</div><div class="fs-partition-details">{descriptions}</div><div class="fs-app-location"><h3>{t("app_path")}</h3>{trail}<p>{t("app_note")}</p><p class="fs-infrastructure-note">{t("build_infra")}</p><p class="fs-mount-map"><code>cFE /cf</code><span aria-hidden="true">↔</span><code>/opt/cFS/build-rpi_linux/exe/cpu1/cf/</code></p></div>'

    def drivers(self):
        t=self.t
        chains=[('i2c_title','i2c_body',[('APP','thermal_app'),('SENSOR LIB','tmp105_lib'),('BUS LIB','linux_i2c_lib'),('LINUX','/dev/i2c-1'),('QEMU','TMP105')]),('uart_title','uart_body',[('LINUX','console=ttyAMA1'),('UART','BCM / PL011'),('QEMU','-serial'),('HOST','logs/latest.log')])]
        buttons=''.join(f'<button type="button" data-fs-driver="{i}" aria-pressed="{str(i==0).lower()}" aria-controls="fs-driver-{i}">{t(key)}</button>' for i,(key,_,_) in enumerate(chains))
        panels=''
        for i,(key,body,chain) in enumerate(chains):
            blocks=''.join(f'<div><span>{name}</span><strong>{value}</strong></div>' for name,value in chain)
            end=f'<p class="fs-driver-return">← {t("driver_return")} · <output data-fs-driver-value>27.5 °C</output></p>' if i==0 else f'<p class="fs-driver-return">{t("uart_caption")}</p>'
            panels+=f'<article id="fs-driver-{i}" data-fs-driver-detail="{i}"><h3>{t(key)}</h3><div class="fs-driver-chain">{blocks}</div>{end}<p>{t(body)}</p>{self.link("project/drivers/"+("linux_i2c_lib" if i==0 else "linux_uart_lib")+"/README.md")}</article>'
        return f'<div class="fs-driver-lab"><div class="fs-driver-choices" data-fs-controls hidden>{buttons}</div>{panels}<p class="fs-channel-note">{t("driver_channels")}</p></div>'

    def editing(self):
        t=self.t
        rows=[('edit_board','Toolbar','project/config.json → toolchain'),('edit_device','Architecture / Hardware','project/config.json → QEMU / DTB'),('edit_wave','Synthetic data','sensors/tmp105.py + sensors/signals.py'),('edit_app','Architecture / Edit','_user.c → CMake / startup / SCH / TO')]
        return '<ol class="fs-edit-map">'+''.join(f'<li><span class="fs-edit-number">0{i+1}</span><div><p class="eyebrow">{label}</p><h3>{t(key)}</h3><p>{t(key+"_body")}</p></div><code>{E(path)}</code></li>' for i,(key,label,path) in enumerate(rows))+'</ol>'

    def page(self):
        c=self.c;t=self.t
        hero=self.draw['hero'](self.labels(signals='source',sensor='sensor',apps='apps_short',linux='guest',virtual_board='board_runtime'))
        sections=[('data-journey','flow_title','flow_intro',self.flow(),'flow_short'),('virtual-board','board_title','board_intro',self.board(),'board_short'),('mission-storage','disk_title','disk_intro',self.storage(),'disk_short'),('device-drivers','drivers_title','drivers_intro',self.drivers(),'drivers_short'),('where-to-edit','where_title','where_intro',self.editing(),'where_short')]
        chapters=''.join(c.chapter(i+1,sid,title,body,intro) for i,(sid,title,intro,body,_) in enumerate(sections))
        navigation=[(sid,t(short)) for sid,_,_,_,short in sections]
        footer=f'<p>{t("sources_body")}</p>'+''.join(self.link(path,label) for path,label in [('hardware/README.md','QEMU / Linux'),('sensors/README.md','Python / sensors'),('project/README.md','cFS / mission')])
        c.config['infrastructure']={'status':self.copy['sample_status'][c.lang],'missing':self.copy['missing_sensor'][c.lang],'locale':c.lang}
        return c.shell(chapters,navigation,hero,t('scope'),[('QEMU',t('board_metric')),('Linux',t('linux_metric')),('cFS',t('cfs_metric'))],footer).replace('engineering-case flight-case','engineering-case flight-case flight-infra')

def render(case):
    return Infrastructure(case).page()
