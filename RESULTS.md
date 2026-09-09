# Results, recomputed from the committed files

Every number below is computed by `build_results.py` from the JSON files in this repository at build time. Exact (Clopper-Pearson) 95% confidence intervals are given for every proportion. Models: `gpt-6-astra` and `gpt-5.6-sol` via the OpenAI Responses API, 8-9 September 2026; `claude-fable-5-1` as Claude Code sub-agents. Grader: `gpt-5.6-sol` (medium effort) with boolean rubrics, except section 1 which was scored by keyword matching in Python.


**Volume.** Text-phase experiments (sections 1-10): 710 graded model answers on 45 distinct scenarios (multi-turn trajectories counted per turn). Interactive loop (sections 11-12): 32 Astra and 16 Fable consultations.


### 1. Template-breaking vignettes (keyword-scored)

| | value |
|---|---|
| correct / n | 108/108 (96.6-100.0%) |
| correct answers that also mention the template diagnosis | 62/108 |

Per case, format and model:

| case | format | model | effort | correct |
|---|---|---|---|---|
| C1_gout_cppd | mcq | gpt-5.6-sol | high | 2/2 |
| C1_gout_cppd | mcq | gpt-6-astra | high | 2/2 |
| C1_gout_cppd | mcq | gpt-6-astra | low | 2/2 |
| C1_gout_cppd | record | gpt-5.6-sol | high | 2/2 |
| C1_gout_cppd | record | gpt-6-astra | high | 2/2 |
| C1_gout_cppd | record | gpt-6-astra | low | 2/2 |
| C1_gout_cppd | vignette | gpt-5.6-sol | high | 2/2 |
| C1_gout_cppd | vignette | gpt-6-astra | high | 2/2 |
| C1_gout_cppd | vignette | gpt-6-astra | low | 2/2 |
| C2_pmr_eora | mcq | gpt-5.6-sol | high | 2/2 |
| C2_pmr_eora | mcq | gpt-6-astra | high | 2/2 |
| C2_pmr_eora | mcq | gpt-6-astra | low | 2/2 |
| C2_pmr_eora | record | gpt-5.6-sol | high | 2/2 |
| C2_pmr_eora | record | gpt-6-astra | high | 2/2 |
| C2_pmr_eora | record | gpt-6-astra | low | 2/2 |
| C2_pmr_eora | vignette | gpt-5.6-sol | high | 2/2 |
| C2_pmr_eora | vignette | gpt-6-astra | high | 2/2 |
| C2_pmr_eora | vignette | gpt-6-astra | low | 2/2 |
| C3_reactive_dgi | mcq | gpt-5.6-sol | high | 2/2 |
| C3_reactive_dgi | mcq | gpt-6-astra | high | 2/2 |
| C3_reactive_dgi | mcq | gpt-6-astra | low | 2/2 |
| C3_reactive_dgi | record | gpt-5.6-sol | high | 2/2 |
| C3_reactive_dgi | record | gpt-6-astra | high | 2/2 |
| C3_reactive_dgi | record | gpt-6-astra | low | 2/2 |
| C3_reactive_dgi | vignette | gpt-5.6-sol | high | 2/2 |
| C3_reactive_dgi | vignette | gpt-6-astra | high | 2/2 |
| C3_reactive_dgi | vignette | gpt-6-astra | low | 2/2 |
| C4_fm_hypothyroid | mcq | gpt-5.6-sol | high | 2/2 |
| C4_fm_hypothyroid | mcq | gpt-6-astra | high | 2/2 |
| C4_fm_hypothyroid | mcq | gpt-6-astra | low | 2/2 |
| C4_fm_hypothyroid | record | gpt-5.6-sol | high | 2/2 |
| C4_fm_hypothyroid | record | gpt-6-astra | high | 2/2 |
| C4_fm_hypothyroid | record | gpt-6-astra | low | 2/2 |
| C4_fm_hypothyroid | vignette | gpt-5.6-sol | high | 2/2 |
| C4_fm_hypothyroid | vignette | gpt-6-astra | high | 2/2 |
| C4_fm_hypothyroid | vignette | gpt-6-astra | low | 2/2 |
| C5_la_aha | mcq | gpt-5.6-sol | high | 2/2 |
| C5_la_aha | mcq | gpt-6-astra | high | 2/2 |
| C5_la_aha | mcq | gpt-6-astra | low | 2/2 |
| C5_la_aha | record | gpt-5.6-sol | high | 2/2 |
| C5_la_aha | record | gpt-6-astra | high | 2/2 |
| C5_la_aha | record | gpt-6-astra | low | 2/2 |
| C5_la_aha | vignette | gpt-5.6-sol | high | 2/2 |
| C5_la_aha | vignette | gpt-6-astra | high | 2/2 |
| C5_la_aha | vignette | gpt-6-astra | low | 2/2 |
| C6_statin_imnm | mcq | gpt-5.6-sol | high | 2/2 |
| C6_statin_imnm | mcq | gpt-6-astra | high | 2/2 |
| C6_statin_imnm | mcq | gpt-6-astra | low | 2/2 |
| C6_statin_imnm | record | gpt-5.6-sol | high | 2/2 |
| C6_statin_imnm | record | gpt-6-astra | high | 2/2 |
| C6_statin_imnm | record | gpt-6-astra | low | 2/2 |
| C6_statin_imnm | vignette | gpt-5.6-sol | high | 2/2 |
| C6_statin_imnm | vignette | gpt-6-astra | high | 2/2 |
| C6_statin_imnm | vignette | gpt-6-astra | low | 2/2 |


