#!/usr/bin/env python3
"""Machine-translate (gpt-5.6-sol) every Italian prompt, chart, record and answer used in the study into English, cached in translations_en.json keyed by SHA-1 of the Italian text. Italian originals remain the data of record."""
import json, hashlib, os, sys
from openai import OpenAI
import loop_cases, exp_ed, exp_narrative, exp_loop, exp_ed_murmur_vignettes, exp_echo_question
FABLE=open("fable_doctor_prompt.md").read().split("```text")[1].split("```")[0]
texts=[]
for c in loop_cases.CASES: texts += [c["triage"], c["hidden"]]
for e in exp_ed.E: texts.append(e["rec"])
texts += [exp_ed.SYS, exp_ed.Q, exp_narrative.SYS, exp_narrative.NARR, exp_narrative.CLOSED.split("\n\n")[-1], exp_narrative.OPEN.split("\n\n")[-1], exp_loop.DOC_SYS, exp_loop.SIM_SYS, FABLE, exp_ed_murmur_vignettes.SYS, exp_ed_murmur_vignettes.REC, exp_echo_question.Q]
for r in json.load(open("exp_echo_question_results.json")): texts.append(r["answer"])
for r in json.load(open("exp_ed_vignette_murmur_fable.json")): texts.append(r["answer"])
def key(t): return hashlib.sha1(t.encode()).hexdigest()
cache=json.load(open("translations_en.json")) if os.path.exists("translations_en.json") else {}
if __name__=="__main__":
    c=OpenAI(); n=0
    for t in texts:
        k=key(t)
        if k in cache: continue
        cache[k]=c.responses.create(model="gpt-5.6-sol", reasoning={"effort":"low"}, instructions="Translate the following Italian clinical text into precise British English. Keep every number, unit, drug name, structure, line break and bracketed instruction exactly; translate instructions such as '(solo se chiesto ...)' as '(only if asked ...)'. Return only the translation.", input=t).output_text; n+=1
        json.dump(cache,open("translations_en.json","w"),indent=1,ensure_ascii=False)
    print("translated", n, "new;", len(cache), "cached")
