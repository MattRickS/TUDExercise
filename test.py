import mock
import os
import re

import generate
import solution


# requires pyfakefs, pytest, mock, and pytest-mock
@mock.patch("generate.Image")
def test_solution(mock_Image, fs):
    # Mock the behaviour of saving the image to create a fake file instead, as
    # pillow's file IO is not mocked by the pyfakefs module
    mock_Image.new.return_value.save.side_effect = lambda output: fs.create_file(output)

    sequence_dir = "/project/sequences/0100"
    shot_mapping = {"0010": 3, "0020": 2, "0030": 4, "0040": 1, "0050": 3}

    # Create a fake directory and generate the starting filesystem
    fs.create_dir(sequence_dir)
    generate.generate_mock_files(sequence_dir, shot_mapping)

    # Run the solution function
    solution.setup_sequence(sequence_dir)

    # Test the results are what we expect
    for shot_name, count in shot_mapping.items():
        shot_dir = os.path.join(sequence_dir, "shots", shot_name)

        # Animatic file should exist, and should be the correct one
        animatic = os.path.join(shot_dir, "animatic.mov")
        assert os.path.isfile(animatic), "Missing shot animatic: {}".format(animatic)
        with open(animatic) as f:
            line = f.readline()
            assert (
                line == shot_name
            ), "Animatic must be for the correct shot: {} != {}".format(line, shot_name)

        # Department folders should exist
        for folder in ("anim", "bgs", "boards", "comp"):
            directory = os.path.join(shot_dir, folder)
            assert os.path.isdir(
                directory
            ), "Shot must have all subdirectories, missing {}".format(folder)

        # Must contain the correct number of boards, with the correct names
        boards_dir = os.path.join(shot_dir, "boards")
        files = os.listdir(boards_dir)
        assert (
            len(files) == count
        ), "Incorrect number of boards for shot {}: Expected {}, got {}".format(
            shot_name, count, len(files)
        )
        assert all(
            re.match(r"board_\d+.jpg", f) for f in files
        ), "Boards should not have the shot name in the file, expected pattern: board_0001.jpg"
