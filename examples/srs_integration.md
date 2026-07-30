# SRS Integration Examples

Complete examples for integrating the Spaced Repetition System into your platform.

## Python Examples

### Basic Usage

```python
from tools.spaced_repetition import SRS, Card

# Create SRS instance
srs = SRS()

# Create cards
card1 = srs.create_card("What is AI?", "Artificial Intelligence")
card2 = srs.create_card("What is ML?", "Machine Learning")

# Get due cards
due = srs.get_due_cards()
print(f"Cards due: {len(due)}")

# Review a card
result = srs.review_card(card1, quality=4)
print(f"Next review: {result['next_review']}")

# Get statistics
stats = srs.get_statistics()
print(f"Retention: {stats['retention_rate']}%")

# Save state
srs.save('my_srs.json')

# Load state
srs = SRS.load('my_srs.json')
```

### Batch Card Creation

```python
# Create multiple cards from content
concepts = [
    ("What is AI?", "Artificial Intelligence"),
    ("What is ML?", "Machine Learning"),
    ("What is DL?", "Deep Learning"),
]

for question, answer in concepts:
    srs.create_card(question, answer)

print(f"Created {len(srs.cards)} cards")
```

### Custom Review Schedule

```python
from datetime import datetime, timedelta

# Review with custom date
custom_date = datetime.now() + timedelta(days=1)
result = srs.review_card(card, quality=4, review_date=custom_date)
```

### Performance Tracking

```python
# Track performance over time
for i in range(10):
    card = srs.create_card(f"Question {i}", f"Answer {i}")
    srs.review_card(card, quality=4)

# Get statistics
stats = srs.get_statistics()
print(f"Total cards: {stats['total_cards']}")
print(f"Retention: {stats['retention_rate']}%")
```

## TypeScript/JavaScript Examples

### Basic Usage

```typescript
import { SRS, Card } from '@/lib/srs/core';

// Create SRS
const srs = new SRS();

// Create card
const card: Card = {
  id: 'card-1',
  userId: 'user-1',
  lessonId: 'lesson-1',
  question: 'What is AI?',
  answer: 'Artificial Intelligence',
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

### API Integration

```typescript
// GET /api/srs/due
const response = await fetch('/api/srs/due', {
  headers: { 'x-user-id': userId }
});
const { cards } = await response.json();

// POST /api/srs/review
const result = await fetch('/api/srs/review', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-user-id': userId
  },
  body: JSON.stringify({
    cardId: 'card-1',
    quality: 4
  })
});
const { result: reviewResult } = await response.json();
```

### React Component

```tsx
'use client';

import { useState, useEffect } from 'react';

export function SRSReviewer({ userId }) {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDueCards();
  }, []);

  const fetchDueCards = async () => {
    const response = await fetch('/api/srs/due', {
      headers: { 'x-user-id': userId }
    });
    const { cards } = await response.json();
    setCards(cards);
    setLoading(false);
  };

  const handleReview = async (cardId, quality) => {
    await fetch('/api/srs/review', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-user-id': userId
      },
      body: JSON.stringify({ cardId, quality })
    });
    fetchDueCards();
  };

  if (loading) return <div>Loading...</div>;
  if (cards.length === 0) return <div>No reviews due!</div>;

  return (
    <div>
      {cards.map(card => (
        <div key={card.id}>
          <h3>{card.question}</h3>
          <button onClick={() => handleReview(card.id, 4)}>
            Good
          </button>
        </div>
      ))}
    </div>
  );
}
```

## Database Integration

### PostgreSQL Schema

```sql
CREATE TABLE srs_cards (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  lesson_id VARCHAR(50) NOT NULL,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  interval INTEGER DEFAULT 0,
  repetitions INTEGER DEFAULT 0,
  stability FLOAT DEFAULT 1.0,
  difficulty FLOAT DEFAULT 5.0,
  next_review TIMESTAMP,
  last_reviewed TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_srs_user_due ON srs_cards(user_id, next_review);
```

### Prisma Integration

```prisma
model SRSCard {
  id          String   @id @default(uuid())
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  lessonId    String
  question    String
  answer      String
  interval    Int      @default(0)
  repetitions Int      @default(0)
  stability   Float    @default(1.0)
  difficulty  Float    @default(5.0)
  nextReview  DateTime?
  lastReviewed DateTime?
  createdAt   DateTime @default(now())
}
```

## Best Practices

### 1. Card Design

✅ Good:
- Atomic: One fact per card
- Clear: Unambiguous question
- Context: Enough information
- Useful: Important to remember

❌ Bad:
- Complex: Multiple concepts
- Vague: "What about X?"
- Trivial: Unimportant details

### 2. Review Quality

- Be honest with ratings
- 3 (Hard) is better than fake 4s
- Don't game the system
- Consistency matters more than perfection

### 3. Performance

- Batch card creation
- Cache due cards
- Lazy load performance data
- Use indexes for queries

### 4. Monitoring

- Track retention rates
- Monitor review completion
- Alert on low engagement
- A/B test parameters

---

**Contact:** ki-kompetenz-training@tobias-weiss.org  
**Based on:** 1,732 research papers
