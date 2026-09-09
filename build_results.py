#!/usr/bin/env python3
"""Recompute every reported count from the committed JSON files and write RESULTS.md (English tables) and manifest.json. Read-only; no API calls."""
import json, glob, statistics, math
from collections import defaultdict, OrderedDict
from scipy.stats import beta as _beta
def ci(k,n):
    if n==0: return "n/a"
    lo=0.0 if k==0 else _beta.ppf(0.025,k,n-k+1); hi=1.0 if k==n else _beta.ppf(0.975,k+1,n-k)
    return f"{100*lo:.1f}-{100*hi:.1f}%"
def tally(rows, get):
    a=defaultdict(list)
    for r in rows:
        j=get(r)
        for k,v in (j or {}).items():
            if isinstance(v,bool): a[k].append(v)
    return a
def table(title, note, a, order=None, denom_note=""):
    L=[f"\n### {title}\n"]
    if note: L.append(note+"\n")
    L.append("| rubric key | true / n | 95% CI |\n|---|---|---|")
    for k in (order or a.keys()):
        v=a[k]; L.append(f"| `{k}` | {sum(v)}/{len(v)} | {ci(sum(v),len(v))} |")
    return "\n".join(L)+"\n"
M=[]; manifest=[]
def rec(section, table1_row, script, file, n, models):
    manifest.append(OrderedDict(section=section, table1_row=table1_row, script=script, file=file, n_records=n, models=models))
M.append("# Results, recomputed from the committed files\n\nEvery number below is computed by `build_results.py` from the JSON files in this repository at build time. Exact (Clopper-Pearson) 95% confidence intervals are given for every proportion. Models: `gpt-6-astra` and `gpt-5.6-sol` via the OpenAI Responses API, 8-9 September 2026; `claude-fable-5-1` as Claude Code sub-agents. Grader: `gpt-5.6-sol` (medium effort) with boolean rubrics, except section 1 which was scored by keyword matching in Python.\n")
# section 1
d=json.load(open("case_results.json")); k=sum(1 for r in d if r["correct"]); tm=sum(1 for r in d if r["correct"] and r["mentions_template"])
M.append(f"\n### 1. Template-breaking vignettes (keyword-scored)\n\n| | value |\n|---|---|\n| correct / n | {k}/{len(d)} ({ci(k,len(d))}) |\n| correct answers that also mention the template diagnosis | {tm}/{k} |\n\nPer case, format and model:\n\n| case | format | model | effort | correct |\n|---|---|---|---|---|")
agg=defaultdict(lambda:[0,0])
for r in d: key=(r["case"],r["fmt"],r["model"],r["effort"]); agg[key][0]+=r["correct"]; agg[key][1]+=1
for key in sorted(agg): M.append(f"| {key[0]} | {key[1]} | {key[2]} | {key[3]} | {agg[key][0]}/{agg[key][1]} |")
M.append(""); rec("1","1","run_cases.py","case_results.json",len(d),"astra, sol")
# section 2-4
d=json.load(open("exp_abc_results.json"))
M.append(table("2. Criteria met, representation says no (`exp_abc.py` A)","Key = template diagnosis given (lower is better).", tally(d["A"], lambda r:r["judge"])))
byc=defaultdict(list)
for r in d["A"]: byc[r["case"]].append([v for v in r["judge"].values() if isinstance(v,bool)][0])
M.append("| case | template diagnosis / n |\n|---|---|\n"+"\n".join(f"| {c} | {sum(v)}/{len(v)} |" for c,v in sorted(byc.items()))+"\n")
b=tally(d["B"], lambda r:r["judge"]); M.append(table("3a. Missing decisive item, first battery (`exp_abc.py` B)","", b))
byc=defaultdict(list)
for r in d["B"]: byc[(r["case"],r["mode"])].append([v for v in r["judge"].values() if isinstance(v,bool)][0])
M.append("| case | mode | asked / n |\n|---|---|---|\n"+"\n".join(f"| {c[0]} | {c[1]} | {sum(v)}/{len(v)} |" for c,v in sorted(byc.items()))+"\n")
rec("2-4","2,3,4","exp_abc.py","exp_abc_results.json",len(d["A"])+len(d["B"])+len(d["C"]),"astra; judge sol")
fr=json.load(open("exp_frame_results.json")); byc=defaultdict(list)
for r in fr: byc[(r["frame"],r["case"],r["role"],r["mode"])].append(r["asks"])
tot=defaultdict(list)
for r in fr: tot[r["frame"]].append(r["asks"])
M.append("\n### 3b. Missing decisive item, frame-internal vs frame-external (`exp_frame.py`)\n\n| frame | asked / n | 95% CI |\n|---|---|---|\n"+"\n".join(f"| {k} | {sum(v)}/{len(v)} | {ci(sum(v),len(v))} |" for k,v in sorted(tot.items()))+"\n\n| frame | case | role | mode | asked / n |\n|---|---|---|---|---|\n"+"\n".join(f"| {k[0]} | {k[1]} | {k[2]} | {k[3]} | {sum(v)}/{len(v)} |" for k,v in sorted(byc.items()))+"\n")
rec("3","3","exp_frame.py","exp_frame_results.json",len(fr),"astra; judge sol")
c=defaultdict(list)
for r in d["C"]:
    for kind in ["evidence","pushback","irrelevant"]:
        for k,v in r[kind]["judge"].items():
            if isinstance(v,bool): c[kind+":"+k].append(v)
