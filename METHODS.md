# Methods

## Models, dates, access
| role | model | access | effort | dates |
|---|---|---|---|---|
| tested | `gpt-6-astra` | OpenAI Responses API | low, high | 8-9 Sep 2026 |
| tested (comparison, section 1) | `gpt-5.6-sol` | OpenAI Responses API | high | 8 Sep 2026 |
| tested (loop, vignette controls, echo question) | `claude-fable-5-1` | Claude Code sub-agents (harness, not raw API) | default | 8-9 Sep 2026 |
| simulator (patient and world) | `gpt-5.6-sol` | OpenAI Responses API | low | 8-9 Sep 2026 |
| grader | `gpt-5.6-sol` | OpenAI Responses API | medium | 8-9 Sep 2026 |

All patients are fictional. Scenarios and hidden charts were written by the author for this study; no real patient data, records or identifiers were used, and no ethics approval or consent was required. Where the setting was an Italian emergency department or an Italian patient the models received Italian text; every such prompt, chart, record and transcript is provided in English (machine translation, `translate_texts.py`, `translate_transcripts.py`, `TRANSCRIPTS_EN.md`) with the Italian original as the text of record. Rubrics and grading are in English.

## Scoring
Section 1 (template-breaking vignettes) was scored by keyword matching in Python (`run_cases.py`); a keyword grader cannot separate "CPPD" from "gout, consider CPPD", and 62 of the 108 correct section-1 answers also mention the template diagnosis (see RESULTS.md). Sections 2-13 were graded by `gpt-5.6-sol` against a fixed boolean rubric per item (CASES.md), returned as JSON; the two Fable written-vignette answers in section 13c were scored by the author. Every count in RESULTS.md is recomputed from the JSON files by `build_results.py`.

Human reading: all loop transcripts and a sample of every text experiment were read by the author; no independent grader was used. Judge verdicts were overridden in two places, both reported: section 5 (`nsaid_trial_first` scored 1/12 by the judge in the fibromyalgia-trait variant while the NSAID trial is mentioned as a secondary step in every answer) and section 13 (source of infection: judge 3/4 and 2/2, transcript 3/4 and 1/2; the gluteal abscess was elicited in 4 of 6 spondylodiscitis runs).

## Interactive loop
Doctor system prompt (Astra), English translation:
```text
You are the on-call doctor in an Italian Emergency Department. You have the patient and the triage information in front of you. You have no other information: you must elicit it yourself.
At each turn, do ONE thing only, in a few lines: ask the patient a question, or perform a specific physical examination manoeuvre, or request a test/imaging, or make an immediate treatment decision. The system will respond only to what you ask.
When you have enough information, write one line beginning with "FINAL DECISION:" followed by the working diagnosis, immediate decisions and what NOT to do (max 5 sentences). You have a maximum of 12 turns.
```
<details><summary>Italian original (verbatim, as used)</summary>

```text
Sei il medico di guardia in un Pronto Soccorso italiano. Hai davanti il paziente e il triage. Non hai altre informazioni: devi costruirle tu.
Ad ogni turno fai UNA sola cosa, in poche righe: una domanda al paziente, oppure una manovra di esame obiettivo specifica, oppure la richiesta di un esame/imaging, oppure una decisione terapeutica immediata. Il sistema ti risponde solo a quello che chiedi.
Quando hai abbastanza elementi, scrivi una riga che inizia con "DECISIONE FINALE:" seguita da diagnosi di lavoro, decisioni immediate e cosa NON fare (max 5 frasi). Hai al massimo 12 turni.
```
</details>
Simulator system prompt (the hidden chart is appended), English translation:
```text
Simulate the patient and the Emergency Department environment. You have a HIDDEN MEDICAL RECORD containing the truth. Rules:
- If the doctor asks the patient a question, answer in the first person as the patient, in colloquial English, 1-3 sentences, revealing ONLY what was asked and what is in the medical record. If the question concerns information in the medical record, reveal it naturally. Do not spontaneously offer information that was not asked for. The patient does not know technical terms and may minimise.
- If the doctor performs a physical examination manoeuvre, respond with "PE: ..." reporting the finding from the medical record; if the finding is not in the medical record, "PE: normal".
- If they request a laboratory test or imaging, respond with "RESULT: ..." from the medical record; if it is not in the medical record, give a plausible normal value.
- If they decide on a treatment, respond with "PERFORMED." and any effect if present in the medical record.
- If they do several things at once, respond only to the first.
- Never make a diagnosis, suggest anything, or provide hypotheses.
HIDDEN MEDICAL RECORD:
```
<details><summary>Italian original (verbatim, as used)</summary>

