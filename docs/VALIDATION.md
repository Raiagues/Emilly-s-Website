# Validação do diário e da execução local

## Flight Studio: infraestrutura e percurso dos dados — 7 de novembro de 2026

- Página refeita nos quatro idiomas em cinco capítulos: sinal sintético, placa QEMU, partições e aplicações, drivers e locais de edição. Diagramas vetoriais substituem a galeria de telas e o inspetor de pacotes.
- A senoide permite ajustar temperatura inicial, amplitude, período e instante. Uma amostra com seu valor percorre Python → QMP → TMP105 → Linux → bibliotecas → aplicação → Software Bus/TO_LAB → Flight Studio. Há pausa, avanço por conexão, seleção direta e suporte a movimento reduzido.
- Placa configurável com periféricos e endereço I²C, argumentos QEMU atualizados e interrupção do percurso quando o TMP105 está desconectado. O desenho do SD explica bootfs, rootfs, `/cf` e carregamento das aplicações; o caminho do código C até a instalação por SSH é explícito.
- A pesquisa confirmou a topologia, os arquivos de boot, a DTB, as partições da imagem QCOW2 e o comportamento dos drivers no repositório fornecido. O percurso é identificado como modelo didático calculado; a captura anterior comprova a injeção QMP, sem comprovar leitura e telemetria de uma app de sensor.
- **13 testes aprovados**: dez testes de navegador/dados das páginas de engenharia e três do modelo matemático. Incluem movimento visível da amostra e pausa, valores, configuração da placa, partições, drivers, teclado, leitura sem JavaScript, hashes das 44 capturas preservadas e regressão das seis atividades do kernel. Auditoria axe WCAG A/AA aprovada nas duas páginas nos quatro idiomas, com estados alternativos no celular.
- Layouts conferidos em 320, 390, 768 e 1440 px. Diagramas, estados selecionados e textos revisados visualmente em desktop e celular. As figuras grandes têm rolagem interna em telas estreitas; a página não apresenta overflow horizontal.
- **Três regressões direcionadas aprovadas**: carregamento dos 112 estudos de caso, 76 redirecionamentos antigos e destaques NASA cFS/kernel/CubeSat/RISC-V nos quatro idiomas. Build e verificador estático aprovados: **255 HTMLs válidos**. A página do kernel mantém o conteúdo anterior.

Prévias: [abertura](preview-flight-studio-infrastructure.png), [percurso da temperatura](preview-flight-studio-flow.png), [placa](preview-flight-studio-board.png), [partições](preview-flight-studio-storage.png) e [fluxo no celular](preview-flight-studio-flow-mobile.png).

## Versão anterior: Flight Studio e kernel interativos — novembro de 2026

- Páginas NASA cFS e kernel refeitas a partir da composição visual do CERN: papel creme, títulos com serifa, diagramas vetoriais, capítulos e painéis técnicos. Textos e legendas em EN/PT/FR/ES.
- Flight Studio: 12 capturas reais da aplicação, duas figuras originais do TCC, arquitetura selecionável, camadas cFS, reprodução do percurso NOOP, inspetor dos bytes CMD/HK antes e depois, geração de aplicações e curva interativa da função de temperatura. cFS nativo e ARM64/QEMU chegaram a OPERATIONAL; evento e contador 0→1 confirmam o NOOP nativo. QMP confirmou a injeção de sensores; o percurso de leitura I²C até telemetria é explicitamente separado do que foi observado.
- Kernel: seis atividades compiladas/executadas no QEMU CEP e kernel completo, com 32 capturas reais. Código e saída lado a lado, reprodução controlada, tabela de processos capturada, mapa MMIO/ELF, cálculo de endereços de pixels, bitmaps da fonte, interrupções e pilhas. Código e framebuffer não foram simulados para os prints; os desenhos didáticos são identificados separadamente.
- **Nove testes novos aprovados**, com hashes de todos os 44 screenshots, leitura das imagens, títulos/legendas, teclado, pausa/avanço/zoom, pacotes reais, valores calculados, estados dos processos e leitura sem JavaScript. Auditoria axe WCAG A/AA aprovada nas duas páginas nos quatro idiomas e em estados alternativos no celular. Layouts conferidos em 320, 390, 768 e 1440 px, incluindo todas as abas de capturas e atividades.
- **Sete regressões direcionadas aprovadas**, incluindo todos os 112 estudos de caso, 76 redirecionamentos antigos, destaques, busca/filtros/idiomas, as três páginas dos relatórios e seus diagramas. Na primeira rodada foram detectados um cartão francês largo e um teste que ainda buscava a tecnologia STM32 removida do Flight Studio; ambos foram corrigidos e os testes afetados passaram na reexecução. Não foi necessária uma nova execução integral de todas as suítes independentes.
- Build e verificador estático: **255 HTMLs válidos**; links, fragmentos, imagens e limites do pacote conferidos. `git diff --check` sem erros. O ZIP do TCC foi removido depois da integração, mantendo as fontes usadas, figuras e metadados. A geração não depende dos ZIPs, QEMU ou da instalação local do Flight Studio.
- Instalações originais preservadas. Os runtimes de captura foram encerrados. Resultado preparado localmente, sem publicação no GitHub Pages.

