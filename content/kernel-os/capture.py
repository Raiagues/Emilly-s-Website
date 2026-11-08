"""Capture actual CEP framebuffer memory and UART. No guest source modifications."""
from pathlib import Path
import os, subprocess, json, time, hashlib, re, struct
from PIL import Image
BASE=Path('/tmp/emilly-kernel-evidence')
REPO=BASE/'OS'
OUT=BASE/'captures'
TOOLS='/matieres/4MMPCSEA/xinul/bin'
WIDTH,HEIGHT=1280,720
FB=0x80000000
SIZE=WIDTH*HEIGHT*4
CAPTURES={}

def png(raw):
    data=raw.read_bytes()
    assert len(data)==SIZE,(raw,len(data))
    im=Image.frombytes('RGB',(WIDTH,HEIGHT),data,'raw','BGRX')
    dest=raw.with_suffix('.png')
    im.save(dest,optimize=True)
    return str(dest)

def static(folder, slug, stages):
    root=REPO if folder is None else REPO/'examples'/folder
    serial=OUT/(slug+'-uart.txt')
    meta=OUT/(slug+'-frames.json')
    basecmd=['sh','scripts/course-env.sh',TOOLS+'/qemu-system-riscv64','-machine','cep','-bios','none','-kernel','build/cep/kernel.elf','-m','32M','-smp','1','-display','none','-monitor','none','-serial','file:'+str(serial),'-no-user-config','-S','-gdb','stdio']
    commands=['set pagination off','set confirm off','set debuginfod enabled off','file build/cep/kernel.elf','target remote | '+' '.join(basecmd),'python import time,json,pathlib; capture_start=time.monotonic(); capture_frames=[]']
    disassembly=subprocess.check_output(['gdb-multiarch','--batch','build/cep/kernel.elf','-ex','disassemble kernel_start'],cwd=root,text=True)
    final_pc=re.search(r'(0x[0-9a-f]+) <[^>]+>:\s+wfi',disassembly)[1]
    for i,(breakpoint,label) in enumerate(stages):
        if breakpoint=='FINAL':breakpoint='*'+final_pc
        path=OUT/(slug+f'-{i+1:02}.bin')
        commands += ['tbreak '+breakpoint, 'continue',f'dump binary memory {path} {FB:#x} {FB+SIZE:#x}',f'python capture_frames.append(dict(file="{path.with_suffix(".png")}",time=round(time.monotonic()-capture_start,3),label={label!r},breakpoint={breakpoint!r},pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path({str(serial)!r}).read_bytes().decode("utf8","replace")))']
    commands += [f'python pathlib.Path({str(meta)!r}).write_text(json.dumps(capture_frames,ensure_ascii=False,indent=2))','kill','quit']
    script=OUT/(slug+'-capture.gdb')
    script.write_text('\n'.join(commands)+'\n')
    with (OUT/(slug+'-gdb.txt')).open('w') as log:
        result=subprocess.run(['gdb-multiarch','--batch','-x',str(script)],cwd=root,stdout=log,stderr=subprocess.STDOUT,timeout=90)
    if result.returncode or not meta.exists():
        raise RuntimeError(slug+' failed: '+(OUT/(slug+'-gdb.txt')).read_text()[-1800:])
    frames=json.loads(meta.read_text())
    assert len(frames)==len(stages)
    for frame in frames:png(Path(frame['file']).with_suffix('.bin'))
    CAPTURES[slug]=dict(folder=folder,kind='gdb-breakpoints',command=' '.join(basecmd),frames=frames,log=str(serial))
    print(slug,len(frames),'frames',flush=True)

