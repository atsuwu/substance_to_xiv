import shutil
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import tomllib


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_CONFIG = PROJECT_ROOT / "substance_to_xiv.toml"


def load_config():
    with PROJECT_CONFIG.open("rb") as f:
        data = tomllib.load(f)

    cfg = data.get("substance_to_xiv", {})
    dst = cfg.get("destination")

    if not dst:
        print("Missing [substance_to_xiv].destination in substance_to_xiv.toml")
        sys.exit(1)

    return (
        (PROJECT_ROOT / "src/substance_to_xiv").resolve(),
        (Path(dst)).resolve(),
    )


def copy_file(src: Path, dst_root: Path):
    rel = src.relative_to(SRC_DIR)
    dst = dst_root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"Copied: {rel}")


class Handler(FileSystemEventHandler):
    def __init__(self, dst_root: Path):
        self.dst_root = dst_root

    def on_modified(self, event):
        if not event.is_directory:
            copy_file(Path(event.src_path), self.dst_root)

    def on_created(self, event):
        if not event.is_directory:
            copy_file(Path(event.src_path), self.dst_root)


def initial_copy(src_root: Path, dst_root: Path):
    for path in src_root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(src_root)
            dst = dst_root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dst)


def main():
    global SRC_DIR

    SRC_DIR, DST_DIR = load_config()
    DST_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Source:      {SRC_DIR}")
    print(f"Destination: {DST_DIR}")

    print("Initial copy…")
    initial_copy(SRC_DIR, DST_DIR)

    observer = Observer()
    observer.schedule(Handler(DST_DIR), SRC_DIR, recursive=True)
    observer.start()

    print("Watching for changes…")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
