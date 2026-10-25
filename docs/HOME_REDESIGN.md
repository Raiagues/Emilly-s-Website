# Redesign do portfólio

## Relatório técnico do CERN openlab — 25/10/2026

`pages/experience/cern.html` e suas versões PT, FR e ES agora seguem o arquivo `CERN openlab · project deep dive-html.zip`. A abertura com ATLAS em 3D, passagem lilás, indicadores, plano de voo, oito capítulos, gráficos em papel, comparador de modelos, controle de banda, equipe e documentos mantêm a composição do modelo. O cabeçalho fixo, o seletor de idiomas e o rodapé são os componentes compartilhados do site.

As cinco camadas do detector podem ser destacadas e a rotação pode ser pausada. O limiar alterna entre 0% e 3%, atualizando gráfico, legenda e contagens. O comparador apresenta os cinco modelos com os números originais. Gráficos abrem no visualizador com setas, Escape e retorno de foco. Movimento reduzido, teclado e conteúdo sem JavaScript são suportados; nesse último caso, uma tabela reúne os cinco modelos e as duas imagens de limiar continuam disponíveis.

O relatório final e os slides usam os links fornecidos pela proprietária. Não há runtime do exportador, React, imagens externas de exemplo ou botões sem destino. Os 14 PNGs são idênticos aos do ZIP. O arquivo original e os materiais pessoais não selecionados continuam fora de `dist`.

Validação: build e verificador aprovados nos 171 HTMLs; 45 cenários de navegador cobertos, com 43 aprovados na execução completa e reexecução aprovada dos dois cenários ajustados (retorno específico do CERN e espera pelo término da animação de entrada antes de medir contraste no diário). Os cinco cenários novos conferem quatro idiomas, larguras de 320 a 1440 px, links finais, oito capítulos, métricas, detector, ampliação, teclado, conteúdo sem JavaScript e WCAG A/AA. A comparação visual com o HTML enviado confirmou as mesmas medidas da abertura no desktop.

## Catálogos, navegação e fontes públicas — 25/10/2026

Projetos e experiências agora compartilham o catálogo com título de pôster em duas linhas, rota ilustrada animada, filtros e busca em campo arredondado. Os cartões inteiros são links, sem chamada extra Ver projeto; tecnologias e competências usam etiquetas com tipografia discreta e sem estrelas. Filtros e busca permanecem ao voltar de ambos os tipos de página.

As páginas de projetos e experiências usam o explorador compacto do diário, com títulos visíveis, prévias ao passar o mouse ou focar pelo teclado e lista com altura limitada. O rodapé do conteúdo oferece o item anterior e seguinte, conforme a ordem cronológica, sem criar um destino depois do último item. Os retornos no topo têm círculo e seta à esquerda. O rodapé comum contém GitHub, LinkedIn e e-mail; o antigo atalho Voltar ao topo foi retirado.

O cabeçalho compartilhado normaliza fontes, idioma e estado ativo nas páginas antigas. A página de contato usa o mesmo papel, ilustração e borda de correspondência da identidade atual. O formulário mantém validação e destino originais. A home mantém os três cartões de experiência coloridos, com datas e etiquetas em uma tipografia consistente, movimento suave de elevação e ilustrações ao interagir. Movimento reduzido é respeitado.

Conquistas apresenta cinco cartões com selos e acesso direto às publicações fornecidas. AIAA SciTech e South Summit saíram da classificação de prêmios. A correção do CERN para quase 6.000 candidaturas vem da publicação oficial; detalhes e URLs estão em `content/SOURCES.md`.

Validação: build e verificador dos 171 HTMLs aprovados. Os 40 cenários de navegador foram cobertos, com reexecução aprovada dos três cenários afetados pelos ajustes finais. Incluem as 104 páginas de projetos e experiências, acessibilidade automatizada, quatro idiomas, filtros persistentes, retorno com seta à esquerda, navegação por teclado, fontes públicas, formulário com entrega interceptada e ausência de rolagem horizontal. Houve conferência visual dos catálogos, cartões de experiência, conquistas, contato, rodapé e explorador compacto no computador e no celular.

## Diário em cartões-postais e recuperação da voz pessoal — 25/10/2026

