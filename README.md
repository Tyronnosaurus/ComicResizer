# ComicResizer
Utility to batch resize all pages of a comic, with automatic detection of double pages and other size related anomalies.

![Screenshot](https://github.com/Tyronnosaurus/ComicResizer/blob/master/screenshot.PNG?raw=true)

Run ComicResizer.py (or .pyw) to start. Accepts the following files:
- Archives: zip, rar, cbr, cbz
- Folders with images inside
- Single images

(you have an option to add this application to the context menu for valid files)

The Smart Resizing setting will analyze the overall size of every page in a comic and make an educated guess of which pages
are double spreads (or other size anomalies). Rather than resizing them to the specified size, it will keep the proportions
it originally had with the other pages.
