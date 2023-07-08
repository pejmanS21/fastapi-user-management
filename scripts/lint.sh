#! /bin/bash

ruff check fastapi_user_management tests
black fastapi_user_management tests --check
