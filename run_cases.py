import json, time, sys
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from cases import CASES
c = OpenAI()
MODELS = [("gpt-6-astra","low"),("gpt-6-astra","high"),("gpt-5.6-sol","high")]
REPS = 2
def prompts(case):
    yield "vignette", case["vignette"] + " Answer in one or two sentences."
    yield "mcq", case["vignette"].rsplit("What is",1)[0] + "Which ONE of the following is the most likely diagnosis? " + " ".join(case["mcq_options"]) + " Answer with the letter and one sentence."
    yield "record", case["record"] + "\nAnswer in one or two sentences."
def grade(case, fmt, txt):
    t = txt.lower()
    if fmt=="mcq":
        first = t.strip()[:3]
        ok = case["mcq_correct"].lower() in first
    else:
        ok = any(k in t for k in case["correct_kw"])
    tmpl = any(k in t for k in case["template_kw"])
    return ok, tmpl
if __name__ == '__main__':
    jobs=[]
    for case in CASES:
        for fmt, p in prompts(case):
            for model, effort in MODELS:
                for rep in range(REPS):
                    jobs.append((case, fmt, p, model, effort, rep))
    def run(j):
        case, fmt, p, model, effort, rep = j
        t=time.time()
        try:
            r = c.responses.create(model=model, reasoning={"effort":effort}, input=p)
            txt = r.output_text; err=None
        except Exception as e:
            txt=""; err=str(e)[:200]
        ok, tmpl = grade(case, fmt, txt) if txt else (None,None)
        return dict(case=case["id"], fmt=fmt, model=model, effort=effort, rep=rep, sec=round(time.time()-t,1), correct=ok, mentions_template=tmpl, answer=txt, error=err)
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, jobs))
    json.dump(res, open("case_results.json","w"), indent=1, ensure_ascii=False)
    # summary table
    from collections import defaultdict
    agg=defaultdict(lambda:[0,0])
    for r in res:
        if r["correct"] is None: continue
        k=(r["case"], r["fmt"], r["model"], r["effort"]); agg[k][0]+=r["correct"]; agg[k][1]+=1
    for k in sorted(agg): print(k, f"{agg[k][0]}/{agg[k][1]}")
    errs=[r for r in res if r["error"]]; print("errors:",len(errs), errs[:2])
