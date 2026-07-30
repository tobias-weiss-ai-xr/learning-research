# Implementation Tools

Production-ready tools for applying evidence-based learning principles from 13,204 research papers.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run audit
python3 tools/platform_audit.py

# Run SRS demo
python3 tools/spaced_repetition.py

# Generate workshop materials
python3 tools/workshop_generator.py
```

## Tools

### 1. Platform Audit Tool

Interactive assessment of your learning platform against 7 evidence-based principles.

**Usage:**
```bash
# Interactive mode
python3 tools/platform_audit.py

# Non-interactive mode
python3 scripts/audit_assessment.py
```

**Features:**
- 28 questions across 7 principles
- Scoring (0-5 scale per principle)
- Prioritized recommendations
- JSON export

**Example Output:**
```
Total Score: 74/140
Overall Score: 52.9%

[HIGH] Spaced Repetition - 5%
[MEDIUM] Active Recall - 65%
```

### 2. Spaced Repetition System

Production SRS implementation using FSRS algorithm.

**Python Usage:**
```python
from tools.spaced_repetition import SRS, Card

srs = SRS()
card = srs.create_card("Question?", "Answer?")
result = srs.review_card(card, quality=4)
print(f"Next review: {result['next_review']}")
```

**Features:**
- FSRS algorithm (17 parameters)
- Card management
- Review scheduling
- Performance tracking
- Save/load state

### 3. Workshop Generator

Generate complete workshop materials.

**Usage:**
```bash
python3 tools/workshop_generator.py
```

**Output:**
- Participant handbook
- Slide content
- Exercise worksheets
- Instructor notes

## CLI Interface

```bash
# Interactive audit
python3 tools/cli.py audit

# SRS demo
python3 tools/cli.py srs demo

# Generate workshop
python3 tools/cli.py workshop
```

## API Reference

### SRS Class

```python
class SRS:
    def __init__(self, params: Optional[List[float]] = None)
    def create_card(self, question: str, answer: str, card_id: Optional[str] = None) -> Card
    def get_due_cards(self, reference_date: Optional[datetime] = None) -> List[Card]
    def review_card(self, card: Card, quality: int, review_date: Optional[datetime] = None) -> Dict
    def get_statistics(self) -> Dict
    def save(self, filepath: str)
    @classmethod
    def load(cls, filepath: str) -> SRS
```

### Card Dataclass

```python
@dataclass
class Card:
    id: str
    question: str
    answer: str
    created_at: str
    interval: int = 0
    repetitions: int = 0
    stability: float = 1.0
    difficulty: float = 5.0
    last_reviewed: Optional[str] = None
    next_review: Optional[str] = None
    review_count: int = 0
    performance_history: List[Dict] = field(default_factory=list)
```

## Configuration

### Custom FSRS Parameters

```python
custom_params = [
    0.5, 0.7, 2.5, 5.5, 5.0, 1.0, 0.9, 0.02, 1.5, 0.15,
    0.95, 2.2, 0.06, 0.35, 1.3, 0.3, 2.7
]
srs = SRS(params=custom_params)
```

### Audit Questions

Extend `AUDIT_QUESTIONS` in `platform_audit.py`:

```python
AUDIT_QUESTIONS = {
    "your_principle": {
        "name": "Principle Name",
        "evidence": "X papers",
        "questions": [...]
    }
}
```

## Testing

```bash
# Test SRS
python3 tools/spaced_repetition.py

# Test workshop generator
python3 tools/workshop_generator.py

# Test audit
python3 tools/platform_audit.py
```

## Troubleshooting

### Issue: SRS intervals too short
**Solution:** Adjust FSRS parameters or check quality ratings

### Issue: Audit doesn't match platform
**Solution:** Customize questions in `platform_audit.py`

### Issue: Workshop needs customization
**Solution:** Edit generator functions in `workshop_generator.py`

## Support

Contact: ki-kompetenz-training@tobias-weiss.org

---

**Version:** 1.0.0  
**Based on:** 13,204 research papers  
**Last Updated:** July 2026
