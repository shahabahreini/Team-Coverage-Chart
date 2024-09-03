import yaml
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

# Create subplots
num_skills = len(skill_groups)
fig = make_subplots(rows=num_skills, cols=1, shared_xaxes=False, vertical_spacing=0.15,
                    subplot_titles=list(skill_groups.keys()))

# Consistent color coding
colors = {
    'Senior Developer': 'rgb(31, 119, 180)',  # Blue
    'Mid-Level Developer': 'rgb(44, 160, 44)',  # Green
    'Junior Developer': 'rgb(255, 127, 14)',  # Orange
    'Principal/Lead Developer': 'rgb(214, 39, 40)'  # Red
}

for skill_index, (skill, dev_list) in enumerate(skill_groups.items(), start=1):
    for dev_name in dev_list:
        dev_data = df[(df['Skill'] == skill) & (
            df['Name'] == dev_name)].iloc[0]

        fig.add_trace(go.Bar(
            y=[dev_name],
            x=[dev_data['End_float'] - dev_data['Start_float']],
            base=dev_data['Start_float'],
            name=dev_data['Expertise'],
            orientation='h',
            text=f"{dev_data['Name']} ({dev_data['Expertise']})",
            hoverinfo='text',
            marker_color=colors.get(dev_data['Expertise'], 'grey'),
            showlegend=skill_index == 1,  # Show legend only for the first subplot
        ), row=skill_index, col=1)

# Update layout
fig.update_layout(
    title='Skill Coverage by Expertise During the Day',
    height=300 * num_skills,  # Adjust height based on number of skills
    width=1200,
    showlegend=True,
    legend=dict(
        title="Expertise Level",
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02
    ),
    bargap=0.2,
    bargroupgap=0.2,
)

# Update x-axes and add time axes for each subplot
for i in range(1, num_skills + 1):
    fig.update_xaxes(
        title_text="Time (hours)",
        tickvals=[i for i in range(25)],
        ticktext=[f"{i:02d}:00" for i in range(25)],
        range=[0, 24],
        row=i, col=1
    )


# Update y-axes
for i in range(1, num_skills + 1):
    fig.update_yaxes(title_text="Developers", row=i, col=1)

fig.show()
