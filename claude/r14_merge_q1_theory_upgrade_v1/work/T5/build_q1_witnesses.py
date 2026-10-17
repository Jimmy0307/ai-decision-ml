"""Integrator T5 build tool: assembles Q/q1_theory_witnesses.py (standalone) from Q/witness_parts/*.py.
Deterministic text transform; the generated file has no imports from witness_parts or 51."""
import pathlib, re, sys

Q = pathlib.Path(__file__).resolve().parents[2]
PARTS = [("T1", "w_dl_gov.py"), ("T2", "w_mono_rob_miss.py"), ("T3", "w_voi.py"), ("T4", "w_mech.py")]


def strip(text, agent):
    text = text.replace("\r\n", "\n")
    i = text.find('\nif __name__ == "__main__":')
    if i >= 0:
        text = text[:i] + "\n"
    text = re.sub(r"\nALL_WDG = \[[^\]]*\]\n", "\n", text)
    text = re.sub(r"\nALL_T2 = \[[^\]]*\]\n", "\n", text)
    assert text.startswith('"""'), agent
    text = "_DOC_%s = " % agent + text
    if agent == "T1":
        n = text.count("def witness_W5():")
        assert n == 1
        text = text.replace("def witness_W5():", "def witness_W_DL_AL3():")
    return text


def main():
    harness = (Q / "work" / "T5" / "harness_q1.py").read_text(encoding="utf-8").replace("\r\n", "\n")
    head, tail = harness.split("# @@PARTS@@\n")
    body = []
    for agent, fn in PARTS:
        src = (Q / "witness_parts" / fn).read_text(encoding="utf-8")
        body.append("# " + "=" * 100 + "\n# PART %s -- copied verbatim from witness_parts/%s (main block and ALL_* list removed%s)\n# "
                    % (agent, fn, "; witness_W5 renamed witness_W_DL_AL3" if agent == "T1" else "") + "=" * 100 + "\n")
        body.append(strip(src, agent))
    out = head + "\n".join(body) + "\n\n" + tail
    assert "import w_" not in out and "from w_" not in out
    (Q / "q1_theory_witnesses.py").write_text(out, encoding="utf-8", newline="\n")
    print("written", len(out.splitlines()), "lines")


if __name__ == "__main__":
    main()
