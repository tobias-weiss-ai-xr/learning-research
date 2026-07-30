#!/usr/bin/env python3
"""
Workshop Material Generator
Creates printable handouts, slides content, and exercises for Learn-to-Learn workshop.

Based on 13,204 research papers from learning-research corpus.

Usage: python3 workshop_generator.py
"""

from pathlib import Path
from datetime import datetime


def generate_handout():
    """Generate participant handout."""
    handout = """
================================================================================
LEARN-TO-LEARN WORKSHOP HANDBOOK
Evidence-Based Learning Mastery
================================================================================

Author: Tobias Weiss | KI-Kompetenz-Training
Based on: 13,204 research papers across 20 disciplines
Date: July 2026

================================================================================
TABLE OF CONTENTS
================================================================================

Day 1: Understanding How Learning Works
  Module 1: The Science of Memory
  Module 2: Active Learning vs. Passive Review
  Module 3: Managing Cognitive Load

Day 2: Building Your Personal Learning System
  Module 4: Spaced Repetition Systems
  Module 5: Adaptive Learning Strategies
  Module 6: Motivation and Metacognition
  Module 7: Putting It All Together

================================================================================
KEY PRINCIPLES AT A GLANCE
================================================================================

1. SPACED REPETITION (1,732 papers)
   • Review at increasing intervals: 1 day, 3 days, 1 week, 2 weeks, 1 month
   • Test yourself, don't just re-read
   • 70% forgotten within 24 hours without review

2. ACTIVE RECALL (1,732 papers)
   • Retrieval practice strengthens memory 2-3x more than passive review
   • Hide answers and force retrieval
   • Embrace the struggle—it's when learning happens

3. COGNITIVE LOAD (162 papers)
   • Working memory holds ~4±1 items
   • Chunk information into groups of 4-7
   • Eliminate distractions during learning

4. ADAPTIVE PERSONALIZATION (4,495 papers)
   • Target 70-80% success rate for optimal engagement
   • Adjust difficulty based on performance
   • One-size-fits-all fails 60%+ of learners

5. IMMEDIATE FEEDBACK (926 papers)
   • Immediate feedback for simple tasks
   • Explanatory feedback > correctness-only
   • Hints should scaffold, not give answers

6. MOTIVATION DESIGN (848 papers)
   • Self-Determination Theory: Autonomy, Competence, Relatedness
   • Visible progress maintains motivation
   • Habits > motivation for long-term success

7. SOCIAL LEARNING (562 papers)
   • Peer explanation helps both parties
   • Social accountability increases completion
   • Teaching others reinforces learning

================================================================================
MODULE 1: THE SCIENCE OF MEMORY
================================================================================

KEY FINDINGS

Working Memory Limits
• Holds ~4±1 items at once (not 7±2 as previously thought)
• Design learning to respect this limit
• Use external aids to offload working memory

The Forgetting Curve
• Without review: 70% forgotten in 24 hours, 90% in 1 week
• With spaced repetition: 80% retained after 1 month
• Reviews become more efficient over time

Encoding Strategies
• Multiple pathways = stronger memory
• Visual + verbal (dual-coding)
• Emotional engagement enhances consolidation

EXERCISE: Chunking Practice

Task: Memorize this list of 16 items:

apple  book   car    dog
egg    fish   grape  house
ice    juice  kite   lamp
moon   nest   orange piano

Strategy 1: Try to memorize all 16 at once (2 min)
Strategy 2: Chunk into groups of 4 (2 min)

Compare: Which was easier? Why?

ANSWER: Chunking reduces cognitive load by organizing items into meaningful groups.
Working memory can hold 4±1 chunks, where each chunk can contain multiple items.

================================================================================
MODULE 2: ACTIVE LEARNING VS. PASSIVE REVIEW
================================================================================

KEY FINDINGS

The Testing Effect
• Active recall strengthens memory 2-3x more than re-reading
• The struggle of retrieval IS the learning
• Testing before you feel ready is most effective

Question Types That Work
✓ Retrieval: "What are the 3 principles of X?"
✓ Application: "How would you use X in situation Y?"
✓ Explanation: "Explain X to someone who knows nothing"

✗ Recognition: "Which of these is X?" (too easy)
✗ Copy-paste: Just copying without processing

EXERCISE: Convert Passive to Active

Passive: "Read chapter 3 on project management"
Active: "After reading chapter 3, answer:
  1. What are the 5 phases of project management?
  2. Which phase do you struggle with most?
  3. How would you apply this to your current project?"

Your Turn: Convert 3 pieces of your own learning content

================================================================================
MODULE 3: MANAGING COGNITIVE LOAD
================================================================================

KEY FINDINGS

Types of Cognitive Load
• Intrinsic: Difficulty of material (can't change)
• Extraneous: Poor design, distractions (can reduce)
• Germane: Processing that builds understanding (want to increase)

Strategies to Reduce Extraneous Load
• Eliminate distractions (phone, notifications, tabs)
• Focus on one task at a time
• Use templates and checklists
• Clean, minimal interface design

Dual-Coding Principle
• Visual + verbal together > either alone
• Diagrams explain relationships
• Animations show processes
• Avoid text + narration (both use verbal channel)

EXERCISE: Environment Audit

Current Learning Environment:
• Phone notifications: ___ (on/off)
• Browser tabs open: ___
• Background noise: ___ (yes/no)
• Multitasking: ___ (yes/no)

Action Plan: Remove 3 distractions this week

================================================================================
MODULE 4: SPACED REPETITION SYSTEMS
================================================================================

KEY FINDINGS

How SRS Algorithms Work
• Review at the edge of forgetting
• Optimal intervals: Day 1, 3, 7, 14, 30, 90
• Adapt based on performance

Common Algorithms
• SM-2: Original Anki algorithm (simple, effective)
• FSRS: Modern algorithm (more accurate)
• Custom: Your own rules

Card Design Best Practices
✓ Atomic: One fact per card
✓ Clear: Unambiguous question
✓ Context: Enough information to answer
✓ Useful: Actually important to remember

✗ Too complex: Multiple concepts on one card
✗ Vague: "What about X?" (which aspect?)
✗ Trivial: Unimportant details

EXERCISE: Create Your SRS

Step 1: Choose your tool
□ Anki (free, powerful, cross-platform)
□ RemNote (notes + SRS)
□ Paper cards (simple, tactile)

Step 2: Create 10 cards for your current learning

Card Template:
Front: [Clear question]
Back: [Concise answer]
Tags: [topic, difficulty]

Step 3: Set up review schedule
□ Daily: 10-30 minutes
□ Time: [when will you review?]
□ Location: [where will you review?]

================================================================================
MODULE 5: ADAPTIVE LEARNING STRATEGIES
================================================================================

KEY FINDINGS

Self-Assessment
• Most people overestimate their knowledge
• Use "Feynman technique": Explain to a 10-year-old
• Track confidence vs. accuracy

Difficulty Adjustment
• Target 70-80% success rate
• If >85%: Increase difficulty
• If <60%: Add scaffolding
• Track and adjust regularly

Learning Pathways
• Map prerequisites for your goal
• Create multiple paths based on background
• Allow skipping for prior knowledge

EXERCISE: Design Your Learning Pathway

Goal: What do you want to learn?
_________________________________

Prerequisites: What do you need first?
_________________________________

Current State: Where are you now?
_________________________________

Path: What's your route from A to B?
_________________________________

Milestones: How will you know you're progressing?
_________________________________

================================================================================
MODULE 6: MOTIVATION AND METACOGNITION
================================================================================

KEY FINDINGS

Self-Determination Theory (SDT)
1. Autonomy: Choice and control over learning
2. Competence: Visible progress and mastery
3. Relatedness: Connection to others and purpose

Metacognitive Awareness
• Before: What do I already know? What do I want to learn?
• During: Am I understanding? (1-5 scale)
• After: What did I learn? What's still unclear?

Building Learning Habits
• Habit stacking: "After X, I will learn for 15 minutes"
• Environment design: Make learning easy, distraction hard
• Identity: "I am a learner" vs. "I'm trying to learn"

EXERCISE: Build Your Learning Habit

Trigger: What existing habit will you stack onto?
Example: "After morning coffee, I will review SRS cards"
Your trigger: _________________________________

Action: What exactly will you do?
Example: "Open Anki, complete daily reviews (10 min)"
Your action: _________________________________

Reward: How will you celebrate?
Example: "Check off on calendar, enjoy coffee"
Your reward: _________________________________

================================================================================
MODULE 7: PUTTING IT ALL TOGETHER
================================================================================

YOUR PERSONAL LEARNING SYSTEM

Memory: Which SRS? When do you review?
_________________________________

Practice: How do you practice actively?
_________________________________

Load: How do you manage cognitive load?
_________________________________

Adaptation: How do you adjust difficulty?
_________________________________

Motivation: What drives you? What habits?
_________________________________

Social: Who's your accountability partner?
_________________________________

90-DAY IMPLEMENTATION PLAN

Month 1:
  Week 1: _________________________________
  Week 2: _________________________________
  Week 3: _________________________________
  Week 4: _________________________________

Month 2:
  Focus: _________________________________
  Metrics: _________________________________

Month 3:
  Optimization: _________________________________
  Scaling: _________________________________

ACCOUNTABILITY

Accountability Partner: Who will check in weekly?
_________________________________

Public Commitment: Where will you share progress?
_________________________________

Learning Community: Who else is learning?
_________________________________

Progress Tracking: How will you measure success?
_________________________________

COMMITMENT CONTRACT

My Learning Goal: _________________________________
My System: _________________________________
My Timeline: _________________________________
My Accountability: _________________________________

Signature: _________________________________
Date: _________________________________

Share with your accountability partner

================================================================================
QUICK REFERENCE: DAILY ROUTINE
================================================================================

Morning (5 min):
□ Review SRS cards
□ Check learning goals
□ Set intention for the day

Learning Session (25-50 min):
□ Remove distractions
□ Active recall practice
□ Take breaks (Pomodoro)
□ Self-assess understanding

Evening (5 min):
□ Quick review of key concepts
□ Plan tomorrow's learning
□ Log progress

Weekly (30 min):
□ Review weekly progress
□ Adjust difficulty if needed
□ Plan next week
□ Connect with accountability partner

================================================================================
RESOURCES
================================================================================

Recommended Tools
• Spaced Repetition: Anki, RemNote, SuperMemo
• Note-taking: Obsidian, Notion, Roam Research
• Habit Tracking: Streaks, Habitica, Loop
• Focus: Forest, Freedom, Cold Turkey

Recommended Reading
• "Make It Stick" by Brown, Roediger, McDaniel
• "A Mind for Numbers" by Barbara Oakley
• "Ultralearning" by Scott Young
• "Learning How to Learn" (Coursera course)

Contact
Tobias Weiss | KI-Kompetenz-Training
ki-kompetenz-training@tobias-weiss.org
www.ki-kompetenz-training.org

================================================================================
© 2026 KI-Kompetenz-Training | Tobias Weiss | ki-kompetenz-training.org
Based on analysis of 13,204 research papers across 20 academic disciplines.
================================================================================
"""
    return handout


