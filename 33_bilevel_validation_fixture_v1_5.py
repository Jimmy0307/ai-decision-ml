"""Synthetic-only finite validation fixture for the v1.3 bilevel lookup proposal.

No JPC observation, calibrated parameter, or claimed empirical result appears here.
Run: python 33_bilevel_validation_fixture_v1_5.py
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose


class InvalidInput(ValueError):
    pass


@dataclass(frozen=True)
class Lookup:
    # One event, one period, TWD/event except capital and implementation TWD/period.
    value: float
    loss: float
    op_cost: float
    manager_loss: float


def expected_outcome(
    option: str,
    probability: dict[tuple[str, str], float],
    responses: dict[tuple[str, str], dict[str, float]],
    outcome: dict[tuple[str, str, str, str], Lookup],
) -> Lookup:
    if set(probability) != {("visible", "good"), ("visible", "bad")}:
        raise InvalidInput("P must enumerate visible signal and hidden outcome")
    if any(p < 0 for p in probability.values()) or not isclose(sum(probability.values()), 1):
        raise InvalidInput("P must be nonnegative and normalized")
    result = [0.0, 0.0, 0.0, 0.0]
    for (signal, truth), p in probability.items():
        # The lookup for a respondent has no truth in its key.
        choices = responses.get((option, signal))
        if choices is None or any(v < 0 for v in choices.values()) or not isclose(sum(choices.values()), 1):
            raise InvalidInput("rho missing, negative, or not normalized")
        for response, q in choices.items():
            item = outcome.get((option, signal, truth, response))
            if item is None:
                raise InvalidInput("INSUFFICIENT_IDENTIFIED_INPUTS: outcome lookup missing")
            if any(v < 0 for v in vars(item).values()):
                raise InvalidInput("lookup contains negative cost/value")
            for j, v in enumerate(vars(item).values()):
                result[j] += p * q * v
    return Lookup(*result)


def solve(
    feasible: dict[str, tuple[str, ...]],
    capital: dict[str, float],
    implementation: dict[str, float],
    expected: dict[str, Lookup],
    n_events: float = 1.0,
) -> dict:
    if n_events < 0 or set(feasible) != set(capital):
        raise InvalidInput("period/event inputs incompatible")
    if any(not opts for opts in feasible.values()):
        raise InvalidInput("empty feasible set")
    if any(o not in expected or o not in implementation for opts in feasible.values() for o in opts):
        raise InvalidInput("INSUFFICIENT_IDENTIFIED_INPUTS: option missing")

    def boss(b: str, o: str) -> float:
        t = expected[o]
        return n_events * (t.value - t.loss - t.op_cost) - capital[b]

    def manager(o: str) -> float:
        t = expected[o]
        return -n_events * (t.manager_loss + t.op_cost) - implementation[o]

    # Ties are reported as optimistic/pessimistic Boss bounds, never silently resolved.
    replies = {}
    for b, opts in feasible.items():
        best = max(manager(o) for o in opts)
        replies[b] = tuple(o for o in opts if isclose(manager(o), best))
    optimistic = max(
        ((boss(b, o), b, o) for b, opts in replies.items() for o in opts),
        key=lambda row: row[0],
    )
    pessimistic = max(
        ((min(boss(b, o) for o in opts), b, opts) for b, opts in replies.items()),
        key=lambda row: row[0],
    )
    central = max(
        ((boss(b, o), b, o) for b, opts in feasible.items() for o in opts),
        key=lambda row: row[0],
    )
    return {"bilevel_optimistic": optimistic, "bilevel_pessimistic": pessimistic,
            "central": central, "replies": replies, "gap": central[0] - optimistic[0]}


def synthetic_fixture() -> tuple[dict, dict, dict]:
    p = {("visible", "good"): .7, ("visible", "bad"): .3}
    rho = {
        ("HumanOnly", "visible"): {"review": 1.0},
        ("AIAssist", "visible"): {"accept": .8, "review": .2},
    }
    outcome = {
        ("HumanOnly", "visible", t, "review"): Lookup(10, 2, 2, 2)
        for t in ("good", "bad")
    }
    for truth, accepted in (("good", Lookup(20, 0, 1, 4)),
                            ("bad", Lookup(0, 10, 1, 4))):
        outcome[("AIAssist", "visible", truth, "accept")] = accepted
        outcome[("AIAssist", "visible", truth, "review")] = Lookup(15, 1, 3, 4)
    return p, rho, outcome


def validate() -> dict:
    p, rho, outcome = synthetic_fixture()
    e = {o: expected_outcome(o, p, rho, outcome) for o in ("HumanOnly", "AIAssist")}
    assert e["HumanOnly"] == Lookup(10, 2, 2, 2)
    assert all(isclose(a, b) for a, b in zip(vars(e["AIAssist"]).values(),
                                             (14.2, 2.6, 1.4, 4)))
    result = solve({"b0": ("HumanOnly",), "b1": ("HumanOnly", "AIAssist")},
                   {"b0": 0, "b1": 1}, {"HumanOnly": 0, "AIAssist": 2}, e)
    assert result["bilevel_optimistic"] == (6.0, "b0", "HumanOnly")
    assert isclose(result["central"][0], 9.2)
    assert isclose(result["gap"], 3.2)
    assert result["bilevel_pessimistic"][0] == 6.0

    # Same TWD quantities expressed in thousands: rankings stay fixed.
    k = 1_000
    scaled = {o: Lookup(*(v * k for v in vars(t).values())) for o, t in e.items()}
    scaled_result = solve({"b0": ("HumanOnly",), "b1": ("HumanOnly", "AIAssist")},
                          {"b0": 0, "b1": k},
                          {"HumanOnly": 0, "AIAssist": 2 * k}, scaled)
    assert scaled_result["central"][1:] == result["central"][1:]
    assert scaled_result["bilevel_optimistic"][1:] == result["bilevel_optimistic"][1:]
    assert isclose(scaled_result["gap"], k * result["gap"])

    # A Manager tie must expose different Boss outcomes, not pick a hidden rule.
    tied = {**e, "AIAssist": Lookup(14.2, 2.6, 1.4, 1.0)}
    tie = solve({"b0": ("HumanOnly",), "b1": ("HumanOnly", "AIAssist")},
                {"b0": 0, "b1": 1},
                {"HumanOnly": 0, "AIAssist": 1.6}, tied)
    assert tie["replies"]["b1"] == ("HumanOnly", "AIAssist")
    assert isclose(tie["bilevel_optimistic"][0], 9.2)
    assert isclose(tie["bilevel_pessimistic"][0], 6.0)

    rejected = []
    for label, call in (
        ("non-normalized rho", lambda: expected_outcome(
            "AIAssist", p, {**rho, ("AIAssist", "visible"): {"accept": .9}}, outcome)),
        ("missing outcome", lambda: expected_outcome(
            "AIAssist", p, rho, {k: v for k, v in outcome.items()
                                if k != ("AIAssist", "visible", "bad", "accept")})),
        ("missing option", lambda: solve({"b0": ("Unknown",)}, {"b0": 0},
                                         {"HumanOnly": 0}, e)),
        ("empty feasible set", lambda: solve({"b0": ()}, {"b0": 0},
                                             {"HumanOnly": 0}, e)),
    ):
        try:
            call()
        except InvalidInput:
            rejected.append(label)
        else:
            raise AssertionError("should reject: " + label)
    return {"e_ai": vars(e["AIAssist"]), "solution": result,
            "tie_bounds": [tie["bilevel_pessimistic"][0], tie["bilevel_optimistic"][0]],
            "unit_scaling": "PASS", "rejected": rejected,
            "status": "SYNTHETIC_STRUCTURAL_PASS_ONLY"}


if __name__ == "__main__":
    import json
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
