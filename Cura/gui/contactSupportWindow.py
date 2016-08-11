__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import wx

class contactSupportWindow(wx.Frame):
	def __init__(self):
		super(contactSupportWindow, self).__init__(None, title="Contact Support", size=(500,100))

		wx.EVT_CLOSE(self, self.OnClose)

		panel = wx.Panel(self, -1)
		hbox = wx.BoxSizer(wx.HORIZONTAL)

		st_support =wx.StaticText(panel, -1, style = wx.ALIGN_LEFT)
		st_support.SetLabel("\n If you are facing any problem with our printers,\n kindly contact us at +91-8144 077 077 or mail us at support@3Ding.in.")

		hbox.Add(st_support, flag=wx.RIGHT)
		panel.SetSizer(hbox)

	def OnClose(self, e):
		self.Destroy()
