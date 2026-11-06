# AI Video Script Model

**Owner:** Aravinth  
**Collaborator:** @khaileeness-lang  
**Stage:** Dataset design and collection  
**Goal:** Train a custom model on example scripts for AI-generated videos.

[Dataset guide](data/README.md) · [Collection sheet](data/COLLECTION_TEMPLATE.md) · [Evaluation](EVALUATION.md) · [Experiment template](experiments/TEMPLATE.md)

## What is decided

- This is a custom model training project.
- We need to create or collect the dataset first.
- Both collaborators will review examples and model outputs in this repository.

## Decisions to make together

1. Choose one initial video format, audience, language, and duration range.
2. Define whether the target output is narration, scene directions, or both.
3. Agree on sources for usable examples and the qualities we want to teach.
4. Select a base model and training method after the output contract and data are clear.

Proposed first input: a creator brief containing audience, objective, platform, duration, tone, and supplied facts. Proposed first target: an approved script. These are starting contracts, not a final dataset specification.

## First useful milestone: an approved dataset pilot

- [ ] Agree on the narrow initial use case and output format.
- [ ] Create or collect a pilot of 20 reviewed brief/script pairs. This is a workflow pilot, not a claim that 20 examples are enough to train a useful model.
- [ ] Record provenance and permission for every example.
- [ ] Assign related examples to a single split before training.
- [ ] Validate the data and have the mentor review the pilot.
- [ ] Agree on the next collection target based on coverage and quality.

## Build sequence

| Stage | Deliverable | Exit condition |
| --- | --- | --- |
| Define | Output contract and rubric | Both collaborators agree on what a good script looks like |
| Collect | Reviewed pilot dataset | Examples pass validation and human review |
| Baseline | Outputs from an untrained baseline | Saved against fixed validation briefs |
| Train | First custom model experiment | Configuration, data version, cost, and results recorded |
| Evaluate | Blind comparison on untouched test briefs | Improvement or failure documented with examples |
| Integrate | Script generation entry point | Only after useful quality is demonstrated |

Training from scratch versus adapting a pretrained model remains an explicit decision. No training service, paid run, or model has been selected or launched.

## Existing starting point

An earlier Script Lab prototype exists locally in the parent workspace at `script-bot/`. It compiles prompts and supports baseline comparisons; it is not a trained custom model. Its brief fields and evaluation approach can inform this project. It has not been imported into this project folder.

## Validate locally

Python 3.11+; no external packages required.

```sh
python3 projects/ai-video-script-model/scripts/validate_dataset.py --data-dir projects/ai-video-script-model/data
python3 -m unittest discover -s projects/ai-video-script-model/tests -v
```

The validator fails when no actual data exists. The file under `examples/` is a synthetic format illustration and is deliberately excluded from training data.

## Progress and discussion

Use Task issues for work, Work log issues for collection sessions and experiments, and Mentor review issues for dataset or output review. Link the dataset version and exact examples when discussing quality. Do not report model gains until a comparison has actually been run.