def generate_slides_content():
    """Generate slide content for presentation."""
    slides = []
    
    slide_templates = [
        {
            "title": "LEARN-TO-LEARN WORKSHOP",
            "subtitle": "Evidence-Based Learning Mastery",
            "content": [
                "Based on 13,204 research papers",
                "20 academic disciplines",
                "62 years of research",
                "",
                "Tobias Weiss | KI-Kompetenz-Training"
            ]
        },
        {
            "title": "WORKSHOP GOALS",
            "content": [
                "✓ Understand how memory and learning work",
                "✓ Apply spaced repetition to your learning",
                "✓ Design effective study sessions",
                "✓ Implement adaptive learning strategies",
                "✓ Build personal learning systems"
            ]
        },
        {
            "title": "THE 7 EVIDENCE-BASED PRINCIPLES",
            "content": [
                "1. Spaced Repetition (1,732 papers)",
                "2. Active Recall (1,732 papers)",
                "3. Cognitive Load (162 papers)",
                "4. Adaptive Personalization (4,495 papers)",
                "5. Immediate Feedback (926 papers)",
                "6. Motivation Design (848 papers)",
                "7. Social Learning (562 papers)"
            ]
        },
        {
            "title": "PRINCIPLE 1: SPACED REPETITION",
            "content": [
                "KEY FINDING: 70% forgotten within 24 hours",
                "",
                "Optimal intervals:",
                "  • Day 1: Initial learning",
                "  • Day 3: First review",
                "  • Day 7: Second review",
                "  • Day 14: Third review",
                "  • Day 30: Fourth review",
                "  • Day 90: Final review"
            ]
        },
        {
            "title": "PRINCIPLE 2: ACTIVE RECALL",
            "content": [
                "KEY FINDING: Testing strengthens memory 2-3x",
                "",
                "DO:",
                "  ✓ Test yourself before you feel ready",
                "  ✓ Hide answers and force retrieval",
                "  ✓ Embrace the struggle",
                "",
                "DON'T:",
                "  ✗ Just re-read content",
                "  ✗ Highlight without processing"
            ]
        },
        {
            "title": "PRINCIPLE 3: COGNITIVE LOAD",
            "content": [
                "KEY FINDING: Working memory holds ~4±1 items",
                "",
                "Strategies:",
                "  • Chunk into groups of 4-7",
                "  • Eliminate distractions",
                "  • Use dual-coding (visual + text)",
                "  • Progressive disclosure"
            ]
        },
        {
            "title": "YOUR TURN: Chunking Exercise",
            "content": [
                "Memorize this list (2 min):",
                "",
                "apple  book   car    dog",
                "egg    fish   grape  house",
                "ice    juice  kite   lamp",
                "moon   nest   orange piano",
                "",
                "Strategy 1: All 16 at once",
                "Strategy 2: Chunk into groups of 4",
                "",
                "Which was easier? Why?"
            ]
        },
        {
            "title": "SPACED REPETITION IN PRACTICE",
            "content": [
                "Tools:",
                "  • Anki (free, powerful)",
                "  • RemNote (notes + SRS)",
                "  • Paper cards (simple)",
                "",
                "Daily routine:",
                "  • 10-30 minutes",
                "  • Same time each day",
                "  • Don't let reviews pile up"
            ]
        },
        {
            "title": "BUILD YOUR HABIT",
            "content": [
                "Habit Formula:",
                "",
                "WHEN [trigger], I will [action]",
                "THEN I will [reward]",
                "",
                "Example:",
                "WHEN I finish morning coffee,",
                "I will review SRS cards (10 min)",
                "THEN I check off on calendar"
            ]
        },
        {
            "title": "NEXT STEPS",
            "content": [
                "1. Set up your SRS today",
                "2. Create 10 cards for current learning",
                "3. Schedule daily reviews",
                "4. Find accountability partner",
                "5. Start the 90-day plan",
                "",
                "Remember: Consistency > Intensity"
            ]
        }
    ]
    
    for i, slide in enumerate(slide_templates, 1):
        slide_content = f"""
SLIDE {i}: {slide['title']}
{'=' * 50}
{slide['subtitle'] + chr(10) + chr(10) if 'subtitle' in slide else ''}
{chr(10).join(['  • ' + line for line in slide['content']])}
"""
        slides.append(slide_content)
    
    return '\n'.join(slides)


