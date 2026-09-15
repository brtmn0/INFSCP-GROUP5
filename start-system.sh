#!/usr/bin/env bash

# Start the CargoHUB WMS API. Run from the repo `code/` dir, or from anywhere -
# we cd into `api/` so the `providers` / `models` / `processors` namespace
# packages resolve and the absolute ROOT_PATH in data_provider.py finds data/.
(cd api; python3 main.py)