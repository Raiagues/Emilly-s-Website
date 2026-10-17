# Validação local — página inicial e diário editorial, 17/10/2026

- `python3 scripts/build.py`: concluído; seis páginas principais, seis histórias do diário, 20 projetos e 6 experiências em quatro idiomas.
- `python3 scripts/check.py`: 159 HTMLs verificados; links, âncoras e imagens locais íntegros, idioma e título principal presentes, formulário com o e-mail confirmado, pacote de publicação sem ferramentas ou fontes editoriais.
- `node --check src/script.js`, `node --check src/projects.js` e `node --check src/journal.js`: sem erros de sintaxe.
- `git diff --check`: sem erros de whitespace.
- `npm test`, usando o Chromium disponível via `BROWSER_EXECUTABLE`: **23 testes aprovados**, incluindo as 28 páginas de histórias e conexões nas verificações de acessibilidade.

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
14. Nenhuma violação automática WCAG A/AA nas 28 páginas de histórias e conexões (CERN, Estados Unidos, Visiona, South Summit, China, prêmio Na Prática e Pessoas e instituições, em quatro idiomas).
15. CSS antigo previamente guardado em cache não substitui o estilo restaurado; layout, fonte, fundo e órbitas corretos após navegar e recarregar.
16. História dos Estados Unidos acessível pelo diário e por Conquistas, nos quatro idiomas; sete capítulos, 15 fotos carregando, fontes, galeria e distinção de financiamento, sem overflow.
17. Visiona acessível pelo diário e pela página profissional, com retorno para a experiência no idioma atual, nove fotos, galeria, navegação por capítulos abaixo do menu fixo e layout sem overflow entre 320 e 1440 px.

18. Linha do tempo ordenada pelas datas reais das experiências, com entradas próprias para BSV e Brasil Project; acesso direto ao capítulo de Boston e retorno ao diário sem JavaScript. O teste usa a preferência de movimento reduzido para evitar a disputa entre a rolagem animada do fragmento e o auto-scroll do navegador de testes.
19. Pessoas e instituições nos quatro idiomas, com Visiona conectando duas histórias e Verônica/Fundação Estudar aparecendo apenas nos relatos em que são citadas; dez fotos do South Summit carregam e não há overflow entre 320 e 1440 px.
20. Três prints dos e-mails acessíveis como PNGs; os pixels dos endereços são opacos e já estão protegidos no próprio arquivo. Os dois trechos transcritos do CERN continuam disponíveis em controles expansíveis.

21. China acessível pela conquista do prêmio, com acesso direto à história da candidatura, oito capítulos e 26 fotos carregando nos quatro idiomas; galeria, índice de pessoas/instituições, títulos abaixo do menu fixo e layout de 320 a 1440 px. Cronologia com a imersão de 25–31/01/2026 e a cerimônia de 03/11/2025, totalizando sete acontecimentos.

22. Relato do prêmio nos quatro idiomas, com seis capítulos e 14 fotos; ambos os links (prêmio e China) permanecem na mesma conquista. Links entre prêmio, China e Estados Unidos funcionam nos dois sentidos; capítulos ficam abaixo do menu fixo e a página não transborda entre 320 e 1440 px.

Conferência adicional dos PNGs por comparação de pixels com os originais: só a área da tarja foi alterada, o restante do texto foi preservado, não há metadados nos arquivos protegidos e as cópias de publicação são idênticas. Os originais ficaram fora do repositório.

Inspeção visual da página inicial em desktop e celular, das fotos, dos capítulos e dos trechos dos e-mails. Capturas: `preview-desktop.png`, `preview-mobile.png`, `preview-projects.png`, `preview-journal.png`, `preview-journal-mobile.png`, `preview-us-diary.png`, `preview-us-diary-mobile.png`, `preview-visiona-diary.png` e `preview-visiona-diary-mobile.png`. A cronologia e o South Summit foram conferidos em `preview-timeline.png`, `preview-south-summit.png` e `preview-south-summit-mobile.png`; os prints protegidos e a página de conexões também foram inspecionados em celular. A página inicial publicada foi inspecionada no navegador após a correção do cache; o CSS versionado carregou com fundo creme, fonte Georgia e hero em grid. A história da China foi conferida visualmente em `preview-china-diary.png` e `preview-china-diary-mobile.png`, e a linha do tempo atualizada em `preview-timeline.png`. O relato do prêmio e a linha do tempo foram inspecionados em `preview-award-diary.png`, `preview-award-diary-mobile.png` e na nova `preview-timeline.png`. A verificação automática de acessibilidade não substitui avaliação manual por pessoas com deficiência.

O repositório já tem publicação via GitHub Actions. Nenhuma mensagem real foi enviada durante os testes; a ativação do FormSubmit e a confirmação de entrega dependem da proprietária. Os vídeos e relatórios mantêm os links fornecidos nos PDFs e no site original; permissões de acesso externas não foram alteradas.

23. Página inicial nas quatro línguas: CTA leva ao projeto atual, destaque abre os detalhes corretos, ilustrações de projetos/experiências carregam, formação está presente e o formulário envia os dados ao destino correto com a requisição interceptada. Sem overflow a 320, 390, 768 e 1440 px.

Nesta revisão, foram novamente inspecionados no navegador: retrato e órbitas, faixa de instituições, destaque da plataforma, cartões SVG, história pessoal e formação, índice do diário, formulário completo, abertura dos artigos, capítulos com foto ao lado e o álbum com as três novas fotos da Visiona. As capturas de início, projetos, CERN e Visiona acima foram atualizadas para o novo desenho. As reflexões foram revistas em EN/PT/FR/ES; os capítulos e a conclusão originais da Visiona foram preservados. Duas falhas de contraste encontradas durante o desenvolvimento foram corrigidas antes da execução final da suíte.

A lista do diário carrega apenas uma foto de capa por história, sob demanda; os mosaicos completos ficam nas páginas dos relatos. Após esse ajuste de carregamento, build e verificação estática passaram novamente, assim como os dois testes direcionados à página inicial e à navegação do diário.
