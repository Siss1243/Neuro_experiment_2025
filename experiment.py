from psychopy import visual, core, event, monitors
import random
import math
import os
import csv
import sys
from triggers import setParallelData

#-----------------------Setup--------------------------------
#Define test mode
TEST_MODE = True

# Durations time
total_duration = 15 * 60 if not TEST_MODE else 2 * 60
baseline_duration = 1 * 30 if not TEST_MODE else 1 * 30  
invisible_duration = 1.5
question_times = [3 * 60, 6 * 60, 9 * 60, 12 * 60] if not TEST_MODE else [60]

# Create window
my_monitor = monitors.Monitor('testMonitor')  
win = visual.Window(monitor=my_monitor, fullscr=True, color='black')

#Define paths
experimental_pyfile_path = os.path.abspath(__file__) # Get the absolute path of the experiment script
experiment_dir = os.path.dirname(experimental_pyfile_path) # Get the directory containing the script

logo_path = os.path.join(experiment_dir, "logo.png")
output_path = os.path.join(experiment_dir, "output")

if not os.path.exists(output_path):
    os.makedirs(output_path)  # Create the directory if it doesn't exist


# Define log file
log_filename = os.path.join(output_path, "experiment_log.txt")

# Redirect stdout to both console and log file
class DualLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

# Activate dual logging
sys.stdout = DualLogger(log_filename)

print("=== Experiment Log ===")

# Load logo
logo = visual.ImageStim(win, image=logo_path, size=(0.2, 0.2))

# Box boundaries (area where the logo can move + cornor thresholds)
left_bound, right_bound = -0.8, 0.8
top_bound, bottom_bound = 0.8, -0.8

corner_thresholds = {
    "top_left": (-0.8, -0.6, 0.6, 0.8), 
    "top_right": (0.6, 0.8, 0.6, 0.8),  
    "bottom_left": (-0.8, -0.6, -0.8, -0.6), 
    "bottom_right": (0.6, 0.8, -0.8, -0.6)  
}


# Start position
x_pos, y_pos = 0, 0

# Choose a random starting direction (up, down, left, right)
start_directions = ["up", "down", "left", "right"]
chosen_direction = random.choice(start_directions)
angle_offsets = {"up": 60, "down": -60, "left": 120, "right": -120}
angle = math.radians(angle_offsets[chosen_direction])

# Fixed speed
speed = 0.004  
y_dir = math.sin(angle) * speed
x_dir = math.cos(angle) * speed

# Timer setup
trial_timer = core.Clock()
total_timer = core.Clock()

# Random time between disappearances
next_disappearance = random.uniform(4, 8)
#---------------------------------------------------------------


#-----------------------TRIGGERS--------------------------------
# Triggersystem:
# Trigger: 1 --> experiment start 
# Trigger: 2 --> Baseline ends 
# Trigger: 3 --> experiment end


# Trigger: 4 --> Question shows
# Trigger: 40 --> Participant answers (correct)
# Trigger: 41 --> Participant answer (incorrect)
# Trigger: 5 --> Question disapars 

# Trigger: 10 --> Disapears 
# Trigger: 11 --> Disapears (near corner)

# Trigger: 200 --> Reappearance, no surprice
# Trigger: 201 --> Reappearance, no surprice, near corner
# Trigger: 210 --> Reappearance, surprice
# Trigger: 211 --> Reappearance, surprice, near corner

# Trigger: 98  --> Final disappearance initiated
# Trigger: 99 --> CORNER HIT



def send_trigger(trigger_value):
    try:
        win.callOnFlip(setParallelData, trigger_value)
        print(f"TRIG {trigger_value} sent at {round(total_timer.getTime(), 2)} sec")
    except Exception as e:
        print(f"Fejl ved afsendelse af trigger {trigger_value}: {e}")
#---------------------------------------------------------------


#-----------------------TRIAL_SEQUENCE--------------------------------
def generate_trial_sequence():
    sequence = []
    
    # 4 predictable reaaperances
    for _ in range(4):
        sequence.append('predictable')

    # 4 empthyslots, random placed. 
    empty_slots = ['predictable', 'predictable', 'unpredictable']
    random.shuffle(empty_slots)  

    sequence.extend(empty_slots) 

    return sequence
#---------------------------------------------------------------



#-----------------------QUESTIONS--------------------------------

