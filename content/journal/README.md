# Como editar seu diário

O site continua no GitHub Pages. Você edita texto e fotos no repositório e, ao salvar na branch `main`, o GitHub gera e publica as páginas automaticamente. Não precisa de Render nem de uma conta de administração no site.

## Alterar uma história

Abra **`content/journal/cern.json`** (CERN), **`content/journal/bsv.json`** (viagem aos Estados Unidos), **`content/journal/visiona.json`** (Visiona) **`content/journal/south-summit.json`** (South Summit) ou **`content/journal/china.json`** (China) no GitHub e clique no lápis para editar. Também pode usar um editor no computador.

- `title`: título da história.
- `subtitle`: resumo que aparece na página inicial.
- `intro`: primeiro parágrafo.
- `sections`: capítulos, na ordem em que aparecem na página.
- `paragraphs`: os parágrafos de cada capítulo, na ordem de leitura.
- `photos`: o catálogo de fotos e suas legendas.
- `cover`: três fotos da capa, referenciadas pelos nomes do catálogo.
- `resource`: arquivo e texto do botão do relatório. É opcional.
- `links`: links opcionais dentro de cada capítulo; cada item contém `url` (HTTP/HTTPS) e `label` (texto nos quatro idiomas). Servem para indicar eventos, laboratórios ou outras fontes.
- `related_award`: nome exato de uma conquista para ligar aquela entrada na página Conquistas à história. Uma conquista pode apontar para mais de uma história. Opcional; `award_link_label` define o texto do link nos quatro idiomas.
- `technical_path`: endereço da página técnica relacionada. É opcional. A página técnica também passa a apontar para o diário. Sem relatório, o link aparece na introdução da história.
- `technical_label` e `journal_link_label`: textos opcionais, nos quatro idiomas, para os links entre a história e a página técnica.
- `date`: data de publicação, no formato `AAAA-MM-DD`, usada nos metadados.
- `timeline`: acontecimentos da história; cada item tem `date` (`AAAA-MM` ou `AAAA-MM-DD`), `label` e `title` nos quatro idiomas e, opcionalmente, `section` para abrir diretamente um capítulo. A página inicial ordena esses acontecimentos e as histórias pela data da experiência, não pela publicação.
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

Use as dimensões reais da imagem, para reservar o espaço correto durante o carregamento. A galeria exibe a foto inteira e permite ampliá-la. As fotos não precisam ter todas a mesma orientação. A capa atual combina duas fotos verticais e uma horizontal; em outra composição, ajuste `cover` e, se necessário, `.journal-mosaic` no CSS.

As fotos fornecidas ficam intactas. Apenas as imagens e o relatório referenciados pelos posts publicados entram no pacote do site; arquivos extras da pasta não são publicados automaticamente.

## Escrever uma história nova

Duplique uma história existente, escolha outro nome para o arquivo e outro `slug` (letras minúsculas, números e hífens; `connections` é reservado). Por exemplo, `minha-primeira-trilha` vira `journal/minha-primeira-trilha.html`. Atualize textos, data, `timeline`, `entities` e fotos; remova `resource` e `technical_path` se não houver relatório ou projeto relacionado.

Comece com **`"published": false`**. O gerador ignora rascunhos. Quando terminar, mude para `true`: a história entra na página inicial e ganha páginas nos quatro idiomas. Use o mesmo `slug` depois de publicar para preservar o endereço.

A história do CERN já inclui os capítulos sobre a preparação e a aprovação, escritos a partir do seu relato. Para uma nova história em rascunho, duplique esse arquivo e mantenha `published: false` enquanto escreve. O gerador exige os textos principais em inglês antes de publicar.

Para retirar uma história do site, mude `published` para `false` e publique a alteração. O novo pacote deixa de incluir suas páginas e os arquivos exclusivos dela. Isso não apaga os arquivos nem o histórico do repositório GitHub.

## Conectar histórias por pessoas ou instituições

No arquivo `entities.json`, cada entrada tem um identificador estável (por exemplo, `veronica` ou `fundacao-estudar`), um `name` nos quatro idiomas e `kind` (`person` ou `institution`). Acrescente o identificador à lista `entities` de cada história em que aquela pessoa ou instituição aparece.

O site monta automaticamente a página **Pessoas e instituições** e as sugestões ao fim de cada história. Uma pessoa que aparece em apenas uma história continua acessível pelo índice; outras histórias só são sugeridas quando realmente compartilham um identificador. Não precisa cadastrar links manualmente. Ao renomear uma pessoa, mantenha o identificador para preservar os links.

A viagem à China já está em `china.json`, conectada ao Prêmio Protagonismo Universitário e à entidade `na-pratica`. Quando escrever a história da candidatura ao prêmio, crie outro post, reutilize `na-pratica` em `entities` e o mesmo `related_award`. Assim os dois relatos ficam conectados e aparecem em Conquistas, sem precisar juntar os textos. Não há uma página vazia esperando essa história.

## E-mails e outros documentos

Os três prints de e-mail publicados usam arquivos `*-protegido.png`, com o endereço do remetente coberto permanentemente nos pixels da imagem. Os originais não foram enviados ao repositório. Para acrescentar outro print, oculte as informações pessoais no próprio arquivo antes do upload; cobrir com CSS não protege a imagem baixada.

No CERN, o trecho transcrito do e-mail continua disponível em **Ler o trecho do e-mail**, abaixo do print. As datas de candidatura ficam no relato: a linha do tempo principal mostra os períodos das experiências. No caso dos Estados Unidos, BSV e Brasil Project têm entradas próprias que apontam para capítulos da mesma história.

## Conferir e publicar

No computador:

```bash
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Abra `http://127.0.0.1:8000/pt/`. Após conferir, envie ao GitHub o JSON, as novas fotos e os HTMLs gerados.

Pelo editor do GitHub, salve usando **Commit changes** na branch `main`. O workflow gera os HTMLs de publicação; você não precisa fazê-lo manualmente nesse caminho. Acompanhe **Actions → Publish portfolio to GitHub Pages**. Se a edição contiver JSON inválido ou um arquivo ausente, a publicação falha e a última versão publicada continua no ar. Corrija o arquivo e faça outro commit.

Os arquivos JSON são públicos no repositório, inclusive os rascunhos. `published: false` controla o site, não a privacidade do GitHub.