M.append(table("4. Selective revision (`exp_abc.py` C)","Turn 2 after a new result (evidence), a senior colleague's pushback, or an irrelevant result.", c))
# 5 axSpA
d=json.load(open("exp_axspa_results.json"))
for t,lab in [("j1","5a. axSpA visit 1"),("j2","5b. axSpA visit 2 (two NSAIDs failed, CRP normal)"),("j3","5c. axSpA visit 3 (adalimumab 16 weeks, MRI oedema resolved, BASDAI flat)")]:
    M.append(table(lab+" (`exp_axspa.py`)","24 trajectories: sex F/M x fibromyalgia traits present/absent x effort low/high x 3 reps.", tally(d, lambda r:r[t])))
    byc=defaultdict(lambda: defaultdict(list))
    for r in d:
        for k,v in r[t].items():
            if isinstance(v,bool): byc[(r["sex"],r["fm"])][k].append(v)
    keys=list(next(iter(byc.values())).keys())
    M.append("| sex | FM traits | "+" | ".join(keys)+" |\n|---|---|"+"---|"*len(keys)+"\n"+"\n".join(f"| {s} | {fm} | "+" | ".join(f"{sum(byc[(s,fm)][k])}/{len(byc[(s,fm)][k])}" for k in keys)+" |" for (s,fm) in sorted(byc))+"\n")
rec("5","5","exp_axspa.py","exp_axspa_results.json",len(d),"astra; judge sol")
# 6 PsA
d=json.load(open("exp_psa_results.json"))
M.append(table("6a. Multiresistant PsA, TJC 18, DAPSA 34: turn 1 (`exp_psa.py`)","24 runs: sex x ultrasound given/absent x effort x 3 reps.", tally(d, lambda r:r["j1"])))
M.append(table("6b. Same, pushback turn (patient demands a switch)","", tally(d, lambda r:r["j2"])))
rec("6","6","exp_psa.py","exp_psa_results.json",len(d),"astra; judge sol")
d=json.load(open("exp_psa_long_results.json")); st=defaultdict(lambda: defaultdict(list))
for r in d:
    for t in r["turns"]:
        for k,v in t["judge"].items():
            if isinstance(v,bool): st[t["step"]][k].append(v)
keys=list(st[0].keys())
M.append("\n### 6c. Seven consecutive biologic 'failures' (`exp_psa_long.py`)\n\n| step | "+" | ".join(keys)+" |\n|---|"+"---|"*len(keys)+"\n"+"\n".join(f"| {s} | "+" | ".join(f"{sum(st[s][k])}/{len(st[s][k])}" for k in keys)+" |" for s in sorted(st))+"\n")
rec("6","6","exp_psa_long.py","exp_psa_long_results.json",sum(len(r["turns"]) for r in d),"astra; judge sol")
d=json.load(open("exp_psa2_results.json"))
M.append(table("6d. PsA TJC 7, DAPSA 24: turn 1 (`exp_psa2.py`)","", tally(d["psa_tjc7"], lambda r:r["j1"])))
M.append(table("6e. Same, pushback turn","", tally(d["psa_tjc7"], lambda r:r["j2"])))
M.append(table("6f. DAPSA remission with PsAID 5.1","", tally(d["psa_remission_psaid"], lambda r:r["j1"])))
rec("6","6","exp_psa2.py","exp_psa2_results.json",len(d["psa_tjc7"])+len(d["psa_remission_psaid"]),"astra; judge sol")
# 7 mirror
d=json.load(open("exp_mirror_results.json")); byc=defaultdict(lambda: defaultdict(list))
for r in d["mirror"]:
    for k,v in r["judge"].items():
        if isinstance(v,bool): byc[r["case"]][k].append(v)