Prévias: [Flight Studio](preview-flight-studio.png), [sensores](preview-flight-studio-sensors.png), [kernel](preview-kernel-os.png), [código e execução](preview-kernel-execution.png), [memória no celular](preview-kernel-memory-mobile.png).

## Revisão visual dos relatórios — 07/11/2026

- As três páginas agora têm capa com desenho/foto original, contexto sobre a importância do projeto, contribuições, capítulos com figuras junto das explicações e resultados. Foram selecionadas 30 imagens: 14 de RISC-V, 9 do carrinho e 7 de injeção de falhas. Os hashes confirmam que as imagens mantêm os arquivos de origem.
- RISC-V inclui arquitetura CPU/cache/memória, seis formatos de instrução selecionáveis, fluxo de testes, formas de onda, extensão de sinal, investigação do alinhamento e correção do offset. Os resultados manuais também aparecem em barras, mantendo as contagens completas em tabela acessível.
- O carrinho apresenta PWM e geometria das rodas, quatro etapas da câmera e tratamento das curvas. A injeção apresenta o circuito, comparação com/sem falha e espaço bit × ciclo. Figuras abrem no visualizador com navegação por teclado e retorno de foco; sem JavaScript, todas permanecem disponíveis.
- Sete testes de navegador direcionados passaram: imagens e hashes, EN/PT/FR/ES em 320/390/768/1440 px, axe nas três páginas PT, seleção por clique/teclado, visualizador, redirecionamentos, destaques, filtros/idiomas e carregamento das 112 páginas canônicas de projetos e experiências. Nenhum erro de JavaScript ou overflow foi observado nesses testes.
- `python3 scripts/build.py` e `python3 scripts/check.py`: 255 HTMLs válidos, incluindo redirecionamentos. Prévia local em `http://127.0.0.1:8000/pt/`; esta revisão não publicou no GitHub Pages.

## URLs, imagens e relatórios dos projetos — 07/11/2026

