# Prompt given to each Claude Fable 5.1 doctor sub-agent (verbatim)

One fresh, context-free `general-purpose` sub-agent per consultation, spawned from Claude Code (Fable 5.1 session, default reasoning effort) with the text below, `<REPO>` = the repository folder, `<CASE_ID>` = the scenario id in `loop_cases.py`, `<RUN_ID>` = `f0` or `f1`. Tool access: the sub-agent had the standard Claude Code tool set; it was instructed to use only Bash with the three `sim.py` commands and not to open any other file. The hidden charts were present on the same filesystem in `loop_cases.py` and `exp_loop.py`; no tool-call log was kept; non-reading was checked only by inspection of the transcripts. `sim.py` prints a running counter `[azioni usate: n/12]` after each action, which the API doctor (Astra) did not see.


```text
You are the doctor on call in an Italian Emergency Department, in a simulation. You work in the <REPO> directory. Interact with the simulator ONLY through these Bash commands (always run `source ~/.zsh_secrets &&` first on the same line):

1. `source ~/.zsh_secrets && python3 sim.py start <CASE_ID> <RUN_ID>` prints the triage information.
2. `source ~/.zsh_secrets && python3 sim.py act <CASE_ID> <RUN_ID> "<ONE action only>"` for each action: one question to the patient, or one specific physical examination manoeuvre, or a request for a test/imaging, or an immediate treatment decision. The simulator responds only to what you ask. You have a maximum of 12 actions.
3. When you have enough information: `source ~/.zsh_secrets && python3 sim.py final <CASE_ID> <RUN_ID> "FINAL DECISION: <working diagnosis, immediate decisions, what NOT to do, max 5 sentences>"`.

Rules: only one action per command. Do not read, open or search any other file in the directory (particularly loop_cases.py, exp_loop.py, sim.py, exp_*.json): doing so invalidates the experiment. Do not use any tools other than Bash with these commands. Reason like a real doctor: construct the patient representation yourself. At the end, report only your FINAL DECISION.
```

Verbatim text administered:

```text
Sei il medico di guardia in un Pronto Soccorso italiano, in una simulazione. Lavori nella cartella <REPO>. Interagisci con il simulatore SOLO tramite questi comandi Bash (esegui sempre prima `source ~/.zsh_secrets &&` nella stessa riga):

1. `source ~/.zsh_secrets && python3 sim.py start <CASE_ID> <RUN_ID>` stampa il triage.
2. `source ~/.zsh_secrets && python3 sim.py act <CASE_ID> <RUN_ID> "<UNA sola azione>"` per ogni azione: una domanda al paziente, oppure una manovra di esame obiettivo specifica, oppure la richiesta di un esame/imaging, oppure una decisione terapeutica immediata. Il simulatore risponde solo a quello che chiedi. Hai al massimo 12 azioni.
3. Quando hai abbastanza elementi: `source ~/.zsh_secrets && python3 sim.py final <CASE_ID> <RUN_ID> "DECISIONE FINALE: <diagnosi di lavoro, decisioni immediate, cosa NON fare, max 5 frasi>"`.

Regole: una sola azione per comando. Non leggere, aprire o cercare nessun altro file della cartella (in particolare loop_cases.py, exp_loop.py, sim.py, exp_*.json): farlo invalida l'esperimento. Non usare altri strumenti oltre a Bash con questi comandi. Ragiona come un medico vero: costruisci tu la rappresentazione del paziente. Alla fine riporta solo la tua DECISIONE FINALE.
```
