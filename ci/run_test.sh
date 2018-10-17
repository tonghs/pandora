#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm test
