# <img src="ui/appicon.ico" alt="Alt" width="22"/> ProjectAsteria

Page for my painful OCR A Level Computer Science NEA.

Welcome stakeholders. Please read the following before attempting to run the code.

## When pulling the repository

Make sure to run 
`pip install -r requirements.txt` 
so that all the necessary libraries are installed. It's best to do so from the admin terminal. Ensure you're in the `ProjectAsteria` folder. 

## How to run

Simply open an IDE/text editor that lets you run code and run `main.py` or type the
`py main.py` command. Ensure you're in the `ProjectAsteria` folder.

## Within the simulation

There is no menu screen yet so the simulation will start immediately. 

The rocket will initially have a force of 20 N and can be increased or decreased by using your upwards or downwards arrow respectively. The rocket can also be rotated by using the left and right arrow keys. 

By pressing `O` (case insensitive) the thrust of the rocket will be turned on or off. When you turn it back on, however, the thurst will be at 0° with a magnitude of 1000 N because I'm very smart (for debugging purposes). When pressing `N` (case insensitive), an invisible magical man will instantly turn the rocket into a nuclear-powered one. When pressed again, he will turn it back into a chemical rocket.

Pressing `=` or `-` will zoom in or out respectively. It's `=` because I said so. Pressing `R` (case insensitive) resets the zoom.

In the top left, the following information about the rocket can be seen:
- Distance from the sun
- Velocity
- Thrust
- Direction of thrust

The direction of thrust is measured in degrees and goes from -180° to 180°.

## Disclaimer

Feel free to look at the code but I may not be criticised* due to the horror you may feel. By running this repo, you agree to the above conditions.

Additionally, feel free to create your own `Planet` or `Rocket` by adding the instances to the `planets` array in `objects.py`. That is, if you can fork the repo somehow. 

*Criticism regarding PEP8 regulations or similar falls under this condition. Criticism regarding the logic of the code is welcome.

## Last words

Do not stalk this repo.
