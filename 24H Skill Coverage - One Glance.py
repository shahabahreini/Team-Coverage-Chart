import yaml
import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict

# Function to convert time to float (e.g., 1:30 AM -> 1.5)


def time_to_float(t):
    return t.hour + t.minute / 60.0


# Load YAML data
yaml_file_path = 'team_data.yaml'
with open(yaml_file_path, 'r') as file:
    data = yaml.safe_load(file)

# Flatten and process YAML data
developers = []
skill_groups = defaultdict(list)
for skill, devs in data.items():
    if skill != "People":
        for name, details in devs.items():
            start_time = pd.to_datetime(details['start']).time()
            end_time = pd.to_datetime(details['end']).time()
            expertise = details['expertise']
            main_skill = data['People'][name]['main_skill']
            developers.append({
                'Name': name,
                'Skill': skill,
                'Start': start_time,
                'End': end_time,
                'Start_float': time_to_float(start_time),
                'End_float': time_to_float(end_time),
                'Expertise': expertise,
                'Main Skill': main_skill
            })
            skill_groups[skill].append(name)

# Convert to DataFrame
df = pd.DataFrame(developers)

# Create a skill coverage chart with time on the x-axis
fig = go.Figure()

# Add traces for senior, mid-level, and junior developers
colors = {
    'Senior Developer': 'blue',
    'Mid-Level Developer': 'green',
    'Junior Developer': 'orange',
    'Principal/Lead Developer': 'red'
}

# Calculate the number of skills and developers
num_skills = len(skill_groups)
max_devs_per_skill = max(len(devs) for devs in skill_groups.values())

# Add separators between skill groups
for i in range(1, num_skills):
    fig.add_shape(
        type="line",
        x0=0, x1=24,
        y0=i - 0.1, y1=i - 0.1,
        line=dict(color="rgba(0,0,0,0.3)", width=1, dash="dot"),
    )

for skill_index, (skill, dev_list) in enumerate(skill_groups.items()):
    for dev_index, dev_name in enumerate(dev_list):
        dev_data = df[(df['Skill'] == skill) & (
            df['Name'] == dev_name)].iloc[0]
        y_position = skill_index + (dev_index / (max_devs_per_skill + 1))

        fig.add_trace(go.Bar(
            y=[y_position],
            x=[dev_data['End_float'] - dev_data['Start_float']],
            base=dev_data['Start_float'],
            name=dev_data['Name'],
            orientation='h',
            text=f"{dev_data['Name']} ({dev_data['Expertise']})",
            hoverinfo='text',
            marker_color=colors.get(dev_data['Expertise'], 'grey'),
            width=0.8 / (max_devs_per_skill + 1),
            legendgroup=dev_data['Expertise'],
            legendgrouptitle_text=dev_data['Expertise']
        ))

# Update layout
fig.update_layout(
    barmode='stack',
    title='Skill Coverage by Expertise During the Day',
    xaxis_title='Time (hours)',
    yaxis_title='Skill',
    xaxis=dict(
        tickvals=[i for i in range(25)],
        ticktext=[f"{i}:00" for i in range(25)],
        range=[0, 24]
    ),
    yaxis=dict(
        tickvals=[i + 0.5 for i in range(num_skills)],
        ticktext=list(skill_groups.keys()),
        range=[-0.5, num_skills - 0.5]
    ),
    height=800,
    width=1400,
    showlegend=True,
    legend=dict(
        title="Developers",
        orientation="v",
        x=1.05,
        y=1,
        traceorder='grouped'
    ),
    plot_bgcolor='white',
)

fig.show()
