set pagination off
set confirm off
set debuginfod enabled off
file build/cep/kernel.elf
target remote | sh scripts/course-env.sh /matieres/4MMPCSEA/xinul/bin/qemu-system-riscv64 -machine cep -bios none -kernel build/cep/kernel.elf -m 32M -smp 1 -display none -monitor none -serial file:/tmp/emilly-kernel-evidence/captures/pixels-uart.txt -no-user-config -S -gdb stdio
python import time,json,pathlib; capture_start=time.monotonic(); capture_frames=[]
tbreak src/main.c:33
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/pixels-01.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/pixels-01.png",time=round(time.monotonic()-capture_start,3),label='Primeira linha de glifos: pixels vermelhos',breakpoint='src/main.c:33',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/pixels-uart.txt').read_bytes().decode("utf8","replace")))
tbreak src/main.c:34
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/pixels-02.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/pixels-02.png",time=round(time.monotonic()-capture_start,3),label='Segunda linha: pixels verdes',breakpoint='src/main.c:34',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/pixels-uart.txt').read_bytes().decode("utf8","replace")))
tbreak src/main.c:35
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/pixels-03.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/pixels-03.png",time=round(time.monotonic()-capture_start,3),label='Terceira linha: pixels azuis',breakpoint='src/main.c:35',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/pixels-uart.txt').read_bytes().decode("utf8","replace")))
tbreak src/main.c:39
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/pixels-04.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/pixels-04.png",time=round(time.monotonic()-capture_start,3),label='Quarta linha: caracteres brancos',breakpoint='src/main.c:39',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/pixels-uart.txt').read_bytes().decode("utf8","replace")))
tbreak *0x00000000000019f4
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/pixels-05.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/pixels-05.png",time=round(time.monotonic()-capture_start,3),label='Texto ultrapassa a última coluna e continua na linha seguinte',breakpoint='*0x00000000000019f4',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/pixels-uart.txt').read_bytes().decode("utf8","replace")))
python pathlib.Path('/tmp/emilly-kernel-evidence/captures/pixels-frames.json').write_text(json.dumps(capture_frames,ensure_ascii=False,indent=2))
kill
quit
