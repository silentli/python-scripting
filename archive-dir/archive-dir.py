import os
import zipfile
import datetime
import logging
import sys
from pathlib import Path
import argparse


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s: %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def zip_directory(source_dir: Path, output_dir: Path) -> Path:
    """
    Zip a directory and return the path to the zip file.
    The zip filename includes the timestamp of the archive.

    Raises:
        FileNotFoundError: If the source directory does not exist
        PermissionError: If the source directory is not readable
        OSError: For general filesystem errors
    """
    if not source_dir.exists() or not source_dir.is_dir():
        raise FileNotFoundError(f"Source directory {source_dir} does not exist or is not a directory")
    
    output_dir.mkdir(parents=True, exist_ok=True)

    # Resolve to absolute paths to ensure consistency regardless of input path type
    source_dir = source_dir.resolve()
    output_dir = output_dir.resolve()

    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    zip_path = output_dir / f"{source_dir.name}_{date_str}.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(source_dir)
                zipf.write(file_path, arcname)
                logger.debug(f"Added {arcname}")

    return zip_path


def parse_args():
    parser = argparse.ArgumentParser(description='Archive a directory')
    parser.add_argument('--source-dir', type=Path, help='Path to the source directory to archive')
    parser.add_argument('--output-dir', type=Path, help='Path to the output directory to archive to')
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        zip_path = zip_directory(args.source_dir, args.output_dir)
        logger.info(f"Zipped {args.source_dir} to {zip_path}")
    except FileNotFoundError as e:
        logger.error(e)
        sys.exit(1)
    except PermissionError as e:
        logger.error(f"Permission error: {e}")
        sys.exit(1)
    except OSError as e:
        logger.error(f"OS error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
