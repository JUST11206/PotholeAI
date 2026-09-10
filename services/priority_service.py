def calculate_priority(
    severity,
    confidence,
    report_count=1,
    traffic_level=1,
    road_importance=1
):

    severity_score = {
        "low": 20,
        "medium": 50,
        "high": 80,
        "critical": 100
    }

    severity_value = severity_score.get(
        severity.lower(),
        50
    )

    confidence_value = confidence * 100

    report_value = min(
        report_count * 10,
        100
    )

    traffic_value = min(
        traffic_level * 20,
        100
    )

    road_value = min(
        road_importance * 20,
        100
    )

    score = (
        severity_value * 0.40
        + confidence_value * 0.20
        + report_value * 0.15
        + traffic_value * 0.15
        + road_value * 0.10
    )

    if score >= 80:
        priority = "critical"

    elif score >= 60:
        priority = "high"

    elif score >= 40:
        priority = "medium"

    else:
        priority = "low"

    return round(score, 2), priority