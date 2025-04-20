import wx
from core.config import Config
import GUI.record as record

class HotkeysPage(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_UI()
        self.Bind_EVT()
        
    def init_UI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 创建键盘热键设置区域
        keyboard_box = wx.StaticBox(self, label="键盘热键")
        keyboard_box_sizer = wx.StaticBoxSizer(keyboard_box, wx.VERTICAL)
        
        grid_sizer = wx.FlexGridSizer(rows=2, cols=3, gap=(10, 20))
        grid_sizer.AddGrowableCol(1, 1)
        
        # 隐藏/显示窗口热键
        hide_show_label = wx.StaticText(self, label="隐藏/显示窗口热键:")
        self.hide_show_text = wx.TextCtrl(self)
        self.hide_show_btn = wx.Button(self, label="录制热键")
        
        grid_sizer.Add(hide_show_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        grid_sizer.Add(self.hide_show_text, 1, wx.EXPAND | wx.ALL, 10)
        grid_sizer.Add(self.hide_show_btn, 0, wx.EXPAND | wx.ALL, 10)
        
        # 一键关闭程序热键
        close_label = wx.StaticText(self, label="一键关闭程序热键:")
        self.close_text = wx.TextCtrl(self)
        self.close_btn = wx.Button(self, label="录制热键")
        
        grid_sizer.Add(close_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        grid_sizer.Add(self.close_text, 1, wx.EXPAND | wx.ALL, 10)
        grid_sizer.Add(self.close_btn, 0, wx.EXPAND | wx.ALL, 10)
        
        keyboard_box_sizer.Add(grid_sizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(keyboard_box_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # 添加鼠标隐藏选项
        mouse_box = wx.StaticBox(self, label="鼠标隐藏")
        mouse_box_sizer = wx.StaticBoxSizer(mouse_box, wx.VERTICAL)
        
        # 中键选项
        self.middle_button_checkbox = wx.CheckBox(self, label="启用鼠标中键隐藏窗口")
        self.middle_button_checkbox.SetToolTip(wx.ToolTip("点击鼠标中键可快速隐藏/显示窗口"))
        
        # 侧键1选项
        self.side_button1_checkbox = wx.CheckBox(self, label="启用鼠标侧键1隐藏窗口")
        self.side_button1_checkbox.SetToolTip(wx.ToolTip("点击鼠标侧键1(前进键)可快速隐藏/显示窗口"))
        
        # 侧键2选项
        self.side_button2_checkbox = wx.CheckBox(self, label="启用鼠标侧键2隐藏窗口")
        self.side_button2_checkbox.SetToolTip(wx.ToolTip("点击鼠标侧键2(后退键)可快速隐藏/显示窗口"))
        
        mouse_box_sizer.Add(self.middle_button_checkbox, 0, wx.ALL, 10)
        mouse_box_sizer.Add(self.side_button1_checkbox, 0, wx.ALL, 10)
        mouse_box_sizer.Add(self.side_button2_checkbox, 0, wx.ALL, 10)
        
        sizer.Add(mouse_box_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        self.SetSizer(sizer)
        
    def Bind_EVT(self):
        self.hide_show_btn.Bind(wx.EVT_BUTTON, self.OnRecordHideShow)
        self.close_btn.Bind(wx.EVT_BUTTON, self.OnRecordClose)
        
    def SetData(self):
        self.hide_show_text.SetValue(Config.hide_hotkey)
        self.close_text.SetValue(Config.close_hotkey)
        self.middle_button_checkbox.SetValue(Config.middle_button_hide if hasattr(Config, 'middle_button_hide') else False)
        self.side_button1_checkbox.SetValue(Config.side_button1_hide if hasattr(Config, 'side_button1_hide') else False)
        self.side_button2_checkbox.SetValue(Config.side_button2_hide if hasattr(Config, 'side_button2_hide') else False)
        
    def SaveData(self):
        Config.hide_hotkey = self.hide_show_text.GetValue()
        Config.close_hotkey = self.close_text.GetValue()
        Config.middle_button_hide = self.middle_button_checkbox.GetValue()
        Config.side_button1_hide = self.side_button1_checkbox.GetValue()
        Config.side_button2_hide = self.side_button2_checkbox.GetValue()
        
    def Reset(self):
        self.hide_show_text.SetValue("Ctrl+Q")
        self.close_text.SetValue("Win+Esc")
        self.middle_button_checkbox.SetValue(False)
        self.side_button1_checkbox.SetValue(False)
        self.side_button2_checkbox.SetValue(False)
        
    def OnRecordHideShow(self, e):
        self.recordHotkey(self.hide_show_text, self.hide_show_btn)
        
    def OnRecordClose(self, e):
        self.recordHotkey(self.close_text, self.close_btn)
        
    def recordHotkey(self, text_ctrl: wx.TextCtrl, btn: wx.Button):
        try:
            Config.HotkeyListener.stop()
        except:
            pass
        btn.Disable()
        btn.SetLabel("录制中...")
        record.RecordedHotkey.confirm = False
        RecordWindow = record.RecordWindow()
        RecordWindow.ShowModal()
        btn.Enable()
        btn.SetLabel("录制热键")
        if record.RecordedHotkey.confirm:
            text_ctrl.SetValue(record.RecordedHotkey.final_key)