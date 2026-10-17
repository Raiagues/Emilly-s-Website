# Validação — ilustrações, álbum e navegação, 17/10/2026

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
