# Under research: current practices in scripting for AI video generation

**Status:** Under research  
**Research date:** November 6, 2026  
**Scope:** Current practices and findings through point 5. Model recommendations are excluded.

The strongest pattern is a staged workflow: write the story, turn it into an explicit shot plan, generate against visual references, then review and edit. Specialized scripting models exist, but even a good script does not guarantee faithful video execution.

This research reviews vendor documentation and research available as of November 6, 2026. Vendor guides show supported workflows; research results demonstrate performance within particular test settings. Neither establishes reliable performance on every kind of video.

## What people currently do, where it works, and where it fails

| Practice | Where it works | Where it fails or becomes unreliable |
| --- | --- | --- |
| **Expand a brief into detailed video prompts using an LLM** | Turning vague requests into concrete subjects, actions, framing, and style. Meta’s Movie Gen used a specialized, fine-tuned prompt rewriter. | Extra detail can introduce unwanted creative choices. Meta specifically observed that overly elaborate motion descriptions could introduce artifacts. This approach handles shot description more directly than whole-story development. [Movie Gen, §3.4.1](https://arxiv.org/html/2410.13720v1#S3.SS4.SSS1) |
| **Break the script into short, focused shots** | Isolating actions makes generation easier to inspect, retry, and assemble. Google recommends one focused scene per short-video prompt. | Packing several events into one short generation can produce missing or muddled actions. Generating shots separately also creates continuity work between them. [Google’s production guidance](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/best-practice) |
| **Create storyboard images and character references before video** | Establishing appearance, composition, wardrobe, and locations before animating them. Runway recommends character plates showing multiple angles. | A single reference image leaves unseen angles ambiguous. References reduce the need to invent appearance again; they do not guarantee consistent movement or geometry. [Runway’s longer-film workflow](https://help.runwayml.com/hc/en-us/articles/26871350018835-How-to-create-longer-videos-and-films) |
| **Use native multi-shot generation** | Quickly exploring a short sequence without manually generating every cut. Runway currently offers an app supporting up to five connected shots. | The existence of this feature does not establish dependable execution of precise shot order, transitions, or editorial intent. Those require separate evaluation. [Runway documentation](https://help.runwayml.com/hc/en-us/articles/51200254894483-Multi-Shot-Video) |
| **Separate analysis, planning, writing, and review into stages** | Handling complicated briefs, supplied footage, missing shots, and structured output. MCSC-Bench found benefits from an analysis → planning → writing workflow. | More calls add latency and cost. The study also found degradation under longer inputs, more distractors, and longer requested outputs. [MCSC-Bench](https://arxiv.org/html/2604.15127v1) |
| **Train a specialized script planner** | Learning a consistent production format and domain-specific planning behavior. Tencent researchers trained ScripterAgent to turn dialogue into executable cinematic scripts. | Its evidence concerns a defined dialogue-to-script task. It does not demonstrate universally superior screenwriting or eliminate downstream rendering errors. [ScripterAgent](https://arxiv.org/html/2601.17737v1) |
| **Generate several candidates, critique, and revise** | Catching incomplete plans and improving intermediate outputs before paying for downstream generation. | The critic can miss the same problems as the generator. MAViS explicitly reports limitations in its visual evaluators and in character interaction, dialogue, and editing. [MAViS, EACL 2026](https://aclanthology.org/2026.eacl-long.101.pdf) |

## 1. “Looks good” and “followed the script” are different achievements

The September 2026 **CutCraft** benchmark examines editing execution, including shot organization, montage, transitions, and audio–video relationships. Its findings show that visually plausible, smooth footage can still fail the intended editing plan. Transition execution generally deteriorated as shot counts increased.

Explicit planning and composition helped discrete controls such as shot count and transitions more than higher-level editorial meaning. The practical implication is to evaluate whether each intended event and transition happened, alongside aesthetics. [CutCraft findings](https://arxiv.org/html/2609.08275v1#S4.SS3)

For example, a beautiful close-up of someone holding a key is insufficient if the script required them to discover it, recognize it, and conceal it before another character enters.

## 2. References improve identity, but state and causality remain difficult

**MSVBench**, which evaluated 20 methods, found persistent weaknesses in physical interactions and maintaining character attributes across shots. It also identified tradeoffs: stronger movement could undermine physical accuracy, while aggressive camera changes could disrupt identity.

Image references helped consistency, but a static image does not fully specify depth or how objects should move. These are results for the models and settings tested, rather than a claim that every current system fails identically. [MSVBench analysis](https://arxiv.org/html/2602.23969v1#S4.SS3)

For a scripting system, this suggests tracking explicit scene state: who holds an object, where each person stands, what changed, and what must remain unchanged.

## 3. Some apparent improvements come from making the story easier to render

MAViS adapts its writing guidelines to generation limitations. Its recommendations include inserting cutaways and avoiding certain closely connected spatial transitions. The authors acknowledge that this limits shot diversity and expressiveness.

Its evaluation used **20 prompts targeting roughly one-minute videos**—useful evidence, but a limited basis for broad production claims. [MAViS guidelines, evaluation, and limitations](https://aclanthology.org/2026.eacl-long.101.pdf)

That creates an important distinction for experiments: did the system preserve a challenging creative idea more successfully, or simplify the idea until the generator could handle it? Both may be useful, but they should be reported separately.

## 4. Training can help, but the published examples use substantial curation

ScripterAgent used **1,750 finalized examples**, with 1,700 for training and 50 for testing. Its pipeline combined supervised fine-tuning with preference-based reinforcement learning. Human auditing still uncovered subtle errors after automated checks, including inconsistent props and dialogue–action conflicts. Its video execution stage retained lip-sync and fine-action limitations. [ScripterAgent methods and limitations](https://arxiv.org/html/2601.17737v1)

MCSC-Bench used **9,752 training examples**, plus in-domain and out-of-domain evaluation. Targeted training improved structural control, and its reinforcement-learning stage improved broader evaluation scores. However, the task involves selecting supplied materials and producing production scripts; that evidence does not directly establish better advertising persuasion or audience retention. [MCSC-Bench experiments](https://arxiv.org/html/2604.15127v1#S4)

Our 20-example pilot is therefore a sensible way to test annotation quality and scope, not a research-backed training-size target.

## 5. Timing deserves its own checks

The September 2026 **DramaChain Bench** identified production scheduling and duration budgeting as important storyboard-stage weaknesses. It also found that automated judging was more dependable for explicit checks, such as dialogue fidelity, than for some fine perceptual judgments, including synchronization and motion smoothness. [DramaChain analysis](https://arxiv.org/html/2609.00646v1#S4.SS4)

This supports a practical split: use code to check duration totals, required fields, and missing dialogue; use human review for delivery, pacing, and rendered quality.
