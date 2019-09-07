#!/usr/bin/env bash

gcloud beta emulators datastore start --no-legacy --data-dir=. --project test --host-port "localhost:8001"
