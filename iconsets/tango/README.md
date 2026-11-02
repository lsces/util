# Tango icon set

`scalable/` holds the SVG icons (48x48). Icons are looked up by file name (`biticon` `iname`).

## bwfm- icons (media workflow)

`bwfm-<media>.svg` (the base icon at full size) with `bwfm-<media>-add.svg` (blue plus) and `bwfm-<media>-load.svg` (green down arrow) are composed from
existing Tango icons by `make_icons.py`, so they stay together and in step on the icon crib sheet:

| Media | Base icon |
|---|---|
| `bwfm-film` | `video` |
| `bwfm-tv` | `video-television` |
| `bwfm-music` | `audio-x-generic` |
| `bwfm-book` | `accessories-dictionary` |
| `bwfm-tutorial` | `application-vnd.ms-powerpoint.presentation.macroEnabled.12` (a presentation board; one of ten identical copies) |
| `bwfm-author` | `dashboard-show` + `cs-user` badge (author workbench; single file, no add/load) |
| `bwfm-series` | `dashboard-show` + `cs-user-accounts` badge (series workbench; single file, no add/load) |

Regenerate (overwrites the seventeen files; needs python3 and lxml):

    cd util/iconsets/tango
    python3 -I make_icons.py scalable scalable bwfm-film=video bwfm-tv=video-television \
        bwfm-music=audio-x-generic bwfm-book=accessories-dictionary \
        bwfm-tutorial=application-vnd.ms-powerpoint.presentation.macroEnabled.12 \
        bwfm-author=dashboard-show+cs-user bwfm-series=dashboard-show+cs-user-accounts

To add another set, pass more `name=base` pairs; `name=base+badge` uses another icon as the corner badge (scaled to 62%). The base is scaled to 84% and pinned top-left; the
badge is 80% size, bottom-right. The badges are drawn in `make_icons.py` (`BADGES`).
