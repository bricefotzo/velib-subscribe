import argparse
import os


def generate_config(email: str, station: str, time: str) -> str:
    """
    Generates a GitHub Actions YML configuration based on the user's email, station, and time preferences.

    Args:
        email (str): User's email.
        station (str): User's preferred station.
        time (str): Time in HH:MM format.

    Returns:
        str: GitHub Actions YML configuration.
    """
    # Validate the time format
    try:
        cron_hour, cron_minute = time.split(':')
    except ValueError:
        raise ValueError("Invalid time format. Expected 'HH:MM'")

    github_config = f"""
name: Scheduled Notification for {email}
on:
  schedule:
    - cron: "{cron_minute} {cron_hour} * * *"
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
    - name: Check out code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Execute script
      run: PYTHONPATH=$(pwd) python jobs/notifier.py "{email}" "{station}"
      env:
        MONGO_URI: ${{ secrets.MONGO_URI }}
        EMAIL_USER: ${{ secrets.EMAIL_USER }}
        EMAIL_PASS: ${{ secrets.EMAIL_PASS }}
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""
    return github_config


def register(email: str, github_config: str) -> None:
    """
    Writes the GitHub Actions configuration to a file.

    Args:
        email (str): User's email.
        github_config (str): GitHub Actions YML configuration.
    """
    # Create folder if not exists
    folder_path = ".github/workflows"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Generate file name based on the email
    filename = f"{folder_path}/schedule_{email.replace('@', '_').replace('.', '_')}.yml"

    # Write to file
    with open(filename, 'w') as file:
        file.write(github_config)


def main():
    parser = argparse.ArgumentParser(description="Generate GitHub Actions configurations.")
    parser.add_argument("email", type=str, help="User's email")
    parser.add_argument("station", type=str, help="Preferred station")
    parser.add_argument("time", type=str, help="Preferred time in HH:MM format")

    args = parser.parse_args()

    try:
        config = generate_config(args.email, args.station, args.time)
        register(args.email, config)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
