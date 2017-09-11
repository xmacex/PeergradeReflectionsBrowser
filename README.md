# PeergradeReflectionsBrowser

A more streamlined browser for [Peergrade](https://peergrade.io) reflections. The idea here is to be able to quickly flip through large amount of students assignments.

Built for IT University of Copenhagen course *Navigating Complexity: Mapping Visualisation and Decisionmaking*, Autumn 2017. We have students hand in a reflection on their readings every week.

## Installing

1. Clone or download this repository.
1. Download each assignment as zip files from Peergrade
1. Place the zip files in the same directory as the `ReflectionsServer.py`
1. List the filenames in `ReflectionsServer.py` variable called `reflections`, currently on line 75
1. Say `python3 ./ReflectionsServer.py`
1. Navigate to http://localhost:8000
