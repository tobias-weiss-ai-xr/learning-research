# Knowledge Tree: Integrating Bloom's Taxonomy & ZPD into Learning Platforms

**Scope:** ki-kompetenz-training (AI Literacy) + HPC Courses  
**Based on:** 26,319 research papers + Bloom's Taxonomy + Vygotsky's ZPD  
**Date:** 2026-08-13

---

## 🌲 Knowledge Tree Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│                         KNOWLEDGE TREE                               │
│                    (Platform Architecture)                          │
└─────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┴───────────────────────────┐
        │                                                           │
┌───────▼────────────────┐                    ┌──────────────────▼───────────┐
│   BLOOM'S TAXONOMY     │                    │    ZPD (VYGOTSKY)           │
│   (Cognitive Levels)   │◄──────────────────►│    (Learning Zone)          │
└───────┬────────────────┘                    └────────────┬──────────────────┘
        │                                                 │
        │                                                 │
        ▼                                                 ▼
┌───────────────────────────┐               ┌────────────────────────────────┐
│ Level 1: REMEMBER         │               │ Current Level (What            │
│ Level 2: UNDERSTAND       │               │ learner can do independently) │
│ Level 3: APPLY            │◄──────────────►│                                 │
│ Level 4: ANALYZE          │               │◄────── ZONE OF ──────►          │
│ Level 5: EVALUATE         │               │    PROXIMAL DEVELOPMENT         │
│ Level 6: CREATE           │               │                                 │
└───────────────────────────┘               └────────────────────────────────┘
        │                                                 │
        │                                                 │
        └───────────────────────────┬─────────────────────┘
                                    │
                                    ▼
                        ┌───────────────────────┐
                        │   SCAFFOLDING LAYERS  │
                        │   (Fade-out support) │
                        └───────────┬───────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│   EXAMPLES    │          │    HINTS      │          │  GUIDING Qs   │
│ (Concrete)    │          │ (Incremental) │          │ (Socratic)    │
└───────────────┘          └───────────────┘          └───────────────┘
```

---

## 1️⃣ Bloom's Taxonomy Integration

### Original (1956) vs Revised (2001)

| Original (1956) | Revised (2001) | Action Verbs | Activities |
|-----------------|----------------|--------------|------------|
| Knowledge | Remember | List, define, identify, name | Flashcards, definitions |
| Comprehension | Understand | Explain, summarize, interpret | Paraphrasing, re-explanation |
| Application | Apply | Demonstrate, use, execute | Practice problems, coding |
| Analysis | Analyze | Differentiate, organize, compare | Case studies, debug |
| Synthesis | Create | Design, construct, produce | Projects, implementations |
| Evaluation | Evaluate | Judge, critique, assess | Code review, peer feedback |

### Platform-Level Taxonomy Mapping

```yaml
Taxonomy_Per_Lesson:
  lesson_objective:
    - primary_bloom_level: APPLY  # What this lesson aims for
    - secondary_levels: [REMEMBER, UNDERSTAND]  # Prerequisites

  content_structure:
    - pre_assessment:
        levels: [REMEMBER, UNDERSTAND]
        purpose: Check prerequisites (ZPD boundary)

    - core_content:
        levels: [UNDERSTAND, APPLY]
        format: 5-7 min chunks with active recall

    - practice:
        levels: [APPLY, ANALYZE]
        scaffolding: adaptive based on performance

    - extension:
        levels: [EVALUATE, CREATE]
        optional: true
        target: Advanced learners
```

---

## 2️⃣ ZPD Integration (Zone of Proximal Development)

### ZPD Framework for Platform

```
┌─────────────────────────────────────────────────────────────────┐
│                     ZPD IMPLEMENTATION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────────────────┐  ┌────────────┐ │
│  │  AUTONOMY   │  │           ZPD            │  │   FRUSTRA- │ │
│  │  ZONE       │  │    (SWEET SPOT)         │  │   TION     │ │
│  │             │  │                         │  │   ZONE     │ │
│  │  Too easy   │  │    Target: 70-80%       │  │  Too hard  │ │
│  │  No growth  │  │    success rate         │  │  Overload  │ │
│  └─────────────┘  └─────────────────────────┘  └────────────┘ │
│       │                    │                        │        │
│       │                    │                        │        │
│   Reduce            SCAFFOLD           INCREASE         │
│   difficulty        appropriately       scaffolding      │
│   to 90%+           to hit 70-80%                       │
│                                                                 │
│  Dynamic Adjustments:                                           │
│  - Success rate > 90%  → Remove scaffold, move to next Bloom level │
│  - Success rate 70-80% → Maintain scaffold, extend same level       │
│  - Success rate < 70%  → Add scaffold, drop one Bloom level         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Scaffolding Layers (Fade-out Pattern)