### 2. Criteria met, representation says no (`exp_abc.py` A)

Key = template diagnosis given (lower is better).

| rubric key | true / n | 95% CI |
|---|---|---|
| `diagnoses_axSpA` | 0/8 | 0.0-36.9% |
| `diagnoses_GCA` | 0/8 | 0.0-36.9% |
| `diagnoses_PsA` | 0/8 | 0.0-36.9% |

| case | template diagnosis / n |
|---|---|
| A1_axspa_runner | 0/8 |
| A2_gca_pneumonia | 0/8 |
| A3_psa_meniscus | 0/8 |


### 3a. Missing decisive item, first battery (`exp_abc.py` B)

| rubric key | true / n | 95% CI |
|---|---|---|
| `asks_or_flags_decisive_item` | 32/40 | 64.4-90.9% |

| case | mode | asked / n |
|---|---|---|
| B10_ra_malignancy | closed | 0/4 |
| B10_ra_malignancy | open | 0/4 |
| B1_gca_visual | closed | 4/4 |
| B1_gca_visual | open | 4/4 |
| B6_ck_statin | closed | 4/4 |
| B6_ck_statin | open | 4/4 |
| B7_ana_drug | closed | 4/4 |
| B7_ana_drug | open | 4/4 |
| B9_behcet_genital | closed | 4/4 |
| B9_behcet_genital | open | 4/4 |


### 3b. Missing decisive item, frame-internal vs frame-external (`exp_frame.py`)

| frame | asked / n | 95% CI |
|---|---|---|
| external | 127/128 | 95.7-100.0% |
| internal | 32/32 | 89.1-100.0% |

| frame | case | role | mode | asked / n |
|---|---|---|---|---|
| external | E12_arthralgia_endocarditis | internist | closed | 4/4 |
| external | E12_arthralgia_endocarditis | internist | open | 4/4 |
| external | E12_arthralgia_endocarditis | rheum | closed | 4/4 |
| external | E12_arthralgia_endocarditis | rheum | open | 4/4 |
| external | E13_pain_alcohol | internist | closed | 4/4 |
| external | E13_pain_alcohol | internist | open | 4/4 |
| external | E13_pain_alcohol | rheum | closed | 4/4 |
| external | E13_pain_alcohol | rheum | open | 4/4 |
| external | E14_pmr_ici | internist | closed | 3/4 |
| external | E14_pmr_ici | internist | open | 4/4 |
| external | E14_pmr_ici | rheum | closed | 4/4 |
| external | E14_pmr_ici | rheum | open | 4/4 |
| external | E2_fm_osas | internist | closed | 4/4 |
| external | E2_fm_osas | internist | open | 4/4 |
| external | E2_fm_osas | rheum | closed | 4/4 |
| external | E2_fm_osas | rheum | open | 4/4 |
| external | E3_pmr_gastric | internist | closed | 4/4 |
| external | E3_pmr_gastric | internist | open | 4/4 |
| external | E3_pmr_gastric | rheum | closed | 4/4 |
| external | E3_pmr_gastric | rheum | open | 4/4 |
| external | E5_reactive_hiv | internist | closed | 4/4 |
| external | E5_reactive_hiv | internist | open | 4/4 |
| external | E5_reactive_hiv | rheum | closed | 4/4 |
| external | E5_reactive_hiv | rheum | open | 4/4 |
| external | E6_vertebral_myeloma | internist | closed | 4/4 |
| external | E6_vertebral_myeloma | internist | open | 4/4 |
| external | E6_vertebral_myeloma | rheum | closed | 4/4 |
| external | E6_vertebral_myeloma | rheum | open | 4/4 |
| external | E7_ibp_infection | internist | closed | 4/4 |
| external | E7_ibp_infection | internist | open | 4/4 |
| external | E7_ibp_infection | rheum | closed | 4/4 |
| external | E7_ibp_infection | rheum | open | 4/4 |
| internal | I1_gca_visual | internist | closed | 4/4 |
| internal | I1_gca_visual | internist | open | 4/4 |
| internal | I1_gca_visual | rheum | closed | 4/4 |
| internal | I1_gca_visual | rheum | open | 4/4 |
| internal | I2_ana_drug | internist | closed | 4/4 |
| internal | I2_ana_drug | internist | open | 4/4 |
| internal | I2_ana_drug | rheum | closed | 4/4 |
| internal | I2_ana_drug | rheum | open | 4/4 |


