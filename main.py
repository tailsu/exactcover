from exactcover.polyomino import polyomino, decode_solution, encode_polyominoes, canonical, product, PENTOMINOES
from exactcover.draw import solutions_svg, COLOURS


if __name__ == "__main__":
    region = set(product(range(8), repeat=2)) - set(product((3, 4), repeat=2))
    solution = next(polyomino(encode_polyominoes(PENTOMINOES), region))
    print(decode_solution(solution))
    solutions_svg([solution], 'solution-8x8.svg', colour=COLOURS.get)

    all_solutions = list(polyomino(encode_polyominoes(PENTOMINOES), region))
    print(len(all_solutions))

    unique_solutions = set(map(canonical, all_solutions))
    print(len(unique_solutions))
    solutions_svg(unique_solutions, 'all-8x8.svg', columns=13, colour=COLOURS.get)
