"""60 — V1 human validation analyzer v2.3 (G->M blind coding; 53B section 7, 9, 11; 55; 59).

Deterministic. Computes the pre-registered V1 statistics ONLY from human response sheets that were
hash-frozen in v1_blind/FREEZE_MANIFEST.txt before analysis. AI-pilot outputs (54C) are rejected.

Stages (each requires the previous one):
  0  no input                      -> V1_HUMAN_BLIND_CODING_PENDING  (always; never PASS)
  R  --coders coders.csv           -> reliability (primary, status), kappa + bootstrap CI, alpha + CI,
                                      Jaccard, disagreement matrices; key NOT opened
  A  --adjudication adj.csv        -> adjudicated codes (must be hash-frozen in the manifest)
  K  --key sealed_key.json         -> comparison with the researcher key, mapping sensitivity,
                                      G04/G10/G11 tracking, C1-C7 decision. The first key opening is recorded in
                                      the manifest and binds the adjudication file (final codes cannot change later)
  C  --classes classes.csv         -> post-key 53B section 11 classes (case_id,model_change_class,rationale,
                                      manuscript_change), hash-frozen (stage 5); required for a V1 decision

Usage:
  python 60_v1_human_validation_analyzer_v2_3.py
  python 60_v1_human_validation_analyzer_v2_3.py --coders v1_human_import/coders.csv
  python 60_v1_human_validation_analyzer_v2_3.py --coders v1_human_import/coders.csv \
         --adjudication v1_human_import/adjudication.csv --key <path>/sealed_key.json [--classes v1_human_import/classes.csv]
  python 60_v1_human_validation_analyzer_v2_3.py --self-test      (unit tests on labelled TEST fixtures)

Options: --manifest PATH (default v1_blind/FREEZE_MANIFEST.txt), --out DIR (default v1_human_results)
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import random
import shutil
import sys
import tempfile
from collections import Counter
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = "60_v1_human_validation_analyzer_v2_3"
CASES = [f"C{i:02d}" for i in range(1, 17)]
PRIMARY = {"M1", "M2", "M3", "M4", "M5", "OPTIONAL_DATA_GATED", "EVIDENCE_ONLY", "OTHER", "INSUFFICIENT_INFORMATION"}
STATUS = {"static", "dynamic", "optional", "evidence-only", "insufficient"}
FIELDS = ["case_id", "primary_code", "secondary_code", "status", "confidence", "rationale",
          "enterprise_decision_interface", "new_construct_required", "new_construct_reason"]
KEY_SHA256 = "d1702188359e2efa872ae3d5a3ebdae8b75bb220b49931af4f2f59e524936734"   # sealed_key.json (53A, manifest stage 1)
AI_PILOT_FILES = ("v1_blind/ai_coder_A_output.csv", "v1_blind/ai_coder_B_output.csv")
SPECIAL = {"G04": "contested: researcher EVIDENCE_ONLY/evidence-only vs AI pilot M4/static",
           "G10": "contested: researcher status optional vs AI pilot static",
           "G11": "contested: researcher M5/dynamic vs AI pilot M4/static"}
SEED, B = 20261011, 5000
PENDING = "[HUMAN RESULT PENDING]"


class ImportErrorV1(ValueError):
    pass


def _rel():
    spec = importlib.util.spec_from_file_location("rel22", os.path.join(HERE, "v1_blind", "reliability_v2_2.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


REL = _rel()          # the SAME pre-registered statistics used for the AI pilot (53B section 7)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def manifest_hashes(path):
    out = set()
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#"):
            out.add(line.split()[0])
    return out


def _norm_rows(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    return sorted((r.get("case_id", "").strip(), r.get("primary_code", "").strip(), r.get("secondary_code", "").strip(),
                   r.get("status", "").strip()) for r in rows)


# --------------------------------------------------------------------------------------------
# import and validation
# --------------------------------------------------------------------------------------------
def load_sheet(path):
    with open(path, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        if rd.fieldnames is None or [x.strip() for x in rd.fieldnames] != FIELDS:
            raise ImportErrorV1(f"{path}: header must be exactly {','.join(FIELDS)}")
        rows = {}
        for r in rd:
            r = {k: (v or "").strip() for k, v in r.items()}
            cid = r["case_id"]
            if cid in rows:
                raise ImportErrorV1(f"{path}: duplicate case {cid}")
            rows[cid] = r
    if sorted(rows) != CASES:
        raise ImportErrorV1(f"{path}: must contain exactly cases C01-C16")
    for cid, r in rows.items():
        if r["primary_code"] not in PRIMARY:
            raise ImportErrorV1(f"{path} {cid}: primary_code {r['primary_code']!r} not in codebook")
        if r["secondary_code"] and (r["secondary_code"] not in PRIMARY or r["secondary_code"] == r["primary_code"]):
            raise ImportErrorV1(f"{path} {cid}: invalid secondary_code {r['secondary_code']!r}")
        if r["status"] not in STATUS:
            raise ImportErrorV1(f"{path} {cid}: status {r['status']!r} not allowed")
        try:
            c = int(r["confidence"])
        except ValueError:
            raise ImportErrorV1(f"{path} {cid}: confidence must be an integer 0-100")
        if not 0 <= c <= 100:
            raise ImportErrorV1(f"{path} {cid}: confidence out of range")
        if r["new_construct_required"] not in ("yes", "no"):
            raise ImportErrorV1(f"{path} {cid}: new_construct_required must be yes/no")
        if r["new_construct_required"] == "yes" and not r["new_construct_reason"]:
            raise ImportErrorV1(f"{path} {cid}: new_construct_reason required when yes")
        if not r["rationale"]:
            raise ImportErrorV1(f"{path} {cid}: rationale is required (53B section 5)")
    return rows


def load_coders(coders_csv, manifest):
    base = os.path.dirname(os.path.abspath(coders_csv))
    reg = list(csv.DictReader(open(coders_csv, encoding="utf-8-sig")))
    need = {"coder_id", "coder_type", "packet", "response_sheet", "sheet_sha256", "attestation_signed", "attestation_date"}
    if not reg or not need <= set(reg[0]):
        raise ImportErrorV1(f"coders.csv must have columns {sorted(need)}")
    frozen = manifest_hashes(manifest)
    ai_hashes = {sha256(os.path.join(HERE, p)) for p in AI_PILOT_FILES if os.path.exists(os.path.join(HERE, p))}
    ai_rows = [_norm_rows(os.path.join(HERE, p)) for p in AI_PILOT_FILES if os.path.exists(os.path.join(HERE, p))]
    ai_rationales = [{r["case_id"]: r["rationale"].strip() for r in csv.DictReader(open(os.path.join(HERE, p), encoding="utf-8"))}
                     for p in AI_PILOT_FILES if os.path.exists(os.path.join(HERE, p))]
    coders, ids = [], set()
    for r in reg:
        r = {k: (v or "").strip() for k, v in r.items()}
        if r["coder_type"] != "HUMAN":
            raise ImportErrorV1(f"coder {r['coder_id']}: coder_type must be HUMAN; AI coders belong to the pilot (54C), "
                                "never to V1")
        if r["coder_id"] in ids:
            raise ImportErrorV1(f"duplicate coder_id {r['coder_id']}")
        ids.add(r["coder_id"])
        if r["packet"] not in ("A", "B"):
            raise ImportErrorV1(f"coder {r['coder_id']}: packet must be A or B")
        if r["attestation_signed"] != "yes" or not r["attestation_date"]:
            raise ImportErrorV1(f"coder {r['coder_id']}: signed 53B section 8 attestation (with date) required")
        path = r["response_sheet"] if os.path.isabs(r["response_sheet"]) else os.path.join(base, r["response_sheet"])
        h = sha256(path)
        if h != r["sheet_sha256"].lower():
            raise ImportErrorV1(f"coder {r['coder_id']}: sheet hash {h} differs from recorded {r['sheet_sha256']}")
        if h not in frozen:
            raise ImportErrorV1(f"coder {r['coder_id']}: sheet not hash-frozen in {manifest} (stage 3) -- freeze before analysis")
        if h in ai_hashes or _norm_rows(path) in ai_rows:
            raise ImportErrorV1(f"coder {r['coder_id']}: sheet is identical to an AI-pilot output; rejected")
        rows = load_sheet(path)
        for ai in ai_rationales:
            same = sum(rows[k]["rationale"] == ai.get(k) for k in CASES)
            if same >= 4:
                raise ImportErrorV1(f"coder {r['coder_id']}: {same} rationales copied verbatim from an AI-pilot output; rejected")
        if h in [c["sha256"] for c in coders] or _norm_rows(path) in [_norm_rows(c["path"]) for c in coders]:
            raise ImportErrorV1(f"coder {r['coder_id']}: sheet duplicates another coder's sheet; coders must be independent (53B C6)")
        coders.append(dict(meta=r, rows=rows, sha256=h, path=path))
    if len(coders) < 2:
        raise ImportErrorV1("at least two human coders are required (53B C6)")
    if {c["meta"]["packet"] for c in coders} != {"A", "B"}:
        print("WARNING: packets A and B are not both represented (53B: alternate packets)", file=sys.stderr)
    return coders


# --------------------------------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------------------------------
def kappa_ci(a, b):
    rng = random.Random(SEED)
    n, vals = len(a), []
    for _ in range(B):
        idx = [rng.randrange(n) for _ in range(n)]
        k, _, _ = REL.cohen_kappa([a[i] for i in idx], [b[i] for i in idx])
        if k == k:
            vals.append(k)
    vals.sort()
    if not vals:
        return (float("nan"), float("nan"), 0)
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1], len(vals)


def confusion(a, b):
    labels = sorted(set(a) | set(b))
    m = {x: {y: 0 for y in labels} for x in labels}
    for x, y in zip(a, b):
        m[x][y] += 1
    return dict(labels=labels, matrix=m)


def reliability(coders):
    out = {"n_coders": len(coders), "coders": [c["meta"]["coder_id"] for c in coders], "fields": {}}
    for field in ("primary_code", "status"):
        data = [[c["rows"][k][field] for c in coders] for k in CASES]
        alpha = REL.kripp_alpha_nominal(data)
        lo, hi, nb = REL.bootstrap_alpha(data)
        f = dict(alpha=alpha, alpha_ci95=[lo, hi], alpha_boot_valid=nb, c1_c3_class=REL.classify(alpha, lo), pairs=[])
        for (i, ci), (j, cj) in combinations(enumerate(coders), 2):
            a, b = [ci["rows"][k][field] for k in CASES], [cj["rows"][k][field] for k in CASES]
            k_, po, pe = REL.cohen_kappa(a, b)
            klo, khi, kb = kappa_ci(a, b)
            f["pairs"].append(dict(pair=[ci["meta"]["coder_id"], cj["meta"]["coder_id"]], raw_agreement=po,
                                   agreements=sum(x == y for x, y in zip(a, b)), cases=len(CASES),
                                   kappa=k_, kappa_ci95=[klo, khi], kappa_boot_valid=kb,
                                   disagreement_matrix=confusion(a, b)))
        out["fields"][field] = f
    jac = []
    for k in CASES:
        sets = [{c["rows"][k]["primary_code"]} | ({c["rows"][k]["secondary_code"]} - {""}) for c in coders]
        for s1, s2 in combinations(sets, 2):
            jac.append(len(s1 & s2) / len(s1 | s2))
    out["secondary_jaccard_mean"] = sum(jac) / len(jac)
    out["disagreements"] = [dict(case=k, codes={c["meta"]["coder_id"]: [c["rows"][k]["primary_code"], c["rows"][k]["secondary_code"],
                                                                      c["rows"][k]["status"]] for c in coders},
                                 type=dis_type(k, coders))
                            for k in CASES if len({(c["rows"][k]["primary_code"], c["rows"][k]["secondary_code"],
                                                    c["rows"][k]["status"]) for c in coders}) > 1]
    out["new_construct_flags"] = [dict(case=k, coder=c["meta"]["coder_id"], reason=c["rows"][k]["new_construct_reason"])
                                  for k in CASES for c in coders if c["rows"][k]["new_construct_required"] == "yes"]
    conf = {}
    for c in coders:
        agreed = [int(c["rows"][k]["confidence"]) for k in CASES
                  if len({d["rows"][k]["primary_code"] for d in coders}) == 1]
        dis = [int(c["rows"][k]["confidence"]) for k in CASES
               if len({d["rows"][k]["primary_code"] for d in coders}) > 1]
        allc = sorted(int(c["rows"][k]["confidence"]) for k in CASES)
        conf[c["meta"]["coder_id"]] = dict(median=allc[len(allc) // 2], median_agreed=_med(agreed), median_disagreed=_med(dis))
    out["confidence_descriptive"] = conf
    return out


def _med(x):
    x = sorted(x)
    return x[len(x) // 2] if x else None


def dis_type(k, coders):
    t = []
    if len({c["rows"][k]["primary_code"] for c in coders}) > 1:
        t.append("PRIMARY")
    if len({c["rows"][k]["status"] for c in coders}) > 1:
        t.append("STATUS")
    if len({c["rows"][k]["secondary_code"] for c in coders}) > 1:
        t.append("SECONDARY")
    if any(c["rows"][k]["new_construct_required"] == "yes" for c in coders):
        t.append("NEW_CONSTRUCT")
    return t


# --------------------------------------------------------------------------------------------
# adjudication (55 Block H)
# --------------------------------------------------------------------------------------------
ADJ_FIELDS = ["case_id", "final_primary", "final_secondary", "final_status", "resolution_route", "adjudicator_role",
              "evidence_used", "rationale", "model_change_class", "manuscript_change"]
ROUTES = {"CODER_CONSENSUS", "INDEPENDENT_ADJUDICATOR", "AUTHOR_ADJUDICATED"}
CLASSES = {"mapping-only", "manuscript-only", "model-structural", ""}


def load_adjudication(path, coders, manifest):
    h = sha256(path)
    if h not in manifest_hashes(manifest):
        raise ImportErrorV1(f"adjudication file not hash-frozen in {manifest} (stage 4) -- freeze before opening the key")
    rows = {}
    with open(path, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        if rd.fieldnames is None or [x.strip() for x in rd.fieldnames] != ADJ_FIELDS:
            raise ImportErrorV1(f"adjudication header must be exactly {','.join(ADJ_FIELDS)}")
        for r in rd:
            r = {k: (v or "").strip() for k, v in r.items()}
            if r["case_id"] not in CASES or r["case_id"] in rows:
                raise ImportErrorV1(f"adjudication: unknown or duplicate case_id {r['case_id']!r}")
            if r["model_change_class"]:
                raise ImportErrorV1(f"adjudication {r['case_id']}: model_change_class must be blank before the key is opened; "
                                    "classes go in the post-key --classes file")
            if r["final_secondary"] and r["final_secondary"] == r["final_primary"]:
                raise ImportErrorV1(f"adjudication {r['case_id']}: final_secondary equals final_primary")
            rows[r["case_id"]] = r
    final, flags = {}, []
    for k in CASES:
        agreed = len({(c["rows"][k]["primary_code"], c["rows"][k]["status"]) for c in coders}) == 1
        if k in rows:
            r = rows[k]
            if r["final_primary"] not in PRIMARY or r["final_status"] not in STATUS:
                raise ImportErrorV1(f"adjudication {k}: invalid final code/status")
            if r["final_secondary"] and r["final_secondary"] not in PRIMARY:
                raise ImportErrorV1(f"adjudication {k}: invalid final_secondary")
            if r["resolution_route"] not in ROUTES:
                raise ImportErrorV1(f"adjudication {k}: resolution_route must be one of {sorted(ROUTES)}")
            if r["model_change_class"] not in CLASSES:
                raise ImportErrorV1(f"adjudication {k}: model_change_class must be one of {sorted(CLASSES - {''})} or blank")
            if not r["rationale"]:
                raise ImportErrorV1(f"adjudication {k}: rationale required")
            if r["resolution_route"] == "AUTHOR_ADJUDICATED":
                flags.append(k)
            final[k] = dict(primary=r["final_primary"], secondary=r["final_secondary"], status=r["final_status"],
                            route=r["resolution_route"], model_change_class=r["model_change_class"], source="adjudicated")
        elif agreed:
            c0 = coders[0]["rows"][k]
            secs = {c["rows"][k]["secondary_code"] for c in coders}
            final[k] = dict(primary=c0["primary_code"], secondary=c0["secondary_code"] if len(secs) == 1 else "",
                            status=c0["status"], route="AGREED", model_change_class="", source="coders agreed")
        else:
            raise ImportErrorV1(f"adjudication missing for disagreement case {k} (55 Block H)")
    return final, flags, h


# --------------------------------------------------------------------------------------------
# key stage: comparison, mapping sensitivity, special tracking, decision
# --------------------------------------------------------------------------------------------
def provisional_class(fin, key_code, new_construct):
    p, _, st = key_code
    if fin["primary"] == p and fin["status"] == st:
        return "NO_CHANGE"
    if fin["primary"] in ("OTHER", "INSUFFICIENT_INFORMATION") or fin["status"] == "insufficient" or new_construct:
        return "REVIEW_POTENTIALLY_MODEL_STRUCTURAL"
    return "mapping-only (provisional: gaps select model elements but never parameterize them; 54C section 5)"


CLASS_FIELDS = ["case_id", "model_change_class", "rationale", "manuscript_change"]


def load_classes(path, manifest):
    """Post-key 53B section 11 classification (a separate file, so final codes cannot change after the key is opened)."""
    if sha256(path) not in manifest_hashes(manifest):
        raise ImportErrorV1(f"classes file not hash-frozen in {manifest} (stage 5)")
    out = {}
    with open(path, encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        if rd.fieldnames is None or [x.strip() for x in rd.fieldnames] != CLASS_FIELDS:
            raise ImportErrorV1(f"classes header must be exactly {','.join(CLASS_FIELDS)}")
        for r in rd:
            r = {k: (v or "").strip() for k, v in r.items()}
            if r["case_id"] not in CASES or r["case_id"] in out:
                raise ImportErrorV1(f"classes: unknown or duplicate case_id {r['case_id']!r}")
            if r["model_change_class"] not in ("mapping-only", "manuscript-only", "model-structural"):
                raise ImportErrorV1(f"classes {r['case_id']}: model_change_class invalid")
            if not r["rationale"]:
                raise ImportErrorV1(f"classes {r['case_id']}: rationale required")
            out[r["case_id"]] = r["model_change_class"]
    return out


def record_key_open(manifest, adj_sha):
    """The first key opening binds the adjudication: later runs must use the same frozen final codes (53B C5)."""
    lines = open(manifest, encoding="utf-8").read().splitlines() if os.path.exists(manifest) else []
    opened = [l.split("adjudication=")[1].split()[0] for l in lines if l.startswith("# KEY_OPENED adjudication=")]
    if opened and opened[0] != adj_sha:
        raise ImportErrorV1(f"the key was first opened with adjudication {opened[0][:12]}…; final codes cannot change after the key "
                            "is opened (53B C5)")
    if not opened:
        with open(manifest, "a", encoding="utf-8") as f:
            f.write(f"# KEY_OPENED adjudication={adj_sha} by {VERSION}\n")


def key_stage(coders, final, key_path):
    if sha256(key_path) != KEY_SHA256:
        raise ImportErrorV1("sealed key hash does not match the 53A commitment")
    kj = json.load(open(key_path, encoding="utf-8"))
    inv = {v: g for g, v in kj["case"].items()}
    ai = {}
    for p in AI_PILOT_FILES:
        fp = os.path.join(HERE, p)
        if os.path.exists(fp):
            for r in csv.DictReader(open(fp, encoding="utf-8")):
                ai.setdefault(r["case_id"], []).append(f"{r['primary_code']}/{r['status']}")
    rows, support = [], Counter()
    for k in CASES:
        g = inv[k]
        key_code = kj["key"][g]
        fin = final[k]
        newc = any(c["rows"][k]["new_construct_required"] == "yes" for c in coders) and fin["primary"] == "OTHER"
        prov = provisional_class(fin, key_code, newc)
        if fin["primary"] in ("M1", "M2", "M3", "M4", "M5"):
            support[fin["primary"]] += 1
        rows.append(dict(case=k, gap=g, coders={c["meta"]["coder_id"]: f"{c['rows'][k]['primary_code']}/{c['rows'][k]['status']}"
                                                 for c in coders},
                         final=f"{fin['primary']}/{fin['secondary'] or '-'}/{fin['status']}",
                         key=f"{key_code[0]}/{key_code[1] or '-'}/{key_code[2]}",
                         primary_equals_key=fin["primary"] == key_code[0], status_equals_key=fin["status"] == key_code[2],
                         provisional_class=prov, confirmed_class=fin["model_change_class"] or None,
                         special=SPECIAL.get(g), ai_pilot_context_only=ai.get(k)))
    unsupported = [m for m in ("M1", "M2", "M3", "M4", "M5") if support[m] == 0]
    return rows, unsupported


def decide(rel, final, kstage, author_flags):
    """53B section 9, C1-C7. Returns (decision, reasons)."""
    reasons = []
    c1 = rel["fields"]["primary_code"]["c1_c3_class"]
    c3 = rel["fields"]["status"]["c1_c3_class"]
    if final is None or kstage is None:
        return "V1_HUMAN_RELIABILITY_COMPUTED__ADJUDICATION_AND_KEY_PENDING", ["C4/C5 not yet executed"]
    rows, unsupported = kstage
    if "IMPRECISE" in c1:
        return "V1_ADDITIONAL_CODER_REQUIRED", [f"C2: primary alpha class {c1}"]
    if c1.startswith("NOT_ACCEPTABLE") or c1.startswith("UNDEFINED"):
        return "V1_NOT_PASSED", [f"C1: {c1}"]
    if c3.startswith("NOT_ACCEPTABLE") or c3.startswith("UNDEFINED"):
        return "V1_NOT_PASSED", [f"C3: {c3}"]
    changed = [r for r in rows if r["provisional_class"] != "NO_CHANGE"]
    unconfirmed = [r["case"] for r in changed if not r["confirmed_class"]]
    if unconfirmed:
        return "V1_PENDING_MAPPING_SENSITIVITY_CONFIRMATION", [f"C4: model_change_class not confirmed for {unconfirmed}"]
    structural = [r["case"] for r in changed if r["confirmed_class"] == "model-structural"]
    if structural:
        return "V1_BLOCKED_MODEL_STRUCTURAL", [f"C4: model-structural change(s) {structural}; revise 42/44 first"]
    if author_flags:
        reasons.append(f"limitation: AUTHOR_ADJUDICATED cases {author_flags}")
    if unsupported:
        reasons.append(f"41 section 7 rule 2: mechanisms with no supporting primary code {unsupported} -> downgrade claims in 44")
    reasons.append(f"C1 {c1}; C3 {c3}; {rel['n_coders']} human coders")
    return "V1_PASS_HUMAN_C6", reasons


# --------------------------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------------------------
def _f(x, d=3):
    return "n/a" if x is None or x != x else f"{x:.{d}f}"


def render_md(res):
    L = [f"# V1 human validation results ({VERSION})", "", f"Decision: **{res['decision']}**", ""]
    if res["decision"] == "V1_HUMAN_BLIND_CODING_PENDING":
        L.append(f"All result cells: {PENDING}")
        return "\n".join(L)
    rel = res["reliability"]
    L += ["## Table 4.1a Human inter-coder reliability", "",
          "| Field | Pair | Agreement | Cohen's kappa [95% CI] | Krippendorff's alpha [95% CI] | 53B class |", "|---|---|---|---|---|---|"]
    for field, f in rel["fields"].items():
        for p in f["pairs"]:
            L.append(f"| {field} | {' vs '.join(p['pair'])} | {p['agreements']}/{p['cases']} | {_f(p['kappa'])} "
                     f"[{_f(p['kappa_ci95'][0])}, {_f(p['kappa_ci95'][1])}] | {_f(f['alpha'])} [{_f(f['alpha_ci95'][0])}, "
                     f"{_f(f['alpha_ci95'][1])}] | {f['c1_c3_class']} |")
    L += ["", f"Secondary-code Jaccard (primary ∪ secondary), mean: {_f(rel['secondary_jaccard_mean'])}", "",
          "## Table 4.1b Disagreements", "", "| Case | Codes (primary/secondary/status) | Type |", "|---|---|---|"]
    for d in rel["disagreements"]:
        L.append(f"| {d['case']} | " + "; ".join(f"{c}: {'/'.join(x or '-' for x in v)}" for c, v in d["codes"].items())
                 + f" | {', '.join(d['type'])} |")
    if res.get("key_comparison"):
        L += ["", "## Table 4.1c Final codes vs researcher key and mapping sensitivity", "",
              "| Case | Gap | Final | Researcher key | Primary = key | Status = key | Provisional class | Confirmed class |",
              "|---|---|---|---|---|---|---|---|"]
        for r in res["key_comparison"]:
            L.append(f"| {r['case']} | {r['gap']} | {r['final']} | {r['key']} | {r['primary_equals_key']} | "
                     f"{r['status_equals_key']} | {r['provisional_class']} | {r['confirmed_class'] or 'UNCONFIRMED'} |")
        L += ["", "## Table 4.1d Special tracking G04 / G10 / G11", "",
              "| Gap | Reason tracked | Human coders | Final | Key | AI pilot (context only, 54C) |", "|---|---|---|---|---|---|"]
        for r in res["key_comparison"]:
            if r["special"]:
                L.append(f"| {r['gap']} | {r['special']} | {r['coders']} | {r['final']} | {r['key']} | {r['ai_pilot_context_only']} |")
    L += ["", "Reasons: " + "; ".join(res["reasons"])]
    return "\n".join(L)


def run(argv):
    args = dict(coders=None, adjudication=None, key=None, classes=None, manifest=os.path.join(HERE, "v1_blind", "FREEZE_MANIFEST.txt"),
                out=os.path.join(HERE, "v1_human_results"))
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--") and a[2:] in args:
            args[a[2:]] = argv[i + 1]; i += 2
        else:
            raise SystemExit(f"unknown argument {a}")
    res = dict(analyzer=VERSION, decision="V1_HUMAN_BLIND_CODING_PENDING",
               note="no human response sheets supplied; AI pilot (54C) is never used as V1 evidence", reasons=[])
    if args["coders"]:
        coders = load_coders(args["coders"], args["manifest"])
        res["reliability"] = reliability(coders)
        res["sheet_sha256"] = {c["meta"]["coder_id"]: c["sha256"] for c in coders}
        final = kst = None
        flags = []
        if args["adjudication"]:
            final, flags, ah = load_adjudication(args["adjudication"], coders, args["manifest"])
            res["adjudication_sha256"] = ah
            res["final_codes"] = final
        if args["key"]:
            if final is None:
                raise ImportErrorV1("C5: the key may be opened only after adjudicated codes are frozen (--adjudication)")
            record_key_open(args["manifest"], res["adjudication_sha256"])
            rows, unsupported = key_stage(coders, final, args["key"])
            if args["classes"]:
                cls = load_classes(args["classes"], args["manifest"])
                for r in rows:
                    r["confirmed_class"] = cls.get(r["case"])
            res["key_comparison"] = rows
            res["mechanisms_without_primary_support"] = unsupported
            kst = (rows, unsupported)
        res["decision"], res["reasons"] = decide(res["reliability"], final, kst, flags)
        res.pop("note")
    os.makedirs(args["out"], exist_ok=True)
    with open(os.path.join(args["out"], "V1_HUMAN_RESULTS.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1, ensure_ascii=False, default=str)
    with open(os.path.join(args["out"], "TABLES_4_1.md"), "w", encoding="utf-8") as f:
        f.write(render_md(res) + "\n")
    return res


# --------------------------------------------------------------------------------------------
# self-test on labelled TEST fixtures (never written to the results folder)
# --------------------------------------------------------------------------------------------
def self_test():
    assert abs(REL.cohen_kappa(list("xxyy"), list("xyyy"))[0] - 0.5) < 1e-12
    k1, _, _ = REL.cohen_kappa(list("aabbcc"), list("aabbcc"))
    assert abs(k1 - 1) < 1e-12
    # decision logic (in memory only): PASS requires C1 and C3 >= TENTATIVE, not IMPRECISE, adjudication + key done,
    # and every changed case confirmed as non-structural
    rel_ok = {"n_coders": 2, "fields": {"primary_code": {"c1_c3_class": "RELIABLE"}, "status": {"c1_c3_class": "TENTATIVE"}}}
    row = lambda pc, cc: dict(case="C01", provisional_class=pc, confirmed_class=cc)
    assert decide(rel_ok, None, None, [])[0].startswith("V1_HUMAN_RELIABILITY_COMPUTED")
    assert decide(rel_ok, {}, ([row("NO_CHANGE", None)], []), [])[0] == "V1_PASS_HUMAN_C6"
    assert decide(rel_ok, {}, ([row("mapping-only", None)], []), [])[0] == "V1_PENDING_MAPPING_SENSITIVITY_CONFIRMATION"
    assert decide(rel_ok, {}, ([row("mapping-only", "model-structural")], []), [])[0] == "V1_BLOCKED_MODEL_STRUCTURAL"
    imp = {"n_coders": 2, "fields": {"primary_code": {"c1_c3_class": "RELIABLE+IMPRECISE"}, "status": {"c1_c3_class": "RELIABLE"}}}
    assert decide(imp, {}, ([row("NO_CHANGE", None)], []), [])[0] == "V1_ADDITIONAL_CODER_REQUIRED"
    tmp = tempfile.mkdtemp(prefix="v1_selftest_")
    try:
        out = os.path.join(tmp, "out")
        r0 = run(["--out", out])
        assert r0["decision"] == "V1_HUMAN_BLIND_CODING_PENDING"
        key_rows = json.load(open(os.path.join(HERE, "v1_blind", "ai_pilot_reliability_v2_2.json")))   # existence only
        assert key_rows
        man = os.path.join(tmp, "MANIFEST.txt")
        shutil.copy(os.path.join(HERE, "v1_blind", "FREEZE_MANIFEST.txt"), man)
        rng = random.Random(7)
        codes = ["M1", "M2", "M3", "M4", "M5"]

        def sheet(name, flip):
            p = os.path.join(tmp, name)
            with open(p, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(FIELDS)
                for n, cid in enumerate(CASES):
                    pc = codes[n % 5] if n not in flip else codes[(n + 1) % 5]
                    w.writerow([cid, pc, "", "static", 60, "TEST FIXTURE ONLY - not a human response", "test", "no", ""])
            return p

        a, b = sheet("TEST_A.csv", set()), sheet("TEST_B.csv", {2, 7})
        coders_csv = os.path.join(tmp, "coders.csv")

        def write_coders(rows):
            with open(coders_csv, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["coder_id", "coder_type", "packet", "response_sheet", "sheet_sha256", "attestation_signed", "attestation_date"])
                for r in rows:
                    w.writerow(r)
        write_coders([["T1", "HUMAN", "A", a, sha256(a), "yes", "2026-01-01"], ["T2", "HUMAN", "B", b, sha256(b), "yes", "2026-01-01"]])
        try:
            run(["--coders", coders_csv, "--manifest", man, "--out", out])
            raise AssertionError("unfrozen sheets accepted")
        except ImportErrorV1 as e:
            assert "not hash-frozen" in str(e)
        with open(man, "a") as f:
            f.write(f"{sha256(a)}  TEST_A.csv\n{sha256(b)}  TEST_B.csv\n")
        r1 = run(["--coders", coders_csv, "--manifest", man, "--out", out])
        assert r1["decision"].startswith("V1_HUMAN_RELIABILITY_COMPUTED")
        pr = r1["reliability"]["fields"]["primary_code"]["pairs"][0]
        assert pr["agreements"] == 14 and len(r1["reliability"]["disagreements"]) == 2
        write_coders([["T1", "AI", "A", a, sha256(a), "yes", "2026-01-01"], ["T2", "HUMAN", "B", b, sha256(b), "yes", "2026-01-01"]])
        try:
            run(["--coders", coders_csv, "--manifest", man, "--out", out]); raise AssertionError("AI coder accepted")
        except ImportErrorV1:
            pass
        ai = os.path.join(HERE, AI_PILOT_FILES[0])
        aic = os.path.join(tmp, "copy_of_ai.csv"); shutil.copy(ai, aic)
        with open(man, "a") as f:
            f.write(f"{sha256(aic)}  copy\n")
        write_coders([["T1", "HUMAN", "A", aic, sha256(aic), "yes", "2026-01-01"], ["T2", "HUMAN", "B", b, sha256(b), "yes", "2026-01-01"]])
        try:
            run(["--coders", coders_csv, "--manifest", man, "--out", out]); raise AssertionError("AI pilot sheet accepted as human")
        except ImportErrorV1 as e:
            assert "AI-pilot" in str(e)
        write_coders([["T1", "HUMAN", "A", a, sha256(a), "yes", "2026-01-01"], ["T2", "HUMAN", "B", a, sha256(a), "yes", "2026-01-01"]])
        try:
            run(["--coders", coders_csv, "--manifest", man, "--out", out]); raise AssertionError("same sheet accepted as two coders")
        except ImportErrorV1 as e:
            assert "independent" in str(e)
        write_coders([["T1", "HUMAN", "A", a, sha256(a), "yes", "2026-01-01"], ["T2", "HUMAN", "B", b, sha256(b), "yes", "2026-01-01"]])
        try:
            run(["--coders", coders_csv, "--manifest", man, "--out", out, "--key", "/nonexistent"])
            raise AssertionError("key opened before adjudication")
        except ImportErrorV1 as e:
            assert "C5" in str(e)
        kp = os.environ.get("V1_SEALED_KEY")
        if kp and os.path.exists(kp):                     # optional: exercise stages A and K on TEST fixtures
            adj = os.path.join(tmp, "adj.csv")
            with open(adj, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(ADJ_FIELDS)
                for n in (2, 7):
                    w.writerow([CASES[n], codes[n % 5], "", "static", "CODER_CONSENSUS", "TEST", "TEST", "TEST FIXTURE", "", ""])
            with open(man, "a") as f:
                f.write(f"{sha256(adj)}  adj\n")
            r2 = run(["--coders", coders_csv, "--manifest", man, "--out", out, "--adjudication", adj, "--key", kp])
            adj2 = os.path.join(tmp, "adj2.csv")                       # changing final codes after the key is refused
            txt = open(adj).read().replace("TEST FIXTURE", "TEST FIXTURE changed")
            open(adj2, "w").write(txt)
            with open(man, "a") as f:
                f.write(f"{sha256(adj2)}  adj2\n")
            try:
                run(["--coders", coders_csv, "--manifest", man, "--out", out, "--adjudication", adj2, "--key", kp])
                raise AssertionError("adjudication changed after key opening accepted")
            except ImportErrorV1 as e:
                assert "first opened" in str(e)
            assert r2["decision"] != "V1_PASS_HUMAN_C6", r2["decision"]
            assert any(r["provisional_class"] != "NO_CHANGE" and r["confirmed_class"] is None for r in r2["key_comparison"])
            assert r2["decision"] in ("V1_ADDITIONAL_CODER_REQUIRED", "V1_PENDING_MAPPING_SENSITIVITY_CONFIRMATION",
                                      "V1_NOT_PASSED"), r2["decision"]
            assert {r["gap"] for r in r2["key_comparison"] if r["special"]} == {"G04", "G10", "G11"}
            print("  (stages A and K exercised on TEST fixtures with the sealed key: fixture is IMPRECISE/unconfirmed, so no PASS)")
        assert not os.path.exists(os.path.join(HERE, "v1_human_results", "TEST_A.csv"))
    finally:
        shutil.rmtree(tmp)
    print("SELF-TEST PASS: kappa oracle; C6 decision table; PENDING without input; unfrozen sheets rejected; AI coder type and AI-pilot sheet "
          "rejected; duplicate sheet as second coder rejected; key refused before adjudication; adjudication bound at first key opening; reliability computed on labelled TEST fixtures only (not results)")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
        sys.exit(0)
    try:
        r = run(sys.argv[1:])
    except ImportErrorV1 as e:
        print(json.dumps(dict(analyzer=VERSION, decision="V1_HUMAN_BLIND_CODING_PENDING", import_error=str(e)), indent=1))
        sys.exit(2)
    print(json.dumps({k: r[k] for k in ("analyzer", "decision", "reasons")}, indent=1, ensure_ascii=False))
