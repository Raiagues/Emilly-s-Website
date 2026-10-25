# CERN openlab — supplied project deep dive

Source: `CERN openlab · project deep dive-html.zip`, supplied by Emilly on
25 October 2026. `Cern.dc.html` defines the composition, technical narrative,
detector geometry, interactions and metrics. The original export/runtime and
ZIP are not published.

- `page.html.tmpl`: the supplied body composition, with escaped translation,
  asset, URL and component slots. Its numbered CSS classes map to the original
  inline declarations in `style/cern.css`.
- `strings.json`: English source text and Portuguese, French and Spanish
  translations, including image descriptions and control labels.
- `controls.json`: the five original model measurements, two visibility states
  and five detector layers. String values such as `t095` refer to the catalog.
- `assets.json`: original PNG names, production paths and SHA-256 hashes. All
  14 images are byte-for-byte copies; plots have not been cropped or recreated.
- `scripts/cern_redesign.py`: static rendering and detector geometry. Its two
  document constants are the final report and slides URLs supplied by Emilly.
- `src/cern.js`: progressively enhances the detector, thresholds and comparison.
  Without JavaScript, the report, model table, both threshold images and native
  image/document links remain available.

Integration retains the shared fixed navigation, four-language switcher,
experience catalogue return state, useful footer and keyboard-accessible image
viewer. The supplied desktop dimensions remain intact. Mobile rules stack
content and scale the detector without clipping charts. Small-label contrast,
focus indicators, a rotation pause control and reduced-motion behavior are
accessibility adjustments.

The two prototype document placeholders now link to the supplied final report
and presentation. The presentation is labeled as slides/PDF, not a Zenodo
video. The empty learning placeholder was replaced with a conclusion already
supported by the supplied report (bandwidth feasibility does not establish
FPGA readiness; pile-up remains a data limitation). The explanatory copy and
plots still identify their source as the detailed interim report, as in the
prototype. They do not claim completed FPGA synthesis or deployment.

The final URLs are user-supplied references. Automated access to Zenodo was
denied and CERN Indico returned an anti-bot HTML challenge during implementation;
no downloaded substitute or inferred final-report content is published.
