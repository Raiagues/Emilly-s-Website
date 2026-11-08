# Relatórios dos projetos

Conteúdo e figuras fornecidos pela proprietária em 07/11/2026. Os textos publicados ficam em `content/project_reports.py` e os resumos em `content/data.py`, nos quatro idiomas. O HTML é gerado por `scripts/build.py` e `scripts/inner_redesign.py`.

## CVA6 / RISC-V de 128 bits

Arquivo original: `Rapport_Projet_SEOC.zip`.
SHA-256: `c6cd3746cc5cba8a0655848a31f4257672200def239893dacb3d48b6c8b6565b`.

Relatório **Validation et Évaluation d’un Processeur CVA6 128 bits**, Projet SEOC Systèmes Embarqués, Grenoble INP – Phelma. Autoras: Rokhaya Yvette Fall e Emilly Raiane Rodrigues.

- `chapters/organisation.tex`, “Répartition entre les membres”: Emilly executou simulações, investigou erros de memória e desenvolveu automação; Yvette concentrou-se na escrita e revisão dos testes. A página distingue a contribuição individual do trabalho conjunto.
- `chapters/methodology.tex`: execução com Verilator, inspeção com GTKWave, macros Assembly, dados de entrada/saída esperada, geração Python, seleção e repetição de testes.
- `chapters/problemes.tex`, “Erreur shift mémoire”: limite de offset de 8 para 16 bytes em `core/load_unit`. O screenshot contém um FIXME sobre parametrização por XLEN, preservado na legenda. A página não apresenta o ajuste como uma correção geral certificada.
- `chapters/taux_manuelle.tex`, “Pourcentage après la résolution des problèmes”: 40 aprovados/6 falhas em 46 testes de 32 bits; os mesmos totais para 64 bits; 24 aprovados/22 falhas em 46 testes de 128 bits. Publicadas as contagens, evitando confundir taxa de sucesso nesse conjunto com cobertura exaustiva da ISA.
- O mesmo capítulo, “Résultats de la génération des tests”: apenas ADD possuía verificação implementada no gerador. A cobertura do gerador não equivale à campanha manual.
- Não foram reproduzidas explicações ambíguas do relatório sobre ADD/ADDW nem atribuída uma limitação do montador ao hardware. A extensão é experimental, não apresentada como suporte padrão de todos os CVA6.

## Carrinho autônomo

Arquivo original: `Controle_et_commande.zip`.
SHA-256: `3bc7253fda9c2b08b9e86db1a83152d4502f65340b748c5eaa7893f4614178d5`.

- `chapitre/Moteurs.tex`, “Choix du type de contrôle”: a solução final usa ação **integral**, com ganho de 0,15 na escala do protótipo. Isso substitui a referência a PI da versão anterior do portfólio.
- `chapitre/Direction.tex`: calibração do servo, saturação e diferencial por software para rodas interna e externa.
- `chapitre/Caméra.tex`: câmera de 128 pixels, média local, detecção por derivada, centro de referência no pixel 60 por desalinhamento físico. O tempo da segunda fase de exposição está incompleto no texto; não foi inferida uma unidade ou frequência final.
- `chapitre/Suivi_piste.tex`: erro lateral, deslocamento do centro entre aquisições e falsos candidatos de borda nas curvas; reutilização de referências anteriores quando a detecção é incoerente.
- `chapitre/conclusion.tex`: protótipo funcional, melhorias pendentes sob iluminação variável e em curvas. Desvio de obstáculos é trabalho futuro.
- FRDM-KL25Z e C vêm do conteúdo previamente fornecido. Não foram inventadas velocidades máximas, erro de seguimento, tempo de volta ou taxa de sucesso.

## Injeção de falhas

Arquivo original: `Rapport_TP_sureté.zip`.
SHA-256: `5a48b548adb7748f48790a3c54b745f57d08f64d648bf59ef15cfa469903921b`.

- `chapitre/corps.tex`, “DUT et Testbench”: multiplicador sequencial CoreMult e testbench fornecidos; caminho de dados DPMult e controle FSMMult. Corrigida a afirmação anterior de que o DUT completo tinha sido criado pela autora.
- “Modèle de Fautes et Configuration de la Campagne”: 65 bits no caminho de dados + 5 no controle; período de 50 ns; janela de 9.200 ns; 184 ciclos × 70 bits = 12.880 combinações possíveis. Esse número é o espaço definido, não o número de casos concluídos pelo saboteur.
- “Simulation basée sur l’injection de fautes”: exemplo TCL com `force -deposit` em ACC(12) aos 5.000 ns, campanhas e comparação de BusOut.
- “Injection de fautes sur VHDL”: saboteur controlado por `do_injection`, pulso inicial em ACC(12) aos 5.200 ns por 50 ns e varredura temporal no testbench.
- “Extension du Testbench pour couvrir toutes les cibles”: integração para todos os 70 bits não concluída. A limitação aparece no texto e no resultado da página.
- São simulações; não foram acrescentadas medições de radiação, qualificação espacial ou taxas físicas de falha.

## Figuras e nomes

`assets.json` registra o caminho original de cada uma das 30 imagens selecionadas (14 no RISC-V, 9 no carrinho e 7 na injeção de falhas), o novo nome descritivo, suas dimensões e seu SHA-256. As imagens foram copiadas sem edição; títulos, legendas e explicações foram traduzidos, e os rótulos dentro das figuras preservam o original. Links permitem abrir cada imagem em tamanho original mesmo sem JavaScript.

Arquivos PNG já descritivos foram mantidos. Foram normalizados o retrato, as peças comuns de Damas Espaciais e quatro nomes de documentos do BRAFITEC; os documentos do BRAFITEC não foram adicionados ao site publicado. As referências ao retrato e às peças foram atualizadas no gerador, nos metadados e nos manifests.

Os ZIPs da raiz são referências de entrada, não dependências do gerador. O site usa apenas os textos incorporados e as figuras selecionadas; o build não publica os arquivos de referência.


## Revisão visual

- RISC-V: divisão em duas partes de 64 bits, interfaces CPU/cache/memória, seis formatos de instrução anotados, fluxo de comparação, rastros GTKWave, laço de testes, extensão de sinal, investigação do alinhamento e correção do offset. Os formatos representam codificações de instrução de 32 bits; não são apresentados como instruções de 128 bits. A ilustração de alinhamento é identificada como hipótese de investigação.
- Carrinho: foto real da calibração, PWM, geometria das rodas, aquisição/filtragem/derivada/referência da câmera, geometria do erro lateral e falso candidato de borda. Os gráficos de aquisição e filtragem têm escalas e aquisições diferentes; a legenda não os apresenta como uma medição quantitativa pareada.
- Injeção: desenhos de CoreMult/DPMult/FSMMult, rastros de referência e injeção em 5.000 ns, mapa bit × ciclo e detalhe, registro do saboteur em ACC(12). O mapa representa os alvos e instantes possíveis, não um mapa de falhas medidas.
- O conteúdo está em `content/project_reports.py` e `content/project_visuals.py`; `scripts/project_report_design.py` reúne texto, figuras e resultados nas quatro línguas. As seleções são aprimoramentos progressivos: sem JavaScript, todos os diagramas aparecem na ordem de leitura. Links de imagem funcionam sem scripts; com scripts, abrem o visualizador existente do site.
