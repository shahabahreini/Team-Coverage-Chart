# Team Skill Coverage Chart

## Overview

This project provides a comprehensive visualization of team and skill coverage for companies with developers across different time zones. It generates detailed charts that illustrate the coverage over a 24-hour period and throughout the weekdays, offering insights into the distribution and availability of team members.

## Features

- **Time Zone Visualization**: Displays team coverage across multiple time zones, ensuring global team coordination.
- **Skill-Based Grouping**: Groups team members by their skills, providing a clear view of skill distribution.
- **Interactive Charts**: Offers visually appealing charts that are easy to interpret, enhancing understanding of team dynamics.
- **Customizable**: Easily adapt the YAML configuration to reflect your team's specific structure and time zones.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries: `yaml`, `matplotlib`, `numpy`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/team-skill-coverage-chart.git
   ```

2. Navigate to the project directory:
   ```bash
   cd team-skill-coverage-chart
   ```

3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Update the `team_data.yaml` file with your team's schedule and skills.
2. Run the script to generate the chart:
   ```bash
   python Skill_Coverage_Chart.py
   ```
3. The chart will be saved as `detailed_skill_coverage_chart.png` in the project directory.

## Configuration

The `team_data.yaml` file should be structured as follows:

```yaml
Frontend Development:
  Alex Johnson:
    start: "1:30 AM"
    end: "10:30 AM"
    type: Primary
  ...
Backend Development:
  ...
```

- **start**: The start time of the team member's availability.
- **end**: The end time of the team member's availability.
- **type**: Indicates whether the member is a Primary or Secondary resource.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