def generate_exercises():
    """Generate exercise worksheets."""
    exercises = """
================================================================================
WORKSHOP EXERCISES
================================================================================

EXERCISE 1: Memory Chunking (15 min)
-------------------------------------
Task: Memorize these 16 items

Strategy A: All at once (2 min)
Strategy B: Chunk into 4 groups (2 min)

Items:
apple  book   car    dog
egg    fish   grape  house
ice    juice  kite   lamp
moon   nest   orange piano

Test yourself after 5 minutes:
1. ________________  6. ________________  11. ________________
2. ________________  7. ________________  12. ________________
3. ________________  8. ________________  13. ________________
4. ________________  9. ________________  14. ________________
5. ________________  10. _______________  15. ________________
                        16. ________________

Score: ___/16


EXERCISE 2: Active Recall Practice (20 min)
--------------------------------------------
Read this short passage (2 min):

"Spaced repetition is a learning technique that incorporates increasing 
intervals of time between reviews of previously learned material to exploit 
the psychological spacing effect. The technique relies on the sequencing of 
review sessions based on the strength of each memory trace."

Now, without looking at the passage, answer:

1. What is spaced repetition?
_______________________________________________________________

2. What does it incorporate?
_______________________________________________________________

3. What psychological effect does it exploit?
_______________________________________________________________

4. What does the technique rely on?
_______________________________________________________________

Compare with original. How many did you get right? ___/4


EXERCISE 3: SRS Card Creation (30 min)
---------------------------------------
Create 10 high-quality flashcards for your current learning

Card 1:
Front: _________________________________________________
Back:  _________________________________________________
Tags:  _________________________________________________

Card 2:
Front: _________________________________________________
Back:  _________________________________________________
Tags:  _________________________________________________

[Continue for 10 cards...]


EXERCISE 4: Learning Environment Audit (15 min)
------------------------------------------------
Rate your current learning environment:

Distraction Level (1-5):
• Phone notifications: ___
• Browser tabs open: ___  
• Background noise: ___
• Multitasking tendency: ___

Top 3 distractions to remove:
1. _________________________________________________
2. _________________________________________________
3. _________________________________________________

Action plan for this week:
_______________________________________________________________


EXERCISE 5: Habit Design (20 min)
----------------------------------
Design your daily learning habit using the formula:

WHEN [existing habit], I will [new learning behavior]
THEN I will [reward]

Example:
WHEN I finish morning coffee, I will review SRS cards (10 min)
THEN I check off on my calendar and enjoy my coffee

Your habit:
WHEN _________________________________________________
I will _______________________________________________
THEN _________________________________________________

Start date: _______________


EXERCISE 6: Learning Pathway Mapping (25 min)
----------------------------------------------
Goal: What do you want to learn?
_______________________________________________________________

Current state: Where are you now?
_______________________________________________________________

Prerequisites: What do you need first?
_______________________________________________________________

Milestones: How will you know you're progressing?
_______________________________________________________________

Timeline: When do you want to achieve this?
_______________________________________________________________

Resources: What materials/tools will you use?
_______________________________________________________________


EXERCISE 7: 90-Day Implementation Plan (20 min)
------------------------------------------------
Month 1 - Foundation:
Week 1: _________________________________________________
Week 2: _________________________________________________
Week 3: _________________________________________________
Week 4: _________________________________________________

Month 2 - Enhancement:
Focus: _________________________________________________
Metrics: _______________________________________________

Month 3 - Optimization:
Optimization: __________________________________________
Scaling: _______________________________________________


EXERCISE 8: Accountability Contract (10 min)
---------------------------------------------
My Learning Goal:
_______________________________________________________________

My System:
_______________________________________________________________

My Timeline:
_______________________________________________________________

My Accountability Partner:
Name: ___________________  Email: ___________________

I commit to this learning journey.

Signature: ___________________  Date: _______________

Share with your accountability partner today!

================================================================================
© 2026 KI-Kompetenz-Training | Tobias Weiss | ki-kompetenz-training.org
================================================================================
"""
    return exercises