def live(folder, slug, times):
    root=REPO if folder is None else REPO/'examples'/folder
    serial=OUT/(slug+'-uart.txt')
    cmd=['sh','scripts/course-env.sh',TOOLS+'/qemu-system-riscv64','-machine','cep','-bios','none','-kernel','build/cep/kernel.elf','-m','32M','-smp','1','-display','none','-qmp','stdio','-serial','file:'+str(serial),'-no-user-config']
    p=subprocess.Popen(cmd,cwd=root,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    p.stdout.readline()
    def q(command):
        p.stdin.write(json.dumps(command)+'\n');p.stdin.flush()
        while True:
            result=json.loads(p.stdout.readline())
            if 'error' in result: raise RuntimeError(result)
            if 'return' in result:return result['return']
    q({'execute':'qmp_capabilities'})
    start=time.monotonic();frames=[]
    for i,second in enumerate(times):
        delay=second-(time.monotonic()-start)
        if delay>0:time.sleep(delay)
        q({'execute':'stop'})
        raw=OUT/(slug+f'-{i+1:02}.bin')
        q({'execute':'pmemsave','arguments':{'val':FB,'size':SIZE,'filename':str(raw)}})
        actual=round(time.monotonic()-start,3)
        uart=serial.read_bytes().decode('utf8','replace')
        observed={}
        tick_address=0x3188 if slug=='timer' else 0x240c0
        tick_file=OUT/(slug+f'-{i+1:02}-ticks.bin')
        q({'execute':'pmemsave','arguments':{'val':tick_address,'size':8,'filename':str(tick_file)}})
        ticks=struct.unpack('<Q',tick_file.read_bytes())[0]
        observed.update(ticks=ticks,kernel_seconds=ticks//20)
        if slug in ('processes','complete-kernel'):
            process_file=OUT/(slug+f'-{i+1:02}-process-table.bin')
            q({'execute':'pmemsave','arguments':{'val':0x3d70,'size':131904,'filename':str(process_file)}})
            values=process_file.read_bytes(); processes=[]
            for pid in range(4):
                start_record=pid*32976
                state=struct.unpack_from('<I',values,start_record+36)[0]
                processes.append(dict(pid=pid,name=values[start_record+4:start_record+36].split(b'\x00')[0].decode(),state=state,state_label=['RUN','RUNNABLE','WAIT','DIE'][state],saved_sp=hex(struct.unpack_from('<Q',values,start_record+48)[0]),wake_at=struct.unpack_from('<I',values,start_record+32960)[0]))
            observed['processes']=processes
        frames.append(dict(file=png(raw),time=actual,label=f'Execução real: {ticks//20} s no relógio do kernel',uart=uart,observed=observed))
        q({'execute':'cont'})
    mtree=q({'execute':'human-monitor-command','arguments':{'command-line':'info mtree'}})
    (OUT/(slug+'-memory-map.txt')).write_text(mtree)
    q({'execute':'quit'});p.communicate(timeout=3)
    (OUT/(slug+'-frames.json')).write_text(json.dumps(frames,ensure_ascii=False,indent=2))
    CAPTURES[slug]=dict(folder=folder,kind='timed-run',command=' '.join(cmd),frames=frames,log=str(serial))
    print(slug,len(frames),'frames',flush=True)

static('01-pixels','pixels',[
 ('src/main.c:33','Primeira linha de glifos: pixels vermelhos'),
 ('src/main.c:34','Segunda linha: pixels verdes'),
 ('src/main.c:35','Terceira linha: pixels azuis'),
 ('src/main.c:39','Quarta linha: caracteres brancos'),
 ('FINAL','Texto ultrapassa a última coluna e continua na linha seguinte')])
static('02-console','console',[
 ('src/main.c:17','LF: AB e CD aparecem em linhas diferentes'),
 ('src/main.c:18','BS: o cursor volta e C substitui B'),
 ('src/main.c:19','CR: Z substitui A no início da linha'),
 ('src/main.c:21','HT: B aparece no próximo ponto de tabulação'),
 ('src/main.c:23','Tabulação próxima da borda leva Z à próxima linha'),
 ('FINAL','Console completo, com cursor e explicação dos testes')])
static('03-scroll','scroll',[
 ('src/main.c:15 if i == 20','20 linhas escritas; ainda há espaço na tela'),
 ('src/main.c:15 if i == 80','80 linhas escritas; o cursor se aproxima da borda inferior'),
 ('src/main.c:15 if i == 90','A rolagem desloca o corpo da tela e preserva o cabeçalho'),
 ('FINAL','100 linhas escritas; as primeiras saíram da área visível')])
static('04-uart','uart',[
 ('src/main.c:20','Título enviado para a tela e para a UART'),
 ('src/main.c:22','UART only aparece só no fluxo serial'),
 ('src/main.c:25','Console and UART aparece nos dois destinos'),
 ('FINAL','Saída final: transmissão direta e saída espelhada')])
live('05-clock','timer',[.3,1.2,2.3,3.4,4.5])
live('06-processes','processes',[.4,1.4,2.5,4.6,6.8,9.4])
(OUT/'capture-index.json').write_text(json.dumps(CAPTURES,ensure_ascii=False,indent=2))
