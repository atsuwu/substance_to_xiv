import os
from pathlib import Path
import subprocess

import substance_painter # type: ignore

script_dir = os.path.dirname(os.path.abspath(__file__))
metadata = substance_painter.project.Metadata("SubstanceToXIV")


def get_texconv_bin(textools_path):
    return os.path.join(textools_path, "FFXIV_TexTools/converters/texconv.exe")


def get_consoletools_bin(textools_path):
    return os.path.join(textools_path, "FFXIV_TexTools/ConsoleTools.exe")


def get_tex_path():
    return metadata.get("mod_folder")


def get_format(input_path, settings):
    """Gets the compression format from the input path."""

    name = os.path.splitext(input_path)[0]

    if name.endswith(
        ("_d", "_diff", "_diffuse", "_albedo", "_base", "_basecolor", "_color")
    ):
        return settings["format_d"]

    elif name.endswith("_id"):
        return settings["format_id"]

    elif name.endswith(("_m", "_mask")):
        return settings["format_m"]

    elif name.endswith(("_n", "_norm", "_normal", "_normals")):
        return settings["format_n"]

    else:
        return settings["format_fallback"]


def to_dds(input_path, settings, fast_mode):
    """Converts PNG/TGA to DDS."""

    working_dir = Path(input_path)
    os.chdir(working_dir.parent)

    if fast_mode:
        compression_format = "B8G8R8A8_UNORM"
    else:
        compression_format = get_format(input_path, settings)

    dds_args = (
        get_texconv_bin(settings["textools_path"]),
        '-f',
        compression_format,
        '-m',
        '11',
        '-y',
        input_path,
    )

    subprocess.run(dds_args, stdout=subprocess.PIPE, shell=True)

    output_path = input_path.replace(".png", ".dds")
    output_path = output_path.replace(".tga", ".dds")

    return(output_path, compression_format)


def to_tex(input_path, settings):
    """Converts DDS to TEX."""

    working_dir = Path(input_path)
    os.chdir(working_dir.parent)

    input_path = input_path.replace(".png", ".dds")
    input_path = input_path.replace(".tga", ".dds")
    output_path = input_path.replace(".dds", ".tex")

    if metadata.get("mod_folder") != "" and metadata.get("move_tex") is True:
        Path(metadata.get("mod_folder")).mkdir(parents=True, exist_ok=True)
        output_path = os.path.join(metadata.get("mod_folder"), os.path.basename(output_path))

    tex_args = (
        get_consoletools_bin(settings["textools_path"]),
        '/wrap',
        input_path,
        output_path,
    )

    subprocess.run(tex_args, stdout=subprocess.PIPE, shell=True)

    return(output_path)
