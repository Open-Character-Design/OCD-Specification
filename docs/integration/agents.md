# Operational Guidance for Conversational Agents

Designing interactive agents with the Open Character Specification requires combining authored character data with runtime orchestration. This guide covers four operational pillars, prompt composition, memory synchronization, state management, and safety filtering, for three common deployment modes: AI agents, NPCs, and chatbots.

## Prompt Composition

| Deployment | Recommended Strategy | Implementation Notes |
|------------|----------------------|----------------------|
| **AI Agents** | Blend canonical biography, current goals, and available tools into the system prompt. Attach current scene context and task briefs as user messages. | Serialize selected OCD sections (e.g., `background.biography`, `personality.traits`, `behavior.ai.behavior_model`) into templated snippets so the LLM always sees stable identity anchors. | 
| **NPCs** | Use the OCD file to seed a dialogue state machine: the baseline persona powers greeting lines, while `behavior.improv_guidelines` maps to fallback utterances. | Keep prompts concise, strip metadata not needed for in-world dialogue, and project `state_dynamics` (mood, morale) into tone modifiers. |
| **Chatbots** | Combine safety preambles with `interaction_layer.preferred_modes` to tell the LLM how to respond in chat. Inject `meta_properties.target_audience` to tune register. | Cache the rendered prompt per session to avoid re-reading the full document on every turn; diff in only the user-visible deltas. |

## Memory Synchronization

- **Shared Memory Store**: Mirror `state_dynamics`, `contextual_fit`, and any running quest data into a key-value store. When updates occur (e.g., morale drops), commit them back into the OCD-compatible structure so offline authoring tools stay in sync.
- **Observation Logging**: Capture each exchange as a `TranscriptEvent` (timestamp, speaker, summary). For agents with long-term memory, distill older turns into `background.timeline` style summaries to keep prompts lean.
- **Cross-Agent Sync**: When multiple agents share a world, propagate changes through `relationships` references. An NPC learning about a player action should update their sentiment, which future prompts serialize automatically.

## State Management Patterns

### AI Agents
- Maintain an explicit finite-state machine keyed by `state_dynamics.status` (e.g., `planning`, `executing`, `cooldown`).
- Surface `behavior.ai.safety.boundaries` as guard conditions, if a tool call would violate a boundary, suppress it and produce an apology response instead.
- Persist tool outputs to `extras` so post-run audits can replay how the agent acted.

### NPCs
- Mirror `state_dynamics.location` to the game world entity so pathing or quest systems stay coherent.
- Use `interaction_layer.consent_model` to gate branching dialogue trees and romance/combat options.
- When the NPC transitions scenes, emit an event that updates `meta.tags` (e.g., add `present-in-city`) for downstream analytics.

### Chatbots
- Track `conversation_phase` (onboarding, troubleshooting, closing) derived from `behavior.ai.dialogue_style.max_len` thresholds to avoid runaway sessions.
- Employ a rolling window summarizer that rewrites the last N turns into a short synopsis stored under `extras.session_snapshot`.
- Reset state when `state_dynamics.mood` drifts outside acceptable bands; escalate to a human if repeated resets occur.

## Safety Filtering Pipeline

1. **Pre-Prompt Guardrails**: Inject policy reminders derived from `behavior.ai.safety.boundaries` before each LLM call.
2. **Model Output Screening**: Run outputs through classifiers keyed to `meta_properties.appropriateness`. Flag violations for redaction or re-generation.
3. **Contextual Overrides**: If `meta.tags` contains sensitive markers (e.g., `hivemind`, `symbiote`), enable specialized filters tuned for multi-entity consent or body horror content.
4. **Audit Trails**: Append filter decisions to `extras.moderation_log` with timestamps for compliance review.

## Deployment Checklist

- [ ] Validate the OCD document with the platform-specific validator before shipping prompts.
- [ ] Load-test prompts with representative transcripts to ensure safety filters do not over-trigger.
- [ ] Document your synchronization cadence so authors know when runtime state will be written back to source control.

For additional integration patterns, combine this guide with the validator documentation and extension references in this section.
