#!/bin/bash

npm run build

aws s3 sync dist s3://moger-admin-dev

aws cloudfront create-invalidation --distribution-id E2P9D801AOPE6E --paths "/*"
