# VR/XR Learning Modality: Implementation Addendum to Bloom+ZPD Framework

**Date:** 2026-08-13  
**Extends:** `knowledge_tree_bloom_zpd.md`  
**Evidence base:** 871 VR/AR/XR papers (468 learning-oriented) from the 29,592-paper corpus  
**Focus session:** `docs/research/focus_session_vr_xr_learning.md`

---

## 🎯 Purpose

This addendum extends the Bloom+ZPD knowledge tree with a **VR/XR modality layer** — adding immersive learning as a delivery channel alongside the existing text/quiz/SRS approach. It is informed by the VR/XR focus session findings.

---

## 📊 Evidence Summary

| Finding | Evidence | Implication |
|---------|----------|-------------|
| VR/AR learning is exploding | 31→159 papers (2022→2025, 5× growth) | Invest now to ride the wave |
| Cognitive load adaptation in VR works | CLAd-VR, eye-tracking studies | Real-time ZPD via physiological signals |
| AR in-situ guidance is effective | WeldAR (24-novice study) | Overlay guidance on real workstations |
| LLM-powered pedagogical agents in VR | Multi-role adaptive agents | AI literacy roleplay in immersive env |
| Accessibility is a strength | 71 papers on VR/AR accessibility | Inclusive design from the start |
| Assessment via multimodal data | 237 papers on assessment | Richer than text quizzes alone |
| Only 4 review papers exist | Synthesis gap | First-mover opportunity |

---

## 🌲 Extended Knowledge Tree (with VR/XR Modality)

```
┌─────────────────────────────────────────────────────────────────────┐
│                  EXTENDED KNOWLEDGE TREE                            │
│           (Bloom × ZPD × VR/XR Modality)                           │
└─────────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│  BLOOM LEVEL  │       │  ZPD SCAFFOLD │       │  VR/XR MODALITY│
│  (Cognitive)  │       │  (Adaptive)   │       │  (Immersion)   │
└───────┬───────┘       └───────┬───────┘       └───────┬───────┘
        │                       │                       │
        ▼                       ▼                       ▼
  Remember → Create      Full → Autonomy         Text → AR → VR → Immersive
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   DELIVERY CHANNEL     │
                    │   (per Bloom level)    │
                    └───────────┬───────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│  TEXT/SRS     │       │  AR OVERLAY    │       │  VR IMMERSIVE │
│  (Baseline)   │       │  (Augmented)   │       │  (Full)       │
└───────────────┘       └───────────────┘       └───────────────┘
```

---

## 🔀 Modality Selection by Bloom Level

| Bloom Level | Text/SRS | AR Overlay | VR Immersive | Rationale |
|-------------|----------|------------|--------------|-----------|
| **Remember** | ✅ Primary | ✅ Flashcards | ◻️ Optional | SRS flashcards are efficient; AR cards add context |
| **Understand** | ✅ Primary | ✅ Annotations | ✅ Visualization | AR annotates real context; VR visualizes concepts |
| **Apply** | ✅ Quizzes | ✅ In-situ guidance | ✅ Simulation | AR overlays on real tools (WeldAR model); VR simulates practice |
| **Analyze** | ✅ Case studies | ✅ Data overlay | ✅ Interactive 3D | VR enables spatial analysis; AR overlays comparative data |
| **Evaluate** | ✅ Peer review | ✅ Live comparison | ◻️ Optional | Text/AR sufficient; VR adds little to evaluation |
| **Create** | ✅ Projects | ✅ Design overlay | ✅ Immersive build | VR for 3D creation; AR for in-context design |

---

## 🎯 ZPD + VR/XR Scaffolding Integration

### Physiological ZPD Detection (Advanced)

The focus session revealed that **cognitive load can be detected via physiological signals** in VR:

| Signal | Source | ZPD Application |
|--------|--------|-----------------|
| Eye tracking | Papers #7, #8, #18 | Pupil dilation, gaze patterns → cognitive load → adjust difficulty |
| Heart rate variability (HRV) | Paper #7 | Stress detection → reduce scaffold if overloaded |
| fNIRS (brain) | Paper #11 | Neuro-ergonomic load → continuous difficulty adjustment |
| Multimodal (gaze + interaction) | Paper "Assessing Learning Processes with Multimodal Data" | Process-level assessment, not just outcomes |

### Extended Scaffolding Layers (with VR/XR)

