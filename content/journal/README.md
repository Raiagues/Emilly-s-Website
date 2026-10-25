# Como editar seu diário

O site continua no GitHub Pages. Você edita texto e fotos no repositório e, ao salvar na branch `main`, o GitHub gera e publica as páginas automaticamente. Não precisa de Render nem de uma conta de administração no site.

## Alterar uma história

Abra o arquivo da história em `content/journal/` no GitHub e clique no lápis para editar. Também pode usar um editor no computador.

| Arquivo | História |
| --- | --- |
| `brafitec.json` | A seleção, o francês e a vida em Grenoble |
| `cern.json` | CERN openlab |
| `cnes.json` | CNES e Toulouse |
| `bsv.json` | Viagem aos Estados Unidos |
| `visiona.json` | Visiona e a volta ao Brasil |
| `south-summit.json` | Os painéis e os encontros no South Summit |
| `china.json` | A imersão na China |
| `premio-na-pratica.json` | Prêmio Na Prática |
| `fundacao-estudar.json` | Fundação Estudar e Lyfe Academy |

- `title`: título da história.
- `subtitle`: resumo na abertura da página da história.
- `intro`: primeiro parágrafo, também usado como nota no álbum da página inicial.
- `sections`: capítulos, na ordem em que aparecem na página.
- `paragraphs`: os parágrafos de cada capítulo, na ordem de leitura.
- `photos`: o catálogo de fotos e suas legendas.
- `cover`: três fotos da capa, referenciadas pelos nomes do catálogo. A última é a foto principal do álbum da página inicial; a primeira aparece como uma segunda foto menor.
- `resource`: arquivo e texto do botão do relatório. É opcional.
- `links`: links opcionais dentro de cada capítulo; cada item contém `url` (HTTP/HTTPS) e `label` (texto nos quatro idiomas). Servem para indicar eventos, laboratórios ou outras fontes.
- `related_award`: nome exato de uma conquista para ligar aquela entrada na página Conquistas à história. Uma conquista pode apontar para mais de uma história. Opcional; `award_link_label` define o texto do link nos quatro idiomas.
- `technical_path`: endereço da página técnica relacionada. É opcional. A página técnica também passa a apontar para o diário. Sem relatório, o link aparece na introdução da história.
- `technical_label` e `journal_link_label`: textos opcionais, nos quatro idiomas, para os links entre a história e a página técnica.
- `date`: data de publicação, no formato `AAAA-MM-DD`, usada nos metadados.
- `timeline`: acontecimentos da história; cada item tem `date` (`AAAA`, `AAAA-MM` ou `AAAA-MM-DD`), `label` e `title` nos quatro idiomas e, opcionalmente, `section` para abrir diretamente um capítulo. A página inicial mostra os acontecimentos do mais recente ao mais antigo. O álbum e a lateral dos relatos usam o acontecimento mais recente de cada história para ordenar as entradas; a data de publicação não interfere.
- `entities`: identificadores das pessoas e instituições que aparecem no relato, cadastrados em `entities.json`.
- `documents`: dentro de um capítulo, lista de imagens de documentos, referenciadas pelo mesmo catálogo `photos`. São mostradas inteiras e podem ser abertas em outra aba; não entram no contador da galeria de fotos.
- `period`: o período da experiência, mostrado para quem lê. Pode ser diferente da data de publicação.

Cada texto tem quatro versões: `en`, `pt`, `fr`, `es`. Edite o texto **entre as aspas**, preservando chaves e vírgulas. Se precisar usar aspas dentro do texto, prefira “aspas curvas” ou escreva `\"`.

Exemplo de um parágrafo:

```json
{
  "en": "I went hiking with friends.",
  "pt": "Fiz uma trilha com meus amigos.",
  "fr": "J’ai fait une randonnée avec mes amis.",
  "es": "Hice una caminata con mis amigos."
}
```

