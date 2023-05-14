#!/bin/bash

if [ $# -eq 1 ]; then
    k6 run $1
else
    k6 run small-concert.js
    k6 run presale.js
    k6 run general.js
    k6 run seating.js
    k6 run evening.js
fi

