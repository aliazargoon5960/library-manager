from collections import defaultdict

def normalize_pydantic_error_schema(errors: list) -> dict:
    data = defaultdict(dict)

    for error in errors:
        loc = error["loc"]
        msg = error.get("msg", "خطای نامشخص")

        current = data
        for idx, key in enumerate(loc):
            if isinstance(key, int):
                if key not in current:
                    current[key] = {}
                current = current[key]
            elif idx == len(loc) - 1:
                if key in current:
                    if isinstance(current[key], list):
                        current[key].append(msg)
                    else:
                        current[key] = [current[key], msg]
                else:
                    current[key] = [msg]
            else:
                if key not in current:
                    current[key] = {}
                current = current[key]

    return dict(data)
