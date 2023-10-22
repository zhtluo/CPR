import argparse
import pathlib
import subprocess

parser = argparse.ArgumentParser(description="Format and compress code.")
parser.add_argument("filename")
parser.add_argument(
    "--clangformat",
    action="store",
    default=str(pathlib.Path.home())
    + "/.vscode/extensions/ms-vscode.cpptools-1.17.5-linux-x64/bin/../LLVM/bin/clang-format",
    help="clang-format path",
)
parser.add_argument("--linewidth", action="store", default="52", help="line width")

args = parser.parse_args()
linewidth = int(args.linewidth)

subprocess.run(
    [
        args.clangformat,
        "-style=file",
        "-fallback-style=LLVM",
        "-i",
        f"{args.filename}",
    ],
    check=True,
)

lines = []
output_lines = []

with open(args.filename, "r") as f:
    output_lines = f.readlines()

while output_lines != lines:
    lines = output_lines
    output_lines = []
    last_indent = 0
    current_line = ""
    for line in lines:
        # strip the line break
        line = line[:-1]
        stripped_line = line.lstrip(" ")
        current_indent = len(line) - len(stripped_line)
        if current_line == "":
            current_line = line
            last_indent = current_indent
        elif (
            stripped_line != ""
            and stripped_line[:1] != "#"
            and stripped_line[:2] != "//"
            and (current_indent >= last_indent or "}" in stripped_line)
            and len(current_line) + 1 + len(stripped_line) <= linewidth
        ):
            current_line = current_line + " " + stripped_line
        else:
            output_lines.append(current_line + "\n")
            current_line = line
            last_indent = current_indent

        # output comment directly
        if stripped_line[:1] == "#" or stripped_line[:2] == "//":
            output_lines.append(current_line + "\n")
            current_line = ""

    if current_line != "":
        output_lines.append(current_line + "\n")

with open(args.filename, "w") as f:
    f.writelines(output_lines)
