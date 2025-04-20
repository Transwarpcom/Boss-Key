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
        
        # 创建网格布局
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
        
        sizer.Add(grid_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        self.SetSizer(sizer)
        
    def Bind_EVT(self):
        self.hide_show_btn.Bind(wx.EVT_BUTTON, self.OnRecordHideShow)
        self.close_btn.Bind(wx.EVT_BUTTON, self.OnRecordClose)
        
    def SetData(self):
        self.hide_show_text.SetValue(Config.hide_hotkey)
        self.close_text.SetValue(Config.close_hotkey)
        
    def SaveData(self):
        Config.hide_hotkey = self.hide_show_text.GetValue()
        Config.close_hotkey = self.close_text.GetValue()
        
    def Reset(self):
        self.hide_show_text.SetValue("Ctrl+Q")
        self.close_text.SetValue("Win+Esc")
        
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