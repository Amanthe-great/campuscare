# CampusCare

Small campus helper built with Python basics (conditions, loops, files, dictionaries) plus a Streamlit page so it can be demoed.

It has two tools:

1. **Symptom helper** — matches words in a sentence to a local rule file and suggests next steps. It does not diagnose.
2. **Mentor flag** — reads a student CSV and marks anyone with attendance below 75 or average marks below 40.

## Why this project

Hackathon reviewers ask for a problem, a working demo, and code you can explain. This repo is intentionally small so a first-year student can walk through every line.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL Streamlit prints (usually http://localhost:8501).

Try these inputs on the Symptom tab:

- `fever and headache`
- `cannot sleep before exam`
- `tooth pain` (unknown word; it is saved)

## How the symptom checker works

1. `data/symptom_rules.json` stores a keyword and three fields: category, advice, and when to see a doctor.
2. `symptom_checker.py` lowercases the sentence and checks `if keyword in sentence`.
3. If two keywords match, both are shown. Extra matches are ignored so the answer stays short.
4. If nothing matches, the sentence is appended to `data/unknown_queries.txt`.

Example: `fever and headache` matches `fever` and `headache`. No library and no training step.

## How the mentor flag works

`data/students.csv` has name, attendance, math, physics, python.

For each row, `risk_analyzer.py`:

- converts marks to numbers
- average = (math + physics + python) / 3
- flags the student if attendance < 75 or average < 40
- stores the reason in a list so the table can explain the flag

## What I would say in a shortlist interview

- Problem: students delay clinic visits, and mentors see low attendance too late.
- Solution: two transparent rules, not a black-box model.
- My part: rule file, matching function, CSV loop, Streamlit tabs.
- Limit: keyword match misses spelling mistakes and is not medical advice.
- Next step: replace the keyword list with a small text classifier, and pull attendance from the college portal.

## Project layout

```
app.py                Streamlit screens
symptom_checker.py    keyword match
risk_analyzer.py      CSV rules
data/symptom_rules.json
data/students.csv
```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
