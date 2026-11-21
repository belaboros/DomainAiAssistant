"""Write the API's OpenAPI schema to apps/ontology-builder/web/openapi.json.

Run after any change to the API: uv run python apps/ontology-builder/tools/export_openapi.py
(test_api_guards.py::test_openapi_json_matches_the_app fails while it is out of date).
"""

from __future__ import annotations

from ontology_builder.api import OPENAPI_PATH, export_openapi

if __name__ == "__main__":
    export_openapi()
    print(f"wrote {OPENAPI_PATH}")
