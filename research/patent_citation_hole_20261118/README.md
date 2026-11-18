# Patent-citation structural-hole test (AI × Decision)

> **Result (2026-11-18): `HOLE_NOT_SUPPORTED`; 0/6 sensitivity checks disagree.** AI and decision patents cite each other about 3× the null expectation, higher than 92–98% of comparable fields. See [RESULTS_20261118.md](RESULTS_20261118.md).

Preregistered test of whether AI patents (CPC G06N) and decision/management patents (CPC G06Q10/04, G06Q10/06) cite each other less than comparable technology fields do. See [PREREGISTRATION.md](PREREGISTRATION.md).

## Data (not in this repository)

PatentsView granted-patent tables from the USPTO Open Data Portal, dataset `pvgpatdis`. Since 2026-06-18 the portal needs a USPTO.gov sign-in. Put these files, unchanged, in a local `inputs_LOCAL/` folder:

- `g_patent.tsv.zip`
- `g_cpc_current.tsv.zip`
- `g_us_patent_citation.tsv.zip`
- optional, for the exploratory H3: `g_assignee_disambiguated.tsv.zip`

## Run

```bash
python -m unittest discover -s tests          # synthetic tests, no data needed
python src/patent_hole.py --inputs inputs_LOCAL --out outputs
```

The script needs Python 3.11 with `numpy` and `pandas`. It reads the zips directly without extracting them, and records the SHA-256 of each input. It writes `outputs/PATENT_HOLE_RESULTS.json`, which contains aggregate counts only.