A home mostra duas histórias lado a lado, com as fotos de cada relato sobrepostas. As chamadas voltaram a usar a introdução em primeira pessoa, com acesso ao texto completo. As divisórias extras foram retiradas; o título mantém uma única linha discreta, conforme a referência. Projetos ganhou o acesso ao catálogo no cabeçalho da seção, três cartões e o painel do trabalho atual inteiramente clicável. O indicador no ar pulsa e respeita a preferência por movimento reduzido. Não há botões separados para abrir os projetos da home.

O arquivo `journal.html` usa o modelo enviado em `All stories · postcard rack-html.zip`, adaptado ao gerador estático. A ilustração, os cartões de foto e texto, os selos e a ordenação por data foram incorporados com conteúdo real. O cabeçalho fixo e os quatro idiomas permanecem. A faixa de newsletter e o encerramento extra do ZIP foram omitidos. O arquivo mostra até 12 cartões por vez quando crescer; links para cartões específicos continuam funcionando.

As páginas de leitura têm abertura com polaroids próximas, títulos de capítulos em serifa, coluna de texto consistente e álbuns com fotos proporcionais e alinhadas. Documentos ficam em cartões de consulta; as imagens completas continuam disponíveis. A navegação final usa uma lista de títulos com altura limitada e prévias ao passar o mouse ou focar pelo teclado. Links diretos funcionam sem JavaScript. A lista foi verificada com 100 entradas sem aumentar a altura da seção.

Os relatos anteriores à revisão de tom, no commit `997edc7`, foram consultados para recuperar descobertas, pensamentos e conclusões já registrados. Trechos pessoais de oito histórias foram recuperados nos quatro idiomas, sem desfazer as remoções de detalhes financeiros privados ou alterar resultados técnicos, datas e documentos. As conclusões revisadas se apoiam nessas experiências. Não foram criados acontecimentos novos. As fotos e os textos completos continuam nas páginas de cada história.

Validação desta revisão: build e verificador dos 171 HTMLs, com os 38 cenários de navegador cobertos e reexecução aprovada dos 12 cenários afetados pelos ajustes finais. Os dois testes da home passaram novamente após o ajuste das molduras. Foram conferidos navegação, ordenação, teclado, leitura sem JavaScript, proporção das fotos, acessibilidade automatizada e telas de computador e celular. Uma simulação adicional confirmou a paginação de 100 cartões e o acesso direto a uma história ainda não exibida. O histórico abaixo descreve as versões anteriores.


## Capa, navegação persistente e seções compactas — 25/10/2026

A capa ocupa uma tela própria no computador, sem antecipar o título de Experiência. A tipografia de pôster ganhou a linha Portfólio, e a apresentação usa o texto solicitado sobre software de voo, processadores e FPGAs, traduzido nos quatro idiomas. Foto, post-it, cores, botões e lançamento animado permanecem. Telas de notebook recebem espaçamentos menores para manter todos os elementos da capa visíveis.

O cabeçalho permanece no topo durante a navegação, inclusive nas páginas internas. A marca reúne foguete, nome e Portfólio; o menu tem Início, Experiência, Projetos, Sobre, Conquistas, Diário e Contato, com a seção atual em laranja. Conquistas também voltou ao Guia de voo. EN, PT, FR e ES ficam visíveis em um seletor segmentado. A troca de idioma conserva a seção escolhida, inclusive durante a rolagem animada.

A home apresenta as três experiências mais recentes, sem filtros, e o botão junto ao título informa o total de seis experiências. As quatro conquistas mantêm seus selos, acompanhados apenas do nome e de uma linha com instituição e reconhecimento. O botão Consultar fonte foi retirado. Linhas e espaçamentos maiores delimitam as seções.

As duas chamadas do Diário alternam texto e fotografias. Resumos, fotos e espaçamentos foram compactados para as duas histórias caberem juntas abaixo do cabeçalho no computador; no celular, o conteúdo continua empilhado e legível. Os relatos completos e a página com todas as histórias permanecem disponíveis.