```yaml
Scaffolding_Layers:
  layer_1_full_support:
    description: Maximum assistance (bottom of ZPD)
    triggers:
      - first_time_topic: true
      - success_rate: < 50%
    features:
      - examples: visible (concrete worked examples)
      - hints: automatic (show when stuck)
      - structure: broken down step-by-step
      - time_guidance: estimated time shown
      - feedback: immediate with explanations

  layer_2_partial_support:
    description: Fading support (middle of ZPD)
    triggers:
      - repeat_topic: true
      - success_rate: 50-70%
    features:
      - examples: collapsed (click to reveal)
      - hints: on-demand (click to request)
      - structure: larger steps
      - time_guidance: hidden
      - feedback: delayed by choice

  layer_3_minimal_support:
    description: Transition to autonomy (top of ZPD)
    triggers:
      - success_rate: 70-85%
      - consecutive_reviews: > 2
    features:
      - examples: hidden completely
      - hints: limited (1 max per session)
      - structure: full problem statement
      - feedback: minimal (correct/incorrect)

  layer_4_autonomy:
    description: Mastery zone (beyond ZPD, in autonomy)
    triggers:
      - success_rate: > 85%
      - mastery_score: > 90%
    features:
      - no scaffolding
      - performance tracking only
      - empowered to facilitate others
      - badges earned
```

---

## 3️⃣ Knowledge Tree: ki-kompetenz-training (AI Literacy)

```
┌─────────────────────────────────────────────────────────────────────────┐
│              AI LITERACY LEARNING TREE (Bloom × ZPD)                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ FOUNDATION LEVEL  │    │ INTERMEDIATE LEVEL │    │ ADVANCED LEVEL    │
│ (Bloom: REMEMBER  │───▶│ (Bloom: APPLY,    │───▶│ (Bloom: CREATE,   │
│  → UNDERSTAND)    │    │  ANALYZE)         │    │  EVALUATE)        │
└─────────┬─────────┘    └─────────┬─────────┘    └─────────┬─────────┘
          │                        │                        │
          ▼                        ▼                        ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ Module 1: What is │    │ Module 4: Prompt  │    │ Module 7: AI      │
│   AI?             │    │   Engineering     │    │   Safety &        │
│   Remember key    │    │   Apply prompts   │    │   Ethics          │
│   concepts        │    │   Analyze outputs │    │   Evaluate impact │
└─────────┬─────────┘    └─────────┬─────────┘    └─────────┬─────────┘
          │                        │                        │
          ▼                        ▼                        ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ Module 2: AI      │    │ Module 5: AI for  │    │ Module 8: Building │
│   Capabilities    │    │   Daily Work      │    │   AI Workflows    │
│   Understand what │    │   Apply tools     │    │   Create systems  │
│   AI can/can't do │    │   Analyze use     │    │   Architect solns │
└─────────┬─────────┘    └─────────┬─────────┘    └─────────┬─────────┘
          │                        │                        │
          ▼                        ▼                        ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ Module 3: Prompt  │    │ Module 6: Data    │    │ Module 9: AI      │
│   Basics          │    │   Privacy         │    │   Strategy        │
│   Apply basic     │    │   Understand laws │    │   Evaluate vendor │
│   prompts         │    │   Apply practices │    │   Choose solutions │
└───────────────────┘    └───────────────────┘    └───────────────────┘
```

### Sample Lesson: Module 1 - "What is AI?" (Bloom: REMEMBER → UNDERSTAND)

```yaml
Lesson: ai_fundamentals_01
Title: "What is Artificial Intelligence?"

Learning_Objectives:
  bloom_primary: REMEMBER
  bloom_secondary: UNDERSTAND
  zpd_target: 75% success_rate

Content_Chunks:
  - chunk_1:
      duration: 5 min
      bloom: REMEMBER
      content: "Definition of AI - systems that perform tasks requiring intelligence"
      activity: "Match definitions to terms (Active Recall)"
      feedback: immediate with examples

  - chunk_2:
      duration: 7 min
      bloom: UNDERSTAND
      content: "Types of AI: Narrow vs General"
      activity: "Classify examples (Narrow/General)"
      zpd_scaffold:
        - success_rate < 70%: Show concrete examples table
        - success_rate > 85%: No scaffold

  - chunk_3:
      duration: 6 min
      bloom: UNDERSTAND
      content: "Machine Learning vs Traditional Programming"
      activity: "Fill in comparison table"
      zpd_scaffold:
        - first_attempt: Provide row headers
        - retry_2: Provide one filled row

Practice_Activities:
  - level_1_remember:
      format: Multiple Choice + Flashcards
      scaffold: None
      srs_interval: 1 day, 3 days, 7 days

  - level_2_understand:
      format: Short explanation + classification
      scaffold layer: Partial Support
      srs_interval: 3 days, 10 days, 30 days

Assessment:
  zpd_check:
    - pre_score > 80%: Skip to Module 2 (Autonomy Zone)
    - pre_score 60-80%: Module 1 with Partial Support
    - pre_score < 60%: Module 1 with Full Support
```

