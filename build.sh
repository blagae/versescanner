#!/bin/bash
cd versescanner/typescript
npm install
./node_modules/typescript/bin/tsc
npm run build
