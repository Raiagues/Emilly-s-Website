# Flight Studio — leitura do TCC fornecido

> Esta leitura se refere ao conteúdo do ZIP. Depois, a proprietária forneceu o repositório e a instalação local do Flight Studio, que foram executados. As evidências da implementação, as 12 capturas e os limites dos resultados estão em [runtime/README.md](runtime/README.md). A página combina as duas fontes: contexto e metas do TCC, comportamento observado da implementação.

Fonte: `TCC.zip`, enviado pela proprietária em novembro de 2026. Extração de leitura em `/tmp/emilly-tcc-source`, sem executar `build.sh` ou LaTeX com shell escape. O hash do ZIP e o do PDF estão em `source-data.json`. O nome **Flight Studio** foi relacionado ao trabalho pela própria usuária; o texto acadêmico usa o título “Plataforma interativa para reduzir a barreira de entrada no desenvolvimento de software de voo para satélites”.

## Estado documentado

O arquivo é o projeto de TCC/PFC da Engenharia Aeroespacial da UFSM, para 2026. Contém fundamentação, revisão de trabalhos relacionados, requisitos, arquitetura proposta, metodologia, plano de validação e cronograma. O README identifica os capítulos Desenvolvimento e Conclusão como placeholders; os dois `.tex` confirmam isso. Não há código do Flight Studio, telas de interface, medições, resultados com usuários ou comprovação de execução no alvo de baixo custo.

A página pode apresentar a proposta com bastante profundidade e diagramas didáticos. Atribuir “implementado”, “validado”, tempo medido, resultado de teste ou interface real ao Flight Studio exige outra evidência. Os valores **build < 90 s**, **latência P95 < 100 ms no desktop** e **SUS > 68** são **metas da validação planejada**, não resultados obtidos. A presença de um mês marcado no cronograma tampouco comprova conclusão.

A versão fornecida escolhe **cFS em Linux**, **backend Python**, **HTTP REST** para a interface web e **UDP** para comandos e telemetria. Prevê avaliação em **Raspberry Pi** e integração de sensores **COTS**, sem modelo de placa ou sensor específico. Não especifica React, Flask, FastAPI, WebSockets, portas UDP, Message IDs, valores de pacotes ou código de endpoints. STM32 não faz parte dos requisitos desta versão. RAG aparece na lista de siglas, sem arquitetura ou implementação correspondente no corpo do documento.

## O fio da explicação

1. **Problema humano:** antes da lógica de missão, o iniciante precisa montar ambiente, build, registro de aplicações, mensagens e interfaces. O trabalho propõe reduzir esse esforço mantendo o cFS real. Fontes: `introducao.tex:19–39`, `trabalhos_relacionados.tex:34–46`.
2. **Arquitetura:** navegador ↔ HTTP REST ↔ serviço Python ↔ UDP de comando/telemetria ↔ processo cFS/Linux. O backend reúne decode de telemetria, construção de comandos, análise de código e suporte assistido. Fontes: `metodologia.tex:15–48`.
3. **O que fica abaixo da interface:** aplicações de missão, cFE (ES/SB/EVS/TBL/TIME), OSAL, PSP, sistema operacional/hardware. OSAL e PSP são abstrações com responsabilidades distintas; não desenhar como uma fila obrigatória de toda mensagem. Fontes: `fundamentacao.tex:43–94`.
4. **A automação:** dados do usuário para aplicação integrada; inspeção das definições de código para gerar as interfaces; eventos para suporte à depuração. O plano mantém o sistema de construção nativo e as interfaces reais. Fontes: `metodologia.tex:36–44`.
5. **Missão como propósito:** objetivos → aplicações e comandos → telemetria que ajuda a observar o estado. Isso é a ligação didática proposta entre engenharia de sistemas e operação. Fonte: `metodologia.tex:38`.
6. **Como demonstrar que ajuda:** verificação de integração/fidelidade/performance e experimento educacional que compara tarefa equivalente no fluxo convencional e no fluxo assistido. Fontes: `metodologia.tex:50–112`.

## Diagramas e interações fundamentados

`source-data.json` contém os nós, responsabilidades, interfaces, métricas, referências por arquivo/linha e sete briefs de interação. As seguintes composições podem ser produzidas com SVG/HTML no estilo do CERN:

- Satélite esquemático com subsistemas selecionáveis: energia, atitude/órbita, térmico, comunicação e computador de bordo. O desenho representa funções recorrentes de satélites, não um hardware construído no TCC.
- Arquitetura de três componentes, com caminho do comando e da telemetria em sentidos opostos. Selecionar um bloco revela sua responsabilidade.
- Pilha do cFS que revela aplicações, serviços cFE, OSAL e PSP. Catálogo de CI_LAB, TO_LAB, SCH_LAB, HK, HS, SC, DS, FM e SAMPLE_APP.
- Percurso didático do pacote: interface → backend → CI_LAB → Software Bus → aplicação; retorno da telemetria por TO_LAB/backend/interface. É uma síntese da arquitetura descrita, **não uma captura de tráfego real**; não atribuir bytes/IDs inventados.
- Automação do ciclo de vida: entrada do usuário → modelo → arquivos/registro → build nativa → execução cFS. É a sequência conceitual, sem log fictício apresentado como real.
- Planejamento de missão ligando objetivo, aplicação, comando e telemetria. Um exemplo pode usar housekeeping ou armazenamento, claramente como exemplo didático.
- Painel da validação planejada, alternando critérios técnicos e educacionais. Mostrar **meta**, **como medir** e **evidência esperada**, sem indicadores de aprovação fictícios.

Uma interface de demonstração no portfólio deve ser identificada como **demonstração didática da arquitetura proposta**. Os textos podem ser assertivos sobre as escolhas descritas; a etiqueta de estágio evita confundir a demo do portfólio com uma instalação real do Flight Studio.

## Imagens originais selecionadas

O ZIP contém somente duas composições técnicas relevantes:

- `img/flight-studio/cfs-layered-architecture.png`: cópia exata de `figuras/cfs_layers_conv.png`, 1245 × 867, arquivo citado por `fundamentacao.tex:52`. Figura 1 no TCC, atribuída no documento a adaptação de McComas, Strege e Wilmot (2015). Preservar a atribuição.
- `img/flight-studio/platform-architecture-original.png`: Figura 2 da página física 28 (página impressa 27) de `main.pdf`, renderizada em 240 dpi e recortada para o diagrama original, 1510 × 260. O desenho corresponde a `metodologia.tex:22–32`; seu TikZ foi preservado em `platform-architecture-source.tex`.

`assets.json` contém dimensões, SHA-256 do arquivo usado, SHA-256 da origem e comando de transformação do PDF. As figuras foram inspecionadas visualmente. O recorte preserva integralmente os três componentes e as duas setas/interfaces.

Não foram usados `lombada.png` ou `pretextuais.png`, que pertencem ao modelo acadêmico, nem `estrutura_com.pdf`, que contém gráficos de turbulência sem relação com o Flight Studio. `cfs_layers.png` é outra versão da mesma figura cFS, evitando duplicação.

`technical-source.txt` preserva integralmente os capítulos técnicos, com títulos de arquivo. `references.bib` preserva a bibliografia fornecida. As fontes externas citadas pelo TCC não foram verificadas independentemente nesta leitura; o material preparado descreve o conteúdo do documento da autora, sem adicionar alegações externas.