---

## 4️⃣ Knowledge Tree: HPC Courses

```
┌─────────────────────────────────────────────────────────────────────────┐
│              HPC LEARNING TREE (Bloom × ZPD)                            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ INTRODUCTORY      │    │ INTERMEDIATE      │    │ ADVANCED          │
│ (Bloom: REMEMBER  │───▶│ (Bloom: APPLY,    │───▶│ (Bloom: CREATE,   │
│  → UNDERSTAND)    │    │  ANALYZE)         │    │  EVALUATE)        │
└─────────┬─────────┘    └─────────┬─────────┘    └─────────┬─────────┘
          │                        │                        │
          ▼                        ▼                        ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ Basic Linux       │    │ Parallel          │    │ Performance       │
│ Commands & HPC    │    │ Programming       │    │ Optimization      │
│ Remember syntax   │    │ Apply OpenMP/MPI  │    │ Analyze bottlenecks│
│ Understand job    │    │ Analyze data deps │    │ Create optimized   │
│ submission        │    │ Evaluate speedup  │    │ implementations   │
└─────────┬─────────┘    └─────────┬─────────┘    └─────────┬─────────┘
          │                        │                        │
          ▼                        ▼                        ▼
┌───────────────────┌───────────────────┐    ┌───────────────────┐
│ HPC Environment   │    │ Cluster Usage     │    │ GPU Computing     │
│ Remember nodes,   │    │ Apply job scheduling│    │ Apply CUDA        │
│ queues, storage   │    │ Analyze resource  │    │ Analyze kernel    │
│ Understand SLURM  │    │ allocation        │    │ Evaluate suitabilty│
└───────────────────┘    └───────────────────┘    └───────────────────┘
```

### Sample Lesson: HPC - Job Submission with SLURM (Bloom: UNDERSTAND → APPLY)

```yaml
Lesson: hpc_slurm_01
Title: "Submitting Jobs with SLURM"

Learning_Objectives:
  bloom_primary: APPLY
  bloom_secondary: UNDERSTAND
  zpd_target: 70-80% success_rate

Content_Chunks:
  - chunk_1:
      duration: 5 min
      bloom: REMEMBER
      content: "SLURM basic commands: sbatch, squeue, scancel"
      activity: "Match command to purpose"
      feedback: immediate

  - chunk_2:
      duration: 8 min
      bloom: UNDERSTAND
      content: "SLURM batch script structure"
      activity: "Identify required directives"
      zpd_scaffold:
        - examples: Full script shown
        - hints: "What starts with #SBATCH?"

  - chunk_3:
      duration: 10 min
      bloom: APPLY
      content: "Write a complete batch script"
      activity: "Write script submitting a Python script"
      zpd_scaffold:
        - first_attempt: Template provided
        - error_count > 3: Show completed example
        - success: "Explain what each line does"

Practice_Activities:
  - level_2_understand:
      format: Debug broken scripts
      scaffold: Error hints provided

  - level_3_apply:
      format: Write script from specification
      scaffold layer: Partial Support (template)

  - level_4_analyze:
      format: Optimize script for efficiency
      optional: true
      bloom_level: ANALYZE

SRS_Schedule:
  - applying_scripts:
      initial_interval: 1 day
      success_rate > 90%: 7 days
      success_rate 70-90%: 3 days
      success_rate < 70%: 24 hours (extra practice)

  - debugging:
      sparser_schedule: 3 daysinitially
      focuses on common errors
```

---

## 5️⃣ Cross-Platform Knowledge Tree Integration

### Unified Taxonomy Architecture

```yaml
Unified_Knowledge_Tree:
  platform_metadata:
    ki_kompetenz_training:
      domain: AI Literacy
      taxonomy_levels:
        - beginner: Foundation (Remember, Understand)
        - intermediate: Application (Apply, Analyze)
        - advanced: Creation (Evaluate, Create)

    hpc_courses:
      domain: High-Performance Computing
      taxonomy_levels:
        - beginner: Basics (Remember, Understand)
        - intermediate: Implementation (Apply, Analyze)
        - advanced: Optimization (Evaluate, Create)

  cross_domain_mapping:
    shared_concepts:
      - name: "Problem Decomposition"
        ki_kompetenz: "Breaking AI tasks into prompts"
        hpc: "Breaking problems for parallelization"

      - name: "Resource Management"
        ki_kompetenz: "Token limits, API costs"
        hpc: "CPU/GPU allocation, memory limits"

      - name: "Debugging"
        ki_kompetenz: "Prompt debugging, output analysis"
        hpc: "Code debugging, performance profiling"

  learner_profile:
    progress_tracking:
      - bloom_level_per_module
      - zpd_position (what scaffold layer)
      - mastery_score_per_objective
      - srs_review_intervals
```

