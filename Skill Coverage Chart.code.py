import yaml
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from datetime import datetime, timedelta
import numpy as np

def parse_time(time_str):
    return datetime.strptime(time_str, "%I:%M %p")

def time_to_hours(time):
    return time.hour + time.minute / 60

def load_data(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def plot_skill_coverage(data):
    skills = list(data.keys())
    fig, ax = plt.subplots(figsize=(24, 16))

    y_pos = 0
    colors = plt.cm.get_cmap('tab20')(np.linspace(0, 1, len(skills)))
    skill_colors = dict(zip(skills, colors))

    # Sort skills to group related ones together
    sorted_skills = sorted(skills, key=lambda x: x.split()[-1])

    for skill in sorted_skills:
        people = data[skill]
        skill_height = max(len(people) * 0.6, 1)  # Increase vertical spacing
        people_sorted = sorted(people.items(), key=lambda x: parse_time(x[1]['start']))
        
        for i, (person, info) in enumerate(people_sorted):
            start_time = parse_time(info['start'])
            end_time = parse_time(info['end'])
            
            start_hours = time_to_hours(start_time)
            duration = time_to_hours(end_time) - start_hours
            if duration < 0:  # Handle cases crossing midnight
                duration += 24
            
            color = skill_colors[skill]
            rect_height = 0.5  # Increase rectangle height
            rect_y = y_pos + i * (rect_height + 0.1)  # Add small gap between rectangles
            rect = Rectangle((start_hours, rect_y), duration, rect_height, facecolor=color, edgecolor='black', alpha=0.7)
            ax.add_patch(rect)
            
            # Adjust text position and size
            text_y = rect_y + rect_height / 2
            ax.text(start_hours + duration/2, text_y, f"{person}\n{info['start']}-{info['end']}", 
                    ha='center', va='center', fontsize=8, wrap=True, 
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=2))
        
        # Add skill label
        ax.text(-0.5, y_pos + skill_height/2, skill, ha='right', va='center', fontsize=10, fontweight='bold')
        
        y_pos += skill_height + 1  # Increase space between skills

    ax.set_ylim(0, y_pos)
    ax.set_xlim(0, 24)
    ax.set_yticks([])  # Remove y-axis ticks
    ax.set_xticks(range(0, 25, 1))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 25, 1)], rotation=45)
    ax.set_xlabel('Time (EST)', fontsize=12)
    ax.set_title('Detailed Skill Coverage Chart', fontsize=16)

    # Add legend
    legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor=skill_colors[skill], edgecolor='black', alpha=0.7) for skill in sorted_skills]
    ax.legend(legend_elements, sorted_skills, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

    plt.tight_layout()
    plt.savefig('detailed_skill_coverage_chart.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    data = load_data('team_data.yaml')
    plot_skill_coverage(data)
    print("Chart has been saved as 'detailed_skill_coverage_chart.png'")