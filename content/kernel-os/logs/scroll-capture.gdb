set pagination off
set confirm off
set debuginfod enabled off
file build/cep/kernel.elf
target remote | sh scripts/course-env.sh /matieres/4MMPCSEA/xinul/bin/qemu-system-riscv64 -machine cep -bios none -kernel build/cep/kernel.elf -m 32M -smp 1 -display none -monitor none -serial file:/tmp/emilly-kernel-evidence/captures/scroll-uart.txt -no-user-config -S -gdb stdio
python import time,json,pathlib; capture_start=time.monotonic(); capture_frames=[]
tbreak src/main.c:15 if i == 20
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/scroll-01.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/scroll-01.png",time=round(time.monotonic()-capture_start,3),label='20 linhas escritas; ainda há espaço na tela',breakpoint='src/main.c:15 if i == 20',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/scroll-uart.txt').read_bytes().decode("utf8","replace")))
tbreak src/main.c:15 if i == 80
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/scroll-02.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/scroll-02.png",time=round(time.monotonic()-capture_start,3),label='80 linhas escritas; o cursor se aproxima da borda inferior',breakpoint='src/main.c:15 if i == 80',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/scroll-uart.txt').read_bytes().decode("utf8","replace")))
tbreak src/main.c:15 if i == 90
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/scroll-03.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/scroll-03.png",time=round(time.monotonic()-capture_start,3),label='A rolagem desloca o corpo da tela e preserva o cabeçalho',breakpoint='src/main.c:15 if i == 90',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/scroll-uart.txt').read_bytes().decode("utf8","replace")))
tbreak *0x0000000000002078
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/scroll-04.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/scroll-04.png",time=round(time.monotonic()-capture_start,3),label='100 linhas escritas; as primeiras saíram da área visível',breakpoint='*0x0000000000002078',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/scroll-uart.txt').read_bytes().decode("utf8","replace")))
python pathlib.Path('/tmp/emilly-kernel-evidence/captures/scroll-frames.json').write_text(json.dumps(capture_frames,ensure_ascii=False,indent=2))
kill
quit