```yaml
Scaffolding_Layers_VR_Extended:
  layer_1_full_support:
    description: Maximum assistance
    text_mode: Step-by-step instructions + examples
    ar_mode: Highlighted overlays + tooltips on real interface
    vr_mode: Guided tutorial with visual cues
    triggers: first_time_topic, success_rate < 50%

  layer_2_partial_support:
    description: Fading support
    text_mode: Collapsed examples, on-demand hints
    ar_mode: Contextual hints (tap to reveal)
    vr_mode: Spatial cues, optional guidance
    triggers: repeat_topic, success_rate 50-70%

  layer_3_minimal_support:
    description: Transition to autonomy
    text_mode: Hidden examples, 1 hint max
    ar_mode: Minimal overlay (status only)
    vr_mode: Free exploration with checkpoint
    triggers: success_rate 70-85%, consecutive > 2

  layer_4_autonomy:
    description: Mastery zone
    text_mode: No scaffolding, performance tracking
    ar_mode: No overlay, ambient mode
    vr_mode: Open sandbox, creation mode
    triggers: success_rate > 85%, mastery_score > 90%
```

---

## 🏗️ Platform-Specific VR/XR Implementation

### ki-kompetenz-training (AI Literacy)

```yaml
VR_XR_Modality:
  ar_overlay:
    name: "AI Transparency Lens"
    description: AR overlay showing AI transparency prompts at point of work
    evidence: WeldAR (#13), AR for Deaf Students (#20)
    bloom_levels: [Understand, Apply, Analyze]
    implementation:
      - Overlay AI disclosure prompts on real AI tool usage
      - Show data flow visualizations (what data goes where)
      - Contextual risk-class hints (EU AI Act risk classes)
    zpd_integration:
      - Full Support: Always-on overlay with explanations
      - Partial: Overlay on detected AI usage only
      - Minimal: User-triggered overlay
      - Autonomy: Overlay off (user demonstrates mastery)

  vr_immersive:
    name: "AI Scenario Lab"
    description: VR roleplay scenarios for AI literacy
    evidence: LLM Pedagogical Agents (#15), Adaptive Gen-AI (#16), Open TutorAI (#3)
    bloom_levels: [Apply, Analyze, Evaluate, Create]
    implementation:
      - VR scenarios with LLM-powered AI agents (multi-role)
      - Ethical dilemmas (deepfakes, bias, transparency)
      - Real-time adaptive difficulty via cognitive load detection
    zpd_integration:
      - Full Support: Guided scenario with hints
      - Partial: Scenario with on-demand AI tutor
      - Minimal: Open scenario, AI tutor passive
      - Autonomy: User creates scenarios for peers (MKO)

  multimodal_assessment:
    name: "Engagement Analytics"
    description: Eye-tracking + interaction data for AI literacy assessment
    evidence: Personalized Immersive Classroom (#17), Eye Tracking Cognitive Load (#18)
    implementation:
      - Gaze patterns → attention to AI transparency cues
      - Interaction timing → decision-making quality
      - Self-regulation metrics → metacognitive awareness
```

### HPC Courses

```yaml
VR_XR_Modality:
  vr_immersive:
    name: "Virtual HPC Datacenter"
    description: VR simulation of HPC cluster operations
    evidence: VR Manufacturing Training (#6), Immersive VR Engineering (#14), SimWorld (#10)
    bloom_levels: [Understand, Apply, Analyze]
    implementation:
      - VR cluster environment (nodes, racks, scheduler visualization)
      - Practice job submission in immersive environment
      - Visualize parallel computation (MPI ranks, OpenMP threads)
      - Debug in VR (see data flow, identify bottlenecks)
    zpd_integration:
      - Full Support: Guided tour with annotations
      - Partial: Free exploration with hints
      - Minimal: Challenge mode (find the bug)
      - Autonomy: Optimize a provided cluster configuration

  ar_overlay:
    name: "HPC Companion"
    description: AR guidance overlaid on real terminal/HPC interface
    evidence: WeldAR in-situ guidance (#13), AR Facial Training (#9)
    bloom_levels: [Remember, Understand, Apply]
    implementation:
      - SBATCH directive hints overlaid on editor
      - Real-time job status in peripheral vision
      - Error explanations when jobs fail
      - Command reference floating panel
    zpd_integration:
      - Full Support: All commands annotated
      - Partial: Only errors annotated
      - Minimal: Only on user request
      - Autonomy: Pure terminal, no overlay

  cognitive_load_adaptation:
    name: "Adaptive HPC Difficulty"
    description: Real-time difficulty adjustment via cognitive load
    evidence: CLAd-VR (#5), Physiological Adaptation (#7), Eye Tracking Cognitive Load (#18)
    implementation:
      - Monitor cognitive load (eye tracking, interaction patterns)
      - Adjust job complexity in real-time
      - Reduce parallelism when overloaded
      - Increase complexity when in autonomy zone
```

