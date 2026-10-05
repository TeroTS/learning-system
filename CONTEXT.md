# Domain Vocabulary

## Canonical Terms

### Learner

The single person using the system to learn one or more subjects.

_Avoid:_ User, student

### Subject

Something the learner is studying. Its files live in `subjects/<subject>/`, where the folder name is lowercase and hyphenated.

_Avoid:_ Course, domain

### Goal

The specific outcome the learner wants for a subject: target, current level, deadline and how the learner will be tested. Stored in `goal.md`.

_Avoid:_ Objective

### Map

The structured plan for a subject: its topics, how they depend on each other and where learners usually get stuck. Stored in `map.md`.

_Avoid:_ Curriculum, roadmap, plan

### Topic

One unit in a map. Its status is `todo`, `learning` or `passed`.

_Avoid:_ Module, lesson, sub-module

### Role

One of the ten ways the transcript says AI can support learning: interviewer, mapmaker, explainer, Socratic questioner, examiner, checker, listener, diagnostician, sparring partner and clerk.

_Avoid:_ Mode, persona

### Skill

A repo-local, agent-agnostic instruction file at `.agents/skills/<skill>/SKILL.md`. Each skill implements one role, except `review`.

_Avoid:_ Prompt, command

### Production

Learning by actively producing: recalling, predicting, explaining or attempting. Skills prompt production before they explain anything.

_Avoid:_ Practice (as a synonym)

### Consumption

Passive reading, watching or receiving explanations. It feels like learning but is not enough on its own.

### Session

One run of a skill on a subject. Each session adds one line to `sessions.md`.

_Avoid:_ Conversation, transcript

### Mistake

An error the learner made during a session, recorded in `mistakes.md` with the date, skill, mistake and correct idea.

_Avoid:_ Error, gap (when referring to the log entry)

### Root Misunderstanding

The shared underlying misconception behind repeated mistakes, often across subjects. The diagnostician finds these.

_Avoid:_ Root cause, core issue

### Source

Material the learner supplies in `subjects/<subject>/sources/`, including topic-only guides. It informs scope proposals
and provides context, not answer keys or grading prerequisites. Answers are always assessed by agent judgement.

_Avoid:_ Reference, document

### Card

A spaced-repetition item with a front and back, stored in `cards.json` and changed only by `scripts/cards.py`.

_Avoid:_ Flashcard (in code and files), note

### Box

A card's Leitner level. Boxes 1–5 map to review intervals of 1, 3, 7, 14 and 30 days.

_Avoid:_ Level, stage

### Due

A card is due when its due date is on or before today.

### Grade

Recording whether the learner recalled a due card correctly. This moves the card up one box or back to box 1.

_Avoid:_ Score, rate
