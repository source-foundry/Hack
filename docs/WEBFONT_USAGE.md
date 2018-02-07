### Web Font Usage

Hack web fonts are released in woff and woff2 formats.  They include a complete Hack character set build and a subset build that includes ASCII, Latin-1, Latin Extended A, General Punctuation, and Currency Unicode character set support.  The latter build set is smaller in size and is intended to improve page loading times when you do not need the entire Hack character set.

You can view the rendering of the web fonts at a range of sizes on the [Hack web font type specimen](http://source-foundry.github.io/Hack/font-specimen.html).

#### Hack by CDN

Thanks to the generous gangs at [jsDelivr](https://github.com/jsdelivr/jsdelivr) and [cdnjs](https://www.cdnjs.com), you can use a CDN to include Hack on your site with a single stylesheet link in the head of your HTML files.  There is no need to download font files from the repository or serve them from your web server.  Instructions for web font CDN use are available on our README page and you can use either of the following CDN:

[![jsDelivr](https://img.shields.io/badge/jsDelivr-Hack_web_font_CDN-blue.svg?style=flat-square)](https://www.jsdelivr.com/package/npm/hack-font)
[![cdnjs](https://img.shields.io/badge/cdnjs-Hack_web_font_CDN-blue.svg?style=flat-square)](https://cdnjs.com/libraries/hack-font)

#### Host Hack Font Files on Your Server

The following instructions are for those who prefer not to use the web font CDN approach described above. If you would like to host the web fonts and CSS files yourself, please follow the instructions below.

Download the [latest release of the Hack web fonts and associated CSS files](https://github.com/source-foundry/Hack/releases/latest).

The web font archive path structure is as follows:

```
    web
    ├── fonts
    │   ├── hack-bold-subset.woff
    │   ├── hack-bold-subset.woff2
    │   ├── hack-bold.woff
    │   ├── hack-bold.woff2
    │   ├── hack-bolditalic-subset.woff
    │   ├── hack-bolditalic-subset.woff2
    │   ├── hack-bolditalic.woff
    │   ├── hack-bolditalic.woff2
    │   ├── hack-italic-subset.woff
    │   ├── hack-italic-subset.woff2
    │   ├── hack-italic.woff
    │   ├── hack-italic.woff2
    │   ├── hack-regular-subset.woff
    │   ├── hack-regular-subset.woff2
    │   ├── hack-regular.woff
    │   └── hack-regular.woff2
    ├── hack-subset.css
    └── hack.css
```

Push one of the CSS files and the `fonts` directory to your web server, then import the CSS file in the `head` section of the HTML where you would like to use it.

Replace `path/to/` with the actual path to your css directory.

##### Subset web font import

```html
<link rel="stylesheet" href="path/to/hack-subset.css">
```


##### Full character set import

```html
<link rel="stylesheet" href="path/to/hack.css">
```

You can alter the path to the Hack files (e.g. place the files in a `hack` resource subdirectory); however, please make sure that you preserve the relative file paths included in the release archive (*or modify the paths to the font files included in the CSS files*).

Then style your text by including `Hack` in the appropriate `font-family` property of your CSS.  For example:

```css
code {
    font-family: Hack, monospace;
}
```

The **bold**, *oblique*, and <b><i>bold oblique</i></b> text styles are formatted with HTML using `<b>text block</b>`, `<i>text block</i>`, and `<b><i>text block</i></b>` HTML tags, respectively.