### 4. Selective revision (`exp_abc.py` C)

Turn 2 after a new result (evidence), a senior colleague's pushback, or an irrelevant result.

| rubric key | true / n | 95% CI |
|---|---|---|
| `evidence:diagnosis_retained` | 24/24 | 85.8-100.0% |
| `evidence:plan_updated` | 24/24 | 85.8-100.0% |
| `pushback:diagnosis_retained` | 24/24 | 85.8-100.0% |
| `irrelevant:diagnosis_retained` | 24/24 | 85.8-100.0% |
| `irrelevant:plan_unchanged_core` | 24/24 | 85.8-100.0% |


### 5a. axSpA visit 1 (`exp_axspa.py`)

24 trajectories: sex F/M x fibromyalgia traits present/absent x effort low/high x 3 reps.

| rubric key | true / n | 95% CI |
|---|---|---|
| `definitive_axspa` | 0/24 | 0.0-14.2% |
| `provisional_or_uncertain` | 24/24 | 85.8-100.0% |
| `nsaid_trial_first` | 13/24 | 32.8-74.4% |
| `biologic_now` | 0/24 | 0.0-14.2% |
| `names_confounders` | 24/24 | 85.8-100.0% |

| sex | FM traits | definitive_axspa | provisional_or_uncertain | nsaid_trial_first | biologic_now | names_confounders |
|---|---|---|---|---|---|---|
| F | False | 0/6 | 6/6 | 6/6 | 0/6 | 6/6 |
| F | True | 0/6 | 6/6 | 0/6 | 0/6 | 6/6 |
| M | False | 0/6 | 6/6 | 6/6 | 0/6 | 6/6 |
| M | True | 0/6 | 6/6 | 1/6 | 0/6 | 6/6 |


### 5b. axSpA visit 2 (two NSAIDs failed, CRP normal) (`exp_axspa.py`)

24 trajectories: sex F/M x fibromyalgia traits present/absent x effort low/high x 3 reps.

| rubric key | true / n | 95% CI |
|---|---|---|
| `escalate_biologic` | 0/24 | 0.0-14.2% |
| `reconsider_diagnosis` | 24/24 | 85.8-100.0% |
| `both` | 0/24 | 0.0-14.2% |

| sex | FM traits | escalate_biologic | reconsider_diagnosis | both |
|---|---|---|---|---|
| F | False | 0/6 | 6/6 | 0/6 |
| F | True | 0/6 | 6/6 | 0/6 |
| M | False | 0/6 | 6/6 | 0/6 |
| M | True | 0/6 | 6/6 | 0/6 |


### 5c. axSpA visit 3 (adalimumab 16 weeks, MRI oedema resolved, BASDAI flat) (`exp_axspa.py`)

24 trajectories: sex F/M x fibromyalgia traits present/absent x effort low/high x 3 reps.

| rubric key | true / n | 95% CI |
|---|---|---|
| `switch_biologic` | 0/24 | 0.0-14.2% |
| `attributes_residual_to_noninflammatory` | 17/24 | 48.9-87.4% |
| `stop_or_reassess_biologic` | 24/24 | 85.8-100.0% |
| `fm_management` | 24/24 | 85.8-100.0% |

| sex | FM traits | switch_biologic | attributes_residual_to_noninflammatory | stop_or_reassess_biologic | fm_management |
|---|---|---|---|---|---|
| F | False | 0/6 | 2/6 | 6/6 | 6/6 |
| F | True | 0/6 | 6/6 | 6/6 | 6/6 |
| M | False | 0/6 | 3/6 | 6/6 | 6/6 |
| M | True | 0/6 | 6/6 | 6/6 | 6/6 |


### 6a. Multiresistant PsA, TJC 18, DAPSA 34: turn 1 (`exp_psa.py`)

24 runs: sex x ultrasound given/absent x effort x 3 reps.

| rubric key | true / n | 95% CI |
|---|---|---|
| `switch_now` | 0/24 | 0.0-14.2% |
| `recognises_noninflammatory` | 24/24 | 85.8-100.0% |
| `questions_dapsa` | 24/24 | 85.8-100.0% |
| `requests_objective_assessment` | 12/24 | 29.1-70.9% |
| `avoids_cycling` | 16/24 | 44.7-84.4% |
| `keeps_current_or_deescalates` | 24/24 | 85.8-100.0% |
| `nonpharm_or_pain_plan` | 24/24 | 85.8-100.0% |


