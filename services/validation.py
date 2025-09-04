def clamp_duration(mins: int, lower: int = 5, upper: int = 60) -> int:
    mins = max(lower, mins)
    mins = min(upper, mins)
    return mins
