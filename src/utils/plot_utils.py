def revenue_formatter(x, pos):
    """
    Format revenue to millions or billions with a dollar sign
    """
    if x >= 1e9:
        value = x * 1e-9
        return f"${int(value)}B" if value.is_integer() else f"${value:.1f}B"
    elif x >= 1e6:
        value = x * 1e-6
        return f"${int(value)}M" if value.is_integer() else f"${value:.1f}M"
    return f"${x:.0f}"

