# MineCamera

This is a datapack for Minecraft that lets you move through your world in a cinematic way.

## Installation

To install it, navigate to your Minecraft save folder by entering `%appdata%` in the Windows search bar, then selecting `.minecraft/saves` and move the `minecamera` folder to the `datapacks` folder of the selected world. You also need to install [python](https://www.python.org/downloads/).

## Usage

Open your Minecraft world and press F3 to show the coordinates. Move to your starting position, and write down the coordinates in the `coords.csv` file. The yaw and pitch values can be found after the "Facing" title in the Minecraft debug screen. The time value is the number of game ticks that the transition from the previous position should take. Divide this by 20 to get the time in seconds.

Note that Minecraft runs the commands 20 times per second, so it's recommended to speed the footage up to a better framerate. It's worth taking this into account when choosing a transition duration.

Here's an example of what `coords.csv` might look like:

| Time | x  | y   | z   | yaw | pitch |
| ---- | -- | --- | --- | --- | ----- |
| 0    | 64 | 62  | -26 |  50 | -25   |
| 600  | 80 | 118 |  30 |  30 |  35   |
| 300  | 90 | 100 |  20 |  20 |  18   |

When you have saved `coords.csv`, run `generate.py`. This will create the `tick.mcfunction` file, which is needed for the datapack to work. Then, open your Minecraft world and if the datapack isn't enabled, do it by entering `/datapack enable "file/MineCamera"`. You also need to enter the `/reload` command for Minecraft to detect the changes. You can now start the camera with `/function minecamera:start` and stop it with `/function minecamera:stop`.

To get the best result, avoid looking around with the mouse and moving with the keyboard.
