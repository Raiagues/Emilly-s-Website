# Validação local — South Summit, cronologia e conexões do diário, 17/10/2026

- `python3 scripts/build.py`: concluído; seis páginas principais, quatro histórias do diário, 20 projetos e 6 experiências em quatro idiomas.
- `python3 scripts/check.py`: 151 HTMLs verificados; links, âncoras e imagens locais íntegros, idioma e título principal presentes, formulário com o e-mail confirmado, pacote de publicação sem ferramentas ou fontes editoriais.
- `node --check src/script.js`, `node --check src/projects.js` e `node --check src/journal.js`: sem erros de sintaxe.
- `git diff --check`: sem erros de whitespace.
- `npm test`, usando o Chromium disponível via `BROWSER_EXECUTABLE`: **20 testes aprovados**, incluindo as vinte páginas de histórias e conexões nas verificações de acessibilidade.

Os testes cobrem:

1. Catálogo completo de 20 projetos, busca, categorias, reset e estado vazio.
2. Filtros preservados ao abrir um projeto, voltar, recarregar e mudar o idioma.
3. Idiomas preservando a página de detalhes; links para seções e compatibilidade com âncoras antigas.
4. Seis destinos de navegação visíveis nas quatro línguas, em 320, 390, 768, 1024 e 1440 px, sem overflow.
5. Validação do formulário e POST interceptado com os campos e destinatário corretos.
6. Copiar e-mail: sucesso e indisponibilidade da permissão.
7. Navegação, catálogo completo e contato disponíveis sem JavaScript.
8. Funcionamento sem armazenamento de sessão; consultas não são interpretadas como HTML.
9. Nenhuma violação detectada por axe nos critérios WCAG A/AA selecionados em 11 páginas representativas.
10. As 104 páginas de detalhes carregam sob o prefixo do repositório, com resultados, índice e ferramentas, sem overflow a 320 px.
11. História do CERN nas quatro línguas, com seis capítulos, 16 fotos e relatório PDF carregando corretamente.
12. Galeria com botões, setas do teclado, Escape, retorno do foco e verificação axe dentro do diálogo.
13. História, links de imagens e idiomas funcionando sem JavaScript.
14. Nenhuma violação automática WCAG A/AA nas vinte páginas de histórias e conexões (CERN, Estados Unidos, Visiona, South Summit e Pessoas e instituições, em quatro idiomas).
15. CSS antigo previamente guardado em cache não substitui o estilo restaurado; layout, fonte, fundo e órbitas corretos após navegar e recarregar.
16. História dos Estados Unidos acessível pelo diário e por Conquistas, nos quatro idiomas; sete capítulos, 15 fotos carregando, fontes, galeria e distinção de financiamento, sem overflow.
17. Visiona acessível pelo diário e pela página profissional, com retorno para a experiência no idioma atual, seis fotos, galeria, navegação por capítulos abaixo do menu fixo e layout sem overflow entre 320 e 1440 px.

18. Linha do tempo ordenada pelas datas reais das experiências, com entradas próprias para BSV e Brasil Project; acesso direto ao capítulo de Boston e retorno ao diário sem JavaScript. O teste usa a preferência de movimento reduzido para evitar a disputa entre a rolagem animada do fragmento e o auto-scroll do navegador de testes.
19. Pessoas e instituições nos quatro idiomas, com Visiona conectando duas histórias e Verônica/Fundação Estudar aparecendo apenas nos relatos em que são citadas; dez fotos do South Summit carregam e não há overflow entre 320 e 1440 px.
20. Três prints dos e-mails acessíveis como PNGs; os pixels dos endereços são opacos e já estão protegidos no próprio arquivo. Os dois trechos transcritos do CERN continuam disponíveis em controles expansíveis.

Conferência adicional dos PNGs por comparação de pixels com os originais: só a área da tarja foi alterada, o restante do texto foi preservado, não há metadados nos arquivos protegidos e as cópias de publicação são idênticas. Os originais ficaram fora do repositório.

Inspeção visual da página inicial em desktop e celular, das fotos, dos capítulos e dos trechos dos e-mails. Capturas: `preview-desktop.png`, `preview-mobile.png`, `preview-projects.png`, `preview-journal.png`, `preview-journal-mobile.png`, `preview-us-diary.png`, `preview-us-diary-mobile.png`, `preview-visiona-diary.png` e `preview-visiona-diary-mobile.png`. A cronologia e o South Summit foram conferidos em `preview-timeline.png`, `preview-south-summit.png` e `preview-south-summit-mobile.png`; os prints protegidos e a página de conexões também foram inspecionados em celular. A página inicial publicada foi inspecionada no navegador após a correção do cache; o CSS versionado carregou com fundo creme, fonte Georgia e hero em grid. A verificação automática de acessibilidade não substitui avaliação manual por pessoas com deficiência.

O repositório já tem publicação via GitHub Actions. Nenhuma mensagem real foi enviada durante os testes; a ativação do FormSubmit e a confirmação de entrega dependem da proprietária. Os vídeos e relatórios mantêm os links fornecidos nos PDFs e no site original; permissões de acesso externas não foram alteradas.
