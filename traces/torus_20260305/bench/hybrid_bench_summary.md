# Hybrid Solver Performance Summary

Config: m=3..10, 3 seeds each, restarts=30, steps=3000, temp=0.2

| m | success/trials | median runtime (s) | median accepted swaps | median restart | median step |
|---:|---:|---:|---:|---:|---:|
| 3 | 3/3 | 0.7836 | 1237.0 | 2.0 | 4.0 |
| 4 | 3/3 | 0.0255 | 17.0 | 2.0 | 39.0 |
| 5 | 3/3 | 3.4765 | 777.0 | 2.0 | 38.0 |
| 6 | 3/3 | 0.3983 | 90.0 | 3.0 | 200.0 |
| 7 | 3/3 | 3.0253 | 354.0 | 1.0 | 74.0 |
| 8 | 3/3 | 0.6272 | 52.0 | 1.0 | 133.0 |
| 9 | 3/3 | 0.7898 | 42.0 | 1.0 | 116.0 |
| 10 | 3/3 | 1.3527 | 48.0 | 1.0 | 149.0 |
