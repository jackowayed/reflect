import numpy as np
from numpy.testing import assert_array_equal

from reflect import *

def test_board():
    # note we have to escape a backslash
    blocks = """
....
../\\
.../
....
"""
    board = Board.create(hidden_blocks=blocks)
    assert_array_equal(
        board.values,
        np.array(
            [
                [".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", "."],
            ]
        ),
    )

    # assert str(board).strip() == blocks.strip()

    # corners
    assert board.on_edge(0, 0) == False
    assert board.on_edge(0, 5) == False
    assert board.on_edge(5, 0) == False
    assert board.on_edge(5, 5) == False

    assert board.on_inner_board(0, 0) == False
    assert board.on_inner_board(0, 5) == False
    assert board.on_inner_board(5, 0) == False
    assert board.on_inner_board(5, 5) == False

    # inner board
    assert board.on_edge(1, 1) == False
    assert board.on_edge(2, 1) == False

    assert board.on_inner_board(1, 1) == True
    assert board.on_inner_board(2, 1) == True

    # edges
    assert board.on_edge(1, 0) == True
    assert board.on_edge(0, 1) == True
    assert board.on_edge(4, 0) == True
    assert board.on_edge(0, 4) == True
    assert board.on_edge(1, 5) == True
    assert board.on_edge(5, 1) == True
    assert board.on_edge(4, 5) == True
    assert board.on_edge(5, 4) == True

    assert board.on_inner_board(1, 0) == False
    assert board.on_inner_board(0, 1) == False

    # hidden_board_ints
    assert_array_equal(board.hidden_blocks_ints,
        np.array(
            [
                [0, 0, 0, 0],
                [0, 0, 1, 2],
                [0, 0, 0, 1],
                [0, 0, 0, 0],
            ]
        ), 
    )

def test_full_board():
    full_board = """
....A.
......
......
.../\\A
B....B
...CC.
"""
    board = Board.create(full_board=full_board)
    # check that inner board does not show hidden blocks
    assert_array_equal(
        board.values,
        np.array(
            [
                [".", ".", ".", ".", "A", "."],
                [".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", "A"],
                ["B", ".", ".", ".", ".", "B"],
                [".", ".", ".", "C", "C", "."],
            ]
        ),
    )

    # note that the puzzle string doesn't show hidden blocks
    assert board.puzzle_string() == """....A.
......
......
.....A
B....B
...CC.

Blocks: /\\"""

    boardRot90 = board.rot90()

    assert_array_equal(
        boardRot90.values,
        np.array(
            [
                [".", ".", ".", "A", "B", "."],
                ["A", ".", ".", ".", ".", "C"],
                [".", ".", ".", ".", ".", "C"],
                [".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", "B", "."],
            ]
        ),
    )

    # note that mirrors are rotated too
    assert_array_equal(
        boardRot90.hidden_blocks,
        np.array(
            [
                [".", ".", "/", "."],
                [".", ".", "\\", ".",],
                [".", ".", ".", ".",],
                [".", ".", ".", ".",],
            ]
        ),
    )

    assert_array_equal(
        board.beams,
        np.array([
            [3, -1, 4, 2],
            [-1, 3, 4, 3],
            [2, 4, 3, 4],
        ], dtype=np.int8),
    )
    

def test_beam():
    blocks = """
....
../\\
.../
....
"""
    board = Board.create(hidden_blocks=blocks)
    assert_array_equal(board.pieces, ["/", "/", "\\"])
    path = board.beam(0, 1)
    assert_array_equal(path[-1], [5, 1])
    path = board.beam(0, 2)
    assert_array_equal(path[-1], [3, 0]) 
    path = board.beam(0, 3)
    assert_array_equal(path[-1], [3, 5]) 
    path = board.beam(1, 0)
    assert_array_equal(path[-1], [1, 5]) 
    path = board.beam(4, 0)
    assert_array_equal(path[-1], [5, 2])


