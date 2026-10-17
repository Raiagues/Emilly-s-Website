# Validação local — identidade original restaurada, 17/10/2026

- `python3 scripts/build.py`: concluído; seis páginas principais, uma história do diário, 20 projetos e 6 experiências em quatro idiomas.
- `python3 scripts/check.py`: 135 HTMLs verificados; links, âncoras e imagens locais íntegros, idioma e título principal presentes, formulário com o e-mail confirmado, pacote de publicação sem ferramentas ou fontes editoriais.
- `node --check src/script.js`, `node --check src/projects.js` e `node --check src/journal.js`: sem erros de sintaxe.
- `git diff --check`: sem erros de whitespace.
- `npm test`, usando o Chromium disponível via `BROWSER_EXECUTABLE`: **14 testes aprovados**; a auditoria de acessibilidade foi repetida com sucesso após o ajuste de contraste na seção de imprensa.

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
14. Nenhuma violação automática WCAG A/AA nas quatro versões do diário.

Inspeção visual da página inicial em desktop e celular, das fotos, dos capítulos e dos trechos dos e-mails. Capturas: `preview-desktop.png`, `preview-mobile.png`, `preview-projects.png`, `preview-journal.png` e `preview-journal-mobile.png`. A verificação automática de acessibilidade não substitui avaliação manual por pessoas com deficiência.

O repositório já tem publicação via GitHub Actions. Nenhuma mensagem real foi enviada durante os testes; a ativação do FormSubmit e a confirmação de entrega dependem da proprietária. Os vídeos e relatórios mantêm os links fornecidos nos PDFs e no site original; permissões de acesso externas não foram alteradas.
