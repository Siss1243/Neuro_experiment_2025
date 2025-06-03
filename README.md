# EEG-Mismatch Detection in Cognitive Tracking

This repository contains the stimulus code and relevant documentation for our EEG experiment investigating mismatch detection during object tracking. The experiment was developed in PsychoPy and designed as a visual oddball paradigm with dynamic motion stimuli.

## 🧠 Experimental Design

Participants track a moving DVD-logo across a screen. The logo occasionally disappears (1.5s occlusion) and then reappears either in a predictable or unpredictable position and trajectory. 

The code implements:
- Continuous motion and wall-bounce behavior
- Controlled occlusion and trajectory violation logic
- Parallel port triggers for EEG synchronization
- Attention check prompts

Visual illustration of experiment:
![Stimulus Demo](docs/stimulus_demo.gif)

## 📺 Stimulus 



## 🔢 Trigger List

See [`triggers.md`](triggers.md) for a full description of trigger values used for EEG recording.

EEG Trigger List

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

## 📁 File Overview

- `experiment.py`: Main PsychoPy script
- `logo.png`: Visual stimulus used
- `docs/`: examples of outputs from runned experiments

--

*This work was conducted as part of the Cognitive Neuroscience course, Aarhus University.*
