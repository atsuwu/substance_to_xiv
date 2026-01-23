# Substance to XIV

Substance to XIV is a python plugin for Substance Painter that converts exported textures to XIV TEX format and copies them to a mod folder of your choosing. When the export is done, you have the option to force a Penumbra redraw automatically.

(img/gif of plugin UI)

It works only on Windows and uses ConsoleTools and TexConv (both bundled in TexTools, which is required) to convert your textures to DSS and then package them as TEX files XIV can read.

This makes the process of tweaking & iterating on your project textures and seeing the result in game much faster and effortless.

## How it Works

The general idea behind the plugin is that it sees the textures you export in Substance Painter, and while enabled, it will take any PNG or TGA you've exported, convert it to DDS with some optional compression options, then package the DDS as a TEX file, copy the file to the directory you specify and then send a request to Penumbra to redraw your character.

## Limitations

- The plugin relies on you already doing what's necessary for Substance Painter to spit out textures that will work in XIV, with all the channels configured properly. You can achieve this with the right channels setup in your texture set and export presets that match those channels to the `_id`, `_m`, `_n` files you are exporting.

  I'm planning to make a document where I explain my setup for character (skin shader) and general gear (character shader) project setups and export templates, but some of these rely and build upon efforts from other members in the community that I need to remember and give credit to first.

- For now I'm exporting uncompressed textures only, since Penumbra has convenient settings to compress your textures when done editing them, but I'd like to find a good way to expose the compression formats to be used based on texture suffixes so that final texture can be exported from the plugin.

- Because it relies on TexConv to convert files to DDS and i can't test on Linux anyway, the plugin will only work on Windows. If converting to DDS is doable with another Linux based tool, making this plugin work on Linux maybe not be all that complicated and if anyone wants to look into it, you can get in touch with me.

## How to Install

⚠️ TexTools is required for this plugin to work, and only Windows is supported. If you don't have TextTools yet, get it from [https://www.ffxiv-textools.net/](https://www.ffxiv-textools.net/).

1. [Download the latest release](https://github.com/atsuwu/substance_to_xiv/releases). You will get a zip file with a folder named `substance_to_xiv`.

2. Open substance Painter. Click on the `Python` menu and then on `Plugins Folder`

3. Drop the `substance_to_xiv` folder from the zip file in the plugins directory. Now you'll have a folder structure like this.

```txt
Documents
  Adobe
    Adobe Substance 3D Painter
      python
        plugins
          substance_to_xiv
            __init__.py
            convert.py
            icon.png
            ...
```

Now back in Substance Painter, navigate to the `Python` menu, and click on `Reload Plugins Folder`, then click on the menu again and enable the plugin there. The plugin's panel should pop up somewhere in your UI and you can move it to your liking now.

ℹ️ If you close the panel and can't find it anymore, look for it in the `Window` menu.

ℹ️ Additionally, if you have the `Docks` toolbar enabled and you close the plugin's panel, you will find a `XIV TEX` button on the `Docks` toolbar that you can use to access the plugin at any time without it getting in the way too much.

After the first run the plugin will try to detect your TexTools folder, if you installed it in the default location at `C:\Program Files\FFXIV TexTools`. If you installed it in a different location you will have to use the button at the top of the panel to set the path manually.

## How to Build

If you want to edit the code, dev environment setup is explained in the [BUILD.md](https://github.com/atsuwu/substance_to_xiv/blob/main/README.md) file.

## Acknowledgements

- [Textools](https://www.ffxiv-textools.net/).
- [TexConv](https://github.com/microsoft/DirectXTex).
- Aleks for PenumbraClient class in his Yet Another Addon project.
- Ottermandias for Penumbra.
- SB for texture export presets, color row and color blend material setup.

## License

Substance to XIV, Substance Painter plugin that converts exported textures to XIV TEX format and copies them to a mod folder.

Copyright (C) 2026 Atsu.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
