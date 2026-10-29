def solve(board):
    # Convert to mutable grid
    grid = [list(row) for row in board]
    digits = set('123456789')
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empties = []

    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v != '.':
                rows[r].add(v)
                cols[c].add(v)
                boxes[(r // 3) * 3 + c // 3].add(v)
            else:
                empties.append((r, c))

    def candidates(r, c):
        b = (r // 3) * 3 + c // 3
        return digits - rows[r] - cols[c] - boxes[b]

    def place(r, c, v):
        grid[r][c] = v
        rows[r].add(v)
        cols[c].add(v)
        boxes[(r // 3) * 3 + c // 3].add(v)

    def remove(r, c, v):
        grid[r][c] = '.'
        rows[r].discard(v)
        cols[c].discard(v)
        boxes[(r // 3) * 3 + c // 3].discard(v)

    def propagate():
        # Repeatedly fill forced cells and prune
        changed = True
        while changed:
            changed = False
            # Find cells with a single candidate
            for r, c in list(empties):
                if grid[r][c] != '.':
                    continue
                cand = candidates(r, c)
                if len(cand) == 0:
                    return False
                if len(cand) == 1:
                    v = next(iter(cand))
                    place(r, c, v)
                    empties.remove((r, c))
                    changed = True
            if changed:
                continue
            # Hidden singles: a digit that can only go in one cell within a unit
            for unit_type in range(3):
                for u in range(9):
                    for d in digits:
                        positions = []
                        if unit_type == 0:  # row
                            for c in range(9):
                                if grid[u][c] == '.' and d in candidates(u, c):
                                    positions.append((u, c))
                        elif unit_type == 1:  # col
                            for r in range(9):
                                if grid[r][u] == '.' and d in candidates(r, u):
                                    positions.append((r, u))
                        else:  # box
                            br = (u // 3) * 3
                            bc = (u % 3) * 3
                            for r in range(br, br + 3):
                                for c in range(bc, bc + 3):
                                    if grid[r][c] == '.' and d in candidates(r, c):
                                        positions.append((r, c))
                        if len(positions) == 1:
                            r, c = positions[0]
                            place(r, c, d)
                            empties.remove((r, c))
                            changed = True
                            break
                    if changed:
                        break
                if changed:
                    break
        return True

    def search():
        if not propagate():
            return False
        if not empties:
            return True
        # Choose cell with fewest candidates
        best = None
        best_cand = None
        for r, c in empties:
            cand = candidates(r, c)
            if best is None or len(cand) < len(best_cand):
                best = (r, c)
                best_cand = cand
                if len(cand) == 0:
                    return False
        r, c = best
        for v in best_cand:
            place(r, c, v)
            empties.remove((r, c))
            if search():
                return True
            remove(r, c, v)
            empties.append((r, c))
        return False

    search()
    return [''.join(row) for row in grid]