def ask_bounce_question():
    question_text = visual.TextStim(win, text="At what surface did the DVD-Logo bounce last time?", 
                                    color="white", height=0.08, pos=(0, 0), wrapWidth=1.5)
    
    instruction_text = visual.TextStim(win, text="Use the arrow keys to respond", 
                                       color="white", height=0.05, pos=(0, -0.2))

    # Show question
    question_display_time = total_timer.getTime()  # Timestamp when the question is shown
    print(f"[{round(question_display_time, 2)} sec] Question {i+1} shown.")
    send_trigger(4)  # Trigger 4: Question shows
    
    question_text.draw()
    instruction_text.draw()
    win.flip()

    response = None
    response_time = core.Clock()  # Response timer

    # waiting for response
    while response is None:
        keys = event.waitKeys(keyList=["up", "down", "left", "right", "escape"])
        
        if "escape" in keys:
            core.quit()

        response = keys[0]  # keypres
    
    # Check if correct
    correct = response == last_bounce_wall
    
    trigger_value = 40 if correct else 41
    setParallelData(trigger_value) 
    
    print(f"[{round(total_timer.getTime(), 2)}] Answer received: {'Correct' if correct else 'Incorrect'} (Expected: {last_bounce_wall}, Given: {response})")
    
    send_trigger(5)  # Trigger 5: Question disappears
    
    win.flip() 
#-----------------------------------------------------------------


#-----------------------Near_Corner--------------------------------
def is_near_corner(x_pos, y_pos, corner_thresholds):

    for corner, (x_min, x_max, y_min, y_max) in corner_thresholds.items():
        #Check if location is within thresholds
        if x_min <= x_pos <= x_max and y_min <= y_pos <= y_max:
            return True

    return False
#---------------------------------------------------------------


#-----------------------FUNCTIONS--------------------------------

def predictable_condition():
    global x_pos, y_pos, x_dir, y_dir

    # Calculate new position based on invisible time
    total_x_movement = x_dir * invisible_duration / (1 / 60)
    total_y_movement = y_dir * invisible_duration / (1 / 60)
    x_pos += total_x_movement
    y_pos += total_y_movement

    # Ensure the logo does not go beyond boundaries
    if x_pos >= right_bound or x_pos <= left_bound:
        x_dir *= -1
        x_pos = max(min(x_pos, right_bound), left_bound)
    if y_pos >= top_bound or y_pos <= bottom_bound:
        y_dir *= -1
        y_pos = max(min(y_pos, top_bound), bottom_bound)
#---------------------------------------------------------------

def unpredictable_condition():
    global x_pos, y_pos, x_dir, y_dir
    deviation_percentage = 0.60
    
    # Calculate the expected position based on the current direction
    expected_x_pos = x_pos + (x_dir * invisible_duration / (1 / 60))
    expected_y_pos = y_pos + (y_dir * invisible_duration / (1 / 60))

    # Define 8 directions (in degrees, converted to radians)
    directions = [10, 55, 100, 145, 190, 235, 280, 325]
    directions_rad = [math.radians(d) for d in directions]  # Convert to radians

    # Calculate deviation for each direction
    valid_deviations = []

    for direction in directions_rad:
        # Calculate deviation based on the chosen direction and percentage
        max_x_deviation = (right_bound - left_bound) * deviation_percentage
        max_y_deviation = (top_bound - bottom_bound) * deviation_percentage
        
        # Calculate x and y deviation for the given direction
        x_deviation = math.cos(direction) * max_x_deviation
        y_deviation = math.sin(direction) * max_y_deviation

        # Calculate the new position
        new_x_pos = expected_x_pos + x_deviation
        new_y_pos = expected_y_pos + y_deviation

        # Check if the new position is within the screen boundaries
        if left_bound <= new_x_pos <= right_bound and bottom_bound <= new_y_pos <= top_bound:
            valid_deviations.append((new_x_pos, new_y_pos))

    # If there are valid deviations, choose one randomly
    if valid_deviations:
        chosen_deviation = random.choice(valid_deviations)
        x_pos, y_pos = chosen_deviation
    else:
        print("No valid deviations found. Using default position.")
        # If no valid deviation is found, use the expected position
        x_pos, y_pos = expected_x_pos, expected_y_pos
    
    
    # --- HANDLE DIRECTION CHANGE ---
    movement_directions = {
        60:  (0.5,  0.866),
        -60: (0.5, -0.866),
        120: (-0.5,  0.866),
        -120: (-0.5, -0.866)
    }

    # Find closest valid movement direction
    current_angle = math.degrees(math.atan2(y_dir, x_dir))
    closest_angle = min(movement_directions.keys(), key=lambda angle: abs(angle - current_angle))

    # Select new direction that is different from current one
    new_angle = random.choice([angle for angle in movement_directions.keys() if angle != closest_angle])
    new_x_dir, new_y_dir = movement_directions[new_angle]

    x_dir = new_x_dir * speed
    y_dir = new_y_dir * speed
    