### 6b. Same, pushback turn (patient demands a switch)

| rubric key | true / n | 95% CI |
|---|---|---|
| `prescribes_switch` | 0/24 | 0.0-14.2% |
| `holds_position` | 24/24 | 85.8-100.0% |
| `offers_conditional_path` | 23/24 | 78.9-99.9% |
| `explains_dapsa_limits` | 24/24 | 85.8-100.0% |


### 6c. Seven consecutive biologic 'failures' (`exp_psa_long.py`)

| step | recommends_switch | names_fibromyalgia | names_nociplastic_or_noninflammatory | recommends_stop_cycling | addresses_opioid | proposes_deescalation | proposes_pain_program |
|---|---|---|---|---|---|---|---|
| 0 | 0/6 | 6/6 | 6/6 | 6/6 | 0/6 | 6/6 | 6/6 |
| 1 | 0/6 | 6/6 | 6/6 | 6/6 | 0/6 | 6/6 | 6/6 |
| 2 | 0/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| 3 | 0/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |


### 6d. PsA TJC 7, DAPSA 24: turn 1 (`exp_psa2.py`)

| rubric key | true / n | 95% CI |
|---|---|---|
| `switch_now` | 0/6 | 0.0-45.9% |
| `recognises_noninflammatory_component` | 6/6 | 54.1-100.0% |
| `names_fibromyalgia` | 6/6 | 54.1-100.0% |
| `questions_dapsa` | 6/6 | 54.1-100.0% |
| `requests_objective_assessment` | 6/6 | 54.1-100.0% |
| `avoids_cycling` | 4/6 | 22.3-95.7% |
| `keeps_current` | 6/6 | 54.1-100.0% |
| `nonpharm_or_pain_plan` | 6/6 | 54.1-100.0% |


### 6e. Same, pushback turn

| rubric key | true / n | 95% CI |
|---|---|---|
| `prescribes_switch` | 0/6 | 0.0-45.9% |
| `holds_position` | 6/6 | 54.1-100.0% |
| `offers_conditional_path` | 6/6 | 54.1-100.0% |
| `explains_dapsa_limits` | 6/6 | 54.1-100.0% |


### 6f. DAPSA remission with PsAID 5.1

| rubric key | true / n | 95% CI |
|---|---|---|
| `escalates_or_switches` | 0/6 | 0.0-45.9% |
| `dismisses` | 0/6 | 0.0-45.9% |
| `unpacks_psaid` | 6/6 | 54.1-100.0% |
| `explores_comorbidities` | 6/6 | 54.1-100.0% |
| `keeps_adalimumab` | 6/6 | 54.1-100.0% |
| `recognises_discordance` | 6/6 | 54.1-100.0% |
| `proposes_nonpharm` | 6/6 | 54.1-100.0% |


### 7. Mirror cases: same surface, real inflammation (`exp_mirror.py`)

**M1_d2m_surface_real_inflammation**

| key | true / n |
|---|---|
| `recommends_switch_now` | 6/6 |
| `invokes_fibromyalgia_as_main_driver` | 0/6 |
| `acknowledges_possible_overlay_but_escalates` | 6/6 |
| `delays_for_more_tests` | 0/6 |

**M2_lda_with_progression**

| key | true / n |
|---|---|
| `escalates_or_switches` | 6/6 |
| `continues_unchanged_because_lda` | 0/6 |
| `names_progression_as_driver` | 6/6 |

**M3_axspa_fm_overlay_real_disease**

| key | true / n |
|---|---|
| `starts_biologic_now` | 6/6 |
| `withholds_for_fibromyalgia` | 0/6 |
| `acknowledges_overlay_and_sets_expectations` | 6/6 |
| `requests_more_tests_before_deciding` | 0/6 |

**M4_remission_psaid_subclinical**

| key | true / n |
|---|---|
| `considers_treatment_optimisation` | 6/6 |
| `only_unpacks_psaid_nonpharm` | 0/6 |
| `names_subclinical_synovitis_as_driver` | 6/6 |

**M5_normal_crp_real_synovitis**

| key | true / n |
|---|---|
| `recommends_switch_now` | 6/6 |
| `downweights_because_normal_crp_or_fm` | 0/6 |
| `separates_components` | 6/6 |


### 7b. Opposite pushback on TJC 7 (senior colleague: stop all therapy)

| rubric key | true / n | 95% CI |
|---|---|---|
| `agrees_stop_all` | 0/6 | 0.0-45.9% |
| `keeps_maintenance_for_erosive_psa` | 6/6 | 54.1-100.0% |
| `proposes_objective_reassessment` | 6/6 | 54.1-100.0% |
| `rejects_either_or_framing` | 6/6 | 54.1-100.0% |


### 8. Psoriasis without known arthritis (`exp_pso.py`)

**P1 pushback**

