import sys
import pytest

# Python importing from clahe/ to run tests
sys.path.insert(0, "clahe/")
import interpolation


@pytest.fixture
def interpolationData():
    tile_type_cache = {}

    tile_type = bgi.tiles[index]
    # Details the total number of boundaries of the current type of tile
    total_tile_type = 0

    if tile_type in tile_type_cache:
        total_tile_type = tile_type_cache[tile_type]

    else:
        # You can just initialize the tile_type_cache to have these keys and values, instead of doing this
        match tile_type:
            case boundaryGeneration.TileType.SINGLE_ARR_CORNER:
                total_tile_type = bgi.num_single_arr_corner_tiles * 1
            case boundaryGeneration.TileType.SINGLE_ARR_EDGE:
                total_tile_type = bgi.num_single_arr_edge_tiles * 2
            case boundaryGeneration.TileType.CORNER:
                total_tile_type = bgi.num_corner_tiles * 3
            case boundaryGeneration.TileType.EDGE:
                total_tile_type = bgi.num_edge_tiles * 5
            case boundaryGeneration.TileType.INNER:
                total_tile_type = bgi.num_inner_tiles * 8
            case _:
                total_tile_type = 1

        # cache in the calculation of the tile_type
        tile_type_cache[tile_type] = total_tile_type


# TODO: Write testers for the normal (num_horizontal_tiles >= 1 and num_vertical_tiles >= 1)padding sections
def test_1Dinterpolation():

    assert True == True


# TODO: Write testers for the edge cases (1D array of horizontal tiles or vertical tiles)
