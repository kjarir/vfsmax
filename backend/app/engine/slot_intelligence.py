from datetime import datetime, date
from typing import List, Optional
from app.schemas.monitoring import SlotMetadata


class SlotScorer:
    def __init__(self, preferred_dates: List[date] = [], preferred_centers: List[str] = []):
        self.preferred_dates = preferred_dates
        self.preferred_centers = preferred_centers

    def calculate_score(self, slot: SlotMetadata) -> int:
        """Calculates a score from 0-100 for a specific slot."""
        score = 50 # Base score

        # Date proximity (closer = better, vs further = better?)
        # Let's say user wants as soon as possible
        days_diff = (slot.slot_date.date() - date.today()).days
        if days_diff < 7: score += 30
        elif days_diff < 14: score += 15
        elif days_diff > 60: score -= 20
        
        # Center preference
        if slot.location in self.preferred_centers:
            score += 20
        
        # Preferred dates match
        if slot.slot_date.date() in self.preferred_dates:
            score += 40

        # Cap at 100
        return min(max(score, 0), 100)


def filter_slots(slots: List[SlotMetadata], threshold: int = 50) -> List[SlotMetadata]:
    """Filters slots below the user threshold."""
    return [s for s in slots if s.score >= threshold]
