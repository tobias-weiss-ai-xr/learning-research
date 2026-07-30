#!/usr/bin/env python3
"""
Platform Audit Tool - Assess your learning platform against 7 evidence-based principles.
Based on 13,204 research papers from learning-research corpus.

Usage: python3 platform_audit.py
"""

import json
from datetime import datetime
from pathlib import Path

# Audit questions for each principle
AUDIT_QUESTIONS = {
    "spaced_repetition": {
        "name": "Spaced Repetition",
        "evidence": "1,732 papers on memory/retention",
        "questions": [
            {
                "id": "sr_1",
                "question": "Do you have any review/recall system?",
                "options": [
                    {"value": 0, "text": "No review system"},
                    {"value": 1, "text": "One-time review only"},
                    {"value": 2, "text": "Fixed interval reviews"},
                    {"value": 3, "text": "Performance-based intervals"},
                    {"value": 4, "text": "Adaptive algorithm (SM-2/FSRS)"},
                    {"value": 5, "text": "Fully adaptive with optimization"}
                ]
            },
            {
                "id": "sr_2",
                "question": "Is content revisited after initial learning?",
                "options": [
                    {"value": 0, "text": "No"},
                    {"value": 2, "text": "Sometimes"},
                    {"value": 5, "text": "Yes, systematically"}
                ]
            },
            {
                "id": "sr_3",
                "question": "Are there scheduled reviews at increasing intervals?",
                "options": [
                    {"value": 0, "text": "No"},
                    {"value": 2, "text": "Fixed intervals"},
                    {"value": 5, "text": "Adaptive intervals"}
                ]
            },
            {
                "id": "sr_4",
                "question": "Does the system adapt based on learner performance?",
                "options": [
                    {"value": 0, "text": "No"},
                    {"value": 3, "text": "Basic adaptation"},
                    {"value": 5, "text": "Advanced adaptation"}
                ]
            }
        ]
    },
    "active_recall": {
        "name": "Active Recall",
        "evidence": "1,732 papers on memory/retention",
        "questions": [
            {
                "id": "ar_1",
                "question": "Is most content passive (videos, readings)?",
                "options": [
                    {"value": 5, "text": "All passive content"},
                    {"value": 3, "text": "Some passive"},
                    {"value": 0, "text": "Mostly active"}
                ]
            },
            {
                "id": "ar_2",
                "question": "Are there quizzes/tests embedded in content?",
                "options": [
                    {"value": 0, "text": "No quizzes"},
                    {"value": 2, "text": "End-of-course only"},
                    {"value": 4, "text": "Some in content"},
                    {"value": 5, "text": "Frequent throughout"}
                ]
            },
            {
                "id": "ar_3",
                "question": "Do learners practice retrieval or just review?",
                "options": [
                    {"value": 0, "text": "Only review"},
                    {"value": 3, "text": "Mixed"},
                    {"value": 5, "text": "Primarily retrieval"}
                ]
            },
            {
                "id": "ar_4",
                "question": "Are answers hidden by default?",
                "options": [
                    {"value": 0, "text": "No"},
                    {"value": 3, "text": "Sometimes"},
                    {"value": 5, "text": "Always"}
                ]
            }
        ]
    },
    "adaptive_personalization": {
        "name": "Adaptive Personalization",
        "evidence": "4,495 papers on personalization",
        "questions": [
            {
                "id": "ap_1",
                "question": "Is content the same for all learners?",
                "options": [
                    {"value": 5, "text": "Yes, one-size-fits-all"},
                    {"value": 3, "text": "Some options"},
                    {"value": 0, "text": "Fully personalized"}
                ]
            },
            {
                "id": "ap_2",
                "question": "Is difficulty fixed or adaptive?",
                "options": [
                    {"value": 5, "text": "Fixed"},
                    {"value": 3, "text": "Manual selection"},
                    {"value": 0, "text": "Adaptive"}
                ]
            },
            {
                "id": "ap_3",
                "question": "Do you assess prior knowledge?",
                "options": [
                    {"value": 5, "text": "No assessment"},
                    {"value": 3, "text": "Optional"},
                    {"value": 0, "text": "Required pre-assessment"}
                ]
            },
            {
                "id": "ap_4",
                "question": "Are there multiple learning paths?",
                "options": [
                    {"value": 5, "text": "No paths"},
                    {"value": 3, "text": "2-3 paths"},
                    {"value": 0, "text": "Many adaptive paths"}
                ]
            }
        ]
    },
    "immediate_feedback": {
        "name": "Immediate Feedback",
        "evidence": "926 papers on feedback",
        "questions": [
            {
                "id": "fb_1",
                "question": "Do learners get feedback immediately?",
                "options": [
                    {"value": 5, "text": "No or delayed"},
                    {"value": 3, "text": "Sometimes"},
                    {"value": 0, "text": "Always immediate"}
                ]
            },
            {
                "id": "fb_2",
                "question": "Is feedback explanatory or just correct/incorrect?",
                "options": [
                    {"value": 5, "text": "Correct/incorrect only"},
                    {"value": 3, "text": "Basic explanations"},
                    {"value": 0, "text": "Detailed explanations"}
                ]
            },
            {
                "id": "fb_3",
                "question": "Are there hints available?",
                "options": [
                    {"value": 5, "text": "No hints"},
                    {"value": 3, "text": "Some hints"},
                    {"value": 0, "text": "Scaffolded hints"}
                ]
            },
            {
                "id": "fb_4",
                "question": "Is feedback personalized?",
                "options": [
                    {"value": 5, "text": "No"},
                    {"value": 3, "text": "Sometimes"},
                    {"value": 0, "text": "Always"}
                ]
            }
        ]
    },
    "cognitive_load": {
        "name": "Cognitive Load Management",
        "evidence": "162 papers on cognitive load",
        "questions": [
            {
                "id": "cl_1",
                "question": "Is content chunked appropriately?",
                "options": [
                    {"value": 5, "text": "No chunking"},
                    {"value": 3, "text": "Some chunking"},
                    {"value": 0, "text": "Optimal chunking (4-7 min)"}
                ]
            },
            {
                "id": "cl_2",
                "question": "Are there too many elements per screen?",
                "options": [
                    {"value": 5, "text": "Information-dense"},
                    {"value": 3, "text": "Moderate"},
                    {"value": 0, "text": "Focused, clean"}
                ]
            },
            {
                "id": "cl_3",
                "question": "Is visual design clean and focused?",
                "options": [
                    {"value": 5, "text": "Distracting"},
                    {"value": 3, "text": "Moderate"},
                    {"value": 0, "text": "Clean, focused"}
                ]
            },
            {
                "id": "cl_4",
                "question": "Are there unnecessary distractions?",
                "options": [
                    {"value": 5, "text": "Many"},
                    {"value": 3, "text": "Some"},
                    {"value": 0, "text": "None"}
                ]
            }
        ]
    },
    "motivation_design": {
        "name": "Motivation Design",
        "evidence": "848 papers on motivation",
        "questions": [
            {
                "id": "md_1",
                "question": "Do learners set goals?",
                "options": [
                    {"value": 5, "text": "No goal setting"},
                    {"value": 3, "text": "Optional"},
                    {"value": 0, "text": "Required at start"}
                ]
            },
            {
                "id": "md_2",
                "question": "Is progress visible?",
                "options": [
                    {"value": 5, "text": "No progress tracking"},
                    {"value": 3, "text": "Basic tracking"},
                    {"value": 0, "text": "Detailed visualization"}
                ]
            },
            {
                "id": "md_3",
                "question": "Are there mastery badges (not just completion)?",
                "options": [
                    {"value": 5, "text": "No badges"},
                    {"value": 3, "text": "Completion badges"},
                    {"value": 0, "text": "Mastery badges"}
                ]
            },
            {
                "id": "md_4",
                "question": "Is there social connection?",
                "options": [
                    {"value": 5, "text": "No social features"},
                    {"value": 3, "text": "Basic forums"},
                    {"value": 0, "text": "Rich social features"}
                ]
            }
        ]
    },
    "social_learning": {
        "name": "Social Learning",
        "evidence": "562 papers on social learning",
        "questions": [
            {
                "id": "sl_1",
                "question": "Do learners interact with each other?",
                "options": [
                    {"value": 5, "text": "No interaction"},
                    {"value": 3, "text": "Limited"},
                    {"value": 0, "text": "Rich interaction"}
                ]
            },
            {
                "id": "sl_2",
                "question": "Are there discussion forums?",
                "options": [
                    {"value": 5, "text": "No forums"},
                    {"value": 3, "text": "Basic forums"},
                    {"value": 0, "text": "Active forums"}
                ]
            },
            {
                "id": "sl_3",
                "question": "Is peer feedback available?",
                "options": [
                    {"value": 5, "text": "No peer feedback"},
                    {"value": 3, "text": "Optional"},
                    {"value": 0, "text": "Integrated"}
                ]
            },
            {
                "id": "sl_4",
                "question": "Are study groups possible?",
                "options": [
                    {"value": 5, "text": "No"},
                    {"value": 3, "text": "Manual"},
                    {"value": 0, "text": "Automated matching"}
                ]
            }
        ]
    }
}


