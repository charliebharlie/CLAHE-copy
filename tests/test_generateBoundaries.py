import sys
import pytest  # type: ignore
import numpy as np  # type: ignore
import matplotlib.image as imgplt  # type: ignore


# Python importing from clahe/ to run tests
sys.path.append("clahe/")
sys.path.append("tests/")
from boundaryGeneration import generateBoundaries  # type: ignore
from errors import UnexpectedCaseError  # type: ignore
from errors import AssertionError  # type: ignore
from errors import DirectionError  # type: ignore


# Change the image file here
img_path = "pictures/summer.bmp"

# Adjust the number of tiles here, sometimes will not working depending on the size of the image
num_horizontal_tiles = 8
num_vertical_tiles = 8

# Predefined padding size to check the boundary offsets are correct
padding_size = 5


@pytest.fixture
def boundariesData():
    """
    Produced result of boundaryGeneration given the testing inputs

    """
    img_orig = np.array(imgplt.imread(img_path))

    height = img_orig.shape[0]
    tile_height = height // num_vertical_tiles
    extra_height = height % num_vertical_tiles

    width = img_orig.shape[1]
    tile_width = width // num_horizontal_tiles
    extra_width = width % num_horizontal_tiles

    boundaryCollection = {}
    neighborsCollection = {}

    boundary_generation_instance = generateBoundaries()
    for row in range(num_vertical_tiles):
        for col in range(num_horizontal_tiles):
            start_point = (col * tile_width, row * tile_height)
            end_point = (
                (col + 1) * tile_width,
                (row + 1) * tile_height,
            )

            current_tile = np.copy(
                # must be by HEIGHT * WIDTH
                img_orig[
                    start_point[1] : end_point[1] + 1,
                    start_point[0] : end_point[0] + 1,
                ]
            )

            neighborsIndex, boundarySections = boundary_generation_instance.run(
                current_tile,
                start_point,
                (width - tile_width - extra_width, height - tile_height - extra_height),
                tile_height,
                tile_width,
                padding_size,
                img_orig,
            )
            boundaryCollection[start_point] = boundarySections
            neighborsCollection[start_point] = neighborsIndex

    return (
        boundaryCollection,
        neighborsCollection,
        boundary_generation_instance,
    )


def test_numTypeTiles(boundariesData):
    """
    Test the number of each type of tile

    :param boundariesData data: processed data from boundaryGeneration
    """
    try:
        _, _, boundary_generation_instance = boundariesData

        # Normal cases:
        actual_num_corner_tiles = boundary_generation_instance.num_corner_tiles
        actual_num_edge_tiles = boundary_generation_instance.num_edge_tiles
        actual_num_inner_tiles = boundary_generation_instance.num_inner_tiles

        if num_horizontal_tiles > 1 and num_vertical_tiles > 1:
            expected_num_corner_tiles = 4
            expected_num_edge_tiles = 2 * (num_horizontal_tiles - 2) + 2 * (
                num_vertical_tiles - 2
            )
            expected_num_inner_tiles = (num_horizontal_tiles - 2) * (
                num_vertical_tiles - 2
            )

        elif num_vertical_tiles == 1 and num_horizontal_tiles == 1:
            expected_num_corner_tiles = 1
            expected_num_edge_tiles = 0
            expected_num_inner_tiles = 0

        # Only 1 vertical row:
        elif num_vertical_tiles == 1:
            actual_num_corner_tiles = (
                boundary_generation_instance.num_single_arr_corner_tiles
            )
            actual_num_edge_tiles = (
                boundary_generation_instance.num_single_arr_edge_tiles
            )

            expected_num_corner_tiles = 2
            expected_num_edge_tiles = num_horizontal_tiles - 2
            expected_num_inner_tiles = 0

        # Only 1 horizontal row:
        elif num_horizontal_tiles == 1:
            actual_num_corner_tiles = (
                boundary_generation_instance.num_single_arr_corner_tiles
            )
            actual_num_edge_tiles = (
                boundary_generation_instance.num_single_arr_edge_tiles
            )

            expected_num_corner_tiles = 2
            expected_num_edge_tiles = num_vertical_tiles - 2
            expected_num_inner_tiles = 0

        else:
            raise UnexpectedCaseError

        if expected_num_corner_tiles != actual_num_corner_tiles:
            raise AssertionError(expected_num_corner_tiles, actual_num_corner_tiles)

        if expected_num_edge_tiles != actual_num_edge_tiles:
            raise AssertionError(expected_num_edge_tiles, actual_num_edge_tiles)

        if expected_num_inner_tiles != actual_num_inner_tiles:
            raise AssertionError(expected_num_inner_tiles, actual_num_inner_tiles)

    except AssertionError as e:
        pytest.fail(e.__str__())

    except Exception as e:
        pytest.fail(e.__str__())


