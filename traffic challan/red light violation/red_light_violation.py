def point_in_quadrilateral(x, y):
    x1, y1, x2, y2, x3, y3, x4, y4 = 378, 119,350, 196,793, 195,793, 112
    def is_same_side(p1, p2, a, b):
        cp1 = (b[0] - a[0]) * (p1[1] - a[1]) - (b[1] - a[1]) * (p1[0] - a[0])
        cp2 = (b[0] - a[0]) * (p2[1] - a[1]) - (b[1] - a[1]) * (p2[0] - a[0])
        return cp1 * cp2 >= 0

    return (
        is_same_side((x, y), (x1, y1), (x2, y2), (x3, y3)) and
        is_same_side((x, y), (x2, y2), (x3, y3), (x4, y4)) and
        is_same_side((x, y), (x3, y3), (x4, y4), (x1, y1)) and
        is_same_side((x, y), (x4, y4), (x1, y1), (x2, y2))
    )