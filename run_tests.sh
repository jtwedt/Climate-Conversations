#!/bin/bash

set -x # trace each command
set -e # exit script if any command fails passing on the exit code

flake8 --exclude .venv
nosetests --with-coverage --cover-html --cover-html-dir=tests/cover --cover-package=play_webapp --cover-package=ClimateConversationsCore
