#!/bin/bash


set -euo pipefail

mypy inventorymgr
pylint inventorymgr
exec pytest --cov inventorymgr --cov-branch --cov-report html tests