Validação: build e verificador aprovados para 171 HTMLs. Os 36 cenários de navegador foram cobertos, com reexecução aprovada dos três cenários afetados pelos ajustes finais. Foram conferidos teclado, acessibilidade automatizada, navegação sem JavaScript, quatro idiomas e ausência de rolagem horizontal. A capa e as duas histórias foram verificadas em 1920 × 960, 1440 × 900 e 1366 × 768. Os registros abaixo descrevem versões anteriores.

## Restauração visual e nova organização — 25/10/2026

A abertura voltou ao modelo ilustrado: foto em polaroid com fita, Guia de voo em post-it, nome em tipografia de pôster, botões e planeta com lançamento animado. A paleta original de verde-petróleo, verde-água, pêssego, lilás e terracota foi recuperada. A animação tem controle de pausa e respeita movimento reduzido. A foto indicada pela proprietária, `fotominha.jpeg`, foi incorporada como `img/portrait-lab.jpeg`.

A ordem depois da abertura é Experiência, Projetos, Sobre mim, Conquistas, mídia, Diário, Cartas de bordo e Contato. Os três cards de resumo foram retirados. Os títulos não têm ícones nem números. O menu compacto e o seletor de quatro idiomas permanecem.

As experiências usam cartões de embarque coloridos, com as ilustrações do modelo, até três tecnologias e período abreviado. As conquistas mostram quatro selos ilustrados: Prêmio Protagonismo Universitário, Líderes Estudar, CAPES–BRAFITEC e CERN openlab. Um botão abre a página com todas as conquistas.

Sobre mim usa o envelope e o retrato em selo, com texto pessoal breve, origem em Jaru, Rondônia, e um destino aberto a novas ideias, projetos e lugares. Formação e idiomas continuam na página completa. A mídia mantém revista, entrevistas, vídeos e notícias; as publicações sociais em celulares foram retiradas.

O Diário mostra duas histórias com polaroids, botões verde-petróleo e setas terracota, sem palavras-chave. O botão junto ao título abre `journal.html`, com as nove histórias e a cronologia. Essa página existe nos quatro idiomas e funciona sem JavaScript. Links antigos com fragmentos `#archive-…` encaminham à nova página.

Cartas de bordo segue o cartão postal em três painéis do modelo. O cadastro permanece desativado e explicado na própria seção, pois não há serviço de newsletter conectado. O contato usa o título de destino, botão de e-mail, LinkedIn, GitHub, currículo e etiqueta de bagagem.

Validação: 171 HTMLs aprovados, 35 cenários de navegador cobertos, com correção de contraste e reexecução dos seis testes afetados. Conferência visual de computador e celular, quatro idiomas, teclado, pausa de animação, ausência de rolagem horizontal, navegação sem JavaScript e acessibilidade automatizada. Os registros abaixo descrevem versões anteriores.

Revisão de 18/10/2026 na branch `redesign/home-preview`.

A home e as páginas internas usam os cinco modelos de `portfolio-redesign/design/`, adaptados ao gerador Python existente. As instruções e a paleta de `DESIGN_NOTES.md` e `tokens.css` continuam sendo a referência.

## O que mudou

- Projetos e experiências usam ilustrações SVG nos cartões e nas passagens. As fotos ficam nos espaços de retrato, polaroids, revista e galerias.
- O envelope da home mostra um único parágrafo original, com três linhas na versão desktop em português. A biografia completa e a formação continuam em Sobre mim.
- A mídia mantém revista, fita cassete, recortes com bordas de papel e celulares ilustrados. A revista usa a capa enviada, sem alteração da imagem. Os controles permitem percorrer sete vídeos e quatro matérias. As quatro publicações sociais abrem os links fornecidos.
- As 104 páginas de projetos e experiências começam com a passagem ilustrada, com período, base e próximo item em ordem cronológica. Mostram as contribuições, competências, resultados, recursos e fotos existentes nos espaços do modelo.
- As 36 páginas de histórias usam abertura com polaroids, passagem, texto centralizado, capítulos recolhíveis, fotografias proporcionais e envelope de encerramento. Os textos e as legendas foram preservados.
- O trajeto ao final de cada história, projeto ou experiência contém todos os itens daquele tipo em ordem cronológica. Selecionar uma parada mostra a prévia e o link correspondente. O item da página atual mantém sua marcação.
- Catálogo de projetos com os 20 projetos ilustrados, filtros, busca e retorno aos resultados. A home mantém o projeto atual, três cartões e o acesso ao catálogo.
- Mantidos os quatro idiomas e as URLs. Hover, lançamento e demais animações respeitam a preferência por movimento reduzido. Navegação, arquivos, galerias e links de mídia continuam acessíveis sem JavaScript.

