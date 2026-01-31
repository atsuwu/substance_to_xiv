import os

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QKeyEvent
import substance_painter # type: ignore
import substance_painter.ui # type: ignore

from . import convert
from .penumbra import PenumbraClient
from .settings import Settings

penumbra = PenumbraClient()
script_dir = os.path.dirname(os.path.abspath(__file__))
settings = Settings(os.path.join(script_dir, "settings.json"))
metadata = substance_painter.project.Metadata("SubstanceToXIV")
version = "0.1.0"

XIVTEX_PLUGIN = None


def init_metadata():
    metadata.set("version", 1)
    metadata.set("plugin_enable", False)
    metadata.set("mod_folder", "")
    metadata.set("move_tex", False)
    metadata.set("fast_mode", False)
    metadata.set("keep_dds", False)
    metadata.set("redraw", False)

    return "Project settings initialized."


def load_metadata():
    project_data = metadata.list()
    if not project_data:
        return init_metadata()
    else:
        return "Project settings loaded."


def init_enable_button(self):
    state = metadata.get("plugin_enable")
    metadata.set("plugin_enable", state)


def get_enable_button_text(self):
    enabled = metadata.get("plugin_enable")
    if enabled:
        return "Substance to XIV Enabled"
    else:
        return "Substance to XIV Disabled"


def get_textools_button_text(self):
    #  TODO: Improve this, separate button label logic from path validation and button initialization.
    textools_path = settings.get("textools_path", "C:/Program Files/FFXIV TexTools")
    console_tools = os.path.join(textools_path, "FFXIV_TexTools/ConsoleTools.exe")
    if os.path.exists(textools_path) and os.path.isfile(console_tools):
        self.TexToolsPath = textools_path
        settings.set("textools_path", textools_path)
        return f"TexTools Path\n'{self.TexToolsPath}'"
    else:
        self.TexToolsPath = None
        return "TexTools not found, click here to set path..."


