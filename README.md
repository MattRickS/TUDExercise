# Course Exercise
This is a mock production scenario that could easily be encountered in a studio. It is a perfect candidate for an automated solution, as it's a lot of repetitive work that requires little to no user input. The solution can be achieved using basic python knowledge.

## Scenario
Editorial have created animatic movies for a feature/episodic sequence (sequence 100) using storyboards provided to them. Production is now ready to start work on the individual shots, but they need to create the filesystem first. This involves creating a folder for each shot, as well as child folders for the 3 main departments: animation, backgrounds, compositing. They also want to *copy* the animatic and all the boards for each shot into the shot directory. The animatic should live directly under the shot folder and be called "animatic.mov". The boards should be placed inside a folder under the shot directory called "boards", and should not have the shot name in them.

Production don't want to have to do this by hand for every sequence, and have asked for a script to generate the folders and copy the files for them.

## Requirements
1. The script should be able to take a sequence directory as input, and calculate everything from there
2. Create a new folder under the "shots" directory for every animatic mov - the folder name should be the same name as the animatic (without the extension)
3. Create the following directories underneath each shot: [anim, bgs, boards, comp]
4. **Copy** the animatic for each shot under the shot folder, and call it "animatic.mov". Each shot must have the correct animatic!
5. **Copy** the story boards for each shot into the "boards" folder inside the shot folder. Only the shot's boards should be included. The shot name should also be removed from the file name, ie, `board_0010_0001.jpg` should become `shots/0010/boards/board_0001.jpg`
6. Only boards and mov files should be copied, and no files in the animatics/boards directories should be modified.

For convenience, a solution.py is provided with an outline of work to be done.

## Expected Folder Structure
```
sequences/
. 0100/
. . shots/
. . . 0010/
. . . . animatic.mov
. . . . anim/
. . . . bgs/
. . . . boards/
. . . . . board_001.jpg
. . . . . board_002.jpg
. . . . . board_003.jpg
. . . . comp/
. . . 0020/
etc...
```

Hints
-----
* The animatics and boards are automatically generated using the generate.py script. This contains some useful examples of how you might achieve parts of the solution. Note, if you want to run this file, you will need to install the 'pillow' python package.
* You will need to use external modules to complete the task.
  * The 'os' module provides Operating System operations for handling filepaths, but you will need another module to be able to copy files - which module to use is an exercise for you to research.
  * While not required, you can use the 'Fileseq' module for handling sequences of files. This is a common industry package, and can be installed using pip. Make sure to check it's documentation to find the methods you need!
