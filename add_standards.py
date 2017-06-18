#!/usr/bin/env python
"""
run the whole migration as:
    psql -U test test < truncate_standards.sql && envdir dev-config ./add_standards.py
"""
import logic as l

standards = ["If I can only make it to 5 talks this year, I want this to be one of the 5",
"I am pretty sure I have seen this talk before and it is great",
"I am pretty sure I have seen this talk before and it is OK, I’d be curious to see what else is there",
"I am pretty sure I have seen this talk before and let’s pass",
"I can be interested in this depending on the speaker",
"The information provided (and subsequent correspondence) did not provide enough information for me to be excited",
"The abstract is written poorly, I have doubts they will present well enough",]

for standard in standards: 
    l.add_standard(standard)
