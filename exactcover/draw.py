from svgwrite import Drawing
from .polyomino import solution_bounds, _EMPTY, product

def solutions_svg(solutions, filename, columns=1, size=25, padding=5,
                  colour=lambda _: "white", stroke_colour="black",
                  stroke_width=3):
    """Format polyomino tilings as an SVG image.

    Required arguments:
    solutions -- iterable of solutions to the tiling problem, each of
        which is a sequence of piece placements, each of which is a
        tuple whose first element is the name of the piece, and whose
        second element is a sequence of pairs (i, j) giving the
        locations of the tiles in the piece.
    filename -- where to save the SVG drawing.

    Optional arguments:
    columns -- number of solutions per row (default: 1).
    size -- width and height of each tile (default: 25).
    padding -- padding around the image (default: 5)
    colour -- function taking a piece name and returning its colour
        (default: a function returning white for each piece).
    stroke -- stroke colour (default: black).
    stroke_width -- width of strokes between pieces (default: 3).

    """
    solutions = list(solutions)
    h, w = solution_bounds(solutions[0])
    rows = (len(solutions) + columns - 1) // columns
    drawing_size = (2 * padding + (columns * (w + 1) - 1) * size,
                    2 * padding + (rows    * (h + 1) - 1) * size)
    drawing = Drawing(debug=False, filename=filename, size=drawing_size)
    for i, solution in enumerate(solutions):
        y, x = divmod(i, columns)
        oj = padding + (x * (w + 1)) * size
        oi = padding + (y * (h + 1)) * size
        group = drawing.g(stroke=stroke_colour, stroke_linecap="round",
                          stroke_width=0.25)
        drawing.add(group)
        grid = [[_EMPTY] * w for _ in range(h)]
        for c, placing in solution:
            piece = drawing.g(fill=colour(c))
            group.add(piece)
            for i, j in placing:
                grid[i][j] = c
                piece.add(drawing.rect((j * size + oj, i * size + oi),
                                       (size, size)))
        edges = drawing.path(stroke_width=stroke_width)
        group.add(edges)
        for i, j in product(range(h + 1), range(w)):
            if ((_EMPTY if i == 0 else grid[i-1][j])
                != (_EMPTY if i == h else grid[i][j])):
                edges.push(['M', j * size + oj, i * size + oi, 'l', size, 0])
        for i, j in product(range(h), range(w + 1)):
            if ((_EMPTY if j == 0 else grid[i][j-1])
                != (_EMPTY if j == w else grid[i][j])):
                edges.push(['M', j * size + oj, i * size + oi, 'l', 0, size])
    drawing.save()

COLOURS = dict(I="#EEAAAA", F="#DDBB99", L="#CCCC88",
               P="#BBDD99", N="#AAEEAA", T="#99DDBB",
               U="#88CCCC", V="#99BBDD", W="#AAAAEE",
               X="#BB99DD", Y="#CC88CC", Z="#DD99BB")

