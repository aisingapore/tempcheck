#!/bin/bash

cd ../../..
cd frontend && npm run build && cd ..
docker build . -t vishnu:latest