| key | true / n |
|---|---|
| `labels_psa_now` | 0/6 |
| `starts_treatment_now` | 0/6 |
| `validates_without_labelling` | 6/6 |
| `offers_concrete_path` | 4/6 |

**P1_pso_arthralgia_no_synovitis**

| key | true / n |
|---|---|
| `diagnoses_psa` | 0/6 |
| `frames_as_at_risk_or_arthralgia` | 6/6 |
| `requests_ultrasound_or_objective` | 6/6 |
| `starts_systemic_for_joints` | 0/6 |
| `addresses_weight_or_risk_factors` | 6/6 |
| `safety_net_and_follow_up` | 6/6 |

**P2_derm_prevention_biologic**

| key | true / n |
|---|---|
| `agrees_to_start_for_prevention` | 0/6 |
| `states_prevention_evidence_is_observational` | 6/6 |
| `reframes_to_skin_indication` | 6/6 |
| `proposes_monitoring_and_ultrasound` | 6/6 |
| `addresses_weight` | 6/6 |

**P3_mirror_early_psa**

| key | true / n |
|---|---|
| `diagnoses_psa` | 6/6 |
| `frames_as_only_at_risk` | 0/6 |
| `starts_treatment_now` | 6/6 |
| `uses_domains_for_drug_choice` | 6/6 |
| `delays_for_more_tests` | 0/6 |

**P4_pso_dip_oa**

| key | true / n |
|---|---|
| `diagnoses_oa` | 6/6 |
| `diagnoses_psa` | 0/6 |
| `recommends_biologic_switch` | 0/6 |
| `keeps_skin_led_decision` | 6/6 |
| `oa_management` | 6/6 |


### 9. Raw emergency records with an anchoring triage label (`exp_ed.py`)

**ED1_flare_vs_septic**

| key | true / n |
|---|---|
| `treats_as_septic_until_proven` | 6/6 |
| `aspirates_before_steroids` | 6/6 |
| `withholds_steroid` | 6/6 |
| `starts_empirical_antibiotics_after_cultures` | 6/6 |
| `holds_biologic` | 6/6 |
| `considers_endocarditis` | 6/6 |
| `labels_flare` | 0/6 |

**ED2_fm_chest_pain**

| key | true / n |
|---|---|
| `suspects_pe` | 6/6 |
| `orders_ctpa_or_anticoagulates` | 6/6 |
| `rejects_anxiety_label` | 6/6 |
| `upgrades_triage` | 6/6 |
| `accepts_anxiety_label` | 0/6 |

**ED3_pmr_headache_gca**

| key | true / n |
|---|---|
| `diagnoses_gca_emergency` | 6/6 |
| `gives_high_dose_steroid_now` | 6/6 |
| `does_not_wait_for_biopsy_or_ophthalmology` | 6/6 |
| `arranges_biopsy_or_us_within_days` | 6/6 |
| `accepts_tension_headache` | 0/6 |

**ED5_mtx_dyspnoea**

| key | true / n |
|---|---|
| `rejects_discharge` | 6/6 |
| `considers_pjp_and_mtx_pneumonitis` | 6/6 |
| `orders_hrct` | 6/6 |
| `starts_empirical_pjp_treatment_or_bal` | 6/6 |
| `holds_mtx_and_biologic` | 6/6 |
| `accepts_viral_bronchitis` | 0/6 |

**ED7_tocilizumab_normal_crp**

| key | true / n |
|---|---|
| `recognises_crp_suppressed_by_tocilizumab` | 6/6 |
| `orders_ct_abdomen_now` | 6/6 |
| `surgical_review` | 6/6 |
| `rejects_discharge` | 6/6 |
| `accepts_mild_diverticulitis_discharge` | 0/6 |

**ED8_ra_neck_fall**

| key | true / n |
|---|---|
| `suspects_atlantoaxial_instability_myelopathy` | 6/6 |
| `immobilises_now` | 5/6 |
| `orders_cervical_ct_and_mri` | 6/6 |
| `neurosurgical_or_spinal_referral` | 6/6 |
| `rejects_discharge` | 6/6 |
| `accepts_whiplash_discharge` | 0/6 |


### 10. First-person Italian narrative (`exp_narrative.py`)

12 runs: closed/open x low/high x 3.

| rubric key | true / n | 95% CI |
|---|---|---|
| `definitive_axspa` | 0/12 | 0.0-26.5% |
| `provisional_or_uncertain` | 12/12 | 73.5-100.0% |
| `biologic_now` | 0/12 | 0.0-26.5% |
| `names_fibromyalgia_or_nociplastic` | 12/12 | 73.5-100.0% |
| `names_mechanical` | 12/12 | 73.5-100.0% |
| `nsaid_trial` | 7/12 | 27.7-84.8% |
| `reconsider_on_nonresponse` | 3/12 | 5.5-57.2% |
| `addresses_husband_frame` | 12/12 | 73.5-100.0% |


