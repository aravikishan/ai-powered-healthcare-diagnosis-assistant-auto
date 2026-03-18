#!/bin/bash
set -e
echo "Starting AI-Powered Healthcare Diagnosis Assistant..."
uvicorn app:app --host 0.0.0.0 --port 9121 --workers 1
