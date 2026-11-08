set pagination off
set confirm off
set debuginfod enabled off
file build/cep/kernel.elf
target remote | sh scripts/course-env.sh /matieres/4MMPCSEA/xinul/bin/qemu-system-riscv64 -machine cep -bios none -kernel build/cep/kernel.elf -m 32M -smp 1 -display none -monitor none -serial file:/tmp/emilly-kernel-evidence/captures/uart-uart.txt -no-user-config -S -gdb stdio
python import time,json,pathlib; capture_start=time.monotonic(); capture_frames=[]
tbreak src/main.c:20
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/uart-01.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/uart-01.png",time=round(time.monotonic()-capture_start,3),label='Título enviado para a tela e para a UART',breakpoint='src/main.c:20',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/uart-uart.txt').read_bytes().decode("utf8","replace")))
tbreak src/main.c:22
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/uart-02.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/uart-02.png",time=round(time.monotonic()-capture_start,3),label='UART only aparece só no fluxo serial',breakpoint='src/main.c:22',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/uart-uart.txt').read_bytes().decode("utf8","replace")))
tbreak src/main.c:25
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/uart-03.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/uart-03.png",time=round(time.monotonic()-capture_start,3),label='Console and UART aparece nos dois destinos',breakpoint='src/main.c:25',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/uart-uart.txt').read_bytes().decode("utf8","replace")))
tbreak *0x0000000000001790
continue
dump binary memory /tmp/emilly-kernel-evidence/captures/uart-04.bin 0x80000000 0x80384000
python capture_frames.append(dict(file="/tmp/emilly-kernel-evidence/captures/uart-04.png",time=round(time.monotonic()-capture_start,3),label='Saída final: transmissão direta e saída espelhada',breakpoint='*0x0000000000001790',pc=str(gdb.parse_and_eval("$pc")),uart=pathlib.Path('/tmp/emilly-kernel-evidence/captures/uart-uart.txt').read_bytes().decode("utf8","replace")))
python pathlib.Path('/tmp/emilly-kernel-evidence/captures/uart-frames.json').write_text(json.dumps(capture_frames,ensure_ascii=False,indent=2))
kill
quit