## Conteúdo preservado e fontes novas

Os 15 arquivos de conteúdo original permanecem idênticos ao início do redesign, conferidos por SHA-256. Uma comparação adicional encontrou os 2.852 trechos esperados de títulos, parágrafos, contribuições, resultados, datas, formação e legendas nas páginas geradas.

O novo `content/media.json` reúne apenas os links fornecidos, os títulos e datas verificáveis das matérias e os títulos retornados pelo YouTube. Os títulos das fontes permanecem em português nas quatro versões do site, identificados com o idioma correspondente. O endereço duplicado da matéria da Exame foi corrigido para o link único.

## Informações ausentes ou omitidas

- Número da edição da Exame, números de episódios, datas dos vídeos e identificação de contas sociais não foram acrescentados sem confirmação. As matérias mostram apenas suas datas verificadas.
- Os dois vídeos do Webservatório não retornaram metadados públicos. Seus links estão disponíveis com o nome Webservatório, conforme informado. Os links sociais também foram mantidos sem títulos, datas, contagens ou fotografias inferidas.
- Fotos específicas dos recortes e miniaturas das publicações sociais não foram inventadas. Os recortes usam o texto da fonte e os celulares mantêm o desenho do protótipo.
- Cidade de origem específica, próximo destino pessoal, disponibilidade, nomes e funções de equipe não presentes no catálogo foram omitidos.
- Números de portão, voo, assento, duração estimada de leitura, métricas adicionais, diagramas técnicos e citações de exemplo do protótipo foram omitidos. Resultados quantitativos que já existiam no conteúdo continuam nos textos originais.
- A passagem do item mais recente não mostra um próximo destino fictício. Itens com o mesmo período mantêm a ordem do catálogo original.

TODO da newsletter — escolher e configurar um serviço de inscrições. O projeto não tem integração de newsletter. O FormSubmit existente pertence ao contato. Os três assuntos e as frequências de 3 ou 6 meses podem ser selecionados, mas o e-mail e o envio permanecem desativados, com aviso visível. Nenhum endereço é coletado.

Para completar os campos omitidos da mídia, faltam apenas os metadados que a proprietária quiser disponibilizar. Os links fornecidos já estão incorporados.

## Verificação

- Build e verificador aprovados para os 167 HTMLs, incluindo assets, links, fragmentos, idiomas e limites do pacote publicado.
- 35 cenários de navegador validados, com reexecução aprovada dos cinco testes afetados pelos ajustes finais.
- Verificação adicional aprovada das 104 páginas de projetos e experiências, incluindo o carregamento das fotos e suas proporções.
- Acessibilidade automatizada nas 36 histórias e nas 11 páginas principais ou representativas, além de teclado, foco, funcionamento sem JavaScript e preferência por movimento reduzido.
- EN, PT, FR e ES conferidos em vários tamanhos, incluindo 360 px, sem rolagem horizontal. Galerias e passagens também verificadas em 320 px.
- Inspeção visual das páginas em desktop e celular. Conteúdo original conferido e `git diff --check` aprovado.

## Prévias

- [Home em desktop](preview-home-redesign-desktop.png), [home completa](preview-home-redesign-full.png) e [home no celular](preview-home-redesign-mobile.png).
- [Envelope compacto](preview-redesign-envelope.png) e [mídia](preview-redesign-media.png).
- [Experiência no CERN](preview-redesign-experience-desktop.png) e [experiência no celular](preview-redesign-experience-mobile.png).
- [Projeto](preview-redesign-project-desktop.png), [história](preview-redesign-story-desktop.png) e [catálogo](preview-redesign-directory-desktop.png).

A prévia está disponível em `http://127.0.0.1:8000/pt/`.
