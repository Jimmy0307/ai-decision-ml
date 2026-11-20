# Coding guide (from PROTOCOL.md §3; do not change)

Code each **included** study from its title and abstract. Use open-access full text only if you can actually open it; most coders will work from abstracts, so set E = abstract. Code what the text shows. When the text does not let you tell, use **unclear**. Do not guess.

## Descriptive variables

| Variable | Values |
|---|---|
| D1 relation type | coword · cocitation · coauthorship · patent · comembership · other · mixed |
| D2 claim type | hole (Burt structural hole) · broker (bridge or broker node, topic or actor, e.g. via betweenness) · gap (research gap, missing link, white space, opportunity) · several |
| D3 measure named | constraint (Burt constraint or effective size) · betweenness (betweenness or brokerage roles) · absence (absent, weak or sparse links between clusters) · position (cluster or map position, density, centrality without brokerage) · none |

## Failure-mode indicators (yes / no / unclear)

**F1 Projection read as flow or structure**
- **yes:** the study treats co-occurrence or projected ties as relations through which knowledge or information passes, or as relations that create brokerage or control positions for the nodes. Examples: "keywords bridging communities enable knowledge flow"; "authors in structural holes control information".
- **no:** it treats the network only as a descriptive map of topical proximity and makes no flow or brokerage reading.

**F2 Constraint or betweenness on a co-occurrence network**
- **yes:** a Burt measure (constraint, effective size, structural holes index) or betweenness is computed on a co-occurrence or projected network **and** read as brokerage, a hole or a bridge.
- **no:** no such measure is used, or it is used only descriptively without that reading.

**F3 Absence read as a gap without a baseline**
- **yes:** low, weak or absent co-occurrence (sparse regions, unconnected clusters, few links) is read as a research gap, hole or opportunity, **and** the abstract reports no null model, expected count, randomisation or comparison set against which the sparsity is judged.
- **no:** a baseline or null is mentioned, or no absence-based inference is made.

**F4 Label validity unreported**
- **yes:** node labels (keywords, topics, classes, author identities) come from automated extraction, topic models, LLMs, author keywords or manual classification, **and** no reliability, validation or disambiguation step is reported.
- **no:** a validation step is reported.
- **unclear:** the label source cannot be told.

**V Validation of the claim**
- **yes:** the claimed hole, broker or gap is checked against independent evidence (later outcomes, flow data, expert validation, out-of-sample prediction).
- **no:** no such check.

**E Evidence basis:** abstract · fulltext

## Output (CSV; header exactly)

`rid,D1,D2,D3,F1,F2,F3,F4,V,E,note`

- `note`: at most 20 words. Never quote the abstract.
- Use lower-case values exactly as listed above.