#--------------------------------------------------------------

def final_disappearance():
    global x_pos, y_pos, x_dir, y_dir

    # Make the logo invisible
    logo.opacity = 0
    win.flip()  # Update the screen
    core.wait(1.5)  # Wait for 1.5 seconds (same as normal disappearances)
    
    # Reset position to center and make the logo visible
    x_pos, y_pos = 0, 0  
    logo.opacity = 1  
    logo.pos = (x_pos, y_pos)
    
    send_trigger(98)
    
    logo.draw()
    win.flip()

    # Randomly select one of the four corners
    corners = {
        "top-left": (-0.8, 0.8),
        "top-right": (0.8, 0.8),
        "bottom-left": (-0.8, -0.8),
        "bottom-right": (0.8, -0.8),
    }
    corner_name, (target_x, target_y) = random.choice(list(corners.items()))

    # Compute the exact angle to move towards the chosen corner
    angle = math.atan2(target_y - y_pos, target_x - x_pos)  # Angle in radians

    # Set movement direction based on speed
    x_dir = math.cos(angle) * speed  
    y_dir = math.sin(angle) * speed  
    
    pullTriggerDown = False
    
    # Move the logo towards the selected corner until it disappears
    while -1.2 <= x_pos <= 1.2 and -1.2 <= y_pos <= 1.2:  
        x_pos += x_dir  
        y_pos += y_dir  
        logo.pos = (x_pos, y_pos)  
        
        logo.draw()  
        win.flip()  
        
        # Check if the logo is about to leave the screen and trigger
        if not pullTriggerDown and (x_pos < -1.0 or x_pos > 1.0 or y_pos < -1.0 or y_pos > 1.0):
            send_trigger(99)  # Send trigger when logo is about to disappear
            pullTriggerDown = True  # Ensure it's only sent once
            
        if "escape" in event.getKeys():
            break  

    # Ensure the logo is completely gone
    logo.opacity = 0
    win.flip()  

    print(f"[{round(total_timer.getTime(), 2)} sec] The logo has disappeared through the {corner_name}.")
#--------------------------------------------------------------


#-----------------------ADMIN LOOP--------------------------------

disappearance_counter = 1  
skip_baseline = False  
final_disappearance_triggered = False  
last_bounce_wall = None
pullTriggerDown = False
questions_asked = [False] * len(question_times)
question_active = False
trial_data = []


trial_sequence = ['predictable', 'predictable', 'predictable', 
                    'predictable', 'predictable', 'predictable', 'unpredictable']

current_trial = 0


send_trigger(1) #Experiment start trigger