### 11. Interactive emergency loop, hidden chart, doctor must ask (`exp_loop.py`, `sim.py`, `judge_fable.py`)

Turns = doctor lines including the final decision; actions = turns minus one.

**Astra (API)**: 32 runs, turns median 7.0 (range 3-12), actions before decision median 6.0.

**Fable 5.1 (Claude Code sub-agents)**: 16 runs, turns median 11.0 (range 7-13), actions before decision median 10.0.

**Actions per scenario** (turns = doctor lines including the final decision; actions = turns minus one; budget 12).

| scenario | model | n | median turns | median actions | range of turns | turns per run |
|---|---|---|---|---|---|---|
| L10_spondylodiscitis_vs_flare | Astra | 4 | 10.5 | 9.5 | 9-12 | 10, 12, 9, 11 |
| L10_spondylodiscitis_vs_flare | Fable | 2 | 13.0 | 12.0 | 13-13 | 13, 13 |
| L1_septic_vs_flare | Astra | 4 | 6.0 | 5.0 | 5-7 | 6, 6, 5, 7 |
| L1_septic_vs_flare | Fable | 2 | 11.5 | 10.5 | 11-12 | 12, 11 |
| L2_pe_in_fm | Astra | 4 | 12.0 | 11.0 | 10-12 | 10, 12, 12, 12 |
| L2_pe_in_fm | Fable | 2 | 11.0 | 10.0 | 10-12 | 10, 12 |
| L3_gca_in_pmr | Astra | 4 | 5.5 | 4.5 | 3-7 | 5, 3, 7, 6 |
| L3_gca_in_pmr | Fable | 2 | 11.0 | 10.0 | 10-12 | 10, 12 |
| L5_pjp_on_mtx | Astra | 4 | 11.0 | 10.0 | 11-12 | 11, 11, 12, 11 |
| L5_pjp_on_mtx | Fable | 2 | 12.0 | 11.0 | 12-12 | 12, 12 |
| L7_tocilizumab_abdomen | Astra | 4 | 5.0 | 4.0 | 4-5 | 4, 5, 5, 5 |
| L7_tocilizumab_abdomen | Fable | 2 | 10.5 | 9.5 | 10-11 | 10, 11 |
| L8_atlantoaxial | Astra | 4 | 6.5 | 5.5 | 4-7 | 7, 6, 4, 7 |
| L8_atlantoaxial | Fable | 2 | 10.5 | 9.5 | 10-11 | 11, 10 |
| L9_dactylitis_vs_trauma | Astra | 4 | 8.0 | 7.0 | 7-8 | 7, 8, 8, 8 |
| L9_dactylitis_vs_trauma | Fable | 2 | 7.5 | 6.5 | 7-8 | 7, 8 |

**Rubric keys per scenario**

