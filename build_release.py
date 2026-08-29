#!/usr/bin/env python3
"""Build and verify the complete R4 release artifact from a clean directory."""

from __future__ import annotations

import argparse
import hashlib
import lzma
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REFERENCE_PARTS = ROOT / "assets/reference"
REFERENCE_GLOB = "dock3713_assembly.stl.xz.part-*"
REFERENCE_SHA256 = "86f9a3d3d35259efc6da8f8f69338404213f196d88631f9772347e5200d273d9"
ARCHIVE_NAME = "Tang_Primer_20K_LCD_Case_R4.zip"

SOURCE_FILES = (
    "README.md",
    "DESIGN_R4.md",
    "assembly_r4.py",
    "build_release.py",
    "drawing_assembly_r4.py",
    "generate_assembled_stl_r4.py",
    "generate_case.py",
    "generate_case_r4.py",
    "generate_design_spec_r4.py",
    "generate_drawings.py",
    "generate_reference_3mf_r4.py",
    "generate_release_drawings.py",
    "render_preview.py",
    "render_preview_r4.py",
    "render_spatial_assembly_r4.py",
    "requirements-drawings.txt",
    "requirements-preview.txt",
    "tests/test_drawings.py",
    "tests/test_geometry.py",
    "tests/test_r4.py",
    "verify_release.py",
)


def run(*arguments: str) -> None:
    subprocess.run(
        [sys.executable, *arguments], cwd=ROOT, check=True,
    )


def reset_directory(path: Path) -> None:
    resolved = path.resolve()
    if resolved == ROOT or ROOT not in resolved.parents:
        raise ValueError(f"refusing to clean path outside repository: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True)


def write_checksums(release: Path) -> None:
    entries: list[str] = []
    for path in sorted(release.rglob("*")):
        if not path.is_file() or path.name == "CHECKSUMS.sha256":
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        entries.append(f"{digest}  {path.relative_to(release).as_posix()}")
    (release / "CHECKSUMS.sha256").write_text(
        "\n".join(entries) + "\n", encoding="ascii",
    )


def write_archive(release: Path, archive: Path) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.unlink(missing_ok=True)
    with zipfile.ZipFile(
        archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9,
    ) as bundle:
        for relative in SOURCE_FILES:
            bundle.write(ROOT / relative, relative)
        for path in sorted(release.rglob("*")):
            if path.is_file():
                bundle.write(path, Path("output/release") / path.relative_to(release))
    archive_digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(archive.suffix + ".sha256").write_text(
        f"{archive_digest}  {archive.name}\n", encoding="ascii",
    )


def build(release: Path, archive: Path) -> None:
    reference_parts = sorted(REFERENCE_PARTS.glob(REFERENCE_GLOB))
    if not reference_parts:
        raise FileNotFoundError(
            f"compressed official Dock reference mesh parts are missing: "
            f"{REFERENCE_PARTS / REFERENCE_GLOB}"
        )
    reset_directory(release)
    reference = release / "reference/dock3713_assembly.stl"
    reference.parent.mkdir(parents=True)
    compressed = b"".join(path.read_bytes() for path in reference_parts)
    reference.write_bytes(lzma.decompress(compressed))
    reference_digest = hashlib.sha256(reference.read_bytes()).hexdigest()
    if reference_digest != REFERENCE_SHA256:
        raise ValueError(
            f"official Dock reference mesh hash mismatch: {reference_digest}"
        )

    run("generate_case_r4.py", "--out", str(release))
    for spec in ("43", "50"):
        run(
            "generate_assembled_stl_r4.py",
            "--input", str(release),
            "--dock-step-stl", str(reference),
            "--spec", spec,
            "--output", str(release / f"Tang_Primer_20K_Case_R4_Complete_Assembly_{spec}.stl"),
        )
        run(
            "generate_reference_3mf_r4.py",
            "--input", str(release),
            "--dock-step-stl", str(reference),
            "--spec", spec,
            "--output", str(release / f"Tang_Primer_20K_Case_R4_Reference_Assembly_{spec}.3mf"),
        )

    drawing = release / "Tang_Primer_20K_Case_R4_Drawings_1to1.pdf"
    specification = release / "Tang_Primer_20K_Case_R4_Design_Specification.pdf"
    run(
        "generate_release_drawings.py",
        "--input", str(release),
        "--dock-step-stl", str(reference),
        "--output", str(drawing),
    )
    run("generate_design_spec_r4.py", "--output", str(specification))
    run(
        "verify_release.py",
        "--input", str(release),
        "--drawing", str(drawing),
        "--specification", str(specification),
        "--output", str(release / "verification_report.json"),
    )
    write_checksums(release)
    write_archive(release, archive)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--release-dir", type=Path,
        default=ROOT / "build/artifact/release",
    )
    parser.add_argument(
        "--archive", type=Path,
        default=ROOT / "build/artifact" / ARCHIVE_NAME,
    )
    args = parser.parse_args()
    build(args.release_dir.resolve(), args.archive.resolve())
    print(args.archive.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
