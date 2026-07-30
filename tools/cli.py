#!/usr/bin/env python3
"""
Command-Line Interface for Learning Research Tools
Provides easy access to all tools from the command line
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.platform_audit import run_audit, generate_report, print_report, save_report
from tools.spaced_repetition import SRS, Card


def cmd_audit(args):
    """Run platform audit."""
    print("=" * 70)
    print("PLATFORM AUDIT TOOL")
    print("=" * 70)
    
    if args.non_interactive:
        # Non-interactive mode
        try:
            with open(args.assessment_file, 'r') as f:
                answers = json.load(f)
            
            # Import non-interactive evaluator
            from scripts.audit_assessment import evaluate_assessment
            report = evaluate_assessment(answers)
            print_report(report)
            save_report(report)
        except FileNotFoundError:
            print(f"Error: Assessment file not found: {args.assessment_file}")
            sys.exit(1)
    else:
        # Interactive mode
        scores, total_possible = run_audit()
        report = generate_report(scores, total_possible)
        print_report(report)
        save_report(report)


def cmd_srs(args):
    """Spaced repetition commands."""
    srs = SRS()
    
    if args.command == 'create':
        """Create a new card."""
        card = srs.create_card(args.question, args.answer, args.id)
        print(f"✓ Created card: {card.id}")
        
    elif args.command == 'review':
        """Review a card."""
        try:
            with open(args.state_file, 'r') as f:
                data = json.load(f)
                srs.cards = {cid: Card.from_dict(cd) for cid, cd in data['cards'].items()}
        except FileNotFoundError:
            print("No saved state found. Creating new SRS.")
        
        if not srs.cards:
            print("No cards found. Create some first.")
            sys.exit(1)
        
        card = list(srs.cards.values())[0]
        result = srs.review_card(card, args.quality)
        print(f"✓ Reviewed card {card.id}")
        print(f"  Next review: {result['next_review']}")
        print(f"  Interval: {result['interval']} days")
        
        # Save state
        srs.save(args.state_file)
        
    elif args.command == 'stats':
        """Show statistics."""
        try:
            with open(args.state_file, 'r') as f:
                data = json.load(f)
                srs.cards = {cid: Card.from_dict(cd) for cid, cd in data['cards'].items()}
                srs.review_log = data.get('review_log', [])
        except FileNotFoundError:
            print("No saved state found.")
            sys.exit(1)
        
        stats = srs.get_statistics()
        print(f"Total cards: {stats['total_cards']}")
        print(f"Due today: {stats['due_today']}")
        print(f"Total reviews: {stats['total_reviews']}")
        print(f"Retention rate: {stats['retention_rate']}%")
        
    elif args.command == 'demo':
        """Run demo."""
        from tools.spaced_repetition import demo
        demo()
    
    else:
        print(f"Unknown SRS command: {args.command}")
        sys.exit(1)


def cmd_workshop(args):
    """Generate workshop materials."""
    from tools.workshop_generator import main
    main()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Learning Research Tools CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive audit
  python3 cli.py audit
  
  # Non-interactive audit
  python3 cli.py audit --non-interactive --assessment audit.json
  
  # SRS demo
  python3 cli.py srs demo
  
  # Generate workshop materials
  python3 cli.py workshop
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Audit command
    audit_parser = subparsers.add_parser('audit', help='Run platform audit')
    audit_parser.add_argument('--non-interactive', action='store_true',
                             help='Use assessment file instead of interactive')
    audit_parser.add_argument('--assessment', default='audit_assessment.json',
                             help='Assessment file for non-interactive mode')
    audit_parser.set_defaults(func=cmd_audit)
    
    # SRS command
    srs_parser = subparsers.add_parser('srs', help='Spaced repetition commands')
    srs_subparsers = srs_parser.add_subparsers(dest='command', help='SRS commands')
    
    # SRS create
    create_parser = srs_subparsers.add_parser('create', help='Create a new card')
    create_parser.add_argument('question', help='Card question')
    create_parser.add_argument('answer', help='Card answer')
    create_parser.add_argument('--id', help='Custom card ID')
    create_parser.set_defaults(func=cmd_srs)
    
    # SRS review
    review_parser = srs_subparsers.add_parser('review', help='Review a card')
    review_parser.add_argument('--quality', type=int, required=True,
                              help='Quality rating (1-5)')
    review_parser.add_argument('--state-file', default='docs/srs_state.json',
                              help='SRS state file')
    review_parser.set_defaults(func=cmd_srs)
    
    # SRS stats
    stats_parser = srs_subparsers.add_parser('stats', help='Show statistics')
    stats_parser.add_argument('--state-file', default='docs/srs_state.json',
                             help='SRS state file')
    stats_parser.set_defaults(func=cmd_srs)
    
    # SRS demo
    demo_parser = srs_subparsers.add_parser('demo', help='Run demo')
    demo_parser.set_defaults(func=cmd_srs)
    
    # Workshop command
    workshop_parser = subparsers.add_parser('workshop', help='Generate workshop materials')
    workshop_parser.set_defaults(func=cmd_workshop)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    args.func(args)


if __name__ == '__main__':
    main()