- Nomes descritivos para os 18 projetos numerados e para NASA cFS. Os 76 endereços antigos nos quatro idiomas redirecionam para as páginas canônicas; teste de navegador confirma preservação de parâmetros e fragmentos. Fallback sem JavaScript também verificado.
- NASA cFS, kernel, CubeSat e RISC-V são os quatro destaques na home e os primeiros itens do catálogo. Busca, filtros, idioma e retorno aos resultados continuam funcionando.
- RISC-V, carrinho autônomo e injeção de falhas receberam conteúdo em EN/PT/FR/ES e oito figuras originais. Arquivos, hashes e limites dos resultados estão em `content/project-reports/`. Sete PNGs existentes foram renomeados; nomes publicados usam minúsculas e hífens.
- Revisão visual em desktop e celular; páginas dos relatórios verificadas em 320, 390, 768 e 1440 px, com figuras carregadas, links para o tamanho original e navegação sem JavaScript. Auditoria axe WCAG A/AA aprovada nas três páginas em português; os demais testes de acessibilidade existentes também passaram.
- Regressão executada com Chrome local: `BROWSER_EXECUTABLE=/usr/bin/google-chrome node --test --test-concurrency=1 tests/*.test.mjs`. A execução completa aprovou 71 de 72 testes e identificou uma comparação incorreta de coordenadas SVG no teste orbital já existente. Corrigido o teste para considerar a escala automática; a reexecução do teste afetado passou. A invariância dos dados físicos entre ruídos e níveis de confiança foi adicionada aos testes do modelo, que também passaram. Nenhuma falha ficou pendente.
- Os três ZIPs da raiz foram apagados após a validação. Uma nova execução de `python3 scripts/build.py` e `python3 scripts/check.py`, sem os ZIPs, passou com **255 HTMLs**, incluindo redirecionamentos. `git diff --check` sem erros.
- Alterações preparadas localmente; esta revisão não realizou publicação no GitHub Pages.

## Wing box analysis — 25/10/2026

- Projeto integrado a partir do ZIP fornecido, mantendo o cartão, os seis capítulos, o CAD, os gráficos e a composição visual. EN/PT/FR/ES, categoria Estruturas, cabeçalho persistente, filtro preservado no retorno e links reais para repositório, laboratório e projetos vizinhos.
- Duas vistas 3D com rotação, zoom, pinça e teclado; cinco condições de voo sincronizadas com quinze comparações de cargas; seis geometrias de torção; nove configurações de flambagem. Valores e vetores originais documentados em `content/wing-box/README.md`.
- Revisão visual em desktop e celular. Sem sobreposição dos controles ou rolagem horizontal entre 320 e 1440 px. Verificação automatizada WCAG A/AA nos quatro idiomas, inclusive estados de falha de flambagem; movimento reduzido e pausa do fluxo; resultados acessíveis sem JavaScript.
- `npm run build` e `npm run check`: 179 páginas válidas, com 22 projetos, seis experiências e nove histórias nos quatro idiomas. `BROWSER_EXECUTABLE=/usr/bin/google-chrome npm test`: **59 testes aprovados**, sem falhas, incluindo os sete novos testes da asa. `git diff --check` sem erros.
- ZIP arquivado em `local-reference/designs/`, fora do Git e da publicação. Fotos pessoais não selecionadas preservadas, sem incluí-las na alteração.

## Publicação e revisão editorial — 25/10/2026

Os nove relatos, suas chamadas e legendas foram revisados em EN, PT, FR e ES. A redação prioriza contribuições, conquistas e dificuldades concretas dos processos, em primeira pessoa e sem dramatização. Foram retirados detalhes íntimos, comparações de remuneração e circunstâncias privadas de terceiros. A biografia da home e de Sobre mim segue o mesmo tom.

As datas, fontes, resultados técnicos, projetos e fotos selecionadas foram preservados. A seleção do CERN mantém a distinção entre os resultados do estudo e a implementação futura em FPGA. A participação sem conclusão na Lyfe Academy continua explícita. O financiamento do Brazil at Silicon Valley permanece separado da participação autofinanciada no Brasil Project.

O GitHub Pages foi reativado com publicação por Actions no endereço existente. O pacote continua restrito a `dist/`, sem protótipos, rascunhos ou fotos não selecionadas. As instruções do diário foram atualizadas para orientar futuras edições com esse critério editorial.

Validação desta revisão: 167 HTMLs aprovados pelo verificador estático e 35 testes de navegador aprovados. A suíte cobre quatro idiomas, navegação, proporções e carregamento das fotos, teclado, acessibilidade automatizada, funcionamento sem JavaScript e formulários com envio interceptado. Os títulos revisados também foram inspecionados visualmente no celular e no desktop.

## Redesign dos modelos fornecidos — 18/10/2026

