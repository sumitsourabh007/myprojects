"""Parse a published Google Doc describing a 2D grid of Unicode characters
and print the grid so that, in a fixed-width font, it renders a message
made of uppercase letters.

The document contains a table whose columns are:
    x-coordinate | Character | y-coordinate

Coordinate (0, 0) is the bottom-left corner of the grid. The x-axis
increases to the right and the y-axis increases upward. Any position not
listed in the table is rendered as a space.
"""

import requests
from bs4 import BeautifulSoup


def print_grid_from_doc(url: str) -> None:
    """Fetch the published Google Doc at ``url`` and print its character grid."""
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if table is None:
        raise ValueError("No table found in the document.")

    points = []
    for row in table.find_all("tr"):
        cells = row.find_all(["td", "th"])
        if len(cells) < 3:
            continue
        x_text = cells[0].get_text(strip=True)
        char = cells[1].get_text(strip=True)
        y_text = cells[2].get_text(strip=True)
        try:
            x, y = int(x_text), int(y_text)
        except ValueError:
            continue  # header row or malformed line
        points.append((x, y, char))

    if not points:
        return

    max_x = max(x for x, _, _ in points)
    max_y = max(y for _, y, _ in points)

    grid = [[" "] * (max_x + 1) for _ in range(max_y + 1)]
    for x, y, char in points:
        grid[y][x] = char

    # (0, 0) is the bottom-left, so render rows from the top down.
    for y in range(max_y, -1, -1):
        print("".join(grid[y]))


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python solution.py <google-doc-url>", file=sys.stderr)
        sys.exit(1)
    print_grid_from_doc(sys.argv[1])
