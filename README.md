# EEG-Mismatch Detection in Cognitive Tracking

This repository contains the stimulus code and relevant documentation for our EEG experiment investigating mismatch detection during object tracking. The experiment was developed in PsychoPy (2024.2.4) and designed as a visual oddball paradigm with dynamic motion stimuli.

## Experimental Design

Participants track a moving DVD-logo across a screen. The logo occasionally disappears (1.5s occlusion) and then reappears either in a predictable or unpredictable position and trajectory. 

The code implements:
- Continuous motion and wall-bounce behavior
- Controlled occlusion and trajectory violation logic
- Parallel port triggers for EEG synchronization
- Attention check prompts
- Optional logic for near-corner detection and final disappearance event

## Example Trials

Below are side-by-side examples of a **predictable** and an **unpredictable** reappearance:

| Predictable Trial | Unpredictable Trial |
|-------------------|---------------------|
| ![Predictable](predictable_trial.gif) | ![Unpredictable](unpredictable_trial.gif) |


## Stimulus 

*Figure: The red 2D DVD logo used as the moving stimulus in the experiment.*

![DVD Logo](logo.png)

## Trigger List


| Trigger Value | Event Description                        |
|---------------|------------------------------------------|
| 1             | Experiment start                         |
| 2             | Baseline ends                            |
| 3             | Experiment end                           |
| 4             | Attention question appears               |
| 5             | Attention question disappears            |
| 10            | Disappearance (standard location)        |
| 11            | Disappearance (near corner)              |
| 200           | Predictable reappearance                 |
| 201           | Predictable reappearance (near corner)   |
| 210           | Unpredictable reappearance               |
| 211           | Unpredictable reappearance (near corner) |
| 40            | Participant response correct             |
| 41            | Participant response incorrect           |
| 98            | Final disappearance starts               |
| 99            | Final disappearance ends (logo exits)    |

## File Overview

- `experiment.py`: Main PsychoPy script
- `logo.png`: Visual stimulus used in the experiment
- `triggers.py`: Parallel port trigger helper functions
- `output/`: Folder with examples of output files (logfile and CSV)

## Authors

This experiment was developed by:

- Agnes Margrethe Ottosen Gejl  
- Anders Herzog Varan  
- Lukas Kubiena  
- Sissel Højgaard Vang-Pedersen *(main author)*  
- Sofia Scharf-Matthiesen

*This work was conducted as part of the Cognitive Neuroscience course, Aarhus University.*

## Citation

> Gejl, A.M.O., Varan, A.H., Kubiena, L., Vang-Pedersen, S.H.*, & Scharf, S. (2025). *EEG-Mismatch Detection in Cognitive Tracking*. GitHub repository:(https://github.com/Siss1243/Neuro_experiment_2025.git)

