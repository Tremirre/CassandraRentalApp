def name_to_tag(name: str) -> str:
    return name.lower().replace(" ", "_")


def chunks(lst: list, n: int) -> list[list]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
