def get(name, config=None):
    if name == "globalise":
        from .globalise import Globalise
        return Globalise(config)
    if name == "tanap":
        from .tanap import Tanap
        return Tanap(config)
    raise SystemExit(f"unknown corpus adapter {name}")
