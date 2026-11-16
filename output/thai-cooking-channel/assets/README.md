# Thai cooking channel — asset library

Layout (one folder per asset, grouped by pillar):

    assets/
      manifest.json            single source of truth: id, pillar, status, tries, cost, final file, QA verdict
      _style/STYLE.txt         style block appended verbatim to every prompt
      _refs/                   reference photos of real ingredients (empty until the owner supplies them)
      _contact-sheets/         review sheets per generation round
      library/<pillar>/<asset-id>/
          prompt.txt           full prompt as sent (STYLE already appended)
          sources.md           where each drawn detail comes from, and what was deliberately left out
          candidates/r1.png    every generation, never overwritten (+ r1.json with request meta and cost)
          qa.md                review against acceptance criteria, per candidate
          final.png            the accepted candidate (copy), only after QA pass

Status values: prompt-pending -> prompt-audited -> generated -> qa-pass | qa-fail | needs-reference.
No text is drawn in any image; labels are added in HyperFrames.
