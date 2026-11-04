#!/usr/bin/env python3
"""Generate a local-reference mirror from immutable vendored schema snapshots."""

from __future__ import annotations

import argparse
import json
import posixpath
from pathlib import Path, PurePosixPath
from typing import Any


PUBLICSCHEMA_PREFIX = "https://publicschema.org/"
GEOJSON_GEOMETRY = "https://geojson.org/schema/Geometry.json"


def schema_sources(source: Path) -> dict[str, PurePosixPath]:
    sources: dict[str, PurePosixPath] = {}
    for path in sorted(source.glob("*.schema.json")):
        sources[f"{PUBLICSCHEMA_PREFIX}{path.name}"] = PurePosixPath(path.name)
    for path in sorted((source / "crvs").glob("*.schema.json")):
        sources[f"{PUBLICSCHEMA_PREFIX}crvs/{path.name}"] = (
            PurePosixPath("crvs") / path.name
        )
    sources[GEOJSON_GEOMETRY] = PurePosixPath("geojson/Geometry.schema.json")
    return sources


def local_ref(current: PurePosixPath, target: PurePosixPath, fragment: str) -> str:
    relative = posixpath.relpath(str(target), str(current.parent))
    if not relative.startswith("."):
        relative = f"./{relative}"
    return f"{relative}{fragment}"


def rewrite(
    value: Any, current: PurePosixPath, sources: dict[str, PurePosixPath]
) -> Any:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, child in value.items():
            if key == "$id":
                continue
            if key == "$ref" and isinstance(child, str):
                base, separator, suffix = child.partition("#")
                if base in sources:
                    fragment = f"#{suffix}" if separator else ""
                    result[key] = local_ref(current, sources[base], fragment)
                    continue
            result[key] = rewrite(child, current, sources)
        return result
    if isinstance(value, list):
        return [rewrite(child, current, sources) for child in value]
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    sources = schema_sources(args.source)
    for canonical, relative in sources.items():
        source_path = args.source / Path(relative)
        document = json.loads(source_path.read_text(encoding="utf-8"))
        mirrored = rewrite(document, relative, sources)
        destination = args.output / Path(relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(mirrored, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
