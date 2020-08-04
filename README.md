# ComicResizer
Utility to batch resize all pages of a comic, with automatic detection of double pages and other size related anomalies.

![Screenshot](https://github.com/Tyronnosaurus/ComicResizer/blob/master/screenshot.jpg?raw=true)

Run ComicResizer.py (or .pyw) to start, or add it to the context menu for valid files:
- Archives: zip, rar, cbr, cbz
- Folders with images inside
- Single images

The Smart Resizing setting will analyse the overall size of every page in a comic and make an educated guess of which pages
are double spreads (or other size anomalies). Rather than resizing them to the specified size, it will keep the proportions
it originally had with the other pages.
