import json
import subprocess

from aiops.log_processor import process_log_line


def main():
    try:
        result = subprocess.run(
            [
                "docker",
                "logs",
                "--tail",
                "100",
                "cloudops-container",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f"Could not retrieve Docker logs: {error}")
        return

    # Docker may send application logs to either output stream.
    all_logs = result.stdout + "\n" + result.stderr
    processed_count = 0

    for line in all_logs.splitlines():
        line = line.strip()

        # Ignore startup messages and ordinary Flask access logs.
        if not line.startswith("{"):
            continue

        try:
            log_event = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Process only structured HTTP request events.
        if not isinstance(log_event, dict):
            continue

        if log_event.get("event") != "http_request":
            continue

        analysis = process_log_line(line)

        print(json.dumps(analysis, indent=2))
        processed_count += 1

    if processed_count == 0:
        print("No JSON HTTP request events found in Docker logs.")
    else:
        print(f"\nProcessed {processed_count} HTTP request events.")


if __name__ == "__main__":
    main()