### Web Font Usage

Hack webfonts are released in eot, ttf, woff, and woff2 formats.  They include a complete Hack character set build and a smaller [basic Latin](http://www.unicode.org/charts/PDF/U0000.pdf) + [Latin-1 supplement](http://www.unicode.org/charts/PDF/U0080.pdf) Unicode character block build.  The latter build set is smaller in size and is intended to improve page loading times when you do not need the entire Hack character set.

You can view the rendering of the web fonts at a range of sizes on the [Hack type specimen](http://chrissimpkins.github.io/Hack/font-specimen.html).

#### Hack by CDN

Thanks to the generous gang at [jsDelivr](https://github.com/jsdelivr/jsdelivr), you can use a CDN to include Hack on your site with a single stylesheet link in the head of your HTML files.  There is no need to download font files from the repository or serve them from your web server.

Average latency, average uptime, and total downtime data for jsDelivr vs. other popular CDN are available for [http](http://www.cdnperf.com/#jsdelivr,cdnjs,google,yandex,microsoft,jquery,bootstrapcdn/http/30) and [https](http://www.cdnperf.com/#jsdelivr,cdnjs,google,yandex,microsoft,jquery,bootstrapcdn/https/30) protocols.

Include **one** of the following lines in the `<head>` section of your site's HTML:

##### Basic Latin + Latin-1 Supplement Character Set

```html
<link rel="stylesheet" href="//cdn.jsdelivr.net/font-hack/2.020/css/hack.min.css">
```

##### Full Character Set

```html
<link rel="stylesheet" href="//cdn.jsdelivr.net/font-hack/2.020/css/hack-extended.min.css">
```

Then style your text by including `Hack` in the appropriate `font-family` property of your CSS.  For example:

```css
pre, code {
	font-family: Hack, monospace;
}
```

**Bold** and _italic_ styles are included by default and work out-of-the-box via the `<strong>` and `<em>` tags.


#### Host Hack Font Files on Your Server

Download the entire web font archive at this link:

- [Download Web Font Archive (all)](https://github.com/chrissimpkins/Hack/releases/download/v2.020/Hack-v2_020-webfonts.zip)

Or select the fonts that you need in subdirectories of the build directory:

- [Download .eot fonts](https://github.com/chrissimpkins/Hack/tree/master/build/webfonts/fonts/eot)
- [Download .ttf fonts](https://github.com/chrissimpkins/Hack/tree/master/build/webfonts/fonts/web-ttf) - **Note**: these differ from the desktop versions and are intended for web use
- [Download .woff fonts](https://github.com/chrissimpkins/Hack/tree/master/build/webfonts/fonts/woff)
- [Download .woff2 fonts](https://github.com/chrissimpkins/Hack/tree/master/build/webfonts/fonts/woff2)

The web font archive download is structured like this:

```
.
├── css
│   ├── hack-extended.css
│   ├── hack-extended.min.css
│   ├── hack.css
│   └── hack.min.css
└── fonts
    ├── eot
    │   ├── hack-bold-webfont.eot
    │   ├── hack-bolditalic-webfont.eot
    │   ├── hack-regular-webfont.eot
    │   ├── hack-italic-webfont.eot
    │   └── latin
    │       ├── hack-bold-latin-webfont.eot
    │       ├── hack-bolditalic-latin-webfont.eot
    │       ├── hack-regular-latin-webfont.eot
    │       └── hack-italic-latin-webfont.eot
    ├── ttf
    │   ├── hack-bold-webfont.ttf
    │   ├── hack-bolditalic-webfont.ttf
    │   ├── hack-regular-webfont.ttf
    │   ├── hack-italic-webfont.ttf
    │   └── latin
    │       ├── hack-bold-latin-webfont.ttf
    │       ├── hack-bolditalic-latin-webfont.ttf
    │       ├── hack-regular-latin-webfont.ttf
    │       └── hack-italic-latin-webfont.ttf
    ├── woff
    │   ├── hack-bold-webfont.woff
    │   ├── hack-bolditalic-webfont.woff
    │   ├── hack-regular-webfont.woff
    │   ├── hack-italic-webfont.woff
    │   └── latin
    │       ├── hack-bold-latin-webfont.woff
    │       ├── hack-bolditalic-latin-webfont.woff
    │       ├── hack-regular-latin-webfont.woff
    │       └── hack-italic-latin-webfont.woff
    └── woff2
        ├── hack-bold-webfont.woff2
        ├── hack-bolditalic-webfont.woff2
        ├── hack-regular-webfont.woff2
        ├── hack-italic-webfont.woff2
        └── latin
            ├── hack-bold-latin-webfont.woff2
            ├── hack-bolditalic-latin-webfont.woff2
            ├── hack-regular-latin-webfont.woff2
            └── hack-italic-latin-webfont.woff2
```

Push the `css` and `fonts` directories to your web server, then import **one** of the included CSS files in the `head` section of the HTML where you would like to use it.

Replace `path/to/` with the actual path to your css directory.

##### Basic Latin + Latin-1 Supplement Character Set

```html
<link rel="stylesheet" href="path/to/css/hack.min.css">
```


##### Full Character Set

```html
<link rel="stylesheet" href="path/to/css/hack-extended.min.css">
```

You can alter the path to the Hack files (e.g. place the files in a `hack` resource subdirectory); however, please make sure that you preserve the relative file paths included in the release archive (*or be prepared to modify the paths to the font files*).

Then style your text by including `Hack` in the appropriate `font-family` property of your CSS.  For example:

```css
code {
	font-family: Hack, monospace;
}
```

The **bold**, *oblique*, and <b><i>bold oblique</i></b> text styles are formatted with HTML using `<b>text block</b>`, `<i>text block</i>`, and `<b><i>text block</i></b>` HTML tags, respectively.


##### Webfont Caching and gzip Compression with Cloudflare

*The following information applies to both paid and free accounts*

If you use [Cloudflare](https://cloudflare.com), woff files are cached by default.  To cache the remaining webfont files, add a new page rule for the path to your fonts directory:

```
yoursite.com/path/to/fonts/
```

 and set the rule to `Cache Everything`.

 Cloudflare automates gzip compression of ttf, eot, woff, and svg font files.  The service does not gzip compress woff2 files.
