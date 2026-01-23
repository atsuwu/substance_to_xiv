# Substance to XIV

Substance to XIV is a python plugin for Substance Painter that converts exported textures to XIV TEX format and copies them to a mod folder of your choosing. When the export is done, you have the option to force a Penumbra redraw automatically.


TODO: (img/gif of plugin UI)

It works only on Windows and uses ConsoleTools and TexConv (both bundled in TexTools, which is required) to convert your textures to DSS and then package them as TEX files XIV can read.

This makes the process of tweaking & iterating on your project textures and seeing the result in game much faster and effortless.

## How it Works

The general idea behind the plugin is that it sees the textures you export in Substance Painter, and while enabled, it will take any PNG or TGA you've exported, convert it to DDS with some optional compression options, then package the DDS as a TEX file, copy the file to the directory you specify and then send a request to Penumbra to redraw your character.

## Limitations

- The plugin relies on you already doing what's necessary for Substance Painter to spit out textures that will work in XIV, with all the channels configured properly. You can achieve this with the right channels setup in your texture set and export presets that match those channels to the `_id`, `_m`, `_n` files you are exporting.

  If you need help with this, I would recommend this [resource](https://xivmodarchive.com/modid/111473) by SB! which helps you set up your project and organize your color setting textures.

  I'm planning to make a document where I explain my setup for character skin and for gear and export templates, which are based off the link above.

- For now the plugin exports uncompressed textures only, which is faster, since Penumbra has convenient settings to compress your textures when done editing them. I'd like to find a good way to expose the compression formats to be used based on texture suffixes so that final texture can be exported from the plugin.

## Requirements

- **Windows:** Because it relies on TexConv to convert files to DDS and i can't test on Linux anyway, the plugin will only work on Windows. If converting to DDS is doable with another Linux based tool, making this plugin work on Linux maybe not be all that complicated and if anyone wants to look into it, you can give it a try!

- **TexTools:** TexTools needs to be installed on your system for this plugin to work. If you don't have TextTools yet, get it from [https://www.ffxiv-textools.net/](https://www.ffxiv-textools.net/). Installing on the default path is recommended but you can choose your TexTools installation path if needed.

- **Substance Painter:** Substance Painter v11.1.1 or above is recommended, since I can't reliably say whether older versions will work.

## How to Install

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

After the first run the plugin will try to detect your TexTools folder, if you installed it in the default location at `C:\Program Files\FFXIV TexTools`. If you installed it in a different location you will have to use the button near the top of the panel to set the path manually.

ℹ️ If you close the panel and can't find it anymore, look for it in the `Window` menu.

ℹ️ Additionally, if you have the `Docks` toolbar enabled and you close the plugin's panel, you will find a `XIV TEX` button on the `Docks` toolbar that you can use to access the plugin at any time without it getting in the way too much.

## How to Use

The UI should be self explanatory enough, but if you mouse over buttons and so on you will get tooltips that explain things further. To get familiar the best thing to do is make a test project or open an old one, go through the settings in the plugin window and export your textures. Make backups of your files if needed to avoid any chance of loosing data.

Here's a list of the settings and what they do:

<!-- markdownlint-disable -->
<div align="center">
  <img src="https://raw.githubusercontent.com/atsuwu/substance_to_xiv/refs/heads/main/assets/ui.png" alt="Substance Painter to XIV UI" title="Substance Painter to XIV UI" />
</div>
<!-- markdownlint-restore -->

### Main Settings

- **Substance to XIV Enabled/Disabled:** This buttons toggles the plugin on and off. If toggled off, the plugins will ignore exports

- **TexTools Path:** On the first run, the plugin will try to detect if TexTools is installed in the default path, and if so it will set this path for you. If you have installed TexTools in another path, you'll see a prompt to choose the folder. You can click the button at anytime to change the path if you ever need to or if it's not detected automatically.

### Project Settings

- **Texture Folder button:** This is the path that TEX files will be copied to automatically (when the settings to do so is enabled, see below), so it should point to the textures folder in your mod.

  ⚠️ The plugin overwrites files when exporting so make sure to save backups of them if you need to.

- **Move TEX files to mod folder:** This can only be enabled once you have set a path in the previous settings. When enabled TEX files will be moved to the specified folder, if disabled TEX files will be saved on your export folder.

- **Force Penumbra redraw after export:** If enabled, the plugin will try to request to Penumbra to perform a redraw, so that your textures can update in-game right after export. If Penumbra isn't available you'll see an error message in the log.

- **Keep DDS files:** If enabled, DDS files generated before converting to TEX will be kept. DDS files are not moved to any folder, and will remain in your export folder. When this is disabled, the DDS files will be removed as soon as the TEX file is generated.

### Log

- **Log:** The log will show relevant information of what the plugin is doing at any point, loading settings from a project that was opened, saving or deleting files, changing settings, etc.

- **Export:** The Export button will open the Export Textures windows in Substance Painter. In future releases I'd like it to do a quick export.

- **Clear Log:** This just clears the log completely.

## How to Build

If you want to edit the code, dev environment setup is explained in the [BUILD.md](https://github.com/atsuwu/substance_to_xiv/blob/main/BUILD.md) file.

## Acknowledgements

- [Textools](https://www.ffxiv-textools.net/).
- [TexConv](https://github.com/microsoft/DirectXTex).
- Aleks for PenumbraClient class in his [Yet Another Addon](https://github.com/Arrenval/Yet-Another-Addon) project.
- Ottermandias for [Penumbra](https://github.com/xivdev/Penumbra).
- SB for texture export presets, color row and color blend material setup.
- This plugins draws inspiration from [Substance-Painter-DDS-Exporter](https://github.com/emomilol1213/Substance-Painter-DDS-Exporter) by emomilol1213, as well as the sample plugins from the Substance Painter Python API docs.

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

---

Final Fantasy XIV © SQUARE ENIX CO., LTD. All Rights Reserved.

This project is not affiliated with SQUARE ENIX CO., LTD. in any way.
