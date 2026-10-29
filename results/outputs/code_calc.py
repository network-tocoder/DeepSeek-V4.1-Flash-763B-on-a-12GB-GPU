def evaluate(expr: str) -> float:
    s = expr.replace(" ", "")
    if not s:
        raise ValueError("empty expression")

    pos = 0
    n = len(s)

    def peek():
        return s[pos] if pos < n else None

    def parse_expr():
        nonlocal pos
        value = parse_term()
        while pos < n and s[pos] in "+-":
            op = s[pos]
            pos += 1
            right = parse_term()
            if op == "+":
                value += right
            else:
                value -= right
        return value

    def parse_term():
        nonlocal pos
        value = parse_power()
        while pos < n and s[pos] in "*/":
            op = s[pos]
            pos += 1
            right = parse_power()
            if op == "*":
                value *= right
            else:
                if right == 0:
                    raise ValueError("division by zero")
                value /= right
        return value

    def parse_power():
        nonlocal pos
        base = parse_unary()
        if pos < n and s[pos] == "^":
            pos += 1
            exponent = parse_power()
            return base ** exponent
        return base

    def parse_unary():
        nonlocal pos
        if pos < n and s[pos] in "+-":
            sign = s[pos]
            pos += 1
            val = parse_unary()
            return -val if sign == "-" else val
        return parse_atom()

    def parse_atom():
        nonlocal pos
        if pos >= n:
            raise ValueError("unexpected end of expression")
        c = s[pos]
        if c == "(":
            pos += 1
            val = parse_expr()
            if pos >= n or s[pos] != ")":
                raise ValueError("missing closing parenthesis")
            pos += 1
            return val
        if c.isdigit() or c == ".":
            start = pos
            has_dot = False
            while pos < n and (s[pos].isdigit() or s[pos] == "."):
                if s[pos] == ".":
                    if has_dot:
                        raise ValueError("invalid number")
                    has_dot = True
                pos += 1
            if start == pos:
                raise ValueError("invalid number")
            return float(s[start:pos])
        raise ValueError("invalid character: " + c)

    result = parse_expr()
    if pos != n:
        raise ValueError("unexpected trailing characters")
    return result
