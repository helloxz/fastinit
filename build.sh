#!/bin/bash
docker rmi helloz/fastinit
docker build --no-cache -t helloz/fastinit .
docker push helloz/fastinit