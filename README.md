subfolders of this project each define their own sample miniature language.

SimpleBinExpression - left-to-right evaluated arithmetic expressions. supports only 0, 1, times, and plus.

DecimalCalculator - more sophisticated arithmetic expressions. Supports addition, subtraction, multiplication, division, parentheses, and decimal numbers of any length.

kbasic - an ad hoc, informally-specified, bug-ridden, slow, sort-of-functional language.

sample usage:

C:\parser>cd SimpleBinExpression

C:\parser\SimpleBinExpression>main.py

result of 1+1*1+1:

3

C:\parser\SimpleBinExpression>cd ../DecimalCalculator

C:\parser\DecimalCalculator>main.py

result of ((42)/(2)):

21

C:\parser\DecimalCalculator>cd ../kbasic

C:\parser\KBasic>main.py

0, 2, 4, 6, 8, 10, 12, 14, 16, 18