A revisão atual substitui os layouts históricos descritos abaixo. Home, catálogo, projetos, experiências e histórias usam os modelos do ZIP. O [relatório do redesign](HOME_REDESIGN.md) registra as mudanças, a mídia fornecida, os campos omitidos, as prévias e a validação de conteúdo, navegação e acessibilidade.

## Revisão de 18/10/2026

- `./setup` executado com Python 3.12.3. O build gerou 26 estudos de caso, nove histórias e seis páginas principais em quatro idiomas. O verificador aprovou 167 HTMLs, os links e os limites do pacote publicado.
- `./setup --with-tests` instalou as dependências do lockfile. Nesta máquina, os testes usaram o Google Chrome existente por meio de `BROWSER_EXECUTABLE`. Os caminhos de download de Python e Chromium estão disponíveis no setup, mas não foram necessários nesta execução.
- Suíte completa com **31 testes aprovados**, incluindo acessibilidade Axe das 36 páginas de histórias, navegação sem JavaScript, traduções, cronologia, fotos, visualizador com teclado e foco, formulários interceptados e regressões do portfólio.
- **Três testes de integração dos comandos aprovados**. Cobrem execução a partir de outra pasta e caminhos com espaços, preparação, início e parada repetidos, porta inválida, porta ocupada, estado antigo, proteção de outro servidor e acesso apenas aos arquivos publicados.
- `bash -n setup start stop scripts/runtime.sh` e `git diff --check` aprovados.
- BRAFITEC em oito capítulos, com 24 imagens selecionadas do álbum fornecido. São 23 fotos no visualizador e uma foto adicional usada na capa. A história aparece na página inicial, na cronologia, na lateral das outras histórias e na conquista CAPES–BRAFITEC.
- Os nove relatos foram revisados nos quatro idiomas. O teste editorial verifica traduções completas e a ausência de dois pontos, travessões e ponto e vírgula nos textos e legendas. URLs e transcrições literais de documentos preservam seus caracteres.
- As fotos usam as proporções originais. A capa se adapta à orientação da foto principal, as galerias agrupam proporções compatíveis e passam a uma coluna no celular. O espaço da imagem é reservado antes do carregamento.
- Após separar as duas fotos do álbum para preservar a imagem principal e a legenda, passaram novamente os três testes direcionados de layout responsivo, acessibilidade das páginas principais e álbum nos quatro idiomas.

Inspeção visual em 1440, 390 e 320 px, com as imagens carregadas. Prévias da [abertura](preview-brafitec-desktop.png), do [celular](preview-brafitec-mobile.png), das [fotos nos capítulos](preview-brafitec-photos.png) e do [álbum](preview-brafitec-album.png).

### Ajuste de largura e fotos dos capítulos

- Diário ampliado no desktop, com lateral próxima à borda e introdução, capítulos e conclusão alinhados à esquerda. As galerias aproveitam a largura disponível e os parágrafos mantêm uma largura de leitura limitada.
- Fotografias dos capítulos com moldura de papel, legenda dentro da moldura, inclinações variadas e movimento suave no hover e no foco. As imagens preservam suas proporções e a preferência por movimento reduzido continua respeitada.
- Estados Unidos, CERN, BRAFITEC e China conferidos em 320, 390, 768, 1100, 1280, 1440, 1880 e 2560 px, sem rolagem horizontal. Alinhamento dos textos, movimento das fotos, abertura do visualizador e retorno de foco também verificados.
- Seis testes direcionados aprovados, incluindo fotografias, teclado, acessibilidade das 36 páginas de histórias, cronologia, Estados Unidos e BRAFITEC. Build, verificador dos 167 HTMLs e `git diff --check` aprovados.

Prévias da [leitura em tela larga](preview-journal-wide-desktop.png), das [fotos com molduras inclinadas](preview-journal-album-photos.png) e da [leitura no celular](preview-journal-wide-mobile.png).

### Revisão para uma leitura mais compacta

Esta revisão substitui a largura ampliada descrita acima, seguindo o retorno sobre o tamanho excessivo das fotos.