def main():
    """Generate all workshop materials."""
    print("=" * 70)
    print("WORKSHOP MATERIAL GENERATOR")
    print("=" * 70)
    
    output_dir = Path("workshop-repo/workshop_materials")
    output_dir.mkdir(exist_ok=True)
    
    # Generate handout
    print("\nGenerating participant handout...")
    handout = generate_handout()
    handout_path = output_dir / "handout.txt"
    with open(handout_path, 'w', encoding='utf-8') as f:
        f.write(handout)
    print(f"  ✓ Saved to: {handout_path}")
    
    # Generate slides
    print("\nGenerating slide content...")
    slides = generate_slides_content()
    slides_path = output_dir / "slides_content.txt"
    with open(slides_path, 'w', encoding='utf-8') as f:
        f.write(slides)
    print(f"  ✓ Saved to: {slides_path}")
    
    # Generate exercises
    print("\nGenerating exercises...")
    exercises = generate_exercises()
    exercises_path = output_dir / "exercises.txt"
    with open(exercises_path, 'w', encoding='utf-8') as f:
        f.write(exercises)
    print(f"  ✓ Saved to: {exercises_path}")
    
    # Generate instructor notes
    print("\nGenerating instructor notes...")
    instructor_notes = """
================================================================================
INSTRUCTOR NOTES - LEARN-TO-LEARN WORKSHOP
================================================================================

TIMING GUIDE
------------
Day 1:
  Module 1: Science of Memory (90 min)
    - Lecture: 45 min
    - Exercise: 15 min
    - Discussion: 30 min
  
  Module 2: Active vs. Passive (90 min)
    - Lecture: 40 min
    - Exercise: 25 min
    - Discussion: 25 min
  
  Module 3: Cognitive Load (90 min)
    - Lecture: 35 min
    - Exercise: 20 min
    - Discussion: 35 min

Day 2:
  Module 4: SRS Systems (90 min)
    - Lecture: 35 min
    - Exercise: 30 min
    - Q&A: 25 min
  
  Module 5: Adaptive Learning (90 min)
    - Lecture: 35 min
    - Exercise: 30 min
    - Discussion: 25 min
  
  Module 6: Motivation (90 min)
    - Lecture: 35 min
    - Exercise: 25 min
    - Discussion: 30 min
  
  Module 7: Putting Together (90 min)
    - Exercise: 45 min
    - Presentations: 30 min
    - Closing: 15 min

KEY TALKING POINTS
------------------
Module 1:
• Emphasize 4±1 working memory limit
• Show forgetting curve graph
• Demonstrate chunking with exercise

Module 2:
• Share personal example of testing effect
• Show before/after quiz scores
• Emphasize struggle = learning

Module 3:
• Help participants identify their distractions
• Show examples of good vs. bad design
• Practice dual-coding together

Module 4:
• Install Anki together (if possible)
• Create cards in real-time
• Set up daily review schedule

Module 5:
• Discuss prior knowledge assessment
• Show adaptive difficulty examples
• Map learning pathways together

Module 6:
• Discuss SDT components
• Help design personal habits
• Connect to larger purpose

Module 7:
• Review all components
• Ensure commitment contracts signed
• Set up accountability check-ins

COMMON QUESTIONS
----------------
Q: "I don't have time for SRS"
A: Start with 5 minutes/day. Better than nothing.

Q: "Is this just for memorization?"
A: No, applies to all learning. Understanding requires memory.

Q: "What if I miss a day?"
A: Don't panic. Just continue. Consistency > perfection.

Q: "How long until I see results?"
A: 2-4 weeks for habit, 3 months for measurable improvement.

Q: "Which SRS tool is best?"
A: Anki for power, RemNote for notes, paper for simplicity.

TROUBLESHOOTING
---------------
• Participants overwhelmed → Focus on 1-2 principles first
• Low engagement → More exercises, less lecture
• Technical issues → Have paper backup
• Time running out → Prioritize Modules 1, 2, 4, 7

SUCCESS METRICS
---------------
• Participants create SRS deck with 10+ cards
• Everyone designs learning habit
• Commitment contracts signed
• Accountability partners assigned
• 30-day follow-up scheduled

================================================================================
© 2026 KI-Kompetenz-Training | Tobias Weiss | ki-kompetenz-training.org
================================================================================
"""
    instructor_path = output_dir / "instructor_notes.txt"
    with open(instructor_path, 'w', encoding='utf-8') as f:
        f.write(instructor_notes)
    print(f"  ✓ Saved to: {instructor_path}")
    
    print("\n" + "=" * 70)
    print("WORKSHOP MATERIALS READY!")
    print("=" * 70)
    print(f"\nOutput directory: {output_dir}")
    print("\nFiles generated:")
    print("  • handout.txt - Participant handbook")
    print("  • slides_content.txt - Slide content for presentation")
    print("  • exercises.txt - Exercise worksheets")
    print("  • instructor_notes.txt - Instructor guide")
    print("\nNext steps:")
    print("  1. Review materials for your specific audience")
    print("  2. Create slides from slides_content.txt")
    print("  3. Print handouts and exercises")
    print("  4. Practice timing")
    print("  5. Book venue or set up virtual meeting")


if __name__ == "__main__":
    main()
