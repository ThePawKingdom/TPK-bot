def discord_time_format(time, source=None):
    if source:
        return f"<t:{int(time.timestamp())}:{source}>"
    return f"<t:{int(time.timestamp())}>"