def test_numNeighborTiles(boundariesData):
    """
    Test the number of neighbors for each tile

    :param boundariesData data: processed data from boundaryGeneration
    """
    try:
        _, _, boundary_generation_instance = boundariesData

        tiles = boundary_generation_instance.tiles
        expected_tiles_type_collection = []
        # Populate the expected matrix of the number of neighbors
        for row in range(num_vertical_tiles):
            for col in range(num_horizontal_tiles):
                if (col, row) in {
                    (0, 0),
                    (num_horizontal_tiles - 1, 0),
                    (0, num_vertical_tiles - 1),
                    (num_horizontal_tiles - 1, num_vertical_tiles - 1),
                }:
                    if num_horizontal_tiles > 1 and num_vertical_tiles > 1:
                        expected_tiles_type_collection.append(3)
                    elif num_horizontal_tiles == 1 and num_vertical_tiles == 1:
                        expected_tiles_type_collection.append(0)
                    else:
                        expected_tiles_type_collection.append(1)

                elif col in (0, num_horizontal_tiles - 1) or row in (
                    0,
                    num_vertical_tiles - 1,
                ):
                    if num_horizontal_tiles > 1 and num_vertical_tiles > 1:
                        expected_tiles_type_collection.append(5)
                    elif num_horizontal_tiles == 1 and num_vertical_tiles == 1:
                        expected_tiles_type_collection.append(0)
                    else:
                        expected_tiles_type_collection.append(2)
                else:
                    if num_horizontal_tiles > 1 and num_vertical_tiles > 1:
                        expected_tiles_type_collection.append(8)
                    elif num_horizontal_tiles == 1 and num_vertical_tiles == 1:
                        expected_tiles_type_collection.append(0)
                    else:
                        raise UnexpectedCaseError

        for index in range(len(tiles)):
            expected_num_neighbors = expected_tiles_type_collection[index]
            actual_num_neighbors = tiles[index].value

            if expected_num_neighbors != actual_num_neighbors:
                raise AssertionError(expected_num_neighbors, actual_num_neighbors)

    except AssertionError as e:
        pytest.fail(e.__str__())

    except Exception as e:
        pytest.fail(e.__str__())


def test_neighborLocations(boundariesData):
    """
    Test that the neighbors have the correct relationship to the current tile

    :param boundariesData data: processed data from boundaryGeneration
    """
    try:
        TRANSLATE_TO_OPPOSITE = str.maketrans("tblr", "btrl")
        _, neighborsCollection, _ = boundariesData
        for start_point in neighborsCollection:
            currTileNeighbors = neighborsCollection[start_point]
            for relative_location in currTileNeighbors:
                currentNeighborLocation = currTileNeighbors[relative_location]
                check_location = relative_location.translate(TRANSLATE_TO_OPPOSITE)

                expected_start_point = start_point

                # Check the neighbors of the current neighbor we are checking, and checking
                # that the tile in the opposite direction (of the current tile) is the current tile
                actual_start_point = neighborsCollection[currentNeighborLocation][
                    check_location
                ]
                if expected_start_point != actual_start_point:
                    raise AssertionError(expected_start_point, actual_start_point)

    except AssertionError as e:
        pytest.fail(e.__str__())

    except Exception as e:
        pytest.fail(e.__str__())


# TODO: Fix this
def test_boundaryLocations(boundariesData):
    """
    Test the size of the boundary is according to padding_size

    :param boundariesData data: processed data from boundaryGeneration
    """
    try:
        boundaryCollection, _, _ = boundariesData
        location_to_value = {
            "b": (0, padding_size),
            "r": (padding_size, 0),
            "t": (0, padding_size),
            "l": (padding_size, 0),
        }
        for start_point in boundaryCollection:
            curr_tile_boundaries = boundaryCollection[start_point]
            for relative_location in curr_tile_boundaries:
                print("--------------")
                curr_boundary = curr_tile_boundaries[relative_location]
                locations = list(relative_location)

                # this is necessary because the calculation will assume that the starting_boundary is at the Top-Left
                # and the ending_boundary is at the Bottom-Right
                original_starting_boundary, original_ending_boundary = sorted(
                    curr_boundary, key=lambda t: t[1]
                )

                starting_boundary = tuple(
                    min(original_starting_boundary[i], original_ending_boundary[i])
                    for i in range(2)
                )

                ending_boundary = tuple(
                    max(original_starting_boundary[i], original_ending_boundary[i])
                    for i in range(2)
                )

                x_value, y_value = (0, 0)
                for location in locations:
                    # Assuming x_value and y_value are already defined
                    x_delta, y_delta = location_to_value[location]
                    x_value += x_delta
                    y_value += y_delta
                print(x_value, y_value, relative_location)

                x_value = (
                    ending_boundary[0] - starting_boundary[0]
                    if x_value == 0
                    else x_value
                )
                y_value = (
                    ending_boundary[1] - starting_boundary[1]
                    if y_value == 0
                    else y_value
                )
                print(x_value, y_value)
                print(starting_boundary, ending_boundary)

                actual_ending_boundary = (
                    starting_boundary[0] + x_value,
                    starting_boundary[1] + y_value,
                )
                expected_ending_boundary = ending_boundary

                if actual_ending_boundary != expected_ending_boundary:
                    raise AssertionError(
                        actual_ending_boundary, expected_ending_boundary
                    )

                assert (
                    starting_boundary[0] + x_value,
                    starting_boundary[1] + y_value,
                ) == ending_boundary

    except AssertionError as e:
        pytest.fail(e.__str__())

    except Exception as e:
        pytest.fail(e.__str__())


def test_lineBoundariesDirection(boundariesData):
    """
    Ensure that the line boundaries are formatted with their start point at the
    top left and end point at the bottom right

    :param boundariesData data: processed data from boundaryGeneration
    """
    try:
        boundaryCollection, _, _ = boundariesData
        for start_point in boundaryCollection:
            curr_tile_boundaries = boundaryCollection[start_point]
            for relative_location in curr_tile_boundaries:
                if len(relative_location) == 1:
                    curr_boundary = curr_tile_boundaries[relative_location]
                    start, end = curr_boundary
                    if start[0] >= end[0] and start[1] >= end[1]:

                        raise DirectionError((start, end), (relative_location))

    except DirectionError as e:
        pytest.fail(e.__str__())

    except AssertionError as e:
        pytest.fail(e.__str__())

    except Exception as e:
        pytest.fail(e.__str__())
