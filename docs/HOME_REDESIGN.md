# Redesign do portfólio

## Simplificação da abertura — 25/10/2026

A abertura agora usa duas colunas, com o nome e uma apresentação curta à esquerda e a foto à direita. No celular, o texto vem antes da foto. O nome aparece uma única vez na primeira tela, em uma linha e com um único estilo. O hero ocupa a altura disponível da tela, e os três cards começam depois, com espaçamento próprio.

Foram retirados o subtítulo da marca, a saudação repetida, “Portfolio”, o Guia de voo, as tags de formação, os dois botões da abertura, a faixa superior de última parada e a animação do foguete. A última experiência continua no card abaixo. Estrelas e fundos pontilhados foram removidos; a listra de correio aéreo e as fitas permanecem, com superfícies em bege e tons claros de terracota.

O menu tem cinco itens, com Conquistas acessível por Sobre e a mídia pelo Diário. Os idiomas usam um controle compacto com links nativos, operável por teclado e sem JavaScript. O cabeçalho das páginas internas usa a mesma navegação. As versões EN, PT, FR e ES mantêm seus endereços.

Inspeção visual em 1440, 390 e 320 px. Treze cenários direcionados de navegador aprovados, incluindo navegação, idiomas, teclado, ausência de rolagem horizontal, acesso às conquistas por Sobre e acessibilidade das páginas principais e das 36 histórias. A seção abaixo registra o redesign anterior.

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
