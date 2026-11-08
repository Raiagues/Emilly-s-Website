set pagination off
set confirm off
set debuginfod enabled off
file build/cep/kernel.elf
target remote | sh scripts/course-env.sh /matieres/4MMPCSEA/xinul/bin/qemu-system-riscv64 -machine cep -bios none -kernel build/cep/kernel.elf -m 32M -smp 1 -display none -monitor none -serial file:/tmp/emilly-kernel-evidence/captures/console-uart.txt -no-user-config -S -gdb stdio
python import time,json,pathlib; capture_start=time.monotonic(); capture_frames=[]
tbreak src/main.c:17
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/console-01.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/console-01.png",time=round(time.monotonic()-capture_start,3),label='LF: AB e CD aparecem em linhas diferentes',breakpoint='src/main.c:17',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/console-uart.txt').read_bytes().decode("utf8","replace")))
tbreak src/main.c:18
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/console-02.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/console-02.png",time=round(time.monotonic()-capture_start,3),label='BS: o cursor volta e C substitui B',breakpoint='src/main.c:18',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/console-uart.txt').read_bytes().decode("utf8","replace")))
tbreak src/main.c:19
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/console-03.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/console-03.png",time=round(time.monotonic()-capture_start,3),label='CR: Z substitui A no início da linha',breakpoint='src/main.c:19',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/console-uart.txt').read_bytes().decode("utf8","replace")))
tbreak src/main.c:21
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/console-04.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/console-04.png",time=round(time.monotonic()-capture_start,3),label='HT: B aparece no próximo ponto de tabulação',breakpoint='src/main.c:21',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/console-uart.txt').read_bytes().decode("utf8","replace")))
tbreak src/main.c:23
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/console-05.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/console-05.png",time=round(time.monotonic()-capture_start,3),label='Tabulação próxima da borda leva Z à próxima linha',breakpoint='src/main.c:23',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/console-uart.txt').read_bytes().decode("utf8","replace")))
tbreak *0x00000000000020e4
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/console-06.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/console-06.png",time=round(time.monotonic()-capture_start,3),label='Console completo, com cursor e explicação dos testes',breakpoint='*0x00000000000020e4',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/console-uart.txt').read_bytes().decode("utf8","replace")))
python pathlib.Path('/tmp/emilly-kernel-evidence/captures/console-frames.json').write_text(json.dumps(capture_frames,ensure_ascii=False,indent=2))
kill
quit
