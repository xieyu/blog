---------------------- MODULE HourClock ------------
EXTENDS Naturals
VARIABLE hr

HCini == hr \in (1 .. 12)

HCnext == hr' = IF hr # 12 THEN hr + 1 ELSE 1

HC == HCini /\ [][HCnext]_hr
----------------------------------------------------
THEOREM HC => []HCini
====================================================