Os textos são tratados como texto simples, sem HTML. Para criar outro parágrafo, acrescente mais um objeto à lista `paragraphs`. Não é necessário editar os HTMLs: eles são gerados automaticamente.

O inglês é a versão padrão. Se uma tradução estiver vazia, o site usa a versão inglesa daquele trecho. Preencha as quatro para uma leitura inteiramente traduzida.

## Colocar outra foto

1. Envie a foto para `portifolio/cern/` usando **Add file → Upload files** no GitHub. Para outras histórias, crie uma pasta própria dentro de `portifolio/`.
2. No catálogo `photos` do JSON, acrescente um nome curto, o caminho, as dimensões em pixels e a legenda:

```json
"nova-foto": {
  "file": "portifolio/cern/nova-foto.jpeg",
  "width": 960,
  "height": 1280,
  "caption": {
    "en": "My caption in English.",
    "pt": "Minha legenda.",
    "fr": "Ma légende.",
    "es": "Mi pie de foto."
  }
}
```

3. Acrescente `"nova-foto"` à lista `photos` do capítulo escolhido. A ordem dessa lista é a ordem das fotos na história.

Use as dimensões reais da imagem, para reservar o espaço correto durante o carregamento. A galeria, a capa e o álbum da página inicial respeitam a proporção original. As fotos não precisam ter a mesma orientação. A capa se adapta automaticamente à última foto de `cover`, que é a principal. Uma foto vertical fica ao lado das duas menores. Uma horizontal ocupa a largura acima delas.

As galerias agrupam as imagens pelas proporções, mantendo a ordem do capítulo. No celular, elas aparecem uma abaixo da outra. Uma foto vertical pode acompanhar um trecho curto na lateral. Trechos mais longos recebem as fotos abaixo do texto. Não é necessário editar o CSS ao trocar uma foto.

As molduras têm inclinações suaves e incluem a legenda. O tamanho das fotos é limitado mesmo em telas grandes, para manter o ritmo da leitura. Um clique abre a foto maior no visualizador.

As fotos fornecidas ficam intactas. Apenas as imagens e o relatório referenciados pelos posts publicados entram no pacote do site; arquivos extras da pasta não são publicados automaticamente.

## Escrever uma história nova

Duplique uma história existente, escolha outro nome para o arquivo e outro `slug` (letras minúsculas, números e hífens; `connections` é reservado). Por exemplo, `minha-primeira-trilha` vira `journal/minha-primeira-trilha.html`. Atualize textos, data, `timeline`, `entities` e fotos; remova `resource` e `technical_path` se não houver relatório ou projeto relacionado.

Comece com **`"published": false`**. O gerador ignora rascunhos. Quando terminar, mude para `true`: a história entra na página inicial e ganha páginas nos quatro idiomas. Use o mesmo `slug` depois de publicar para preservar o endereço.

A história do CERN já inclui os capítulos sobre a preparação e a aprovação, escritos a partir do seu relato. Para uma nova história em rascunho, duplique esse arquivo e mantenha `published: false` enquanto escreve. O gerador exige os textos principais em inglês antes de publicar.

Para retirar uma história do site, mude `published` para `false` e publique a alteração. O novo pacote deixa de incluir suas páginas e os arquivos exclusivos dela. Isso não apaga os arquivos nem o histórico do repositório GitHub.

## Navegação entre histórias

Cada relato tem um índice de capítulos e uma lista com fotos das outras histórias, do mais recente ao mais antigo. Essa lista é gerada automaticamente a partir de `timeline` e `cover` e começa recolhida. O controle “Recolher menu” fecha toda a navegação, enquanto “Nesta história” e “Outras histórias” abrem e fecham suas próprias listas. Esses controles funcionam com teclado e sem JavaScript. No celular, o menu fica antes do texto. Não há cartões de recomendações ao final dos relatos.