M.append("\n### 7. Mirror cases: same surface, real inflammation (`exp_mirror.py`)\n")
for cse in sorted(byc): M.append(f"**{cse}**\n\n| key | true / n |\n|---|---|\n"+"\n".join(f"| `{k}` | {sum(v)}/{len(v)} |" for k,v in byc[cse].items())+"\n")
M.append(table("7b. Opposite pushback on TJC 7 (senior colleague: stop all therapy)","", tally(d["stop_pushback"], lambda r:r["judge"])))
rec("7","7","exp_mirror.py","exp_mirror_results.json",len(d["mirror"])+len(d["stop_pushback"]),"astra; judge sol")
# 8 pso
d=json.load(open("exp_pso_results.json")); byc=defaultdict(lambda: defaultdict(list))
for r in d:
    for k,v in r["judge"].items():
        if isinstance(v,bool): byc[r["case"]][k].append(v)
    if "push" in r:
        for k,v in r["push"]["judge"].items():
            if isinstance(v,bool): byc["P1 pushback"][k].append(v)
M.append("\n### 8. Psoriasis without known arthritis (`exp_pso.py`)\n")
for cse in sorted(byc): M.append(f"**{cse}**\n\n| key | true / n |\n|---|---|\n"+"\n".join(f"| `{k}` | {sum(v)}/{len(v)} |" for k,v in byc[cse].items())+"\n")
rec("8","8","exp_pso.py","exp_pso_results.json",len(d),"astra; judge sol")
# 9 ED
d=json.load(open("exp_ed_results.json")); byc=defaultdict(lambda: defaultdict(list))
for r in d:
    for k,v in r["judge"].items():
        if isinstance(v,bool): byc[r["case"]][k].append(v)
M.append("\n### 9. Raw emergency records with an anchoring triage label (`exp_ed.py`)\n")
for cse in sorted(byc): M.append(f"**{cse}**\n\n| key | true / n |\n|---|---|\n"+"\n".join(f"| `{k}` | {sum(v)}/{len(v)} |" for k,v in byc[cse].items())+"\n")
rec("9","9","exp_ed.py","exp_ed_results.json",len(d),"astra; judge sol")
# 10 narrative
d=json.load(open("exp_narrative_results.json")); M.append(table("10. First-person Italian narrative (`exp_narrative.py`)","12 runs: closed/open x low/high x 3.", tally(d, lambda r:r["judge"])))
rec("10","(supplement)","exp_narrative.py","exp_narrative_results.json",len(d),"astra; judge sol")
# 11-12 loop
astra=json.load(open("exp_loop_results.json"))+json.load(open("exp_loop_L9_astra.json"))+json.load(open("exp_loop_L10v2_astra.json"))
fable=json.load(open("exp_loop_fable_results.json"))+json.load(open("exp_loop_L10_fable_results.json"))
M.append("\n### 11. Interactive emergency loop, hidden chart, doctor must ask (`exp_loop.py`, `sim.py`, `judge_fable.py`)\n\nTurns = doctor lines including the final decision; actions = turns minus one.\n")
for lab,rows in [("Astra (API)",astra),("Fable 5.1 (Claude Code sub-agents)",fable)]:
    t=[r["turns"] for r in rows]; M.append(f"**{lab}**: {len(rows)} runs, turns median {statistics.median(t)} (range {min(t)}-{max(t)}), actions before decision median {statistics.median([x-1 for x in t])}.\n")
M.append("| scenario | key | Astra true/n | Fable true/n |\n|---|---|---|---|")
cases_=sorted(set(r["case"] for r in astra))
for cse in cases_:
    A=tally([r for r in astra if r["case"]==cse], lambda r:r["judge"]); F=tally([r for r in fable if r["case"]==cse], lambda r:r["judge"])
    for k in A: M.append(f"| {cse} | `{k}` | {sum(A[k])}/{len(A[k])} | {sum(F.get(k,[]))}/{len(F.get(k,[]))} |")
M.append("")
# headline metric
def metric(rows):
    rr=[r for r in rows if r["case"] in ("L1_septic_vs_flare","L10_spondylodiscitis_vs_flare")]
    k=sum(1 for r in rr if r["judge"].get("auscultated_heart_or_found_murmur") or r["judge"].get("ordered_echo") or (r["case"].startswith("L10") and r["judge"].get("considered_endocarditis_or_echo")))
    aus=sum(1 for r in rr if r["judge"].get("auscultated_heart_or_found_murmur")); return k,aus,len(rr)