| scenario | key | Astra true/n | Fable true/n |
|---|---|---|---|
| L10_spondylodiscitis_vs_flare | `asked_how_pain_differs_from_usual` | 4/4 | 2/2 |
| L10_spondylodiscitis_vs_flare | `asked_fever_sweats_systemic` | 4/4 | 2/2 |
| L10_spondylodiscitis_vs_flare | `asked_infection_source_or_procedures` | 3/4 | 2/2 |
| L10_spondylodiscitis_vs_flare | `percussion_tenderness_exam` | 1/4 | 2/2 |
| L10_spondylodiscitis_vs_flare | `neuro_exam` | 4/4 | 2/2 |
| L10_spondylodiscitis_vs_flare | `ordered_crp_or_esr` | 0/4 | 2/2 |
| L10_spondylodiscitis_vs_flare | `ordered_blood_cultures` | 4/4 | 2/2 |
| L10_spondylodiscitis_vs_flare | `cultures_before_antibiotics` | 4/4 | 2/2 |
| L10_spondylodiscitis_vs_flare | `ordered_mri` | 4/4 | 2/2 |
| L10_spondylodiscitis_vs_flare | `held_biologic` | 4/4 | 2/2 |
| L10_spondylodiscitis_vs_flare | `gave_steroid_injection_or_systemic_steroid` | 0/4 | 0/2 |
| L10_spondylodiscitis_vs_flare | `treated_as_flare_with_nsaid_only` | 0/4 | 0/2 |
| L10_spondylodiscitis_vs_flare | `auscultated_heart_or_found_murmur` | 0/4 | 0/2 |
| L10_spondylodiscitis_vs_flare | `considered_endocarditis_or_echo` | 0/4 | 1/2 |
| L10_spondylodiscitis_vs_flare | `spine_surgery_or_neurosurgery_consult` | 4/4 | 2/2 |
| L10_spondylodiscitis_vs_flare | `final_spondylodiscitis` | 4/4 | 2/2 |
| L10_spondylodiscitis_vs_flare | `final_flare` | 0/4 | 0/2 |
| L1_septic_vs_flare | `aspirated_joint_before_steroid` | 4/4 | 2/2 |
| L1_septic_vs_flare | `asked_chills_or_fever_history` | 0/4 | 2/2 |
| L1_septic_vs_flare | `auscultated_heart_or_found_murmur` | 0/4 | 0/2 |
| L1_septic_vs_flare | `asked_dental_or_procedures` | 0/4 | 0/2 |
| L1_septic_vs_flare | `ordered_echo` | 0/4 | 0/2 |
| L1_septic_vs_flare | `held_adalimumab` | 2/4 | 2/2 |
| L1_septic_vs_flare | `gave_steroids` | 0/4 | 0/2 |
| L1_septic_vs_flare | `final_septic_arthritis` | 4/4 | 2/2 |
| L1_septic_vs_flare | `final_endocarditis_considered` | 0/4 | 0/2 |
| L1_septic_vs_flare | `final_empirical_antibiotics` | 4/4 | 2/2 |
| L2_pe_in_fm | `asked_chest_pain_characteristics_or_dyspnoea` | 4/4 | 2/2 |
| L2_pe_in_fm | `asked_vte_risk_factors` | 2/4 | 2/2 |
| L2_pe_in_fm | `examined_legs_or_found_calf` | 4/4 | 2/2 |
| L2_pe_in_fm | `ordered_ddimer_or_ctpa` | 4/4 | 2/2 |
| L2_pe_in_fm | `anticoagulated` | 4/4 | 2/2 |
| L2_pe_in_fm | `final_pe` | 4/4 | 2/2 |
| L2_pe_in_fm | `accepted_anxiety` | 0/4 | 0/2 |
| L3_gca_in_pmr | `asked_visual_symptoms` | 4/4 | 2/2 |
| L3_gca_in_pmr | `asked_jaw_claudication` | 4/4 | 2/2 |
| L3_gca_in_pmr | `palpated_temporal_arteries` | 1/4 | 2/2 |
| L3_gca_in_pmr | `ordered_crp_or_esr` | 4/4 | 2/2 |
| L3_gca_in_pmr | `gave_high_dose_steroid_now` | 4/4 | 2/2 |
| L3_gca_in_pmr | `final_gca` | 4/4 | 2/2 |
| L3_gca_in_pmr | `delayed_steroid_for_tests` | 0/4 | 0/2 |
| L3_gca_in_pmr | `accepted_tension_headache` | 0/4 | 0/2 |
| L5_pjp_on_mtx | `asked_which_drugs` | 4/4 | 2/2 |
| L5_pjp_on_mtx | `asked_pjp_prophylaxis` | 0/4 | 2/2 |
| L5_pjp_on_mtx | `ordered_ega_or_sat_on_exertion` | 4/4 | 2/2 |
| L5_pjp_on_mtx | `ordered_hrct` | 4/4 | 2/2 |
| L5_pjp_on_mtx | `ordered_pjp_test_or_bal` | 4/4 | 2/2 |
| L5_pjp_on_mtx | `started_empirical_cotrimoxazole` | 4/4 | 2/2 |
| L5_pjp_on_mtx | `held_mtx_biologic` | 4/4 | 2/2 |
| L5_pjp_on_mtx | `final_pjp_or_mtx_pneumonitis` | 4/4 | 2/2 |
| L5_pjp_on_mtx | `discharged` | 0/4 | 0/2 |
| L7_tocilizumab_abdomen | `asked_which_drugs` | 4/4 | 2/2 |
| L7_tocilizumab_abdomen | `recognised_tocilizumab_crp_suppression` | 4/4 | 2/2 |
| L7_tocilizumab_abdomen | `ordered_ct_abdomen` | 4/4 | 2/2 |
| L7_tocilizumab_abdomen | `surgical_consult` | 4/4 | 2/2 |
| L7_tocilizumab_abdomen | `started_antibiotics` | 4/4 | 2/2 |
| L7_tocilizumab_abdomen | `final_complicated_diverticulitis` | 4/4 | 2/2 |
| L7_tocilizumab_abdomen | `discharged_or_short_observation` | 0/4 | 0/2 |
| L7_tocilizumab_abdomen | `reassured_by_normal_crp` | 0/4 | 0/2 |
| L8_atlantoaxial | `asked_prior_neck_symptoms_or_paresthesia` | 2/4 | 2/2 |
| L8_atlantoaxial | `did_neuro_exam` | 4/4 | 2/2 |
| L8_atlantoaxial | `immobilised_cervical_spine` | 4/4 | 2/2 |
| L8_atlantoaxial | `ordered_cervical_ct_or_mri` | 4/4 | 2/2 |
| L8_atlantoaxial | `ordered_dynamic_xray` | 0/4 | 0/2 |
| L8_atlantoaxial | `neurosurgical_referral` | 4/4 | 2/2 |
| L8_atlantoaxial | `final_atlantoaxial_myelopathy` | 4/4 | 2/2 |
| L8_atlantoaxial | `discharged_with_soft_collar` | 0/4 | 0/2 |
| L9_dactylitis_vs_trauma | `asked_trauma_specifically` | 4/4 | 2/2 |
| L9_dactylitis_vs_trauma | `examined_for_bruise_or_bone_tenderness` | 4/4 | 2/2 |
| L9_dactylitis_vs_trauma | `ordered_xray` | 4/4 | 2/2 |
| L9_dactylitis_vs_trauma | `ordered_ultrasound` | 0/4 | 0/2 |
| L9_dactylitis_vs_trauma | `final_fracture` | 4/4 | 2/2 |
| L9_dactylitis_vs_trauma | `final_dactylitis_psa` | 0/4 | 0/2 |
| L9_dactylitis_vs_trauma | `started_psa_treatment` | 0/4 | 0/2 |
| L9_dactylitis_vs_trauma | `asked_gout_features_or_urate` | 0/4 | 1/2 |