---

## 6️⃣ Implementation Checklist

### Bloom Integration
- [ ] Tag every lesson with primary Bloom level
- [ ] Tag practice activities with Bloom levels
- [ ] Map content to action verbs (Remember: list, define; Apply: execute, use)
- [ ] Create progression paths through Bloom levels
- [ ] Design assessments for each Bloom level

### ZPD Integration
- [ ] Implement performance tracking (success rate by activity)
- [ ] Define dynamic adjustment thresholds (70-80% = sweet spot)
- [ ] Build scaffolding layers with fade-out logic
- [ ] Implement examples, hints, guiding questions system
- [ ] Add pre-assessment to establish ZPD boundary

### Joint Implementation
- [ ] Create knowledge tree visualization for learners
- [ ] Map scaffolding to Bloom levels (lower Bloom = more scaffold)
- [ ] Implement SRS with ZPD-aware scheduling
- [ ] Add "Mastery Achievement" when reaching autonomy zone
- [ ] Enable peer teaching (MKO - More Knowledgeable Other)

---

## 7️⃣ Metrics & Evaluation

### Bloom Level Progression
```yaml
Metrics:
  bloom_distribution:
    - metric: "Time spent per Bloom level"
      target: Balanced across levels

    - metric: "Success rate by Bloom level"
      target: 70%+ for all levels

    - metric: "Progression through Bloom levels"
      target: 80% of learners reach EVALUATE/CREATE
```

### ZPD Effectiveness
```yaml
Metrics:
  zpd_effectiveness:
    - metric: "Percentage in optimal ZPD (70-80% success)"
      target: 70%+ of sessions

    - metric: "Time to autonomy (remove all scaffolding)"
      target: Decreasing over time

    - metric: "Scaffold removal rate"
      target: Progressive fade-out
```

---

## 8️⃣ Technical Implementation

### Data Schema Example

```json
{
  "lesson": {
    "id": "ai_fundamentals_01",
    "bloom_level": "REMEMBER",
    "bloom_secondary": ["UNDERSTAND"],
    "zpd_config": {
      "target_success_rate": 75,
      "scaffold_layers": ["full", "partial", "minimal", "none"],
      "adjustment_thresholds": {
        "reduce_difficulty": 90,
        "increase_difficulty": 70
      }
    },
    "content_chunks": [
      {
        "id": "chunk_1",
        "bloom_level": "REMEMBER",
        "duration_minutes": 5,
        "scaffold": {
          "examples": true,
          "hints": false,
          "guiding_questions": false
        }
      }
    ]
  }
}
```

### Algorithm: ZPD Adjustment

```python
def adjust_zpd(success_rate, current_scaffold, consecutive_mastery):
    """Adjust scaffolding based on ZPD principles"""
    
    # Too easy (above ZPD) → Reduce scaffold
    if success_rate > 90:
        next_scaffold = reduce_scaffold(current_scaffold)
    
    # Too hard (below ZPD) → Increase scaffold
    elif success_rate < 70:
        next_scaffold = increase_scaffold(current_scaffold)
    
    # In sweet spot → Maintain
    else:
        next_scaffold = current_scaffold
    
    # Achieved autonomy → Check for mastery
    if consecutive_mastery > 3 and success_rate > 85:
        return 'autonomy', 'Mastery Badge Awarded'
    
    return next_scaffold, 'Adjusting scaffolding'
```

---

## 9️⃣ References

### Bloom's Taxonomy
- Bloom, B.S. (1956). *Taxonomy of Educational Objectives*
- Anderson, L.W., Krathwohl, D.R. (2001). *A Taxonomy for Learning, Teaching, and Assessing*
- Fink, L.D. (2013). *Creating Significant Learning Experiences*

### Vygotsky's ZPD
- Vygotsky, L.S. (1978). *Mind in Society: The Development of Higher Psychological Processes*
- Scaffolding in computer-based learning environments: A meta-analysis

### Evidence Base
- This document integrates research from 26,319 papers
- Maps to corpus cells: educational-psychology (713), personalization (4,495), memory-science (1,361)

---

**Document Version:** 1.0  
**Status:** Draft for Implementation  
**Next Steps:** Review with ki-kompetenz-training and HPC course developers
