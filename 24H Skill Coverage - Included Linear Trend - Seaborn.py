import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import yaml
import numpy as np

# Load YAML data from the uploaded file
with open('team_data.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Flatten the data, ignoring the "People" category
rows = []
for skill, devs in data.items():
    if skill == "People":
        continue  # Skip the "People" category
    for name, details in devs.items():
        # Ensure 'start', 'end', and 'expertise' keys are present
        if 'start' in details and 'end' in details and 'expertise' in details:
            rows.append({
                'Developer': name,
                'Skill': skill,
                'Start': details['start'],
                'End': details['end'],
                'Expertise': details['expertise']
            })
        else:
            print(f"Missing data for developer: {name} in skill: {skill}")

# Create DataFrame
df = pd.DataFrame(rows)

# Convert time to datetime for easier plotting
df['Start'] = pd.to_datetime(df['Start'], format='%I:%M %p')
df['End'] = pd.to_datetime(df['End'], format='%I:%M %p')

# Set up the time slots (every hour from 12 AM to 11 PM)
time_slots = pd.date_range('00:00', '23:00', freq='1h').time
time_slots_str = [t.strftime('%H:%M') for t in time_slots]

# Define weights for different expertise levels, including Principal/Lead Developer
weights = {
    'Senior Developer': 3,
    'Mid-Level Developer': 2,
    'Junior Developer': 1,
    'Principal/Lead Developer': 4
}

# Initialize the weighted availability DataFrame
weighted_availability = pd.DataFrame(
    0, index=time_slots, columns=df['Skill'].unique())

# Calculate the weighted availability
for _, row in df.iterrows():
    start_time = row['Start'].time()
    end_time = row['End'].time()
    weight = weights[row['Expertise']]

    for time_slot in time_slots:
        if start_time <= time_slot < end_time:
            weighted_availability.loc[time_slot, row['Skill']] += weight

# Calculate the lack of availability by subtracting from the maximum possible weighted availability
max_weight = sum(weights.values())
for skill in weighted_availability.columns:
    expected_count = df[df['Skill'] == skill].shape[0] * max_weight
    weighted_availability[skill] = expected_count - \
        weighted_availability[skill]

# Custom colormap: light red -> yellow -> green
colors = ["#ffcccc", "#ffff99", "#66ff66"]
cmap = LinearSegmentedColormap.from_list("custom_cmap", colors, N=100)

# Plotting the heatmap with trend lines
fig, axes = plt.subplots(len(weighted_availability.columns), 1, figsize=(
    12, 24), gridspec_kw={'height_ratios': [1]*len(weighted_availability.columns)})

for i, skill in enumerate(weighted_availability.columns):
    ax = axes[i]

    # Plot the heatmap
    sns.heatmap(weighted_availability[[skill]].T, cmap=cmap,
                annot=True, fmt="d", linewidths=.5, ax=ax, cbar=False)

    # Adding the trend line
    trend_ax = ax.twinx()
    trend_ax.plot(time_slots_str, weighted_availability[skill],
                  color='blue', marker='o', linestyle='-', label='Availability Trend')
    trend_ax.set_ylim(0, weighted_availability.max().max())

    ax.set_title(
        f'Weighted Lack of Developer Availability: {skill}', fontsize=14)
    ax.set_xlabel('Time Slot (24hr)', fontsize=10)
    ax.set_ylabel(skill, fontsize=10)
    trend_ax.set_ylabel('Weighted Availability', fontsize=10)

    ax.set_xticks(np.arange(len(time_slots)) + 0.5)
    ax.set_xticklabels(time_slots_str, rotation=45)
    ax.set_yticks([])

plt.tight_layout()
# Save the image to a file
plt.savefig('plots/linear_trend_seaborn.png')
plt.show()
