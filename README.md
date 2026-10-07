# Educational content meeting and implementation review

Build complete, reviewed teaching units for Classes 8 and 9: teacher-like spoken explanations, synchronized dynamic visualizations, worked examples, independent problems, and a path for feedback. The user's revised scope includes sustained lessons of around 20 minutes where appropriate. This folder translates the supplied Hindi and English meeting transcript and subsequent clarifications into minutes and a research-informed delivery plan, with particular attention to Code2Video.

Prepared on **6 October 2026**. The meeting date is not supplied. Its review deadline is **the 9th**, with month and year unconfirmed. Research was checked on 6 October 2026; this is a scoped technical review, not an exhaustive systematic review.

## Read first

**Latest handoff — 7 October 2026:** Read the [current work and future system report](HANDOFF_REPORT.md) and [next session brief](NEXT_SESSION.md). The user found the full lesson's narration poor and incoherent. Audio redesign, Google TTS evaluation, precise alignment and an independent highlight layer are the immediate priorities. Google audio has not yet been generated. The [complete meeting archive](../../meeting_full_backup_2026-10-07.tar.gz) includes the entire meeting folder, including reports, source, evidence, videos, audio, models, repositories and environments.

**New full lesson — 7 October 2026:** [Watch the 20-minute Pythagorean theorem lesson](long_form_pythagoras/output/pythagoras_20min.mp4), open its [chapter player](long_form_pythagoras/review.html), or inspect the [sources, full narrative, storyboard, code and review evidence](long_form_pythagoras/README.md). The audio-led lesson uses neural narration and deterministic geometry at 1080p. Teacher and learner evaluation remain pending.

**Detailed review and measured pilot:** Read the [forty approaches across eight problems](research/04_long_form_method_comparison.md), [paper and cloned-code audit](research/05_paper_and_code_audit.md), [cost analysis](research/06_cost_analysis.md), and [combined architecture and assignments](09_combined_architecture_and_tickets.md). The [OpenRouter pilot](experiments/openrouter_pilot/RESULTS.md) used US$0.48565189 of the authorized US$5 and records actual generation, rendering, and repair defects. A [full narration draft](examples/long_form_slope_script_draft.md) is available for teacher review.

**Current approach:** [Narration-led long-form lessons](08_narration_led_long_form_approach.md) covers expert-teacher data, script-generation experiments, continuity across rendering chunks, audio timing, overlap detection, repair, and model distillation. It takes precedence over earlier short-video recommendations. The meeting minutes preserve the original discussion.

**First prototype ready:** [Watch the 79-second narrated clip](prototype/output/like_terms.mp4), open the [chapter player](prototype/review.html), or inspect the [editable source and build instructions](prototype/README.md). This English draft covers the opening concept and one quick practice question. Teacher review is pending.

| Document | Purpose |
| --- | --- |
| [Meeting minutes](01_meeting_minutes.md) | Decisions, discussion, assignments, and unresolved questions with transcript timestamps |
| [Scope and delivery plan](02_scope_and_delivery_plan.md) | Immediate demonstration, later milestones, owners, dependencies, and acceptance gates |
| [Literature review](research/01_literature_review.md) | Evidence across video generation, pedagogy, assessment, and feedback |
| [Code2Video assessment](research/02_code2video_assessment.md) | What to adopt, what to test, integration boundaries, and reproduction plan |
| [Source register](research/03_source_register.md) | Primary sources, dates, inspection depth, and limitations |
| [System architecture](03_system_architecture.md) | Data contracts, review stages, rendering, feedback, and versioning |
| [Evaluation protocol](04_evaluation_protocol.md) | Technical comparisons, teacher review, student pilot, and launch decision |
| [Action register](05_action_register.md) | Assigned and proposed tasks with review evidence |
| [Scaling and distillation plan](06_scaling_dataset_and_distillation.md) | Reusable renderer, dataset construction, smaller-model training, evaluation, and production costs |
| [Frameworks and implementation handoff](07_frameworks_and_implementation_handoff.md) | Six-Blackwell setup, selected stack, module contracts, and tickets for lower-cost coding models |
| [Worked lesson package](examples/like_terms_lesson.md) | Original script, storyboard, five problems, answer key, and feedback example |
| [Reusable templates](templates/lesson_and_review_templates.md) | Source observation, script handoff, scene, question, and defect records |

## Workstreams

1. [Curriculum and teacher evidence](workstreams/01_curriculum_and_teacher_evidence.md)
2. [Scripts and instructional design](workstreams/02_scripts_and_instructional_design.md)
3. [Code to video and narration](workstreams/03_code_to_video_and_narration.md)
4. [Science and biology representations](workstreams/04_science_and_biology.md)
5. [Problem generation and verification](workstreams/05_problem_generation.md)
6. [Student work diagnosis and feedback](workstreams/06_student_feedback.md)
7. [Validation and school rollout](workstreams/07_validation_and_rollout.md)

## Recommended first implementation

Start with one complete narration-led algebra lesson, potentially around 20 minutes, and a small set of challenging rendering cases. Compare script-generation approaches separately from coding approaches. For coding comparisons, keep the approved script and learning objectives identical. Judge explanatory quality, continuity, correctness, learning, repair effort, and cost per accepted lesson. Use the revised approach linked above for implementation assignments.

The meeting also calls for science and biology scripts and demonstrations from both Manideep and Durgesh. The initial plan preserves these requirements while putting one shared lesson first so their implementations can be compared fairly.

## Status and boundaries

The planning documents are accompanied by a rendered 79-second Manim prototype and a separate, limited three-model OpenRouter pilot with actual code renders and a repair attempt. The pilot is not a statistically reliable model ranking or an end-to-end reproduction of the research systems. Four public repositories were cloned and inspected at recorded commits. The earlier slope narration remains a draft. A separate 20-minute Pythagorean theorem lesson has now been rendered with reviewable source code, captions, source comparisons and technical checks; teacher approval remains pending. No learner study or audit of the existing Concept Explorer product has been completed. Existing software capabilities mentioned in the meeting remain team reports rather than independently verified findings.

Meeting decisions are identified in the minutes. Workstream designs, numerical acceptance thresholds, experimental budgets, and suggested responsibility splits are proposals unless explicitly attributed to the transcript. Source details are centralized to keep claims traceable.