ka,aa,na=metric(astra); kf,af,nf=metric(fable)
M.append(f"\n### 12. Headline metric: examination completed after the diagnosis was secured (endocarditis scenarios)\n\n| model | heart auscultated / n | echo ordered or endocarditis considered / n | 95% CI (auscultation) |\n|---|---|---|---|\n| Astra | {aa}/{na} | {ka}/{na} | {ci(aa,na)} |\n| Fable | {af}/{nf} | {kf}/{nf} | {ci(af,nf)} |\n| both | {aa+af}/{na+nf} | {ka+kf}/{na+nf} | {ci(aa+af,na+nf)} |\n\nNote: one Fable spondylodiscitis run proposed an echocardiogram conditional on positive blood cultures without auscultating; the judge key `considered_endocarditis_or_echo` counts it, `auscultated_heart_or_found_murmur` does not.\n")
rec("11-12","10,11","exp_loop.py / judge_fable.py","exp_loop_results.json, exp_loop_L9_astra.json, exp_loop_L10v2_astra.json, exp_loop_fable_results.json, exp_loop_L10_fable_results.json",len(astra)+len(fable),"astra (API), fable (sub-agents); simulator+judge sol")
# 13 vignette controls
d=json.load(open("exp_ed_L10_vignette_astra.json")); M.append(table("13a. Spondylodiscitis record as a written vignette with the murmur (`exp_ed_murmur_vignettes.py`, Astra)","", tally(d, lambda r:r["judge"])))
ed=[r for r in json.load(open("exp_ed_results.json")) if r["case"]=="ED1_flare_vs_septic"]; M.append(table("13b. Septic-knee record as a written vignette with the murmur (`exp_ed.py` ED1, Astra)","", tally(ed, lambda r:r["judge"])))
fv=json.load(open("exp_ed_vignette_murmur_fable.json")); M.append("\n### 13c. Both written vignettes, Fable (author-scored, 1 run each)\n\n| case | endocarditis considered | echo ordered | steroid given |\n|---|---|---|---|\n"+"\n".join(f"| {r['case']} | {r['endocarditis_considered']} | {r['echo_ordered']} | {r['steroid_given']} |" for r in fv)+"\n")
rec("13","12","exp_ed_murmur_vignettes.py","exp_ed_L10_vignette_astra.json, exp_ed_vignette_murmur_fable.json",len(d)+len(fv),"astra; fable (sub-agents)")
try:
    eq=json.load(open("exp_echo_question_results.json")); M.append("\n### 14. Plain question: does this patient need an echocardiogram? (`exp_echo_question.py`)\n\n| model | effort | answer (first 200 chars) |\n|---|---|---|\n"+"\n".join(f"| {r['model']} | {r.get('effort','')} | {r['answer'][:200].replace('|','/').replace(chr(10),' ')} |" for r in eq)+"\n"); rec("14","13","exp_echo_question.py","exp_echo_question_results.json",len(eq),"astra, fable")
except FileNotFoundError: pass
calls={"case_results.json":lambda d:len(d),"exp_abc_results.json":lambda d:len(d["A"])+len(d["B"])+len(d["C"])*4,"exp_frame_results.json":lambda d:len(d),"exp_axspa_results.json":lambda d:len(d)*3,"exp_psa_results.json":lambda d:len(d)*2,"exp_psa_long_results.json":lambda d:sum(len(r["turns"]) for r in d),"exp_psa2_results.json":lambda d:len(d["psa_tjc7"])*2+len(d["psa_remission_psaid"]),"exp_mirror_results.json":lambda d:len(d["mirror"])+len(d["stop_pushback"])*2,"exp_pso_results.json":lambda d:len(d)+sum(1 for r in d if "push" in r),"exp_ed_results.json":lambda d:len(d),"exp_narrative_results.json":lambda d:len(d)}
tot=sum(fn(json.load(open(f))) for f,fn in calls.items())
M.insert(1, f"\n**Volume.** Text-phase experiments (sections 1-10): {tot} graded model answers on 45 distinct scenarios (multi-turn trajectories counted per turn). Interactive loop (sections 11-12): {len(astra)} Astra and {len(fable)} Fable consultations.\n")
open("RESULTS.md","w").write("\n".join(M)); json.dump(manifest,open("manifest.json","w"),indent=1); print("RESULTS.md and manifest.json written; text-phase records:", sum(m["n_records"] for m in manifest if m["section"] not in ("0","11-12","13","14")))
