# Validação do diário e da execução local

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
