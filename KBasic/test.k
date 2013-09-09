not = FUNCTION(x) BEGIN
    IF x THEN
        result = 0;
    ELSE
        result = 1;
    END;
    result;
END;

iseven = FUNCTION(x) BEGIN
    IF x % 2 EQUALS 0 THEN
        result = 1;
    ELSE
        result = 0;
    END;
    result;
END;

nexthailstone = FUNCTION(x) BEGIN
    IF iseven(x) THEN
        result = x / 2;
    ELSE
        result = 3 * x + 1;
    END;
    result;
END;

hailstonerepr = FUNCTION(x) BEGIN
    ret = "";
    WHILE not(x EQUALS 4) DO
        ret = ret + x;
        ret = ret + ", ";
        x = nexthailstone(x);
    END;
    ret = ret + "4";
    ret;
END;

fib = FUNCTION(func, x) BEGIN
    IF x < 2 THEN
        result = 1;
    ELSE
        a = func(func, x-1);
        b = func(func, x-2);
        result = a+b;
    END;
    result;
END;

ycomb = FUNCTION(func) BEGIN
    ret = FUNCTION(x) BEGIN
        result = func(func, x);
        result;
    END;
    ret;
END;

fibonacci = ycomb(fib);

test = FUNCTION() BEGIN
    i = 1;
    WHILE i < 100 DO
        result = hailstonerepr(i);
        PRINT i + ": " + result;
        i = i+1;
        PRINT "";
    END;
END;

tuple = FUNCTION(x, y) BEGIN
    ret = FUNCTION(z) BEGIN
        IF z THEN
            result = y;
        ELSE
            result = x;
        END;
        result;
    END;
    ret;
END;

first = FUNCTION(t) BEGIN
    t(0);
END;

rest = FUNCTION(t) BEGIN
    t(1);
END;

list = FUNCTION() BEGIN
    tuple(tuple(0,999), 999);
END;

isempty = FUNCTION(l) BEGIN
    IF rest(first(l)) EQUALS 999 THEN
        result = 1;
    ELSE
        result = 0;
    END;
    result;
END;

size = FUNCTION(l) BEGIN
    ret = 0;
    WHILE not(isempty(l)) DO
        ret = ret + 1;
        l = rest(l);
    END;
    ret;
END;

at = FUNCTION(l, x) BEGIN
    WHILE not(x EQUALS 0) DO
        x = x-1;
        l = rest(l);
    END;
    first(first(l));
END;

push = FUNCTION(l, item) BEGIN
    tuple(tuple(item, 0), l);
END;

range = FUNCTION(start, end, step) BEGIN
    ret = list();
    end = end - step;
    start = start - step;
    WHILE end > start DO
        ret = push(ret, end);
        end = end - step;
    END;
    ret;
END;

join = FUNCTION(seq, seperator) BEGIN
    ret = "";
    length = size(seq);
    i = 0;
    WHILE i < length DO
        item = at(seq, i);
        ret = ret + item;
        IF i+1 < length THEN
            ret = ret + seperator;
        END;
        i = i+1;
    END;
    ret;
END;

map = FUNCTION(func, seq) BEGIN
    ret = list();
    i = size(seq);
    WHILE i > 0 DO
        i = i-1;
        item = at(seq, i);
        item = func(item);
        ret = push(ret, item);
    END;
    ret;
END;

mult = FUNCTION(x) BEGIN 
    x*2;
END;

foo = list();
foo = range(0,10,1);
foo = map(FUNCTION(x) BEGIN x*2; END, foo); 
PRINT join(foo, ", ");