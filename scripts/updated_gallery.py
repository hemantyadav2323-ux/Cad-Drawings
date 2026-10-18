
from pathlib import Path
from html import escape
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = ROOT / "images"
README = ROOT / "README.md"

START = "<!-- CAD-GALLERY:START -->"
END = "<!-- CAD-GALLERY:END -->"

SUPPORTED = {
    ".png", ".jpg", ".jpeg", ".gif",
    ".webp", ".bmp", ".svg"
}


def image_title(path):
    return path.stem.replace("_", " ").replace("-", " ").title()


def make_gallery():
    if not IMAGE_DIR.exists():
        return "_Add images to the `images/` folder to build your gallery._"

    images = sorted(
        p for p in IMAGE_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED
    )

    if not images:
        return "_No supported images found in `images/` yet._"

    rows = []

    for index in range(0, len(images), 2):
        cells = []

        for path in images[index:index + 2]:
            relative = path.relative_to(ROOT).as_posix()
            url = quote(relative, safe="/")
            title = escape(image_title(path))

            cells.append(
                f'<td align="center" width="50%">'
                f'<a href="{escape(url, quote=True)}">'
                f'<img src="{escape(url, quote=True)}" '
                f'alt="{title}" width="400" />'
                f'</a><br/><strong>{title}</strong></td>'
            )

        if len(cells) == 1:
            cells.append("<td width=\"50%\"></td>")

        rows.append("<tr>" + "".join(cells) + "</tr>")

    return "<table>\n" + "\n".join(rows) + "\n</table>"


def main():
    readme = README.read_text(encoding="utf-8")

    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain each gallery marker exactly once.")

    before, remainder = readme.split(START, 1)
    _, after = remainder.split(END, 1)

    updated = (
        before + START + "\n"
        + make_gallery() + "\n"
        + END + after
    )

    if updated != readme:
        README.write_text(updated, encoding="utf-8")
        print("README gallery updated.")
    else:
        print("README gallery is already up to date.")


if __name__ == "__main__":
    main()

