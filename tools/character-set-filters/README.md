# AGL name filters for Glyphs

## How to set up the filter lists in this folder

1. Open a font UFO in the Glyphs Mac app.
2. In the bottom left corner, find the “Filters” section.
3. Make sure the detail view below this is expanded.  If it is not, click the squared arrow upwards button.
4. Select the first regular filter, “Mac Roman”.
5. Click the cog icon below, choose “Edit Smart Filter”. *\**
6. Focus the newline-separated character names list.
7. Using <kbd>Cmd</kbd>+<kbd>A</kbd>, <kbd>Backspace</kbd>, delete its contents.
8. Paste the contents from the “Mac-Roman.txt” file in this folder.
9. Confirm with “OK”.
10. Repeat this for the “Windows 1252” filter.
11. Click the cog icon, and choose “Add List Filter”.
12. Name the new filter “MES-1”, and paste the contents of the corresponding file in this folder.
13. After clicking “OK”, repeat this for more custom filters.

\* Editing the existing Glyphs filters is necessary since their AGL list contains some minor errors compared to the official `aglfn.txt`.

## How to add missing characters via a Glyphs filter

1. Right-click the filter.
2. In the appearing popup, click the glyph name that you want to add.
3. Using the search field at the bottom, find the glyph by its Unicode point or name.
4. Double-click to edit the new glyph.
