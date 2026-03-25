#!/bin/bash

cd Assignment_4 || exit 1

echo "Running tests before commit..."
pytest test.py

status=$?

if [ $status -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
else
    echo "All tests passed! Proceeding with commit."
    exit 0
fi
