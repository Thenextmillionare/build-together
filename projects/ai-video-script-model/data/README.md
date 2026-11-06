# Dataset

**Current state: no training examples collected.**

Start with a narrow, agreed use case. First create or collect a pilot of 20 reviewed pairs to check the collection process. Decide the eventual dataset size after inspecting quality, diversity, and the training approach.

## One example per JSONL line

Each record contains:

| Field | Meaning |
| --- | --- |
| `id` | Unique stable example ID |
| `source_group` | Shared identity for a source video, series, creator, or derived variants that must stay in one split |
| `split` | `train`, `validation`, or `test` |
| `source.kind` | `original`, `licensed`, or `permission` |
| `source.reference` | Source URL, internal reference, or original-author record |
| `source.permission_note` | Basis for using it in this training project |
| `source.approved_for_training` | Boolean approval recorded after source review |
| `review.approved` | Boolean quality approval |
| `review.reviewer` | Person who approved the pair |
| `input` | Structured creator brief; fields shown in the example |
| `target.script` | Desired approved script |

See [the synthetic format example](../examples/format-example.jsonl). It is not collected training data. Only approved examples belong in `data/*.jsonl`; keep collection notes separate.

## Collection workflow

1. Agree on the video format and output contract with the mentor.
2. Choose original work, appropriately licensed examples, or examples with permission. Record the basis rather than treating an accessible script as approved.
3. Pair each script with a realistic brief. If reconstructing a brief, mark this in the collection notes and have the mentor check that it does not give away the target script.
4. Remove irrelevant metadata and check factual inputs, spoken quality, and fit to the brief.
5. Keep related scripts, rewrites, translations, and generated variants in the same `source_group`.
6. Assign each group to a split. Keep validation for development and test for the final comparison; never train on either.
7. Review the pair and run the validator. Commit the approved records and link the commit from the collection issue.

For a small pilot, agree on a modest held-out set rather than mechanically splitting by percentage. The test set must contain enough distinct briefs to support useful comparison. Do not revise training examples in response to test results and then report the same test as an untouched evaluation.

## What validation can check

The validator checks required fields, approval flags, duplicate IDs and scripts, and groups crossing splits. It cannot verify permission, detect all paraphrases, judge script quality, or prove facts. Human review remains part of dataset approval.

Use `--require-splits` before a training handoff to require nonempty train, validation, and test sets.
