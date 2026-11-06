# Evaluate the custom script model

## Before training

Agree on the output contract and scoring anchors. Freeze the validation and test source groups. Save baseline outputs using the same input briefs and supplied facts. Record the baseline model identifier and generation settings.

## Human comparison

Present baseline and trained outputs as A/B in random order without model names. Both collaborators score independently before discussing disagreements. Record the actual order in a separate key.

Score each dimension from 1 to 5, with a sentence or exact excerpt explaining the score:

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Brief fit | Misses audience or purpose | Mostly fits with edits | Clearly serves the brief |
| Structure and payoff | Unclear promise or ending | Understandable but uneven | Opening, development, and ending work together |
| Spoken delivery | Difficult to read aloud | Needs some editing | Natural and easy to speak |
| Grounding | Unsupported material claims | Needs factual corrections | Stays within supplied evidence |
| Production usefulness | Hard to turn into the requested video | Some usable parts | Directly useful in the agreed output format |

Measure duration by reading aloud; word count is only an estimate. Record editing time and failure examples. A critical unsupported factual claim or failure to follow the output contract should be reported separately from an average score.

## Report honestly

Include the number and kind of held-out briefs, reviewer disagreements, generation settings, failures, and uncertainty. Agree on a practical improvement threshold before the experiment. Do not select the winner from a single attractive demo or reuse the final test set for prompt or training tuning.

## Review record

| Brief ID | A scores and notes | B scores and notes | Preferred output / tie | Editing required |
| --- | --- | --- | --- | --- |
| | | | | |
