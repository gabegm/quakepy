quakepy
==============================

Find a list of the 10 most nearby earthquakes based on a LAT/LON coorindate provided.

# Instructions

You may choose to either use the Python or Docker method based on your preference.

## Install (Python)

```sh
$ chmod +x install.sh
$ ./install.sh
```

## Install (Docker)

```sh
$ docker build -t quakepy .
```

## Run (Python)

```sh
(quakepy) $ python/main.py 40.730610, -73.935242

M 1.0 - 1 km SW of Meridian, New York || 397
M 1.0 - 22 km NE of Skatepark, Canada || 518
M 1.2 - 18 km NNE of Skatepark, Canada || 520
M 2.5 - 6 km S of Livermore, Maine || 572
M 1.5 - 1 km NNE of Depew, New York || 582
M 2.3 - 7 km E of Sainte-Julienne, Canada || 583
M 2.2 - southern Quebec, Canada || 661
M 2.3 - 4 km SE of Madison, Ohio || 796
M 2.2 - 3 km WSW of McLeansville, North Carolina || 823
M 2.3 - 4 km WSW of McLeansville, North Carolina || 824
```

## Run (Docker)

```sh
$ docker run quakepy 40.730610 -73.935242

M 1.0 - 1 km SW of Meridian, New York || 397
M 1.0 - 22 km NE of Skatepark, Canada || 518
M 1.2 - 18 km NNE of Skatepark, Canada || 520
M 2.5 - 6 km S of Livermore, Maine || 572
M 1.5 - 1 km NNE of Depew, New York || 582
M 2.3 - 7 km E of Sainte-Julienne, Canada || 583
M 2.2 - southern Quebec, Canada || 661
M 2.3 - 4 km SE of Madison, Ohio || 796
M 2.2 - 3 km WSW of McLeansville, North Carolina || 823
M 2.3 - 4 km WSW of McLeansville, North Carolina || 824
```