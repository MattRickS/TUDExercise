import os
import shutil

import fileseq


ANIMATIC_FILENAME = "animatic.mov"
BOARDS_DIR = "boards"
SHOT_CHILD_DIRECTORIES = ("anim", "bgs", BOARDS_DIR, "comp")


def collect_animatics(animatic_directory):
    animatic_mapping = {}
    for animatic in os.listdir(animatic_directory):
        shot_name, _ = os.path.splitext(animatic)
        animatic_mapping[shot_name] = os.path.join(animatic_directory, animatic)
    return animatic_mapping


def collect_boards(boards_directory):
    file_pattern = os.path.join(boards_directory, "board_*.jpg")
    sequences = fileseq.findSequencesOnDisk(file_pattern)
    boards_mapping = {}
    for sequence in sequences:
        filename = sequence.basename()
        shot_name = filename.split("_")[1]
        if not shot_name.isdigit():
            print("Invalid sequence:", sequence)
            continue

        boards_mapping[shot_name] = sequence

    return boards_mapping


def create_shot_child_directories(shot_directory):
    for name in SHOT_CHILD_DIRECTORIES:
        child_path = os.path.join(shot_directory, name)
        os.makedirs(child_path)


def copy_boards_sequence(sequence, shot_directory):
    # Build a sequence pattern using a fake frame range, then use the fileseq api
    # to update the frame range to match our source sequence
    dest_sequence_pattern = os.path.join(shot_directory, BOARDS_DIR, "board_1-1#.jpg")
    dest_sequence = fileseq.FileSequence(dest_sequence_pattern)
    dest_sequence.setFrameRange(sequence.frameRange())
    for src_file, dst_file in zip(sequence, dest_sequence):
        shutil.copy2(src_file, dst_file)


def setup_shot(shot_directory, animatic, boards_sequence):
    # Create directories
    create_shot_child_directories(shot_directory)

    # Copy animatic
    animatic_destination = os.path.join(shot_directory, ANIMATIC_FILENAME)
    shutil.copy2(animatic, animatic_destination)

    # Copy boards
    copy_boards_sequence(boards_sequence, shot_directory)


def setup_sequence(sequence_directory):
    # Calculate source directories
    seq_animatic_dir = os.path.join(sequence_directory, "animatics")
    seq_boards_dir = os.path.join(sequence_directory, "boards")
    seq_shot_dir = os.path.join(sequence_directory, "shots")

    # Collect source resources
    animatic_mapping = collect_animatics(seq_animatic_dir)
    boards_mapping = collect_boards(seq_boards_dir)

    # Construct each shot
    for shot_name, animatic in animatic_mapping.items():
        shot_directory = os.path.join(seq_shot_dir, shot_name)
        setup_shot(shot_directory, animatic, boards_mapping[shot_name])


if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 1:
        print("Usage: solution.py SEQUENCE_DIRECTORY")
        sys.exit(1)

    setup_sequence(sys.argv[1])