def run_audit():
    """Run interactive audit and collect scores."""
    print("=" * 70)
    print("PLATFORM AUDIT TOOL")
    print("Based on 13,204 research papers from learning-research corpus")
    print("=" * 70)
    print()
    
    scores = {}
    total_possible = 0
    
    for principle_key, principle_data in AUDIT_QUESTIONS.items():
        print(f"\n{principle_data['name']}")
        print(f"Evidence: {principle_data['evidence']}")
        print("-" * 50)
        
        principle_score = 0
        max_principle_score = 0
        
        for q in principle_data['questions']:
            print(f"\n{q['question']}")
            for i, opt in enumerate(q['options']):
                print(f"  {i+1}. {opt['text']} (Score: {opt['value']})")
            
            while True:
                try:
                    choice = int(input("\nYour choice (1-6): ")) - 1
                    if 0 <= choice < len(q['options']):
                        selected_value = q['options'][choice]['value']
                        principle_score += selected_value
                        max_principle_score += 5
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a number.")
        
        scores[principle_key] = {
            'name': principle_data['name'],
            'score': principle_score,
            'max': max_principle_score,
            'percentage': (principle_score / max_principle_score * 100) if max_principle_score > 0 else 0
        }
        total_possible += max_principle_score
    
    return scores, total_possible


