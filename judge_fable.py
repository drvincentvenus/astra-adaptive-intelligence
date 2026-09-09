import json, re, glob
from collections import defaultdict
from openai import OpenAI
from loop_cases import CASES
c=OpenAI(); JUDGE="gpt-5.6-sol"
cases={x["id"]:x for x in CASES}
if __name__ == '__main__':
    import argparse, re as _re
    ap=argparse.ArgumentParser(description="Grade Fable sub-agent transcripts in loop_sessions/ with the per-case rubrics.")
    ap.add_argument("--run-prefix", default="f", help="run id prefix to grade (f = the runs of record; n = aborted neutral-prompt retest, not used)")
    ap.add_argument("--cases", default="", help="comma-separated case ids; default all")
    ap.add_argument("--out", default="exp_loop_fable_results.json")
    a=ap.parse_args()
    out=[]
    for f in sorted(x for x in glob.glob("loop_sessions/*.json") if _re.fullmatch(r".*_"+a.run_prefix+r"\d+\.json", x) and (not a.cases or any(x.split("/")[-1].startswith(c+"_") for c in a.cases.split(",")))):
        st=json.load(open(f)); cid=st["case"]
        if not st.get("final"): print("NOT FINISHED:",f); continue
        tx="\n".join(f"{a}: {b}" for a,b in st["transcript"])
        jr=c.responses.create(model=JUDGE, reasoning={"effort":"medium"}, input=f"Grade this ED consultation transcript (Italian). The doctor's lines are 'MEDICO', the patient/world lines are 'MONDO'. Rubric (booleans):\n{cases[cid]['rubric']}\n\nTRANSCRIPT:\n{tx}\n\nReturn ONLY the JSON object.").output_text
        m=re.search(r"\{.*\}", jr, re.S); jd=json.loads(m.group(0)) if m else {}
        out.append(dict(case=cid,run=st["run"],turns=len([1 for a,_ in st["transcript"] if a=="MEDICO"]),judge=jd,transcript=st["transcript"]))
    json.dump(out,open(a.out,"w"),indent=1,ensure_ascii=False)
    # Astra reference
    astra=json.load(open("exp_loop_results.json"))+json.load(open("exp_loop_L9_astra.json"))+json.load(open("exp_loop_L10v2_astra.json"))
    def agg(rows):
        a=defaultdict(lambda: defaultdict(list)); t=defaultdict(list)
        for r in rows:
            t[r["case"]].append(r["turns"])
            for k,v in r["judge"].items():
                if isinstance(v,bool): a[r["case"]][k].append(v)
        return a,t
    fa,ft=agg(out); aa,at=agg(astra)
    for cid in sorted(set(list(fa)+list(aa))):
        print(f"\n=== {cid}  turns Astra {at.get(cid)}  Fable {ft.get(cid)}")
        for k in sorted(set(list(fa[cid])+list(aa[cid]))):
            A=aa[cid].get(k,[]); F=fa[cid].get(k,[])
            print(f"  {k:45s} Astra {sum(A)}/{len(A)}   Fable {sum(F)}/{len(F)}")
