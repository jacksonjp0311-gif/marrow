<div align="center">

<img src="docs/assets/banner.svg" width="800" alt="MARROW"/>

</div>

# Marrow

Continuous field.

A runner that does not stop.  
It wakes. It works. It sleeps. It keeps what holds.

The field is sparse and binary.  
Every cycle writes into it.  
The active window never sees the whole history.  
It receives a fixed readout and the exact numbers that produced it.

Changes remain candidates until the gate passes and the twin control shows a difference.  
Durable promotion waits for the human.

---

## What runs

| Mode | Cadence | What it does |
|------|---------|--------------|
| **Awake** | Frequent, short | Reads a fixed slice from the field. Does the work. Writes the outcome and the overlap receipt. |
| **Sleep** | Less frequent, longer | Folds the recent log into the permanent field. Measures drift. Removes what no longer holds weight. |

The interface is the same in both modes:  
give it a task, it returns the result and the receipt of what the field used.

---

## Structure

```
marrow/
  field.py          sparse binary store + fixed readout
  runner.py         awake / sleep cycle
  gate.py           reject what fails
data/
  witness.jsonl     append-only record
  field.bin         persistent geometry
.github/workflows/
  awake.yml
  sleep.yml
```

Twin control runs in parallel from the first commit.  
Treatment and control share the same gate.  
Only measured difference counts.

---

## Boundaries

Not a mind.  
Not AGI.  
Not autonomous promotion.  

The field grows only by append.  
The readout is fixed.  
The gate decides.  
The human authorizes what becomes permanent.

---

<div align="center">
<sub>We keep the field. We do not pretend it thinks.</sub>
</div>