class XIVTexPlugin:
    def __init__(self):
        # Init settings.
        textools_button_text = get_textools_button_text(self)

        # Layout Elements.
        self.label_mainsettings = QtWidgets.QLabel("MAIN SETTINGS")
        self.button_textools = QtWidgets.QPushButton(textools_button_text)
        self.checkbox_move_tex = QtWidgets.QCheckBox("Move TEX files to mod folder")
        self.checkbox_move_tex.setDisabled(True)
        self.checkbox_redraw = QtWidgets.QCheckBox("Force Penumbra redraw after export")
        self.checkbox_fast_mode = QtWidgets.QCheckBox("Fast Mode (ignore compression settings)")
        self.checkbox_keep_dds = QtWidgets.QCheckBox("Keep DDS files")
        self.label_projectsettings = QtWidgets.QLabel("PROJECT SETTINGS")
        self.button_enable = QtWidgets.QPushButton("Substance to XIV Disabled")
        self.button_modfolder = QtWidgets.QPushButton("Click here to set a texture folder...")
        self.label_log = QtWidgets.QLabel("LOG")
        self.log = QtWidgets.QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Log will be shown here...")
        self.info = QtWidgets.QTextBrowser()
        self.info.setHtml(f"""
            <h3>Substance to XIV v{version}</h3>
            <p>Copyright (C) 2026 Atsu.<br>This software is licensed under GNU GPL-3.0.</p>
            <p>For newer versions check the <a href='https://github.com/atsuwu/substance_to_xiv/releases'>Github releases page</a>.</p>
            <h3>Thanks</h3>
            <p>Here's a list of projects and people that made this plugin possible:</p>
            <ul>
                <li><a href='https://www.ffxiv-textools.net/'>TexTools</a>.</li>
                <li><a href='https://github.com/microsoft/DirectXTex'>TexConv</a>.</li>
                <li>Aleks for PenumbraClient class in his <a href='https://github.com/Arrenval/Yet-Another-Addon'>Yet Another Addon</a> project.</li>
                <li>Ottermandias for <a href='https://github.com/xivdev/Penumbra'>Penumbra</a>.</li>
                <li>The <a href='https://github.com/goatcorp/Dalamud'>Dalamud</a> team for making all this possible.</li>
                <li>SB! for <a href='https://xivmodarchive.com/modid/111473'>Substance Painter Export + Colorsetting Resources</a>, color row and color blend material setup.</li>
                <li>This plugin draws inspiration from <a href='https://github.com/emomilol1213/Substance-Painter-DDS-Exporter'>Substance-Painter-DDS-Exporter</a> by emomilol1213, as well as the sample plugins from the Substance Painter Python API docs.</li>
            </ul>
            <p>Final Fantasy XIV © SQUARE ENIX CO., LTD. All Rights Reserved.<br>This project is not affiliated with SQUARE ENIX CO., LTD. in any way.</p>
        """)
        self.info.setOpenExternalLinks(True)
        self.button_quick_export = QtWidgets.QPushButton("Export")
        self.button_clear_log = QtWidgets.QPushButton("Clear Log")

        # Tooltips.
        self.button_textools.setToolTip("Set TexTools main directory, usually 'C:/Program Files/FFXIV TexTools'.")
        self.checkbox_move_tex.setToolTip("Enable moving of .TEX files, if disabled they will remain your project's export folder.")
        self.checkbox_redraw.setToolTip("This will try to get Penumbra to redraw after textures are exported. Make sure to enable 'Move TEX files to mod folder' for this to work.")
        self.checkbox_fast_mode.setToolTip("When enabled, compression settings will be ignored and all textures will be saved uncompressed to make the export a bit faster.")
        self.checkbox_keep_dds.setToolTip("Keep DDS files generated by TexConv, usually not needed.")
        self.button_modfolder.setToolTip("Set a mod folder where .TEX files will be moved to after export.")
        self.button_quick_export.setToolTip("Open Export Textures window.")
        self.button_clear_log.setToolTip("Clear all log contents.")

        # Handle UI on startup.
        if substance_painter.project.is_open():
            self.update_ui()
        else:
            self.disable_project_settings()

        # Create tabs widgets.
        tabs = QtWidgets.QTabWidget()

        # Tab 1: Project Settings.
        tab_project = QtWidgets.QWidget()
        tab_project_layout = QtWidgets.QVBoxLayout(tab_project)
        tab_project_layout.setAlignment(Qt.AlignTop)
        tab_project_layout.addWidget(self.button_enable)
        tab_project_layout.addWidget(self.button_modfolder)
        tab_project_layout.insertSpacing(2, 5)
        tab_project_layout.addWidget(self.checkbox_move_tex)
        tab_project_layout.addWidget(self.checkbox_redraw)
        tab_project_layout.addWidget(self.checkbox_fast_mode)
        tab_project_layout.addWidget(self.checkbox_keep_dds)
        tab_project_layout.insertSpacing(7, 15)
        tab_project_layout.addWidget(self.log)
        layout_actions = QtWidgets.QHBoxLayout()
        layout_actions.addWidget(self.button_quick_export)
        layout_actions.addWidget(self.button_clear_log)
        tab_project_layout.addLayout(layout_actions)

        # Tab 2: Main Settings.
        tab_settings = QtWidgets.QWidget()
        tab_settings_layout = QtWidgets.QVBoxLayout(tab_settings)
        tab_settings_layout.setAlignment(Qt.AlignTop)
        tab_settings_layout.addWidget(self.button_textools)
        tab_settings_layout.insertSpacing(1, 15)

        # Tab 2: Info.
        tab_info = QtWidgets.QWidget()
        tab_info_layout = QtWidgets.QVBoxLayout(tab_info)
        tab_info_layout.addWidget(self.info)

        self.formats = [
            "BC1_UNORM",
            "BC3_UNORM",
            "BC5_UNORM",
            "BC7_UNORM",
            "B8G8R8A8_UNORM"
        ]

        self.label_formats = QtWidgets.QLabel("COMPRESSION FORMATS:")
        tab_settings_layout.addWidget(self.label_formats)

        self.label_d = QtWidgets.QLabel("Diffuse:")
        self.combo_format_d = QtWidgets.QComboBox()
        self.combo_format_d.addItems(self.formats)

        diffuse_layout = QtWidgets.QHBoxLayout()
        diffuse_layout.addWidget(self.label_d)
        diffuse_layout.addWidget(self.combo_format_d)

        self.label_id = QtWidgets.QLabel("Id:")
        self.combo_format_id = QtWidgets.QComboBox()
        self.combo_format_id.addItems(self.formats)

        id_layout = QtWidgets.QHBoxLayout()
        id_layout.addWidget(self.label_id)
        id_layout.addWidget(self.combo_format_id)

        self.label_m = QtWidgets.QLabel("Mask:")
        self.combo_format_m = QtWidgets.QComboBox()
        self.combo_format_m.addItems(self.formats)

        mask_layout = QtWidgets.QHBoxLayout()
        mask_layout.addWidget(self.label_m)
        mask_layout.addWidget(self.combo_format_m)

        self.label_n = QtWidgets.QLabel("Normal:")
        self.combo_format_n = QtWidgets.QComboBox()
        self.combo_format_n.addItems(self.formats)

        normal_layout = QtWidgets.QHBoxLayout()
        normal_layout.addWidget(self.label_n)
        normal_layout.addWidget(self.combo_format_n)

        tab_settings_layout.addLayout(diffuse_layout)
        tab_settings_layout.addLayout(id_layout)
        tab_settings_layout.addLayout(mask_layout)
        tab_settings_layout.addLayout(normal_layout)

        # Add tabs buttons.
        tabs.addTab(tab_project, "Project")
        tabs.addTab(tab_settings, "Settings")
        tabs.addTab(tab_info, "Info")

        # Add tabs to layout.
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tabs)

        # Hook layout to Substance Painter.
        self.window = QtWidgets.QWidget()
        self.window.setLayout(layout)
        self.window.setWindowTitle("Substance to XIV")
        self.window.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), "icon.png")))
        substance_painter.ui.add_dock_widget(self.window)

        # Handle click events.
        self.button_enable.clicked.connect(self.button_enable_click)
        self.button_textools.clicked.connect(self.button_textools_click)
        self.checkbox_move_tex.clicked.connect(self.checkbox_move_tex_click)
        self.checkbox_redraw.clicked.connect(self.checkbox_redraw_click)
        self.checkbox_fast_mode.clicked.connect(self.checkbox_fast_mode_click)
        self.checkbox_keep_dds.clicked.connect(self.checkbox_keep_dds_click)
        self.button_modfolder.clicked.connect(self.button_modfolder_click)
        self.button_quick_export.clicked.connect(self.button_quick_export_click)
        self.button_clear_log.clicked.connect(self.button_clear_log_click)
        self.combo_format_d.currentTextChanged.connect(self.combo_format_diffuse_changed)
        self.combo_format_id.currentTextChanged.connect(self.combo_format_id_changed)
        self.combo_format_m.currentTextChanged.connect(self.combo_format_mask_changed)
        self.combo_format_n.currentTextChanged.connect(self.combo_format_normal_changed)

        # Combo boxes initial state.
        format_d = settings.get("format_d", "BC7_UNORM")
        index = self.formats.index(format_d)
        self.combo_format_d.setCurrentIndex(index)
        format_id = settings.get("format_id", "BC5_UNORM")
        index = self.formats.index(format_id)
        self.combo_format_id.setCurrentIndex(index)
        format_m = settings.get("format_m", "BC7_UNORM")
        index = self.formats.index(format_m)
        self.combo_format_m.setCurrentIndex(index)
        format_n = settings.get("format_n", "B8G8R8A8_UNORM") # TODO: Test with R8G8B8A8_UNORM and compare.
        index = self.formats.index(format_n)
        self.combo_format_n.setCurrentIndex(index)

        # Subscribe to project related events.
        connections = {
            substance_painter.event.ProjectOpened: self.on_project_opened,
            substance_painter.event.ProjectCreated: self.on_project_created,
            substance_painter.event.ProjectAboutToClose: self.on_project_about_to_close,
            substance_painter.event.ExportTexturesEnded: self.on_export_textures_ended,
        }
        for event, callback in connections.items():
            substance_painter.event.DISPATCHER.connect(event, callback)

        if settings.get("textools_path"):
            self.button_textools.setMinimumHeight(40)

    def button_enable_click(self):
        state = not metadata.get("plugin_enable")
        metadata.set("plugin_enable", state)
        self.button_enable.setText(get_enable_button_text(self))

    def button_textools_click(self):
        if self.TexToolsPath is not None and os.path.exists(self.TexToolsPath):
            path = self.TexToolsPath
        else:
            # TODO: Test this.
            path = "C:/Program Files"

        path = QtWidgets.QFileDialog.getExistingDirectory(
            substance_painter.ui.get_main_window(),
            "Set TexTools Main Directory",
            path
        )

        if path != "":
            settings.set("textools_path", path)
            self.TexToolsPath = path

            textools_button_text = get_textools_button_text(self)
            self.button_textools.setText(textools_button_text)
            self.log.append(f"Textools path: '{self.TexToolsPath}'")

    def checkbox_move_tex_click(self):
        state = metadata.get("move_tex")
        metadata.set("move_tex", not state)

    def checkbox_redraw_click(self):
        state = metadata.get("redraw")
        metadata.set("redraw", not state)

    def checkbox_fast_mode_click(self):
        state = metadata.get("fast_mode")
        metadata.set("fast_mode", not state)

    def checkbox_keep_dds_click(self):
        state = metadata.get("keep_dds")
        metadata.set("keep_dds", not state)

    def button_modfolder_click(self):
        starting_path = metadata.get("mod_folder")
        if starting_path == "":
            starting_path = penumbra.mod_directory()
        # TODO: Needs testing.
        if starting_path == "":
            starting_path = "C:\\"

        path = QtWidgets.QFileDialog.getExistingDirectory(
            substance_painter.ui.get_main_window(),
            "Set Mod Textures Folder",
            starting_path
        )

        if path != "":
            metadata.set("mod_folder", path)
            self.update_ui()

            # textools_path_label = self.TexToolsPath
            self.log.append(f"Mod texture folder: '{path}'")

        self.update_ui()

    def button_quick_export_click(self):
        if not substance_painter.project.is_open():
            self.log.append("No project open!")
            return

        event = QKeyEvent(QEvent.KeyPress, Qt.Key_E, Qt.ControlModifier | Qt.ShiftModifier)
        QtWidgets.QApplication.sendEvent(substance_painter.ui.get_main_window(), event)

        # js_code = 'alg.mapexport.getProjectExportPreset()'
        # baking_parameters = substance_painter.js.evaluate(js_code)
        # self.log.append(str(baking_parameters))
        # ---> resource://your_assets/ATSU XIV Normal Mask Custom AO?version=9846787643662974824.spexp

        #  Generate an export JSON config like in substance_painter.export.list_project_textures
        #  and use the current export preset to export the project.
        #  Will need to set an export directory and get the active texture set with substance_painter.textureset.get_active_stack
        #  Will also need to add an option to get all texture sets and export all.

    def button_clear_log_click(self):
        self.log.clear()

    def combo_format_diffuse_changed(self, value):
        settings.set("format_d", value)

    def combo_format_id_changed(self, value):
        settings.set("format_id", value)

    def combo_format_mask_changed(self, value):
        settings.set("format_m", value)

    def combo_format_normal_changed(self, value):
        settings.set("format_n", value)

    def update_ui(self):
        if metadata.get("plugin_enable"):
            self.button_enable.setText("Substance to XIV Enabled")
        self.checkbox_move_tex.setChecked(True if metadata.get("move_tex") else False)
        self.checkbox_redraw.setChecked(True if metadata.get("redraw") else False)
        self.checkbox_fast_mode.setChecked(True if metadata.get("fast_mode") else False)
        self.checkbox_keep_dds.setChecked(True if metadata.get("keep_dds") else False)

        mod_folder = metadata.get("mod_folder")
        mod_folder_button_size = 0
        if mod_folder == "":
            mod_folder = "Click here to set a texture folder..."
            self.checkbox_move_tex.setDisabled(True)
            self.checkbox_move_tex.setChecked(False)
        else:
            mod_folder = mod_folder[-45:][mod_folder.find('/'):]
            mod_folder = f"Mod folder\n'...{mod_folder}'"
            self.checkbox_move_tex.setDisabled(False)
            mod_folder_button_size = 40
        self.button_modfolder.setText(mod_folder)
        self.button_modfolder.setMinimumHeight(mod_folder_button_size)

    def enable_project_settings(self):
        self.button_enable.setDisabled(False)
        self.button_modfolder.setDisabled(False)
        self.checkbox_move_tex.setDisabled(False)
        self.checkbox_redraw.setDisabled(False)
        self.checkbox_fast_mode.setDisabled(False)
        self.checkbox_keep_dds.setDisabled(False)
        self.button_quick_export.setDisabled(False)

    def disable_project_settings(self):
        self.button_enable.setDisabled(True)
        self.button_modfolder.setDisabled(True)
        self.checkbox_move_tex.setDisabled(True)
        self.checkbox_redraw.setDisabled(True)
        self.checkbox_fast_mode.setDisabled(True)
        self.checkbox_keep_dds.setDisabled(True)
        self.button_quick_export.setDisabled(True)

        self.button_enable.setText("Substance to XIV Disabled")
        self.button_modfolder.setText("Click here to set a texture folder...")
        self.button_modfolder.setMinimumHeight(0)
        self.checkbox_move_tex.setChecked(False)
        self.checkbox_redraw.setChecked(False)
        self.checkbox_fast_mode.setChecked(False)
        self.checkbox_keep_dds.setChecked(False)

    def __del__(self):
        # Remove all added UI elements.
        substance_painter.ui.delete_ui_element(self.log)

    def on_project_opened(self, e):
        self.log.append(f"Project '{substance_painter.project.name()}' opened.")
        result = load_metadata()
        self.log.append(result)
        self.enable_project_settings()
        self.update_ui()

    def on_project_created(self, e):
        self.log.append(f"Project '{substance_painter.project.name()}' created.")
        result = init_metadata()
        self.log.append(result)
        self.enable_project_settings()
        self.update_ui()

    def on_project_about_to_close(self, e):
        self.log.append(f"Project '{substance_painter.project.name()}' closed.")
        self.disable_project_settings()

    def on_export_textures_ended(self, res):
        enabled = metadata.get("plugin_enable")
        if not enabled:
            self.log.append("Plugin disabled, ignoring export.")
            return

        self.log.append(res.message)
        for file_list in res.textures.values():
            for file_path in file_list:
                dds, dds_format = convert.to_dds(file_path, settings.all(), metadata.get("fast_mode"))
                self.log.append(f"Created: {os.path.basename(dds)} ({dds_format})")

                tex = convert.to_tex(file_path, settings.all())
                self.log.append(f"Created: {os.path.basename(tex)}")

                if not metadata.get("keep_dds"):
                    os.remove(dds)
                    self.log.append(f"Deleted: {os.path.basename(dds)}")

        fast_mode = metadata.get("fast_mode")
        if fast_mode:
            self.log.append("Fast mode enabled, all textures saved uncompressed!")

        redraw = metadata.get("redraw")
        if redraw:
            self.log.append("All done, attempting Penumbra redraw...")
            redraw = penumbra.redraw_self()
            self.log.append(redraw)


def start_plugin():
    """This method is called when the plugin is started."""
    global XIVTEX_PLUGIN
    XIVTEX_PLUGIN = XIVTexPlugin()


def close_plugin():
    """This method is called when the plugin is stopped."""
    global XIVTEX_PLUGIN
    del XIVTEX_PLUGIN


if __name__ == "__main__":
    start_plugin()
