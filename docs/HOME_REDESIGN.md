# Redesign do portfólio

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
