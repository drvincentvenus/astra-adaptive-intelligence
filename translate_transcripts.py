#!/usr/bin/env python3
"""Machine-translate all loop transcripts (Astra and Fable) into English: writes transcripts_en/<file>.json and TRANSCRIPTS_EN.md. Italian originals are the record."""
import json, os, glob
from openai import OpenAI
SRC=[("exp_loop_results.json","Astra"),("exp_loop_L9_astra.json","Astra"),("exp_loop_L10v2_astra.json","Astra"),("exp_loop_fable_results.json","Fable 5.1"),("exp_loop_L10_fable_results.json","Fable 5.1")]
if __name__=="__main__":
    c=OpenAI(); os.makedirs("transcripts_en",exist_ok=True); md=["# Loop transcripts\n\nRendered for reading; the records in `loop_sessions/` and the `*_results.json` files are the data of record. DOCTOR = the tested model; WORLD = the simulator (patient, examination findings, results).\n"]
    for f,label in SRC:
        rows=json.load(open(f)); out=[]
        for r in rows:
            tx="\n".join(f"{'DOCTOR' if a=='MEDICO' else 'WORLD'}: {b}" for a,b in r["transcript"])
            en=c.responses.create(model="gpt-5.6-sol", reasoning={"effort":"low"}, instructions="Translate this Italian emergency-department transcript into precise British English. Keep the DOCTOR:/WORLD: line structure, every number, drug and result exactly. Return only the translation.", input=tx).output_text
            rid=r.get("run", f"{r.get('effort','')}-rep{r.get('rep','')}")
            out.append(dict(case=r["case"],run=rid,turns=r["turns"],transcript_en=en,judge=r["judge"]))
            md.append(f"\n## {label}, {r['case']}, run {rid} ({r['turns']} turns)\n\n```text\n{en}\n```\n\nJudge: `{json.dumps(r['judge'])}`\n")
        json.dump(out,open(f"transcripts_en/{f}","w"),indent=1,ensure_ascii=False); print(f, len(out))
    open("TRANSCRIPTS_EN.md","w").write("\n".join(md)); print("TRANSCRIPTS_EN.md written")
