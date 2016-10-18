#!/bin/bash

exec migrate -url postgres:///stock_research_v1?sslmode=disable -path ./migrations $@
