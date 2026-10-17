# Validação local — 17/10/2026

- `python3 scripts/build.py`: concluído; 20 projetos e 6 experiências em quatro idiomas.
- `python3 scripts/check.py`: 111 HTMLs verificados; links, âncoras e imagens locais íntegros, idioma e título principal presentes, formulário apontando para o e-mail confirmado, pacote de publicação sem ferramentas ou fontes editoriais.
- `node --check src/script.js` e `node --check src/projects.js`: sem erros de sintaxe.
- `git diff --check`: sem erros de whitespace.
- `npm test` com `BROWSER_EXECUTABLE` apontando para o Chromium disponível no ambiente: **8 testes passaram, 0 falharam**.

Os oito testes cobrem:

1. Busca, categorias, reset, estado vazio, expandir e recolher projetos.
2. Troca de idioma preservando a página do projeto e a seção da página inicial.
3. Quatro idiomas nas larguras 320, 390, 768, 1024 e 1440 px; menu, Escape e redimensionamento.
4. Validação do formulário e POST interceptado com os campos e destinatário corretos.
5. Copiar e-mail: sucesso e indisponibilidade da permissão.
6. Navegação e conteúdo acessíveis sem JavaScript.
7. Nenhuma violação detectada por axe nos critérios WCAG A/AA selecionados, nas quatro páginas iniciais e duas páginas de detalhes representativas.
8. As 104 páginas de detalhes carregam sob o prefixo de um repositório, sem erros JavaScript, ilustrações principais ausentes ou overflow a 320 px.

Também houve inspeção visual da página inicial em desktop e celular e de uma página interna em francês. Prévia desktop em `preview-desktop.png`; celular em `preview-mobile.png`.

Não foi executado push ou deploy remoto. Nenhuma mensagem real foi enviada durante os testes; a ativação do FormSubmit e a confirmação de entrega dependem da proprietária. Os links de vídeos e relatórios são os fornecidos nos PDFs e no site original; permissões de acesso externas não foram alteradas nem verificadas por autenticação.