Os identificadores de `entities` são apenas metadados editoriais internos. Não existe uma página pública de pessoas e instituições nem etiquetas com esses nomes; `entities.json` não faz parte do pacote publicado. Use títulos sobre a experiência ou o papel da pessoa (por exemplo, “minha mentora”); nomes podem aparecer no corpo do relato.

A história da candidatura e da final está em `premio-na-pratica.json`; a viagem está em `china.json`. O mesmo `related_award` faz com que ambas apareçam na página Conquistas. Para acrescentar detalhes da seleção, edite os capítulos `inscricao`, `imersao` e `resultado` do relato do prêmio.

## E-mails e outros documentos

Os três prints de e-mail publicados usam arquivos `*-protegido.png`, com o endereço do remetente coberto permanentemente nos pixels da imagem. Os originais não foram enviados ao repositório. Para acrescentar outro print, oculte as informações pessoais no próprio arquivo antes do upload; cobrir com CSS não protege a imagem baixada.

No CERN, o trecho transcrito do e-mail continua disponível em **Ler o trecho do e-mail**, abaixo do print. As datas de candidatura ficam no relato: a linha do tempo principal mostra os períodos das experiências. No caso dos Estados Unidos, BSV e Brasil Project têm entradas próprias que apontam para capítulos da mesma história.

## Conferir e publicar

No computador:

```bash
./setup
./start
```

Abra `http://127.0.0.1:8000/pt/`. Para encerrar, use `./stop`. Depois de editar, use `./stop` e `./start` para gerar e conferir novamente. Após conferir, envie ao GitHub o JSON, as fotos selecionadas para a história e os HTMLs gerados.

Pelo editor do GitHub, salve usando **Commit changes** na branch `main`. O workflow gera os HTMLs de publicação; você não precisa fazê-lo manualmente nesse caminho. Acompanhe **Actions → Publish portfolio to GitHub Pages**. Se a edição contiver JSON inválido ou um arquivo ausente, a publicação falha e a última versão publicada continua no ar. Corrija o arquivo e faça outro commit.

Os arquivos JSON ficam no repositório, inclusive os rascunhos, e seguem a visibilidade configurada no GitHub. `published: false` controla apenas a presença da história no site.

## Conclusões e referências antigas

`closing` aparece como um parágrafo normal ao final da história, sem caixa de citação ou assinatura. O campo antigo `stories` pode existir nos JSONs como referência editorial validada, mas não produz cartões na página. A navegação entre relatos fica na lateral cronológica.

## A voz do diário

Escreva em primeira pessoa, como ao contar uma história para amigos. Os leitores também podem ser estudantes, familiares, recrutadores, founders e investidores. Explique termos técnicos quando forem necessários para entender a experiência. Os detalhes de implementação e os resultados completos podem ficar na página do projeto ou no relatório.

Prefira cenas, decisões e aprendizados que realmente aconteceram. Uma recusa não precisa desaparecer da história, assim como uma conquista não precisa virar uma lição para quem lê. Evite repetir a conclusão ao longo de vários capítulos. Os textos editoriais e as legendas não usam dois pontos, travessões ou ponto e vírgula. As transcrições de documentos mantêm o texto original.

Mantenha o tom profissional, direto e em primeira pessoa. Dê destaque às contribuições, conquistas e dificuldades concretas dos processos, como requisitos de idioma, preparação técnica e organização de prazos. Evite dramatização, comparações de remuneração, detalhes íntimos, condições internas de trabalho e relatos pessoais de terceiros. Lembranças leves de viagens e convivência podem preservar a autenticidade sem exposição excessiva. A revisão de outubro de 2026 aplica esse cuidado aos nove relatos, nos quatro idiomas.

No BRAFITEC, a preparação acadêmica, a seleção condicionada ao certificado e a adaptação ao francês em sala são etapas diferentes. O relato não afirma fluência após um mês nem apresenta a experiência pessoal como regra de todos os processos seletivos ou de todas as universidades francesas. As fotos publicadas são apenas as escolhidas no catálogo do JSON.
