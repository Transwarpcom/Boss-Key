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
        
        # 添加其他选项区域
        other_box = wx.StaticBox(self, label="其他")
        other_box_sizer = wx.StaticBoxSizer(other_box, wx.VERTICAL)
        
        # 自动隐藏选项
        auto_hide_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.auto_hide_checkbox = wx.CheckBox(self, label="自动隐藏：")
        self.auto_hide_checkbox.SetToolTip(wx.ToolTip("在无操作指定时间后自动隐藏窗口"))
        auto_hide_sizer.Add(self.auto_hide_checkbox, 0, wx.ALIGN_CENTER_VERTICAL)
        
        # 自动隐藏时间输入框
        self.auto_hide_time = wx.SpinCtrl(self, min=1, max=120, initial=5)
        self.auto_hide_time.SetToolTip(wx.ToolTip("设置多少分钟无操作后自动隐藏"))
        auto_hide_sizer.Add(self.auto_hide_time, 0, wx.LEFT, 10)
        
        # 分钟标签
        minutes_label = wx.StaticText(self, label="分钟")
        auto_hide_sizer.Add(minutes_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        
        other_box_sizer.Add(auto_hide_sizer, 0, wx.ALL, 10)
        
        # 灰色文本提示
        auto_hide_tip = wx.StaticText(self, label="当键盘和鼠标在指定时间内无操作时，将自动隐藏窗口")
        auto_hide_tip.SetForegroundColour(wx.Colour(128, 128, 128))  # 灰色文本
        other_box_sizer.Add(auto_hide_tip, 0, wx.ALL, 10)
        
        sizer.Add(other_box_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        self.SetSizer(sizer)
        
    def Bind_EVT(self):
        self.hide_show_btn.Bind(wx.EVT_BUTTON, self.OnRecordHideShow)
        self.close_btn.Bind(wx.EVT_BUTTON, self.OnRecordClose)
        self.auto_hide_checkbox.Bind(wx.EVT_CHECKBOX, self.OnAutoHideToggle)
        
    def OnAutoHideToggle(self, e):
        # 启用或禁用时间输入框
        self.auto_hide_time.Enable(self.auto_hide_checkbox.GetValue())
        
    def SetData(self):
        self.hide_show_text.SetValue(Config.hide_hotkey)
        self.close_text.SetValue(Config.close_hotkey)
        self.middle_button_checkbox.SetValue(Config.middle_button_hide if hasattr(Config, 'middle_button_hide') else False)
        self.side_button1_checkbox.SetValue(Config.side_button1_hide if hasattr(Config, 'side_button1_hide') else False)
        self.side_button2_checkbox.SetValue(Config.side_button2_hide if hasattr(Config, 'side_button2_hide') else False)
        
        # 设置自动隐藏选项
        auto_hide_enabled = Config.auto_hide_enabled if hasattr(Config, 'auto_hide_enabled') else False
        self.auto_hide_checkbox.SetValue(auto_hide_enabled)
        
        auto_hide_time = Config.auto_hide_time if hasattr(Config, 'auto_hide_time') else 5
        self.auto_hide_time.SetValue(auto_hide_time)
        self.auto_hide_time.Enable(auto_hide_enabled)
        
    def SaveData(self):
        Config.hide_hotkey = self.hide_show_text.GetValue()
        Config.close_hotkey = self.close_text.GetValue()
        Config.middle_button_hide = self.middle_button_checkbox.GetValue()
        Config.side_button1_hide = self.side_button1_checkbox.GetValue()
        Config.side_button2_hide = self.side_button2_checkbox.GetValue()
        
        # 保存自动隐藏设置
        Config.auto_hide_enabled = self.auto_hide_checkbox.GetValue()
        Config.auto_hide_time = self.auto_hide_time.GetValue()
        
    def Reset(self):
        self.hide_show_text.SetValue("Ctrl+Q")
        self.close_text.SetValue("Win+Esc")
        self.middle_button_checkbox.SetValue(False)
        self.side_button1_checkbox.SetValue(False)
        self.side_button2_checkbox.SetValue(False)
        self.auto_hide_checkbox.SetValue(False)
        self.auto_hide_time.SetValue(5)
        self.auto_hide_time.Enable(False)
        
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