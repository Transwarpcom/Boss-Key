import wx
from core.config import Config

class OptionsPage(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_UI()
        self.Bind_EVT()
        
    def init_UI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 创建网格布局
        grid_sizer = wx.GridSizer(rows=3, cols=2, gap=(10, 20))
        
        # 添加复选框
        # 1. 隐藏窗口后静音
        self.mute_checkbox = wx.CheckBox(self, label="隐藏窗口后静音")
        grid_sizer.Add(self.mute_checkbox, 0, wx.ALL, 10)
        
        # 2. 隐藏前发送暂停键（Beta）
        pause_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.send_pause_checkbox = wx.CheckBox(self, label="隐藏前发送暂停键（Beta）")
        self.send_pause_checkbox.SetToolTip(wx.ToolTip("隐藏窗口前发送暂停键，用于关闭弹出的输入框等，隐藏窗口会存在一定的延迟"))
        pause_sizer.Add(self.send_pause_checkbox)
        grid_sizer.Add(pause_sizer, 0, wx.ALL, 10)
        
        # 3. 同时隐藏当前活动窗口
        self.hide_current_checkbox = wx.CheckBox(self, label="同时隐藏当前活动窗口")
        grid_sizer.Add(self.hide_current_checkbox, 0, wx.ALL, 10)
        
        # 4. 点击托盘图标切换隐藏状态
        self.click_hide_checkbox = wx.CheckBox(self, label="点击托盘图标切换隐藏状态")
        grid_sizer.Add(self.click_hide_checkbox, 0, wx.ALL, 10)
        
        # 5. 隐藏窗口后隐藏托盘图标
        self.hide_icon_checkbox = wx.CheckBox(self, label="隐藏窗口后隐藏托盘图标")
        grid_sizer.Add(self.hide_icon_checkbox, 0, wx.ALL, 10)
        
        # 6. 文件路径匹配
        path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.path_match_checkbox = wx.CheckBox(self, label="文件路径匹配")
        path_tooltip = "启用此选项可以一键隐藏绑定程序的所有窗口\n关闭此选项后，将会智能精确隐藏指定窗口"
        self.path_match_checkbox.SetToolTip(wx.ToolTip(path_tooltip))
        info_icon = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, self.FromDIP((14, 14)))
        info_bitmap = wx.StaticBitmap(self, bitmap=info_icon)
        info_bitmap.SetToolTip(wx.ToolTip(path_tooltip))
        path_sizer.Add(self.path_match_checkbox)
        path_sizer.AddSpacer(5)
        path_sizer.Add(info_bitmap)
        grid_sizer.Add(path_sizer, 0, wx.ALL, 10)
        
        sizer.Add(grid_sizer, 0, wx.EXPAND | wx.ALL, 20)
        
        self.SetSizer(sizer)
        
    def Bind_EVT(self):
        self.send_pause_checkbox.Bind(wx.EVT_CHECKBOX, self.OnSendBeforeHide)
        
    def SetData(self):
        self.mute_checkbox.SetValue(Config.mute_after_hide)
        self.send_pause_checkbox.SetValue(Config.send_before_hide)
        self.hide_current_checkbox.SetValue(Config.hide_current)
        self.click_hide_checkbox.SetValue(Config.click_to_hide)
        self.hide_icon_checkbox.SetValue(Config.hide_icon_after_hide)
        self.path_match_checkbox.SetValue(Config.path_match)
        
    def SaveData(self):
        Config.mute_after_hide = self.mute_checkbox.GetValue()
        Config.send_before_hide = self.send_pause_checkbox.GetValue()
        Config.hide_current = self.hide_current_checkbox.GetValue()
        Config.click_to_hide = self.click_hide_checkbox.GetValue()
        Config.hide_icon_after_hide = self.hide_icon_checkbox.GetValue()
        Config.path_match = self.path_match_checkbox.GetValue()
        
    def Reset(self):
        self.mute_checkbox.SetValue(True)
        self.send_pause_checkbox.SetValue(False)
        self.hide_current_checkbox.SetValue(True)
        self.click_hide_checkbox.SetValue(False)
        self.hide_icon_checkbox.SetValue(False)
        self.path_match_checkbox.SetValue(False)
        
    def OnSendBeforeHide(self, e):
        if self.send_pause_checkbox.GetValue():
            wx.MessageDialog(None, "隐藏窗口前向被隐藏的窗口发送空格，用于暂停视频等。启用此功能可能会延迟窗口的隐藏", "Boss Key", wx.OK | wx.ICON_INFORMATION).ShowModal()