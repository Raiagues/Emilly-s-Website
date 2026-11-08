# Flight Studio: implementação e execução local

Fonte indicada pela proprietária: `https://github.com/Raiagues/cfs_emulator`. A execução usou uma cópia da instalação existente em `~/Documents/raspi/pi4-emulator/boot_cfs`, no commit `f9b21e76e04915ec1c401585be115f024bdc3597`. O submódulo cFS já tinha modificações locais; portanto o commit superior, isoladamente, não representa todos os arquivos da instalação. `evidence.json` preserva essa origem e as referências de código.

## Capturas e resultados observados

As 12 imagens de `screenshots.json` são capturas reais do navegador, em 1728 × 1080. O manifesto registra arquivo, legenda, horário e SHA256. Elas mostram editor, arquitetura da missão, execução nativa, comando, evento, telemetria, relações extraídas do C, comunicação observada, prévia do gerador, Python e hardware QEMU.

- cFS nativo chegou a `OPERATIONAL`. O comando `SAMPLE_APP_NOOP_CC` produziu os bytes `18 82 C0 00 00 01 00 A4` enviados por UDP à porta 1234. O evento NOOP retornou e o housekeeping de 18 bytes, MID `0x0883`, mostrou `CommandCounter` de 0 para 1, com `CommandErrorCounter` em 0. Os pacotes e observações estão em `noop-observed.json` e `evidence.json.command_flow`.
- O cFS também foi compilado e executado no Linux ARM64 da Raspberry Pi emulada. A arquitetura `aarch64`, o estado `OPERATIONAL` da invocação atual e a igualdade SHA256 entre binário compilado e instalado foram verificados. O processo nativo estava parado durante essa captura.
- A injeção de sinais por QMP foi executada: TMP105 `27,830 °C → 27830 m°C`, magnetômetro Y `17,321 µT → 17321 nT`, ambos com resposta `OK`. `qemu-observed.json` preserva os dados. A missão capturada não tinha uma aplicação de leitura dos sensores: a captura comprova a injeção no modelo do dispositivo, sem comprovar uma leitura I²C seguida de publicação de telemetria.
- O gerador foi mostrado em prévia; `orbit_lab` não foi criado. A tela de teste Python anterior ao QEMU é identificada como prévia sem envio. Os scripts usam a função de temperatura documentada em `temperature-source.json`.

A interface usa JSON sobre HTTP e polling de 1500 ms, conforme `interface/static/app.js:769`. Não usa WebSocket. `Sent` confirma transmissão; evento e contador são as evidências adicionais de processamento pela aplicação. Os critérios de latência, tempo de build e usabilidade do TCC continuam como metas de avaliação; esta coleta não os mede.

## Reprodução no portfólio

O site oferece sequências de evidências, um inspetor de bytes e uma exploração matemática da função de temperatura. Esses controles atuam localmente no navegador: não iniciam QEMU nem enviam comandos a um sistema de voo. As figuras conceituais são SVGs separados das capturas reais. Todas as imagens e explicações permanecem disponíveis sem JavaScript.

A instalação original foi preservada e os runtimes temporários foram encerrados após as capturas. Os arquivos do site não dependem da instalação em `/tmp`, de Docker ou do ZIP para o build. `locales.json` contém títulos e legendas nas quatro línguas; saídas e código capturados permanecem originais.
