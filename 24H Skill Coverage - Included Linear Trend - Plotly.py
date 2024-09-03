import pandas as pd
import yaml
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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

# Sort the columns (skills) alphabetically or as per another preferred order
weighted_availability = weighted_availability[sorted(
    weighted_availability.columns)]

# Create a subplot for each skill (2 rows per skill: heatmap and linear chart)
fig = make_subplots(
    rows=len(weighted_availability.columns) * 2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.07,
    subplot_titles=[f"{skill} - Heatmap" for skill in weighted_availability.columns] +
                   [f"{skill} - Trend" for skill in weighted_availability.columns]
)

# Custom color scale: light red -> yellow -> green
colorscale = [
    [0.0, "#ffcccc"],
    [0.5, "#ffff99"],
    [1.0, "#66ff66"]
]

# Plot each skill as a heatmap and add the trend line in a separate subplot
for i, skill in enumerate(weighted_availability.columns):
    # Heatmap
    heatmap = go.Heatmap(
        z=[weighted_availability[skill].values],
        x=time_slots_str,
        y=[skill],
        colorscale=colorscale,
        showscale=False
    )
    fig.add_trace(heatmap, row=i*2+1, col=1)

    # Trend line
    trend_line = go.Scatter(
        x=time_slots_str,
        y=weighted_availability[skill],
        mode='lines+markers',
        line=dict(color='blue'),
        name=f'{skill} Availability Trend'
    )
    fig.add_trace(trend_line, row=i*2+2, col=1)

    # Update y-axis range for trend line
    y_max = weighted_availability[skill].max()
    fig.update_yaxes(range=[0, y_max * 1.1], row=i*2+2, col=1)

    # Add dashed line between skill groups
    if i < len(weighted_availability.columns) - 1:
        fig.add_shape(
            type="line",
            x0=0, x1=1, y0=0, y1=0,
            xref="paper", yref="paper",
            line=dict(color="Gray", width=1, dash="dash"),
            row=i*2+2, col=1
        )

# Update layout
fig.update_layout(
    # Increase height to avoid overlapping
    height=300 * len(weighted_availability.columns),
    title_text='Weighted Developer Availability by Skill',
    showlegend=False,
    # Add margins to avoid cutting off labels
    margin=dict(t=50, b=50, l=50, r=50)
)

# Update x-axes for all subplots to show time labels
for i in range(len(weighted_availability.columns) * 2):
    fig.update_xaxes(
        tickangle=45,
        # Only add title to trend charts
        title_text='Time Slot (24hr)' if i % 2 == 1 else None,
        row=i+1, col=1
    )

# Update y-axes to remove skill labels from trend charts
for i in range(len(weighted_availability.columns)):
    fig.update_yaxes(
        title_text='',  # Remove y-axis title
        showticklabels=False,  # Hide tick labels
        row=i*2+2, col=1
    )

# Show the plot
fig.show()
