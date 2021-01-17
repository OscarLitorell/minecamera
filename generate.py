import csv
import numpy as np
import local_transform
import math

class PlayerPosition:
    def __init__(self, x, y, z, longitude, latitude):
        self.x = x
        self.y = y
        self.z = z
        self.longitude = longitude
        self.latitude = latitude


def unit_angles(angle):
    return ((angle + 180) % 360) - 180


def shortest_angle(a_0, a_1):
    return (a_0, a_0 + unit_angles(a_1 - a_0))


def read(fp):
    with open(fp, "r") as f:
        data = f.read()
        return data


def write(fp, data):
    with open(fp, "w") as f:
        f.write(data)


def get_coords_list(fp):
    with open(fp, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        data = list(reader)
        return np.array(data[1:]).astype(np.float)



def main():

    data = get_coords_list("coords.csv")
    
    positions = [PlayerPosition(*row[1:]) for row in data]
    timestamps = [int(sum(data[:i + 1, 0])) for i, _ in enumerate(data)]

    route = list(zip(positions, timestamps))

    duration = route[-1][1]

    origin = route[0][0]

    loopCommands = [
        f"tp @a[scores={{time=0}}] {origin.x} {origin.y} {origin.z} {origin.longitude} {origin.latitude}",
        "gamemode spectator @a[scores={time=0}]",
        "scoreboard players add @a[scores={time=0..}] time 1",
        f"gamemode creative @a[scores={{time={duration}}}]",
        f"scoreboard players set @a[scores={{time={duration}}}] time -1"
    ]

    linear = True

    for i in range(1, len(route)):
        start_position = route[i - 1][0]
        end_position = route[i][0]

        start_time = route[i - 1][1]
        end_time = route[i][1]

        duration = end_time - start_time

        dlat = float(end_position.latitude - start_position.latitude) / duration
        dlong = unit_angles(float((end_position.longitude - start_position.longitude))) / duration

        command  = f"execute at @a[scores={{time={start_time}}}] run tp @p {start_position.x} {start_position.y} {start_position.z} {start_position.longitude} {start_position.latitude}\n"

        if linear:
            dx = float(end_position.x - start_position.x) / duration
            dy = float(end_position.y - start_position.y) / duration
            dz = float(end_position.z - start_position.z) / duration
            command += f"execute at @a[scores={{time={start_time}..{end_time}}}] run tp @p ~{dx} ~{dy} ~{dz} ~{dlong} ~{dlat}"
        else:
            a_0, a_1 = shortest_angle(start_position.longitude, end_position.longitude)
            a_0, a_1 = math.radians(a_0), math.radians(a_1)
            b_0, b_1 = math.radians(start_position.latitude), math.radians(end_position.latitude)
            g_0 = np.array([start_position.x, start_position.y, start_position.z])
            g_1 = np.array([end_position.x, end_position.y, end_position.z])
            dx, dy, dz = tuple(local_transform.local_velocity(a_0, b_0, a_1, b_1, g_0, g_1, duration))
            command += f"execute at @a[scores={{time={start_time}..{end_time}}}] run tp @p ^{dx} ^{dy} ^{dz} ~{dlong} ~{dlat}"


        loopCommands.append(command)


    write("data/minecamera/functions/tick.mcfunction", "\n".join(loopCommands))

if __name__ == "__main__":
    main()
