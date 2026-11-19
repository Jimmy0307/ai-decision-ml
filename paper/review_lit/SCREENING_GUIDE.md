# Screening guide (from PROTOCOL.md §2; do not change)

For each record, decide **INCLUDE** or **EXCLUDE** from the title and abstract only.

## INCLUDE only if both hold

**(a)** The study builds or analyses a network from **co-occurrence or affiliation** relations. Examples:
- keyword or co-word co-occurrence;
- co-citation or bibliographic coupling;
- co-authorship;
- patent co-classification or co-assignment (co-patenting);
- project, alliance or consortium co-membership;
- "two items appear together" networks.

**(b)** From that network's **structure**, it draws at least one substantive inference of these kinds:
- a structural hole or Burt-type brokerage (constraint, effective size, non-redundant ties);
- a broker or bridge node, topic or actor (e.g. high betweenness read as bridging or brokering);
- a research gap, missing link, white space or under-connected opportunity derived from the network (e.g. weakly linked clusters, absent links, sparse regions).

## EXCLUDE if any of these applies

- The network uses only **directed flows**: citations used as directed citing→cited links, communication, transactions, trade or supply flows.
- The paper is purely methodological or a tool description with no substantive claim about a field or actors.
- The gap statements are generic ("future research should…") and not derived from network structure.
- Structural holes are studied with survey or ego-network data of real relations, not a co-occurrence network.
- It is not a research study (editorial, erratum), or it is not in English.

## When unsure

If (a) holds and (b) is plausible but not explicit, choose INCLUDE and set confidence to "low".

## Output (CSV, one row per record, header exactly)

`rid,decision,confidence,relation_type,claim_type,reason`

| Column | Values |
|---|---|
| decision | INCLUDE / EXCLUDE |
| confidence | high / low |
| relation_type | coword / cocitation / coauthorship / patent / comembership / other / none |
| claim_type | hole / broker / gap / several / none |
| reason | at most 20 words, no quotation from the abstract |
