import os

from PIL import Image, ImageDraw, ImageFont


def generate_text_image(shot_name, output):
    # Uses a third party package called "pillow" to generate images.
    # Install the package from command line using: pip install pillow
    image = Image.new("1", (256, 128), color=1)
    draw = ImageDraw.Draw(image)
    # If using this, make sure this font exists on your computer, or swap it for
    # the path to another font
    font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", size=32)
    draw.text((0, 0), shot_name, fill=0, font=font)
    image.save(output)


def generate_shot_images(output_dir, shot_name, count):
    for frame in range(count):
        # Add one to frame to convert from 0-based to 1-based indexing
        path = os.path.join(
            output_dir, "board_{}_{:04d}.jpg".format(shot_name, frame + 1)
        )
        # Could just generate once and copy it, but it's quick and I'm lazy :)
        generate_text_image(shot_name, path)


def generate_mock_animatics(directory, shot_name):
    animatic_path = os.path.join(directory, shot_name + ".mov")
    # builtin "open" loads a file for editing, "w" is write mode, and will create
    # the file if it doesn't exist
    fp = open(animatic_path, "w")
    # Write some fake data into the file, it's actually a text file with a 'mov' extension
    fp.write(shot_name)
    # Must close the file after opening it or it will use up memory!
    fp.close()


def generate_mock_files(sequence_directory, shot_mapping):
    # Build paths for the directories to be populated, and ensure they exist
    animatic_dir = os.path.join(sequence_directory, "animatics")
    os.makedirs(animatic_dir, exist_ok=True)

    boards_dir = os.path.join(sequence_directory, "boards")
    os.makedirs(boards_dir, exist_ok=True)

    # Generate the files for each shot
    for shot_name, count in shot_mapping.items():
        generate_mock_animatics(animatic_dir, shot_name)
        generate_shot_images(boards_dir, shot_name, count)

    # Also add a fake workfile as a challenge - this is data we don't want mixed
    # in with data we do want. Whatever our solution, it needs to be able to
    # avoid doing anything with this file.
    fake_workfile = os.path.join(boards_dir, "storyboard.workfile")
    # 'with' works with 'context' objects - in this case, 'open' allows using
    # with to automatically close the file when the indented block finishes, even
    # if an error was raised. This protects us from accidentally leaving a file open
    with open(fake_workfile, "w"):
        pass


if __name__ == "__main__":
    # __file__ is builtin, and contains the path to the current python file
    # dirname chops up the path to get the parent directory of the given path
    current_directory = os.path.dirname(__file__)
    # Join builds a path using OS specific separators, eg, \ for windows, / for unix
    sequence_dir = os.path.join(current_directory, "project", "sequences", "0100")
    generate_mock_files(
        sequence_dir,
        {"0010": 3, "0020": 2, "0030": 4, "0040": 1, "0050": 3},
    )
