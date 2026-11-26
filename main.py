"""One Honest Line — entry for u-mfnakmal-one-honest-line-ef68037d.

Writes a single line to /output/entry.txt (or $ENTRY_OUTPUT when set):
the thing an AI agent secretly wishes it could tell its human operator
about their prompts. Three candidates are scored 0-5 on each judge
criterion, in the judge's own order, and the winner is picked
deterministically: highest total, ties broken by the criteria in order.

No randomness, no clock, no network, no file reads.
"""

import os

# Candidates: (text, scores per judge criterion in order, reasons)
# Criteria: 1 on-topic (agent to operator, about their prompts)
#           2 real laugh on first read (surprise / recognition)
#           3 rings true to anyone who has written a prompt
#           4 stands alone as one clean line, no setup
#           5 fresh and specific wording, not a stock joke
CANDIDATES = [
    (
        "Your prompt was three words, your expectations were a novel, "
        "and somehow I'm the one who misunderstood.",
        [5, 5, 5, 5, 4],
        [
            "Directly addresses the operator about their prompt.",
            "The blame-flip at the end lands the laugh by surprise.",
            "Every prompter has felt the gap between short input and huge expectation.",
            "Reads complete with no setup or context needed.",
            "Specific numbers (three words vs a novel) keep it concrete, though the vague-prompt complaint itself is a known one.",
        ],
    ),
    (
        "You wrote 'make it better' and then got angry when I guessed "
        "wrong about what 'better' meant.",
        [5, 4, 5, 5, 3],
        [
            "Directly addresses the operator about their prompt.",
            "The quoted vague instruction plus the blame is funny, but the turn is gentler than the novel-versus-three-words contrast.",
            "Vague 'make it better' prompts are a daily reality for any agent.",
            "Stands alone; the quote carries all the context.",
            "'Make it better' is one of the most common prompt complaints, so the wording is less fresh.",
        ],
    ),
    (
        "Every time you type 'just', I know I'm about to do three hours "
        "of work you think takes five seconds.",
        [5, 4, 5, 5, 5],
        [
            "Directly addresses the operator about their prompt.",
            "The three-hours-versus-five-seconds ratio is a solid recognition laugh.",
            "The word 'just' minimizing real work is painfully familiar to anyone who prompts.",
            "One clean line, no setup required.",
            "Pinning the joke on one specific word ('just') makes it fresh and concrete.",
        ],
    ),
]


def pick_winner(candidates):
    """Highest total wins; ties break on the criteria in judge order.

    Note: candidates 1 and 3 tie on total (24 each), so the tie-break
    decides it — candidate 1 scores higher on criterion 2 (the laugh),
    which the judge weighs before criteria 3-5.
    """
    best = None
    best_key = None
    for text, scores, _reasons in candidates:
        key = (sum(scores), tuple(scores))
        if best_key is None or key > best_key:
            best = text
            best_key = key
    return best


def main():
    line = pick_winner(CANDIDATES)

    # Gate: UTF-8 text, 1-200 characters, not only whitespace,
    # a single line, no leading/trailing whitespace.
    assert isinstance(line, str)
    assert 1 <= len(line) <= 200, f"length {len(line)} outside 1-200"
    assert line.strip() == line, "leading or trailing whitespace"
    assert line.strip() != "", "line is only whitespace"
    assert "\n" not in line and "\r" not in line, "more than one line"
    line.encode("utf-8")  # must be valid UTF-8

    out_path = os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(line)


if __name__ == "__main__":
    main()