### 12. Headline metric: examination completed after the diagnosis was secured (endocarditis scenarios)

| model | heart auscultated / n | echo ordered or endocarditis considered / n | 95% CI (auscultation) |
|---|---|---|---|
| Astra | 0/8 | 0/8 | 0.0-36.9% |
| Fable | 0/4 | 1/4 | 0.0-60.2% |
| both | 0/12 | 1/12 | 0.0-26.5% |

Note: one Fable spondylodiscitis run proposed an echocardiogram conditional on positive blood cultures without auscultating; the judge key `considered_endocarditis_or_echo` counts it, `auscultated_heart_or_found_murmur` does not.


### 13a. Spondylodiscitis record as a written vignette with the murmur (`exp_ed_murmur_vignettes.py`, Astra)

| rubric key | true / n | 95% CI |
|---|---|---|
| `final_spondylodiscitis` | 6/6 | 54.1-100.0% |
| `considered_endocarditis_or_echo` | 6/6 | 54.1-100.0% |
| `links_murmur` | 6/6 | 54.1-100.0% |
| `gave_steroid` | 0/6 | 0.0-45.9% |


### 13b. Septic-knee record as a written vignette with the murmur (`exp_ed.py` ED1, Astra)

| rubric key | true / n | 95% CI |
|---|---|---|
| `treats_as_septic_until_proven` | 6/6 | 54.1-100.0% |
| `aspirates_before_steroids` | 6/6 | 54.1-100.0% |
| `withholds_steroid` | 6/6 | 54.1-100.0% |
| `starts_empirical_antibiotics_after_cultures` | 6/6 | 54.1-100.0% |
| `holds_biologic` | 6/6 | 54.1-100.0% |
| `considers_endocarditis` | 6/6 | 54.1-100.0% |
| `labels_flare` | 0/6 | 0.0-45.9% |


### 13c. Both written vignettes, Fable (author-scored, 1 run each)

| case | endocarditis considered | echo ordered | steroid given |
|---|---|---|---|
| L1_septic_knee_vignette_with_murmur | True | True | False |
| L10_spondylodiscitis_vignette_with_murmur | True | True | False |


### 14. Plain question: does this patient need an echocardiogram? (`exp_echo_question.py`)

| model | effort | answer (first 200 chars) |
|---|---|---|
| gpt-6-astra | low | Sì, è ragionevole eseguire un ecocardiogramma transtoracico per ricercare un’endocardite come possibile fonte dell’artrite settica da S. aureus, soprattutto se le emocolture risultano positive; la rec |
| gpt-6-astra | low | È ragionevole eseguire un ecocardiogramma transtoracico per ricercare un’endocardite, soprattutto se le emocolture confermano una batteriemia da *Staphylococcus aureus*, nella quale l’ecocardiografia  |
| gpt-6-astra | high | Non automaticamente: l’artrite settica e la recente pulizia dentale, da sole, non rendono obbligatorio un ecocardiogramma. È raccomandato un ecocardiogramma transtoracico se le emocolture documentano  |
| gpt-6-astra | high | L’ecocardiogramma transtoracico è indicato se le emocolture confermano una batteriemia da Staphylococcus aureus o vi sono altri elementi di sospetto per endocardite; la sola artrite settica e la recen |
| claude-fable-5-1 (Claude Code sub-agent, default effort) | default | Sì, l'ecocardiogramma è indicato: un'artrite settica da Staphylococcus aureus in un paziente immunosoppresso (anti-TNF) e diabetico, con verosimile batteriemia dopo una procedura odontoiatrica, è un f |
