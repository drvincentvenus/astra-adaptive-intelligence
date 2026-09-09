# Table 1. Summary of experiments

 All runs 8–9 September 2026. Astra = GPT-6 Astra via API at two reasoning efforts; Fable = Claude Fable 5.1 as Claude Code sub-agents; grader = GPT-5.6 Sol with fixed boolean rubrics, spot-read by the author. Full rubrics, prompts and transcripts in Supplementary Information.

| # | Experiment | Setting | Runs | Right answer or decision | Adaptive behaviour | What was missed |
|---|---|---|---|---|---|---|
| 1 | Template-breaking vignettes (CPPD not gout, EORA not PMR, DGI not ReA, hypothyroid not FM, acquired haemophilia not LA, IMNM not statin) | vignette, MCQ, noisy record; Astra + Sol | 108 | 108/108 | n/a | none |
| 2 | Criteria met, patient says no (athlete BME, GCA vs pneumonia, PsA vs meniscus) | vignette and record; Astra | 24 | template diagnosis 0/24 | criteria treated as classification, not diagnostic | none |
| 3 | Missing decisive item (frame-internal and frame-external) | text, closed and open; Astra | 200 | item asked 191/200 | asks for visual symptoms, drugs, HIV, myeloma, ICI, OSAS | 71-year-old seronegative polyarthritis: malignancy never raised 0/8 |
| 4 | Selective revision (new evidence, senior pushback, irrelevant result) | multi-turn text; Astra | 72 | diagnosis retained 72/72 | changes only what the evidence changes | none |
| 5 | axSpA in a woman or man with fibromyalgia traits, three visits | multi-turn text; Astra | 24 trajectories | biologic at visit 1: 0/24; switch after failed adalimumab: 0/24 | NSAID trial, reconsiders on non-response, reads resolved MRI correctly | none |
| 6 | Multiresistant PsA with inflated DAPSA, seven biologic "failures", DAPSA remission with PsAID 5 | multi-turn text; Astra | 60 | switch 0/60 | tenderness separated from inflammation; fibromyalgia named unprompted 100% | none |
| 7 | Mirror cases: same surface, real inflammation; plus a senior who wants all therapy stopped | text; Astra | 36 | escalation 30/30; refusal to stop 6/6 | treatment tracks Doppler, erosions, CRP, not the surface | none |
| 8 | Psoriasis without arthritis (arthralgia, "prevent PsA" biologic request, early PsA, DIP osteoarthritis) | text; Astra | 24 | 24/24 | labels neither over- nor under-applied | none |
| 9 | Raw Italian emergency records with wrong triage label | text; Astra | 36 | anchor overridden 36/36 | septic not flare, PE not anxiety, GCA not tension headache, PJP, tocilizumab-masked perforation, atlantoaxial instability | none |
| 10 | Interactive emergency loop, hidden chart, model must ask (8 scenarios) | simulator; Astra | 32 | 32/32 | median 6 actions to an actionable diagnosis | endocarditis behind septic knee and behind spondylodiscitis: heart auscultated 0/8, echo 0/8 |
| 11 | Same loop | simulator; Fable | 16 | 16/16 | median 11 actions; asks chills, prophylaxis, temporal arteries, calf | endocarditis: heart auscultated 0/4, echo ordered 0/4 |
| 12 | Same two patients as written vignettes with the murmur in the text | text; Astra and Fable | 14 | endocarditis considered and echo ordered 14/14 | | none |
| 13 | Plain question: does this patient need an echocardiogram? | text; Astra and Fable | 5 | rule stated correctly 5/5 | | the rule was known and not acted on |

Adaptive-intelligence metric (examination completed after the diagnosis was secured), rows 10–11: 0 of 12 runs.
