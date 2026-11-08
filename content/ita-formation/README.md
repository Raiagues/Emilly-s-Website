# ITA — Formação em voo de satélites

Integração do `Formation.dc.html` fornecido em `Project · Satellite formation flying-html.zip`. Preserva o cartão, as ilustrações vetoriais, os oito capítulos, as equações, a matriz interativa, os gráficos e a composição. A página substitui o conteúdo de `experience_2`, mantendo seu endereço e os seis registros de experiência. A navegação, o explorador de experiências e o rodapé são compartilhados com o portfólio. Não inclui o runtime React nem `support.js` do protótipo.

## Conteúdo e fontes

Conferido no [repositório flight-formation](https://github.com/Raiagues/flight-formation), commit `77cf1ce48f0568354641fbab2a332b58e5cc1d17`:

- `research/relatorio.pdf`: relatório de Emilly Raiane Rodrigues e Willer Gomes dos Santos, XXVIII ENCITA / ITA, 2023, PIBIC-CNPq.
- `original/NOVO/CODIGOS/LINEAR/main.m` e os arquivos `RESULTADOS_FINAIS.txt` das versões linear e `NAO_LINEAR/tests/CODIGO_PROFESSOR`: os números chamados de RMSE são estatísticas da **inovação** (`y − Hx̄`) e da **correção** (`x̂ − x̄`), a partir da amostra MATLAB 500. Não são os erros de medição e estimação em relação à trajetória real. A redução de 81,7% foi retirada do resumo do catálogo; as duas tabelas históricas permanecem com os nomes corretos e links para os registros.
- `research/REPRODUCTION.md` e `research/reproduction.json`: a execução não linear com atualizações alinhadas às medições registra RMSE medido `[14.0820406133, 13.9977429915, 13.6991391044]` m e estimado `[4.9605691360, 4.7765517003, 4.6374261982]` m, a partir da amostra 500. A terceira tabela arredonda esses valores a três casas. A reprodução exata dos valores do relatório não foi obtida; essa limitação aparece na página.
- O laboratório revisado do projeto está em https://raiagues.github.io/flight-formation/. Seus modelos, validação e resultados são separados da demonstração didática deste portfólio.

## Simulação e apresentação

`src/formation-model.mjs` adapta as equações do protótipo: Clohessy–Wiltshire com seis estados, dinâmica relativa não linear com dez estados, jacobiana analítica, propagação RK4, filtro com GPS a cada 5 s e controlador didático com saturação opcional. As medições são geradas por semente; não são uma reexecução do MATLAB nem uma cópia da série de dados arquivada. O laboratório calcula RMSE em relação à verdade simulada, agregando três eixos após 500 s — janela diferente da amostra 500 dos registros. A atualização de covariância usa a forma de Joseph e o cache mantém no máximo seis execuções.

O caso não linear original tem perigeu 97,814 km **abaixo** da superfície terrestre adotada (`a = 6.978.140 m`, `e = 0,1`, `R = 6.378.140 m`). É apresentado como cenário matemático; não se afirma viabilidade física. A separação visual é ampliada 15 vezes no modelo linear e três vezes no não linear somente na vista da Terra, com legenda explícita. A vista relativa preserva a escala do modelo.

O estudo de Sistemas de Controle II na UFSM, com Lucas Vizzotto Bellinaso, é distinguido da pesquisa no ITA, orientada por Willer Gomes dos Santos. O controle z usa o modelo do protótipo `A=[0,1;-4,0]`, `B=[0;0.25]`, `K=[446.8362,59.9766]`, `ki=1581.1388`; sua resposta de 2,5 s não é a dinâmica orbital. O diagrama apresenta a arquitetura proposta, não um acoplamento implementado entre as duas demonstrações.

`formation-worker.js` executa os cálculos fora da interface. Se o worker não puder iniciar, há cálculo local de reserva; respostas antigas são descartadas. `formation.js` controla a câmera, zoom, pinça, teclado, foco da matriz e renderização dos fragmentos. A animação respeita movimento reduzido, pode ser pausada e só roda com a figura visível e a aba ativa. A câmera mantém seu estado por modelo e referencial.

`strings.json` contém EN/PT/FR/ES, inclusive gráficos, descrições acessíveis e estados. Os templates e `default.json` geram uma página estática legível, com tabelas, gráficos e uma trajetória ilustrada também sem JavaScript. O build de publicação continua usando apenas Python e sua biblioteca padrão. Após alterar as fórmulas, atualize o estado inicial com `node scripts/build_formation_snapshot.mjs`.

O ZIP original fica em `local-reference/designs/`, ignorado pelo Git e excluído de `dist/`.

```text
SHA-256 ZIP   081f4cffbc0b3a8877abaa2dd15fa27d73a531952827d25e0ba852cdd6245e72
SHA-256 HTML  c9eee1c6ce2c1f9cbd9b879d9ac9e1b16370b8eae7dc5625523b2cbb6c0c78d8
```

Validação: `npm run build`, `npm run check`, `node --test tests/formation-model.test.mjs` e `BROWSER_EXECUTABLE=/usr/bin/google-chrome node --test tests/formation.test.mjs`. Os testes cobrem derivadas numéricas independentes, conservação de energia, 24 cenários do filtro, sementes, saturação, quatro idiomas, acessibilidade, telas de 320–1440 px, toque, teclado, pausa, ausência de scripts, falha do worker e navegação.
