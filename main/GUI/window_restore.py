import wx
import wx.dataview as dataview
import win32gui
import win32con
from core import tools as tool
from core.model import WindowInfo
from core.config import Config
from GUI.setting.binding_page import BindingPage

class WindowRestorePanel(BindingPage):
    """继承BindingPage实现窗口恢复的面板"""
    def __init__(self, parent):
        super().__init__(parent)
        
    def init_UI(self):
        # 创建界面
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 树形列表 - 复用BindingPage的列表设置方式
        self.left_treelist = dataview.TreeListCtrl(self, style=dataview.TL_CHECKBOX)
        self.left_treelist.AppendColumn('窗口标题', width=300)
        self.left_treelist.AppendColumn('窗口句柄', width=100)
        self.left_treelist.AppendColumn('进程PID', width=150)
        
        # 按钮区域
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.show_btn = wx.Button(self, label="显示窗口")
        self.hide_btn = wx.Button(self, label="隐藏窗口")
        btn_sizer.Add(self.show_btn, proportion=1, flag=wx.RIGHT, border=5)
        btn_sizer.Add(self.hide_btn, proportion=1, flag=wx.LEFT, border=5)
        
        # 布局
        main_sizer.Add(self.left_treelist, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)
        main_sizer.Add(btn_sizer, flag=wx.EXPAND|wx.ALL, border=10)
        
        self.SetSizer(main_sizer)
        
    def Bind_EVT(self):
        self.show_btn.Bind(wx.EVT_BUTTON, self.on_show_window)
        self.hide_btn.Bind(wx.EVT_BUTTON, self.on_hide_window)
        self.left_treelist.Bind(dataview.EVT_TREELIST_ITEM_CHECKED, self.OnToggleCheck)

    def SetData(self):
        self.RefreshLeftList()

    def RefreshLeftList(self, e=None):
        windows = tool.getAllWindows()
        list = []
        for window in windows:
            list.append(window)
        self.InsertTreeList(list, self.left_treelist, True)
        
    def on_show_window(self, e=None):
        windows = self.ItemsData(self.left_treelist, only_checked=True)
        result = wx.MessageBox(f"将恢复{len(windows)}个窗口\r\n恢复未知的窗口可能会导致窗口出错", "警告", wx.OK | wx.CANCEL | wx.ICON_WARNING)
        if result != wx.OK:
            return
        for window in windows:
            win32gui.ShowWindow(window.hwnd, win32con.SW_SHOW)

    def on_hide_window(self, e=None):
        windows = self.ItemsData(self.left_treelist, only_checked=True)
        result = wx.MessageBox(f"将隐藏{len(windows)}个窗口\r\n隐藏未知的窗口可能会导致窗口出错", "警告", wx.OK | wx.CANCEL | wx.ICON_WARNING)        
        if result != wx.OK:
            return
        for window in windows:
            win32gui.ShowWindow(window.hwnd, win32con.SW_HIDE)


class WindowRestoreDialog(wx.Frame):
    def __init__(self, id):
        wx.Frame.__init__(self, None, id=id, title="窗口恢复工具 - Boss Key", style=wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER)
        self.SetIcon(wx.Icon(wx.Image(Config.icon).ConvertToBitmap()))
        self.SetSize((700, 600))
        self.Center()
        
        # 使用继承自BindingPage的面板
        self.panel = WindowRestorePanel(self)
        
        # 创建框架布局
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        # 设置初始数据
        self.panel.SetData()
        
    def Restore(self):
        """恢复窗口，用于taskbar.py中调用"""
        self.Show()