#!/bin/bash

git init

git lfs install

git remote remove origin 2>/dev/null || true
git remote add origin https://huggingface.co/spaces/sunil5990/supercart-sales-forecast

git add .

git commit -m "Deploy SuperCart Sales Forecast App"

git branch -M main

git push -u origin main