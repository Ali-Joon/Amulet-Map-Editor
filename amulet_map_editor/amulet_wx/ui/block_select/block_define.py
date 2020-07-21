import wx
from typing import Tuple

import PyMCTranslate
import amulet_nbt
from amulet.api.block import PropertyType

from amulet_map_editor.amulet_wx.ui.version_select import VersionSelect, EVT_VERSION_CHANGE
from amulet_map_editor.amulet_wx.ui.block_select.block import BlockSelect


class BlockDefine(wx.BoxSizer):
    def __init__(
            self,
            parent,
            translation_manager: PyMCTranslate.TranslationManager,
            orientation=wx.VERTICAL,
            platform: str = None,
            version_number: Tuple[int, int, int] = None,
            force_blockstate: bool = None,
            namespace: str = None,
            block_name: str = None,
            properties: PropertyType = None,
            nbt: amulet_nbt.TAG_Compound = None,
            show_nbt: bool = True,
            **kwargs
    ):
        super().__init__(orientation)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.Add(left_sizer, 1, wx.EXPAND)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        if orientation == wx.HORIZONTAL:
            self.Add(right_sizer, 1, wx.EXPAND | wx.LEFT, 5)
        else:
            self.Add(right_sizer, 1, wx.EXPAND | wx.TOP, 5)

        self._version_picker = VersionSelect(
            parent,
            translation_manager,
            platform,
            version_number,
            force_blockstate,
            **kwargs
        )
        left_sizer.Add(self._version_picker, 0, wx.EXPAND)
        self._version_picker.Bind(EVT_VERSION_CHANGE, self._on_version_change)

        self._block_picker = BlockSelect(
            parent,
            translation_manager,
            self._version_picker.platform,
            self._version_picker.version_number,
            self._version_picker.force_blockstate,
            namespace,
            block_name,
            **kwargs
        )
        left_sizer.Add(self._block_picker, 1, wx.EXPAND | wx.TOP, 5)

    def _on_version_change(self, evt):
        self._block_picker.version = evt.platform, evt.version_number, evt.force_blockstate
        evt.Skip()


if __name__ == '__main__':
    def main():
        translation_manager = PyMCTranslate.new_translation_manager()
        app = wx.App()
        dialog = wx.Dialog(None)
        sizer = wx.BoxSizer()
        dialog.SetSizer(sizer)
        sizer.Add(
            BlockDefine(
                dialog,
                translation_manager,
                wx.HORIZONTAL
            ),
            1,
            wx.ALL,
            5
        )
        dialog.Show()
        dialog.Fit()
        app.MainLoop()
    main()
