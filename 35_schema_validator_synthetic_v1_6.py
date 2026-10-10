"""Synthetic-only contract checks for candidate bilevel lookup inputs.

No JPC observations or calibrated parameters are contained in this file.
Run: python 35_schema_validator_synthetic_v1_6.py
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import product
from math import isclose, isfinite


class InvalidInput(ValueError):
    pass


def number(value: object, label: str) -> float:
    if type(value) not in (int, float) or not isfinite(value) or value < 0:
        raise InvalidInput(f"{label}: expected finite nonnegative number")
    return float(value)


@dataclass(frozen=True)
class TWDPerEvent:
    value: float

    def __post_init__(self):
        number(self.value, "TWD/event")


@dataclass(frozen=True)
class TWDPerPeriod:
    value: float

    def __post_init__(self):
        number(self.value, "TWD/period")


@dataclass(frozen=True)
class HoursPerPeriod:
    value: float

    def __post_init__(self):
        number(self.value, "hours/period")


@dataclass(frozen=True)
class Option:
    name: str
    a: str
    h: str
    wi: str
    ea_v: str
    mode: str
    final_actor: str
    implementation: TWDPerPeriod
    hours: HoursPerPeriod


@dataclass(frozen=True)
class Case:
    case_id: str
    kappa: str
    events: int
    roles: dict[str, float]
    # P(z, omega) is a joint distribution; omega is hidden from respondents.
    p: dict[tuple[str, str], float]
    # rho is keyed by option, role and visible signal only.
    rho: dict[tuple[str, str, str], dict[str, float]]
    # Each response must have an outcome for each hidden truth in P support.
    outcomes: dict[tuple[str, str, str, str, str], TWDPerEvent]
    options: tuple[Option, ...]
    allowed: set[str]
    # Explicit policy table: (A, kappa) -> (min H, min WI, min EA-V).
    requirements: dict[tuple[str, str], tuple[str, str, str]]
    forbidden_responses: set[tuple[str, str]]


def ordinal(value: object, prefix: str) -> int:
    if not isinstance(value, str) or value not in {f"{prefix}{i}" for i in range(4)}:
        raise InvalidInput(f"invalid {prefix} ordinal key")
    return int(value[1])


def distribution(values: dict, label: str):
    if not values or any(type(v) not in (int, float) or not isfinite(v) or v < 0
                         for v in values.values()):
        raise InvalidInput(f"{label}: invalid probability")
    if not isclose(sum(values.values()), 1.0, rel_tol=0, abs_tol=1e-9):
        raise InvalidInput(f"{label}: probabilities do not sum to one")


def validate_case(case: Case) -> dict[str, TWDPerPeriod]:
    if not case.case_id or case.kappa not in {"low", "medium", "high"}:
        raise InvalidInput("case id or kappa invalid")
    if type(case.events) is not int or case.events < 0:
        raise InvalidInput("event count must be nonnegative integer per period")
    distribution(case.roles, "role weights")
    distribution(case.p, "P(z,omega)")
    if not case.options or len({o.name for o in case.options}) != len(case.options):
        raise InvalidInput("options empty or duplicated")
    if not case.allowed or not case.allowed <= {o.name for o in case.options}:
        raise InvalidInput("policy allowed set invalid")
    result = {}
    for option in case.options:
        a = ordinal(option.a, "A")
        h = ordinal(option.h, "H")
        wi = ordinal(option.wi, "W")
        ea = ordinal(option.ea_v, "E")
        if option.mode not in {"HumanOnly", "AI_to_Human", "Human_to_AI", "Delegated", "Aggregated"}:
            raise InvalidInput("unknown decision mode")
        if option.final_actor not in {"human", "ai"}:
            raise InvalidInput("unknown final actor")
        if a == 3 and option.final_actor == "human":
            raise InvalidInput("A3 contradicts human final authority")
        if option.mode == "Delegated" and option.final_actor != "ai":
            raise InvalidInput("delegation contradicts final actor")
        if not isinstance(option.implementation, TWDPerPeriod) or not isinstance(option.hours, HoursPerPeriod):
            raise InvalidInput("implementation or capacity unit mismatch")
        if option.name not in case.allowed:
            continue
        req = case.requirements.get((option.a, case.kappa))
        if req is None or len(req) != 3:
            raise InvalidInput("UNIDENTIFIED: A x kappa policy threshold missing")
        rh, rw, re = (ordinal(v, prefix) for v, prefix in zip(req, "HWE"))
        if h < rh or wi < rw or ea < re:
            raise InvalidInput("POLICY_INFEASIBLE: threshold failed")
        total = 0.0
        for role, weight in case.roles.items():
            for (signal, truth), p in case.p.items():
                responses = case.rho.get((option.name, role, signal))
                if responses is None:
                    raise InvalidInput("UNIDENTIFIED: role/signal response missing")
                distribution(responses, "rho")
                for response, q in responses.items():
                    if (option.name, response) in case.forbidden_responses and q > 0:
                        raise InvalidInput("POLICY_INFEASIBLE: forbidden response has mass")
                    outcome = case.outcomes.get((option.name, role, signal, truth, response))
                    if not isinstance(outcome, TWDPerEvent):
                        raise InvalidInput("UNIDENTIFIED: outcome missing or wrong unit")
                    total += case.events * weight * p * q * outcome.value
        result[option.name] = TWDPerPeriod(total)
    return result


def validate_portfolio(cases: tuple[Case, ...], budget: TWDPerPeriod,
                       capacity: HoursPerPeriod) -> list[tuple[float, tuple[str, ...]]]:
    if not cases or len({c.case_id for c in cases}) != len(cases):
        raise InvalidInput("cases empty or duplicated")
    if not isinstance(budget, TWDPerPeriod) or not isinstance(capacity, HoursPerPeriod):
        raise InvalidInput("portfolio budget or capacity unit mismatch")
    values = [validate_case(c) for c in cases]
    feasible = []
    for selected in product(*(tuple(o for o in c.options if o.name in c.allowed) for c in cases)):
        if sum(o.implementation.value for o in selected) > budget.value:
            continue
        if sum(o.hours.value for o in selected) > capacity.value:
            continue
        net = sum(values[i][o.name].value - o.implementation.value
                  for i, o in enumerate(selected))
        feasible.append((net, tuple(o.name for o in selected)))
    return sorted(feasible, reverse=True)


def fixture() -> tuple[Case, Case]:
    human = Option("human", "A0", "H3", "W1", "E1", "HumanOnly", "human",
                   TWDPerPeriod(0), HoursPerPeriod(1))
    assist = Option("assist", "A2", "H2", "W2", "E2", "AI_to_Human", "human",
                    TWDPerPeriod(4), HoursPerPeriod(2))

    def make(case_id: str, events: int) -> Case:
        roles = {"reviewer": .6, "escalator": .4}
        p = {("shown", "good"): .7, ("shown", "bad"): .3}
        rho = {(name, role, "shown"): {"check": 1.0}
               for name in ("human", "assist") for role in roles}
        outcomes = {(name, role, "shown", truth, "check"): TWDPerEvent(value)
                    for name, value in (("human", 10), ("assist", 14))
                    for role in roles for truth in ("good", "bad")}
        return Case(case_id, "medium", events, roles, p, rho, outcomes,
                    (human, assist), {"human", "assist"},
                    {("A0", "medium"): ("H1", "W1", "E1"),
                     ("A2", "medium"): ("H2", "W2", "E2")}, set())

    return make("Q8_SYNTHETIC", 2), make("H1_SYNTHETIC", 3)


def run() -> dict:
    cases = fixture()
    observed = validate_portfolio(cases, TWDPerPeriod(8), HoursPerPeriod(4))
    expected = [(62.0, ("assist", "assist")),
                (58.0, ("human", "assist")),
                (54.0, ("assist", "human")),
                (50.0, ("human", "human"))]
    assert len(observed) == len(expected)
    assert all(isclose(a, b, abs_tol=1e-9) and x == y
               for (a, x), (b, y) in zip(observed, expected))
    failures = {
        "role weights": lambda: validate_case(replace(cases[0], roles={"reviewer": .8})),
        "P normalization": lambda: validate_case(replace(cases[0], p={("shown", "good"): .8, ("shown", "bad"): .3})),
        "missing role response": lambda: validate_case(replace(cases[0], rho={k: v for k, v in cases[0].rho.items() if k != ("assist", "escalator", "shown")})),
        "missing truth outcome": lambda: validate_case(replace(cases[0], outcomes={k: v for k, v in cases[0].outcomes.items() if k != ("assist", "reviewer", "shown", "bad", "check")})),
        "forbidden response": lambda: validate_case(replace(cases[0], forbidden_responses={("assist", "check")})),
        "policy threshold": lambda: validate_case(replace(cases[0], requirements={**cases[0].requirements, ("A2", "medium"): ("H3", "W2", "E2")})),
        "missing threshold": lambda: validate_case(replace(cases[0], requirements={("A0", "medium"): ("H1", "W1", "E1")})),
        "A3 human final": lambda: validate_case(replace(cases[0], options=(cases[0].options[0], replace(cases[0].options[1], a="A3")))),
        "ordinal as number": lambda: validate_case(replace(cases[0], options=(cases[0].options[0], replace(cases[0].options[1], a=2)))),
        "wrong outcome unit": lambda: validate_case(replace(cases[0], outcomes={**cases[0].outcomes, ("assist", "reviewer", "shown", "good", "check"): TWDPerPeriod(14)})),
        "wrong budget unit": lambda: validate_portfolio(cases, TWDPerEvent(8), HoursPerPeriod(4)),
        "nonfinite number": lambda: TWDPerPeriod(float("nan")),
    }
    for label, attempt in failures.items():
        try:
            attempt()
        except InvalidInput:
            pass
        else:
            raise AssertionError(f"should reject: {label}")
    assert validate_portfolio(cases, TWDPerPeriod(8), HoursPerPeriod(2)) == [(50.0, ("human", "human"))]
    assert validate_portfolio(cases, TWDPerPeriod(0), HoursPerPeriod(4)) == [(50.0, ("human", "human"))]
    return {"status": "SYNTHETIC_SCHEMA_PARTIAL_PASS", "cases": 2,
            "roles_per_case": 2, "feasible_assignments": observed,
            "rejected": list(failures), "capacity_filter": "PASS", "budget_filter": "PASS"}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), ensure_ascii=False, indent=2))