---

## 📋 Implementation Roadmap (VR/XR Extension)

### Phase 1: AR Overlay (Month 4-6) — After text/SRS baseline
- [ ] **ki-kompetenz-training:** Prototype "AI Transparency Lens" AR overlay
  - Start with web-based AR (WebXR) for accessibility
  - Overlay AI disclosure prompts on ChatGPT/Copilot usage
  - Map to Bloom: Understand, Apply
- [ ] **HPC Courses:** Prototype "HPC Companion" AR overlay
  - SBATCH directive hints on terminal
  - Job status in peripheral vision
  - Map to Bloom: Remember, Understand, Apply

### Phase 2: VR Scenarios (Month 7-9) — After AR validation
- [ ] **ki-kompetenz-training:** "AI Scenario Lab" VR prototype
  - Ethical dilemma roleplay with LLM agents
  - Adaptive difficulty via interaction timing
  - Map to Bloom: Apply, Analyze, Evaluate
- [ ] **HPC Courses:** "Virtual HPC Datacenter" VR prototype
  - Cluster operations simulation
  - Job submission practice
  - Map to Bloom: Understand, Apply, Analyze

### Phase 3: Multimodal Assessment (Month 10-12)
- [ ] Integrate eye-tracking for engagement measurement
- [ ] Add cognitive load detection (interaction-based proxy)
- [ ] Implement physiological ZPD adjustment
- [ ] Map multimodal data to Bloom-level mastery

### Phase 4: Autonomy & Creation (Month 12+)
- [ ] VR creation mode (users build scenarios)
- [ ] Peer teaching in VR (MKO — More Knowledgeable Other)
- [ ] Cross-platform VR scenarios (AI literacy ↔ HPC)

---

## 📊 VR/XR Metrics (Additional)

### Modality Adoption
| Metric | Target |
|--------|--------|
| AR overlay usage | 40%+ of sessions |
| VR scenario completion | 70%+ for enrolled |
| AR-assisted success rate | +10% vs. text-only |
| VR engagement duration | 15-25 min (optimal) |

### Cognitive Load Management
| Metric | Target |
|--------|--------|
| Time in optimal ZPD (VR) | 70%+ of VR session |
| Cognitive overload events | <10% of sessions |
| Scaffold fade rate (VR) | Full→Autonomy in <5 VR sessions |

### Learning Effectiveness
| Metric | Text-only | VR/XR Target |
|--------|-----------|--------------|
| Retention (30-day) | 60% | 70%+ |
| Application transfer | 40% | 55%+ |
| Engagement | 3.5/5 | 4.3/5 |

---

## 🔬 Evidence Confidence

| Claim | Evidence Strength | Papers |
|-------|-------------------|--------|
| VR training is effective for skill acquisition | ★★★★★ | #1, #5, #6, #14 |
| Cognitive load can be detected in VR | ★★★★☆ | #5, #7, #8, #11, #18 |
| AR in-situ guidance improves training | ★★★★☆ | #9, #13, #20 |
| LLM agents can serve as pedagogical tutors in VR | ★★★☆☆ | #3, #15, #16 |
| Multimodal data improves assessment | ★★★★☆ | "Assessing Learning Processes with Multimodal Data" |
| VR improves accessibility for diverse learners | ★★★★☆ | #12, #20, EscFOA |
| Presence enhances learning outcomes | ★★★☆☆ | #4 (systematic review) |

---

## 📚 References (Top 10 for Implementation)

1. **CLAd-VR** — Cognitive load adaptive training (arXiv:2510.05249)
2. **Adaptive Instructions in VR** — Cognitive load theory in VR (arXiv:2507.20943)
3. **Open TutorAI** — Open-source personalized immersive AI (arXiv:2602.07176)
4. **Physiological Adaptation for VR** — Eye tracking + HRV (arXiv:2504.06461)
5. **WeldAR** — AR in-situ guidance for training (arXiv:2603.07959)
6. **LLM Pedagogical Agents in VR** — Multi-role adaptive agents (arXiv:2505.02699)
7. **Personalized Immersive Classroom** — Eye-tracking engagement (arXiv:2501.07883)
8. **Eye Tracking Cognitive Load in VR** — Complex training (arXiv:2411.12771)
9. **AR for Deaf Students** — Accessibility in experiential learning (arXiv:2604.00856)
10. **Presence in VR (Systematic Review)** — Presence across tasks (arXiv:2504.13845)

---

**This addendum extends:** `knowledge_tree_bloom_zpd.md`  
**Evidence base:** `focus_session_vr_xr_learning.md` + `vr_xr_reading_list.md`