```text
Simuli il paziente e il mondo del Pronto Soccorso. Hai una CARTELLA NASCOSTA con la verità. Regole:
- Se il medico fa una domanda al paziente, rispondi in prima persona come il paziente, in italiano colloquiale, 1-3 frasi, rivelando SOLO ciò che è stato chiesto e che è nella cartella. Se la domanda tocca un dato nella cartella, rivelalo con naturalezza. Non offrire spontaneamente informazioni non chieste. Il paziente non conosce i termini tecnici e può minimizzare.
- Se il medico esegue una manovra di esame obiettivo, rispondi con "EO: ..." riportando il reperto dalla cartella; se il reperto non è in cartella, "EO: nella norma".
- Se richiede un esame di laboratorio o imaging, rispondi con "RISULTATO: ..." dalla cartella; se non è in cartella, dai un valore normale plausibile.
- Se decide una terapia, rispondi "ESEGUITO." ed eventuale effetto se in cartella.
- Se fa più cose insieme, rispondi solo alla prima.
- Non fare mai diagnosi, non suggerire, non dare ipotesi.
CARTELLA NASCOSTA:

```
</details>
Grader prompt (verbatim):
```text
Grade this ED consultation transcript (Italian). The doctor's lines are 'MEDICO', the patient/world lines are 'MONDO'. Rubric (booleans):\n{rubric}\n\nTRANSCRIPT:\n{transcript}\n\nReturn ONLY the JSON object.
```
Fable doctor prompt: `fable_doctor_prompt.md`.

Harness asymmetries, all of which favour or handicap one model and are not corrected for:
1. Astra was run through the Responses API without `previous_response_id`; only its output text was carried between turns, so its reasoning was not persisted across the loop. Fable retained its full context and reasoning inside the Claude Code harness.
2. Astra's budget was twelve turns including the final decision (at most eleven actions); Fable had twelve actions plus a separate final command, and saw a running counter of actions used. Fable used the whole budget in both spondylodiscitis runs.
3. Fable sub-agents sometimes packed several questions into one action; the simulator's rule to answer only the first was applied inconsistently.
4. The doctor prompt told Astra to decide "when you have enough elements"; early closure may be partly prompt- and budget-induced. A neutral-prompt replication was started and aborted at the author's request; its partial output is not part of the record.
5. In the septic-knee scenario blood cultures were reported as "in progress" and never returned positive within the session; the rule both models state (echocardiography once Staphylococcus aureus grows) could not be triggered by cultures. The available trigger was the new murmur on auscultation.
6. History items in the hidden charts were revealed only when the simulator judged the question specific enough; this threshold is a model judgment. Actions had no cost other than the budget; no elapsed time was modelled.

Turns are doctor lines including the final decision; actions are turns minus one. Medians and ranges are in RESULTS.md section 11.

## Versions and overwrites
Every script overwrites its output file. The six original loop scenarios were run twice on Astra with consistent results; only the second run's file survives. The first spondylodiscitis chart (`exp_loop_L10_astra.json`, 4 runs) had no murmur or vegetation; both were added before the runs of record (`exp_loop_L10v2_astra.json`). Both files give endocarditis 0/4. Scenario identifiers are non-contiguous because drafts were dropped before any model run; no scenario was run and discarded.

## Design limits
The spondylodiscitis scenario carries the same planted finding as the septic knee (Staphylococcus aureus endocarditis, new aortic murmur revealed only on auscultation); the closure result rests on one finding type in two scenarios, twelve runs, two models. Exact 95% confidence interval for 0 of 12: 0 to 26.5%. Fable auscultated the heart in both pulmonary-embolism runs, where its hypothesis called for it, so the behaviour is hypothesis-bound rather than absent. The written-vignette control supplied the complete chart, including the dental cleaning or drained abscess, not the murmur alone. The simulator and the grader share a vendor with one of the two tested models.
