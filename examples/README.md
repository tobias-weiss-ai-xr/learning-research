# Examples

Practical examples for using the learning research tools.

## Table of Contents

- [Platform Audit](#platform-audit)
- [SRS Integration](#srs-integration)
- [Workshop Generation](#workshop-generation)

## Platform Audit

### Interactive Audit

```bash
cd tools
python3 platform_audit.py
```

### Non-Interactive (CI/CD)

```python
# scripts/audit_assessment.py
import json

# Create assessment file
assessment = {
    "spaced_repetition": {
        "sr_1": 3,  # Fixed interval reviews
        "sr_2": 1,  # Sometimes
        "sr_3": 1,  # Fixed intervals
        "sr_4": 1   # No adaptation
    },
    # ... other principles
}

with open('audit_assessment.json', 'w') as f:
    json.dump(assessment, f, indent=2)

# Run assessment
import subprocess
subprocess.run(['python3', 'audit_assessment.py'])
```

## SRS Integration

### Python Usage

```python
from tools.spaced_repetition import SRS, Card

# Create SRS
srs = SRS()

# Create cards
card1 = srs.create_card("What is SRS?", "Spaced repetition system")
card2 = srs.create_card("What is forgetting curve?", "Memory decay")

# Review cards
result = srs.review_card(card1, quality=4)
print(f"Next review: {result['next_review']}")

# Get due cards
due = srs.get_due_cards()
print(f"Cards due: {len(due)}")

# Save state
srs.save("my_srs.json")

# Load state
srs = SRS.load("my_srs.json")
```

### TypeScript Usage

```typescript
import { SRS, Card } from '@/lib/srs/core';

// Create SRS
const srs = new SRS();

// Create card
const card: Card = {
  id: 'card-1',
  userId: 'user-1',
  lessonId: 'lesson-1',
  question: 'What is SRS?',
  answer: 'Spaced repetition system',
  interval: 0,
  repetitions: 0,
  stability: 1.0,
  difficulty: 5.0,
  reviewCount: 0,
  createdAt: new Date()
};

// Review card
const result = srs.reviewCard(card, 4);
console.log(`Next review: ${result.nextReview}`);

// Get due cards
const due = srs.getDueCards();
console.log(`Cards due: ${due.length}`);
```

## Workshop Generation

```bash
# Generate materials
cd tools
python3 workshop_generator.py

# Output location
# workshop-repo/workshop_materials/
# ├── handout.txt
# ├── slides_content.txt
# ├── exercises.txt
# └── instructor_notes.txt
```

## API Integration

### REST API Example

```bash
# Get due cards
curl -X GET http://localhost:3000/api/srs/due \
  -H "x-user-id: user-123"

# Submit review
curl -X POST http://localhost:3000/api/srs/review \
  -H "Content-Type: application/json" \
  -H "x-user-id: user-123" \
  -d '{
    "cardId": "card-1",
    "quality": 4
  }'

# Create cards
curl -X POST http://localhost:3000/api/srs/cards \
  -H "Content-Type: application/json" \
  -H "x-user-id: user-123" \
  -d '{
    "lessonId": "lesson-1",
    "concepts": [
      {"question": "What?", "answer": "Answer"}
    ]
  }'
```
