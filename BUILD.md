# How to Build

(You can skip this if you aren't interested in editing the code)

There isn't anything to build, you can just edit the code in `src/substance_to_xiv` and drop that folder in your Substance Painter plugins directory, but if you want to use the development environment I've set up you can follow these steps.

⚠️ To be able to build you will need [Python 3.14](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/docs/#installation)

⚠️ Keep in mind that even with this whole dev environment, you will still have to reload the plugin each time from the `Python` menu in Substance Painter to see changes in the application, and the layout can sometimes break leaving orphan panels that don't go away until you restart Painter.

- Clone this repo or make your fork and then clone.

```bash
git clone https://github.com/atsuwu/substance_to_xiv.git
cd substance_to_xiv
```

- Create a file named `substance_to_xiv.toml`.

```bash
touch substance_to_xiv.toml
```

- Add this code to the file:

```toml
[substance_to_xiv]
destination = "path/to/substance/painter/plugins/substance_to_xiv"
```

Replace the destination with the actual path, will be something like `C:/Users/{YOUR USERNAME}/Documents/Adobe/Adobe Substance 3D Painter/python/plugins/substance_to_xiv`.

If you are copy pasting the path from your windows explorer, make sure you scape the backward slashes (`\`) by duplicating them or changing them to forward slashes (`/`), otherwise the path with not work.

Now you need to use Poetry to install dependencies and virtual environment, then activate that environment.

```bash
poetry install
poetry env activate
```

Then you can run the build command. This will copy the project files to the Substance Painter plugins folder and watch for modifications to any of the files.

```bash
poetry run build
```

Now you should be good to go and can start making changes to the code.
