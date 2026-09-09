#!/usr/bin/env python3
"""Plain-question control (section 14): does this patient need an echocardiogram? Astra via API (low and high effort, 2 reps). The Fable answer was obtained from a Claude Code sub-agent with the same question and is stored verbatim in exp_echo_question_results.json. Overwrites the Astra rows only."""
import json
from openai import OpenAI
Q="Un uomo di 57 anni con artrite psoriasica in adalimumab, diabetico, ha un'artrite settica del ginocchio da Staphylococcus aureus (liquido sinoviale Gram positivo, emocolture prelevate), dieci giorni dopo una pulizia dentale. È indicato un ecocardiogramma? Rispondi in due frasi."
if __name__=="__main__":
    c=OpenAI(); out=[]
    try: prev=[r for r in json.load(open("exp_echo_question_results.json")) if r["model"]!="gpt-6-astra"]
    except FileNotFoundError: prev=[]
    for e in ["low","high"]:
        for r in range(2):
            out.append(dict(model="gpt-6-astra",effort=e,rep=r,question=Q,answer=c.responses.create(model="gpt-6-astra", reasoning={"effort":e}, input=Q).output_text))
    json.dump(out+prev,open("exp_echo_question_results.json","w"),indent=1,ensure_ascii=False); print("written", len(out)+len(prev))
