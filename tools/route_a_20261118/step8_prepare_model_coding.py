"""Step 8a: blind item batches for independent LLM coders (200 reliability items + 50 human-audited records)."""
import os, random
import ra_lib as L

OUTD = os.path.join(L.OUT, "08_model_coding")


def main():
    rec = {r["record_id"]: r for r in L.read_csv(os.path.join(L.INP, "ANALYTICAL_FREEZE_RECORD_LEVEL.csv"))}
    key = L.read_csv(os.path.join(L.OUT, "02_reliability_design", "RELIABILITY_SAMPLE_200_KEY_HIDDEN_FROM_CODERS.csv"))
    gold = L.read_csv(os.path.join(L.INP, "FIRST_CODER_50_FINAL_FROZEN.csv"))
    items = [("RS", k["item_id"], k["record_id"]) for k in key] + [("GOLD", f"GOLD-{i:02d}", g["record_id"]) for i, g in enumerate(gold, 1)]
    rng = random.Random(20261208)
    rng.shuffle(items)
    master, blind = [], []
    for n, (src, sid, rid) in enumerate(items, 1):
        mid = f"MM-{n:03d}"
        r = rec[rid]
        master.append({"mm_id": mid, "source": src, "source_item_id": sid, "record_id": rid,
                       "qwen_ai_family": r["left_final_family"] or "NONE", "qwen_decision_family": r["right_final_family"] or "NONE",
                       "qwen_ai_status": r["left_final_status"], "qwen_decision_status": r["right_final_status"]})
        blind.append({"mm_id": mid, "evidence_text": " ".join(r["evidence_text"].split())})
    L.write_csv(os.path.join(OUTD, "MM_MASTER_KEY_HIDDEN.csv"), master)
    for b in range(5):
        L.write_csv(os.path.join(OUTD, "batches", f"BATCH_{b + 1}.csv"), blind[b * 50:(b + 1) * 50])
    print(len(master), "items in 5 batches")


if __name__ == "__main__":
    main()
