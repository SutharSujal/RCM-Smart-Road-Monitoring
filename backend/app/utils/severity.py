def calculate_severity(
    total_hazards: int,
    avg_hazard_area_ratio: float,
    repeated_occurrence_score: int,
) -> str:
    score = 0.0

    score += min(total_hazards / 8.0, 1.0) * 0.5
    score += min(avg_hazard_area_ratio / 0.08, 1.0) * 0.3
    score += min(repeated_occurrence_score / 6.0, 1.0) * 0.2

    if score >= 0.66:
        return "High"
    if score >= 0.33:
        return "Medium"
    return "Low"