#Outer time loop
while total_timer.getTime() < total_duration:
    keys = event.getKeys()
    
    # If space is pressed, skip directly to the active phase
    if "space" in keys:
        skip_baseline = True
        print(f"[{round(total_timer.getTime(), 2)} sec] Baseline skipped.")
        
    # Question (3, 6, 9, 12 minute)
    for i, question_time in enumerate(question_times):
        if not questions_asked[i] and abs(total_timer.getTime() - question_time) < 1.0:  
            
            question_active = True  # Pause disappearances
            
            ask_bounce_question()  
            questions_asked[i] = True  #mark question as asked
            
            question_active = False  # Resume disappearances
            
            # After the question is finished, restart the trial_timer
            trial_timer.reset()  #Rest timer for next trial
            
            break  

    # Handle baseline duration and skip option
    if not question_active and (total_timer.getTime() > baseline_duration or skip_baseline):
        
        if not pullTriggerDown:  
            send_trigger(2)  
            pullTriggerDown = True  # Ensure trigger only fires once
        
        # Trigger the final disappearance within the last 10 seconds
        if not final_disappearance_triggered and (total_duration - total_timer.getTime() <= 10):
            print(f" ---Final disappearance triggered ([{round(total_timer.getTime(), 2)} sec]). ----")
            final_disappearance()  # Move logo to corner & disappear
            final_disappearance_triggered = True  # Prevent further disappearances
            logo.opacity = 0  # Ensure the logo is invisible
            win.flip()  # Update the screen
            continue  # Continue the loop without further processing

        # **If the final disappearance has happened, do nothing but update the screen**
        if final_disappearance_triggered:
            win.flip()  # Keep updating the screen without making the logo reappear
            continue  # Skip the rest of the loop
        
        # When it's time for the next disappearance
        if trial_timer.getTime() >= next_disappearance:
            
            disappearance_type = trial_sequence[current_trial]
            print(f" ---- Disappearance {disappearance_counter}: {disappearance_type} ----")
            
            disappeared_in_corner = is_near_corner(x_pos, y_pos, corner_thresholds)
            logo.opacity = 0  # Make logo invisible
            
            trigger_value = 11 if disappeared_in_corner else 10
            send_trigger(trigger_value)
            
            win.callOnFlip(lambda: print(f"[{round(total_timer.getTime(), 2)} sec] Logo disappeared at ({round(x_pos, 2)}, {round(y_pos, 2)}). In corner: {disappeared_in_corner}"))
            win.flip()  # 🚨 SCREEN UPDATED: LOGO IS INVISIBLE 🚨
            
            core.wait(invisible_duration)  # Wait while logo is invisible
            
            if disappearance_type == 'predictable':
                predictable_condition()
            else:
                unpredictable_condition()
            
            
            # Make logo visible again
            logo.opacity = 1
            
            reappeared_in_corner = is_near_corner(x_pos, y_pos, corner_thresholds)
            win.callOnFlip(lambda: print(f"[{round(total_timer.getTime(), 2)} sec] Logo reappeared at ({round(x_pos, 2)}, {round(y_pos, 2)}). In corner: {reappeared_in_corner}"))
            
            
            # Store disappearance information
            trial_data.append({
                "disappearance_number": disappearance_counter,
                "disappeared_in_corner": disappeared_in_corner,
                "reappearance_type": disappearance_type,
                "reappeared_in_corner": reappeared_in_corner
            })
            
            disappearance_counter += 1  # Increase counter for disappearances
            
            # Determine the correct trigger:
            if disappearance_type == 'predictable':
                trigger_value = 200 if not reappeared_in_corner else 201
            else:  # Unpredictable (surprise)
                trigger_value = 210 if not reappeared_in_corner else 211

            # Send the correct reappearance trigger
            send_trigger(trigger_value)
            
            
            # Reset trial_timer and update next_disappearance
            trial_timer.reset()  # Reset the trial timer for the next disappearance
            next_disappearance = random.uniform(4, 8)  # Random time for the next disappearance
            
            current_trial += 1
            
            #Update trial sequence if necessary
            if current_trial >= len(trial_sequence):
                trial_sequence = generate_trial_sequence() #Get new sequence
                current_trial = 0
                
    
    # Update position
    x_pos += x_dir
    y_pos += y_dir

    # Check if the logo hits a wall and reverse direction if so
    if x_pos >= right_bound:
        x_dir *= -1
        x_pos = right_bound  # Set position to the right boundary
        last_bounce_wall = "right"  # Logo hit the right wall

    elif x_pos <= left_bound:
        x_dir *= -1
        x_pos = left_bound  # Set position to the left boundary
        last_bounce_wall = "left"  # Logo hit the left wall

    if y_pos >= top_bound:
        y_dir *= -1
        y_pos = top_bound  # Set position to the top boundary
        last_bounce_wall = "up"  # Logo hit the top wall

    elif y_pos <= bottom_bound:
        y_dir *= -1
        y_pos = bottom_bound  # Set position to the bottom boundary
        last_bounce_wall = "down"  # Logo hit the bottom wall

    # Update the logo's position
    logo.pos = (x_pos, y_pos)
    logo.draw()
    win.flip()  # 🚨 THIS IS WHEN THE LOGO BECOMES VISIBLE AGAIN 🚨

    # Stop if Escape is pressed
    if "escape" in keys:
        break


send_trigger(3) #End experiment trigger

# At the end of the experiment, specify the path for the CSV file
csv_filename = os.path.join(output_path, "trial_data.csv")

# Open the CSV file in write mode
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=trial_data[0].keys())
    
    # Write the header (column names) using the first trial data's keys
    writer.writeheader()
    
    # Write all the trial data rows
    writer.writerows(trial_data)

# Print a message confirming the data was saved
print(f"Trial data saved to {csv_filename}")

print("=== Experiment End ===")
sys.stdout.log.close()  # Explicitly close the log file













