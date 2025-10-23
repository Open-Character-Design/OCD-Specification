---
title: Guided Tutorial Overview
description: Follow a sequenced path to build, enrich, and validate OCD character files.
search:
  boost: 2
tags:
  - tutorial
  - onboarding
---

# Guided Tutorial Overview

Welcome to the OCD tutorial track! Start here to understand how the step-by-step lessons connect to the rest of the documentation. If you need broader context first, review the [Start Here orientation](../start-here/index.md).

## Why Learn OCD?

OCD transforms how you think about character creation. Instead of scattered notes and inconsistent designs, OCD gives you a structured, collaborative approach that works across any medium, from games to novels to AI applications.

**What makes OCD special:**  

- **Structured Creativity**: Transform chaotic character development into organized, systematic workflows.  
- **True Collaboration**: Enable multiple creators to work on the same character simultaneously.  
- **Cross-Media Portability**: Create characters that work seamlessly across games, books, AI, and more.  
- **Technical Integration**: Build applications that understand and work with your character data.  

**Who benefits:**  

- **Writers** building rich and detailed characters for your stories, novels, and other media.  
- **Game Developers** creating portable, procedural character profiles for games and other interactive media.  
- **AI Developers** training and prompt models with structured character data.  
- **Creative Teams** collaborating on character-driven projects. 

??? info "Already comfortable with JSON/YAML?"
    Skip ahead to [Step 3](background.md) or dive straight into the [Authoring Playbook](../authoring/writing-ocd-files.md). Each lesson links back to the detailed references so you can drill into specifics when needed.

## What You'll Learn

By the end of this tutorial, you'll be able to:

- Install and use OCD validators on your machine.
- Create valid character definitions from scratch.
- Add personality traits and background information.
- Integrate with other systems like D&D 5e, ChatGPT, and other AI models.
- Follow best practices for production deployment.

Each step concludes with "Next up" pointers so you can branch into advanced topics without losing momentum.

## Tutorial Structure

### [Step 1: Your First Character](first-character.md)

Learn the basics by creating a minimal valid character and running your first validation.

**What you'll build:** 

- A simple human character with basic identity information.

**Use Case Connection:** 

- Perfect for [Creative Applications](../use-cases/creative.md) 
- Learn the foundation of structured character design.

### [Step 2: Personality & Traits](personality.md)

Explore the trait model by adding personality traits, bipolar axes, and scalar values.

**What you'll build:** 

- A character with detailed personality traits and behavioral tendencies.

**Use Case Connection:** 

- Essential for [Interactive & Storytelling](../use-cases/interactive.md)
- Personality drives AI behavior and dialogue systems  

Need the raw trait schema? Check the [Trait Model reference](../spec/trait-model.md).

### [Step 3: Background & Relationships](background.md)

Add timeline events, affiliations, and relationships between characters.

**What you'll build:** 

- A character with rich background and connections to other characters.

**Use Case Connection:** 

- Core to [Community & Open Source](../use-cases/community.md)
- Relationships enable collaborative worldbuilding
- Cross-check relationship fields in the [Field Reference](../reference/fields.md#relationships)

### [Step 4: System Extensions](extensions.md)

Integrate with game systems using extension blocks like `x-dnd5e`.

**What you'll build:** 

- A D&D 5e character with stats, abilities, and equipment.
- ~~An AI character profile for ChatGPT, etc.~~ (Coming soon)

**Use Case Connection:** 

- Key for [Technical Applications](../use-cases/technical.md)
- Learn how to extend OCD for specific platforms
- You'll also touch the [Extensions & Namespaces guide](../integration/extensions-and-namespaces.md)

### [Step 5: Production Tips](production.md)

Learn best practices for validation, normalization, and deployment workflows.

**What you'll build:** A production-ready character with proper metadata and validation.

**Use Case Connection:** Critical for all use cases - apply the lessons alongside the [Validation Overview](../reference/validation.md) to prepare deployment-ready characters.

## Quick Reference

Throughout the tutorial, you'll see these helpful elements:

!!! tip "Pro Tips"
    Look for these boxes with helpful hints and best practices.

!!! warning "Important"
    Pay attention to these warnings about common mistakes or important concepts.

!!! note "Key Concepts"
    These boxes explain important OCD concepts you'll need to understand.

## Getting Help

If you get stuck at any point:

1. **Check the [FAQ](../faq.md)** for common questions.
2. **Browse [Examples](../authoring/examples.md)** for inspiration.
3. **Read the [Specification Overview](../spec/schema-overview.md)** for detailed information.
4. **Ask on [GitHub Discussions](https://github.com/Open-Character-Design/OCD-Specification/discussions)**.

## Ready to Start?

Jump ahead to [Step 1: Your First Character](first-character.md) when you're ready to create your first OCD character file.
