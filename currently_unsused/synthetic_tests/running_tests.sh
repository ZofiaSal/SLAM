#!/bin/bash
cd synthetic_tests
for f in *test.py; do echo "$f"; python3 "$f"; done