# README

[![gitleaks](https://github.com/fasihu1996/oos/actions/workflows/github-actions.yml/badge.svg)](https://github.com/fasihu1996/oos/actions/workflows/github-actions.yml)

## Purpose

This repository contains all the code created for the course "Objektorientierte Skriptsprachen".

## Organization

All files starting with "afg" are solutions for the various exercise sheets. The categories are as follows:

- afg1: Python introduction
- afg2: Functions and Data types
- afg3: Classes, Modules and Packages
- afg4: Testing, Databases, Lambda, CLI
- afg5: Pygame
- afg6: Tkinter
- Woche 7 Django Projekte
- afg8: Application Scripting und Datenanalyse

- "cli_audiorecorder.py" is part of the first bonus point assignment.
- "esa3_gui_recorder.py" is the GUI implementation of the audio recorder using tkinter and some
  additional theming.

## Usage

All requirements are periodically frozen into the "requirements.txt" file. Make sure to run

`python -m venv .venv` and then pick based on your OS `.venv/Scripts/activate` for Windows and
`source .venv/bin/activate` for UNIX. Finally, run `pip install -r requirements.txt`
to install the included requirements after setting up a virtual environment. Using the `reqs_gen.py` file,
you can also generate custom requirements.txt for individual files. Double-check the output as it relies on
the naming being exact.
