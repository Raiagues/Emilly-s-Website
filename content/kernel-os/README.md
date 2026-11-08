# Evidências do kernel OS

Fonte: https://github.com/Raiagues/OS, commit `920d3c9d93e0cda928e48c6cd77ea239a054976b`.

As seis atividades em `examples/` e o kernel completo da raiz foram compilados com as ferramentas do curso já instaladas em `/matieres/4MMPCSEA/xinul` e executados na máquina CEP do QEMU. O código do clone permanece sem alterações. `evidence.json` guarda os trechos com URLs fixas de commit, o mapa de memória, as pilhas, as saídas UART e os estados capturados.

## Como foram capturados os PNGs

Cada imagem contém os pixels reais da região de framebuffer `0x80000000..0x80384000`, 1280 × 720 × 4 bytes. O código escreve pixels BGRX little-endian, convertidos sem perda para PNG RGB. Os pixels não foram recortados, reescritos, ampliados nem desenhados por IA. O `screendump` padrão do QEMU CEP captura a superfície de controle/logo, por isso foi usada a própria VRAM.

Pixels, console, scrolling e UART foram pausados em linhas do programa original com breakpoints GDB. O contador `time` inclui o custo de depuração e exportação e não mede performance; `playback_time` é apenas uma sugestão de apresentação didática. Timer e processos foram executados continuamente e pausados brevemente por QMP para capturar a imagem. Seus frames incluem valores de `ticks`, segundos do kernel e, para processos, estados/pilhas lidos da própria RAM.

`capture.py` registra o procedimento e `logs/` contém os scripts GDB, logs de build, UART, mapa de endereços e símbolos do ELF. O script usa caminhos locais da sessão e requer um clone do commit indicado, as ferramentas CEP e Pillow. A coleta completa também foi executada a partir do kernel da raiz; os logs e dois PNGs adicionais documentam o início e o fim das tarefas.

## Limites

O repositório oferece exemplos separados com correções posteriores ao curso; não são snapshots brutos de 2023. As tarefas compartilham RAM e machine mode, sem memória virtual, proteção entre processos, filesystem ou teclado. Os endereços dos símbolos/pilhas pertencem ao ELF compilado nesta coleta e podem mudar com o build. Os endereços dos dispositivos vêm da plataforma CEP. Os logs estão em francês/inglês conforme o programa; descrições do portfólio podem ser traduzidas sem alterar a saída capturada.

Créditos e licenças da infraestrutura e fontes são preservados em `COPYING.GPL-2` e no README do repositório original.