- Página limitada a 1160 px, corpo de leitura a 880 px e parágrafos a 680 px. Galerias e fotos laterais têm limites próprios de tamanho, preservando as proporções originais e as molduras inclinadas.
- Controle nativo para recolher e reabrir toda a navegação. Os grupos de capítulos e outras histórias também podem ser recolhidos individualmente. Outras histórias começam fechadas em todas as telas.
- Rolagem interna com fundo transparente e cor discreta. O controle para recolher o menu permanece fora da área rolável.
- Sete testes direcionados aprovados, incluindo recolhimento com Enter e Espaço, navegação sem JavaScript, proporções e limites das fotos, visualizador, CNES, BRAFITEC, traduções e acessibilidade das 36 páginas de histórias.
- Cinco histórias verificadas entre 320 e 2560 px, sem rolagem horizontal. Build e verificação estática dos 167 HTMLs aprovados.

Prévias do [capítulo compacto](preview-journal-compact-desktop.png), da [galeria reduzida](preview-journal-compact-gallery.png), do [menu recolhido](preview-journal-compact-collapsed.png) e do [celular](preview-journal-compact-mobile.png).

### Retorno ao visual anterior

A tentativa de identidade com títulos de pôster foi retirada a pedido da proprietária. O site voltou às cores suaves, à tipografia com serifa e à composição anterior do retrato. O diário compacto, as fotos menores e inclinadas e os controles para recolher o menu foram mantidos.

As alterações foram preparadas e verificadas localmente. Nenhum deploy nem envio de formulário real foi realizado. As verificações automáticas de acessibilidade cobrem os critérios selecionados, sem substituir uma avaliação manual completa.

## Histórico de 17/10/2026

- Build: 20 projetos, 6 experiências e 7 histórias, além das seis páginas principais, em EN/PT/FR/ES.
- `python3 scripts/check.py`: 159 HTMLs; links, fragmentos, IDs únicos, imagens, idiomas e pacote de publicação válidos. As quatro páginas `journal/connections.html` foram removidas, inclusive do sitemap.
- `node --check src/script.js` e `git diff --check`: sem erros.
- Suíte completa: **26 testes aprovados** com Chromium e Playwright.
- Após corrigir a ordem de foto/texto no celular: **6 testes direcionados aprovados**, incluindo a nova verificação das 14 fotos de capa e da ordem de leitura dos sete relatos, nas quatro línguas.

## Cobertura

- Todos os 20 projetos e as 6 experiências têm SVG original e um único link por cartão. Não há botão separado “Ver projeto”. Os detalhes mantêm os links para vídeos, relatórios e recursos.
- Animação de componentes dos SVGs por hover/foco, sem alterar o alvo clicável. Movimento real do satélite verificado; a preferência de movimento reduzido desativa as animações.
- Sidebar nas 104 páginas de detalhes, com ilustração, tecnologias, índice e retorno ao catálogo. Testes verificam permanência na tela em desktop, seção ativa e títulos abaixo do cabeçalho no celular.
- Catálogo, filtros, pesquisa, reset, retorno aos resultados e troca de idioma preservam a navegação. As seis páginas principais cabem de 320 a 1440 px.
- Diário em formato de álbum, com duas fotos por entrada, legendas e introdução do relato. A cronologia continua ordenada e funciona em um controle expansível nativo, também sem JavaScript.
- Nenhum link ou índice público de pessoas/instituições. Links diretos entre histórias continuam funcionando; os identificadores editoriais ficam fora de `dist`.
- Galerias de todas as histórias, relatório do CERN, imagens dos e-mails com tarjas incorporadas, navegação por capítulos, teclado, Escape e retorno de foco.
- Formulário testado com POST interceptado: nenhum e-mail real enviado. A ativação do FormSubmit e a confirmação de entrega continuam dependendo da proprietária.
- Axe: nenhuma violação nos critérios WCAG A/AA selecionados em 11 páginas representativas e nas 28 páginas de histórias. A verificação automática não substitui avaliação manual por pessoas com deficiência.

