#!/usr/bin/env python3
import argparse
import os
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import boto3
from crontab import CronTab


def required_environment(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} must be set")
    return value


def backup_database():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    backup_dir = Path(required_environment("BACKUP_DIR")).expanduser()
    file_path = backup_dir / f"{now}.dump"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "pg_dump",
            required_environment("DB_CONNECTION"),
            "--format=custom",
            f"--file={file_path}",
        ],
        check=True,
    )
    print(f"Backup saved to {file_path}")

    bucket_name = required_environment("S3_BUCKET")
    bucket_folder = os.getenv("S3_BACKUP_DIR", "db-backups/").strip("/")
    object_key = (
        f"{bucket_folder}/{file_path.name}" if bucket_folder else file_path.name
    )

    boto3.client("s3").upload_file(str(file_path), bucket_name, object_key)
    print(f"Backup uploaded to s3://{bucket_name}/{object_key}")


def schedule_weekly_backup():
    cron = CronTab(user=True)
    script_path = Path(__file__).resolve()
    command = shlex.join([sys.executable, str(script_path), "backup_db"])
    job = cron.new(command=command, comment="pause-api-database-backup")
    job.setall("0 0 * * 0")
    cron.write()

    print("Weekly database backup scheduled for Sunday at 00:00.")


def main():
    parser = argparse.ArgumentParser(description="Pause API management commands")
    parser.add_argument(
        "action",
        choices=("backup_db", "sched_backup"),
        help="management action to run",
    )
    args = parser.parse_args()

    if args.action == "backup_db":
        backup_database()
    else:
        schedule_weekly_backup()


if __name__ == "__main__":
    main()