def generate_report(scores, total_possible):
    """Generate audit report."""
    total_score = sum(s['score'] for s in scores.values())
    total_percentage = (total_score / total_possible * 100) if total_possible > 0 else 0
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_score': total_score,
        'total_possible': total_possible,
        'total_percentage': total_percentage,
        'principles': scores,
        'recommendations': []
    }
    
    # Generate recommendations
    for key, data in scores.items():
        if data['percentage'] < 50:
            report['recommendations'].append({
                'principle': data['name'],
                'priority': 'HIGH',
                'current_score': f"{data['score']}/{data['max']}",
                'percentage': f"{data['percentage']:.1f}%",
                'action': f"Implement quick wins for {data['name']}"
            })
        elif data['percentage'] < 75:
            report['recommendations'].append({
                'principle': data['name'],
                'priority': 'MEDIUM',
                'current_score': f"{data['score']}/{data['max']}",
                'percentage': f"{data['percentage']:.1f}%",
                'action': f"Improve {data['name']} with medium-term features"
            })
    
    return report


def print_report(report):
    """Print formatted report."""
    print("\n" + "=" * 70)
    print("AUDIT RESULTS")
    print("=" * 70)
    
    print(f"\nTotal Score: {report['total_score']}/{report['total_possible']}")
    print(f"Overall Score: {report['total_percentage']:.1f}%")
    
    print("\n" + "-" * 70)
    print("PRINCIPLE SCORES")
    print("-" * 70)
    
    for key, data in report['principles'].items():
        bar_length = int(data['percentage'] / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"\n{data['name']:25} [{bar}] {data['percentage']:5.1f}%")
        print(f"  Score: {data['score']}/{data['max']}")
    
    print("\n" + "-" * 70)
    print("RECOMMENDATIONS")
    print("-" * 70)
    
    if report['recommendations']:
        for rec in sorted(report['recommendations'], key=lambda x: 0 if x['priority'] == 'HIGH' else 1):
            print(f"\n[{rec['priority']}] {rec['principle']}")
            print(f"  Current: {rec['current_score']} ({rec['percentage']})")
            print(f"  Action: {rec['action']}")
    else:
        print("\n✓ All principles scoring above 75%. Excellent!")
    
    print("\n" + "=" * 70)
    print("Benchmark: Industry average = 12-15/35 | Target = 28-35/35")
    print("=" * 70)


def save_report(report):
    """Save report to JSON file."""
    output_path = Path("docs/audit_results")
    output_path.mkdir(exist_ok=True)
    
    filename = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = output_path / filename
    
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✓ Report saved to: {filepath}")
    return filepath


def main():
    """Main function."""
    try:
        scores, total_possible = run_audit()
        report = generate_report(scores, total_possible)
        print_report(report)
        save_report(report)
        
        print("\n✓ Audit complete!")
        print("\nNext steps:")
        print("1. Review recommendations above")
        print("2. Start with HIGH priority items")
        print("3. See platform_implementation_plan.md for implementation guide")
        
    except KeyboardInterrupt:
        print("\n\nAudit cancelled.")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise


if __name__ == "__main__":
    main()