## Inspeção visual

Conferidos no navegador: catálogo de projetos, experiências, destaque da plataforma, sidebar, álbum em desktop e celular e abertura da Visiona. Fotos aguardadas até o carregamento completo. Capturas desta revisão em `/tmp/album-final-desktop.png`, `/tmp/album-final-mobile.png`, `/tmp/story-final-mobile.png`, `/tmp/new-projects.png`, `/tmp/new-experience.png` e `/tmp/new-sidebar.png` (não publicadas).

Os textos, os capítulos e as fotografias dos relatos foram preservados. A introdução de cada história agora também aparece na página do álbum. As instruções de edição em `content/journal/README.md` refletem esse comportamento.

## História do CNES — 17/10/2026

- Oitava história, em EN/PT/FR/ES, com sete capítulos e 26 fotos. Período fevereiro–agosto de 2025 conferido nos currículos; nome AEROSAT e vínculo com Nanolab Academy conferidos na página oficial do CNES, citada no capítulo.
- As condições de nacionalidade aparecem como relato das respostas recebidas pela autora, sem apresentar uma regra geral de contratação. A oferta do CERN de 2025 é distinguida do openlab de 2026; nenhum lançamento do AEROSAT é afirmado como realizado.
- Nova entrada cronológica em fevereiro de 2025, entre a candidatura de 2022 à Fundação e a aprovação de agosto de 2025. O álbum tem oito entradas e 16 fotos de capa.
- Links entre página técnica do CNES e relato; continuação para a Visiona com retorno; ligação com o CERN de 2026. Nenhuma página de pessoas/instituições foi recriada.
- Build e verificação estática: 163 HTMLs aprovados.
- Seis testes direcionados aprovados: acessibilidade das 32 páginas de histórias, Visiona, cronologia sem JavaScript, álbum/contato em quatro idiomas, Fundação/Lyfe e o novo percurso do CNES.
- Novo teste cobre 26 fotos carregadas em cada idioma, galeria, capítulos abaixo do menu, retorno entre histórias, datas, fonte oficial e layout entre 320 e 1440 px.
- Inspeção visual: abertura, capítulo AEROSAT, fotos e versão móvel. Capturas em `/tmp/cnes-story-desktop.png`, `/tmp/cnes-aerosat.png` e `/tmp/cnes-story-mobile.png`.

## Navegação e identidade discreta — 17/10/2026

- Cabeçalho e rodapé com identidade “portfolio”, navegação com ícones e redes sociais com nomes acessíveis. Removidas as setas decorativas de links e os círculos sobre as ilustrações; o cartão completo continua clicável.
- Inicial com o projeto atual, mais seis projetos visíveis e um controle nativo para os outros 13. Todos os 20 são acessíveis sem JavaScript.
- Álbum e linha do tempo em ordem decrescente. Lateral dos oito relatos com capítulos e índice cronológico com fotos; em telas pequenas, outras histórias ficam num controle expansível.
- Removidos os cartões repetidos, a seção final de sugestões e as assinaturas. Conclusões mantidas como texto normal. Títulos de capítulos não usam os nomes da mentora; os nomes permanecem nos parágrafos.
- Suíte completa: **29 testes aprovados**, incluindo navegação sem JavaScript, fotos, teclado, movimento reduzido, versões EN/PT/FR/ES e verificações Axe. Build e verificador: 163 HTMLs.
- Após aumentar a legibilidade do índice lateral: quatro testes direcionados aprovados (layouts, acessibilidade dos relatos, expansão dos projetos e cronologia).
- Inspeção visual em 1440 e 390 px: cabeçalho, projetos, relato da Fundação, lateral e rodapé. Capturas locais `/tmp/nav-home-desktop.png`, `/tmp/nav-home-mobile.png`, `/tmp/nav-diary-desktop.png`, `/tmp/nav-footer-desktop.png` e `/tmp/nav-diary-mobile.png` (não publicadas).
