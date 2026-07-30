#!/usr/bin/env python3
"""Unit Tests for SRS Implementation"""

import unittest
import sys
import tempfile
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.spaced_repetition import SRS, Card


class TestSRS(unittest.TestCase):
    def setUp(self):
        self.srs = SRS()
    
    def test_create_card(self):
        card = self.srs.create_card("Test Q", "Test A")
        self.assertIsNotNone(card.id)
        self.assertEqual(card.question, "Test Q")
        self.assertEqual(card.interval, 0)
    
    def test_first_review_quality_3(self):
        card = self.srs.create_card("Q", "A")
        result = self.srs.review_card(card, quality=3)
        self.assertEqual(result['interval'], 1)
    
    def test_first_review_quality_4(self):
        card = self.srs.create_card("Q", "A")
        result = self.srs.review_card(card, quality=4)
        self.assertEqual(result['interval'], 3)
    
    def test_first_review_quality_5(self):
        card = self.srs.create_card("Q", "A")
        result = self.srs.review_card(card, quality=5)
        self.assertEqual(result['interval'], 7)
    
    def test_invalid_quality(self):
        card = self.srs.create_card("Q", "A")
        with self.assertRaises(ValueError):
            self.srs.review_card(card, quality=0)
        with self.assertRaises(ValueError):
            self.srs.review_card(card, quality=6)
    
    def test_get_statistics(self):
        for i in range(5):
            card = self.srs.create_card(f"Q{i}", f"A{i}")
            self.srs.review_card(card, quality=4)
        stats = self.srs.get_statistics()
        self.assertEqual(stats['total_cards'], 5)
    
    def test_save_and_load(self):
        card = self.srs.create_card("Q", "A")
        self.srs.review_card(card, quality=4)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        self.srs.save(temp_path)
        loaded_srs = SRS.load(temp_path)
        
        self.assertEqual(len(loaded_srs.cards), 1)
        os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
