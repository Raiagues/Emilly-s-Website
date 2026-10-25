# Wing box analysis

Integração do arquivo `Wingbox.dc.html`, fornecido em `Project · Wing box analysis-html.zip`. O cartão inicial, os seis capítulos, as figuras, as cores e as proporções seguem esse design. A navegação, o rodapé e o explorador de projetos são os componentes compartilhados do portfólio. Os controles funcionam com JavaScript nativo, sem o runtime React do protótipo.

- `page.html.tmpl` e os cinco fragmentos contêm o layout. `scripts/wingbox_redesign.py` gera os estados estáticos e os links reais nos quatro idiomas.
- `strings.json` contém os textos em EN/PT/FR/ES, inclusive rótulos de gráficos, teclado, estados e alternativas acessíveis.
- `values.json` preserva os resultados e as coordenadas SVG calculados pelo código fornecido: cinco condições de voo, quinze combinações de condição/modo, seis casos de torção e três configurações para cada componente de flambagem. As grandezas são as do projeto original, não as do laboratório revisado.
- `src/wingbox.js` adapta o renderizador Canvas original. As geometrias e deformações são esquemáticas: o contorno simplificado do protótipo não é uma reconstrução exata do NACA 63A415. Arraste, pinça, zoom, vistas predefinidas e teclado mantêm câmeras independentes para cada figura. O modelo não roda continuamente em segundo plano.
- O movimento do fluxo pode ser pausado; respeita movimento reduzido e fica parado sem JavaScript. A tabela das cinco condições, os valores iniciais e o CAD permanecem legíveis sem scripts.
- `img/wing-box/wing-cad.jpg` é a imagem original, copiada sem edição.

O [repositório do projeto](https://github.com/Raiagues/areonautical_structure) e seu [laboratório interativo](https://raiagues.github.io/areonautical_structure/) estão ligados no cabeçalho da página. O README do repositório foi conferido no commit `d9eeb68770e71bb2e05efe8756e1047de932d0e0`; ele documenta a separação entre `originals/`, `legacy/` e o solver revisado em `web/`. O portfólio apresenta os resultados históricos fornecidos e não os mistura com os resultados corrigidos do laboratório.

O ZIP original fica em `local-reference/designs/`, ignorado pelo Git e excluído de `dist/`. Não se publicam os arquivos `support.js`, `vendor/` nem o protótipo bruto.

SHA-256 de origem:

```text
ZIP         23db28d637f98e7058f47d4775d933ae1f69d87e01a3d75cd4865c7fac0cb9db
HTML        083c66ee650bdc399aa700139577f08a5f000b5f5aef8cf5d0303ffc2b7df81c
wing-cad    85ec114c712ae6ff9ce18cd55c68d0485c683886b68d1cfb3384024856c196a9
```

Validação: `npm run build`, `npm run check` e `BROWSER_EXECUTABLE=/usr/bin/google-chrome node --test tests/wingbox.test.mjs`. A suíte exercita as combinações, valores dos relatórios, teclado, toque, animação, navegação, filtros, acessibilidade e larguras de 320 a 1440 px.
