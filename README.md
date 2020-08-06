# ComicResizer
Utility to batch resize all pages of a comic, with automatic detection of double pages and other size related anomalies.

![Screenshot](https://github.com/Tyronnosaurus/ComicResizer/blob/master/screenshot.PNG?raw=true)

Run ComicResizer.py (or .pyw) to start. Requires Python 3.x.

Accepts the following sources:
- Archives: zip, rar, cbr, cbz
- Folders with images inside
- Single images

(you have a tool to add this application to the context menu for valid files)

The Smart Resizing setting will analyze the size of every page in a comic and make an educated guess of which pages
are double spreads (or other size anomalies). For these, rather than resizing to the specified size, it will keep the proportions
they originally had with the other pages.
