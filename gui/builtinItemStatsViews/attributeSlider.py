import wx
from gui.attribute_gauge import AttributeGauge


class AttributeSlider(wx.Panel):
    # Slider which abstracts users values from internal values (because the built in slider does not deal with floats
    # and the like), based on http://wxpython-users.wxwidgets.narkive.com/ekgBzA7u/anyone-ever-thought-of-a-floating-point-slider

    def __init__(self, parent, baseValue, minMod, maxMod):
        wx.Panel.__init__(self, parent)

        self.parent = parent

        self.base_value = baseValue

        self.UserMinValue = minMod
        self.UserMaxValue = maxMod

        # The internal slider basically represents the percentage towards the end of the range. It has to be normalized
        # in this way, otherwise when we start off with a base, if the range is skewed to one side, the base value won't
        # be centered. We use a range of -100,100 so that we can depend on the SliderValue to contain the percentage
        # toward one end

        # Additionally, since we want the slider to be accurate to 3 decimal places, we need to blow out the two ends here
        # (if we have a slider that needs to land on 66.66% towards the right, it will actually be converted to 66%. Se we need it to support 6,666)

        self.SliderMinValue = -100
        self.SliderMaxValue = 100
        self.SliderValue = 0

        self.statxt1 = wx.StaticText(self, wx.ID_ANY, 'left', style=wx.ST_NO_AUTORESIZE | wx.ALIGN_LEFT)
        self.ctrl = wx.SpinCtrlDouble(self, min=(1-self.UserMinValue)*-100, max=(1-self.UserMaxValue)*-100)
        self.ctrl.SetDigits(3)
        self.statxt3 = wx.StaticText(self, wx.ID_ANY, 'right', style=wx.ST_NO_AUTORESIZE | wx.ALIGN_RIGHT)

        self.ctrl.Bind(wx.EVT_SPINCTRLDOUBLE, self.UpdateValue)

        self.statxt1.SetLabel("{0:.3f}".format(self.UserMinValue * self.base_value))
        self.statxt1.SetToolTip("{0:+f}%".format((1-self.UserMinValue)*-100))
        self.statxt3.SetLabel("{0:.3f}".format(self.UserMaxValue * self.base_value))
        self.statxt3.SetToolTip("{0:+f}%".format((1-self.UserMaxValue)*-100))

        self.slider = AttributeGauge(self, size=(-1,8))

        b = 20
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add(self.statxt1, 1, wx.RIGHT, b)
        hsizer1.Add(self.ctrl, 1, wx.LEFT | wx.RIGHT, b)
        hsizer1.Add(self.statxt3, 1, wx.LEFT, b)

        b = 4
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        vsizer1.Add(hsizer1, 0, wx.EXPAND | wx.ALL, b)
        vsizer1.Add(self.slider, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, b)

        self.SetSizerAndFit(vsizer1)
        self.parent.SetClientSize((500, vsizer1.GetSize()[1]))

    def UpdateValue(self, evt):
        self.SetValue(self.ctrl.GetValue())
        evt.Skip()

    def OnScroll(self, event):
        self.CalculateUserValue()

    def SetValue(self, value):
        # todo: check this against values that might be 2.5x and whatnot
        mod = value / self.base_value
        self.ctrl.SetValue(value)
        slider_percentage = 0
        if mod < 1:
            modEnd = -1 * self.UserMinValue
            slider_percentage = (modEnd / mod) * 100
        elif mod > 1:
            modEnd = self.UserMaxValue
            slider_percentage = ((mod-1)/(modEnd-1)) * 100
        print(slider_percentage)
        self.slider.SetValue(slider_percentage)
        self.CalculateUserValue()

    def CalculateUserValue(self):
        self.SliderValue = self.slider.GetValue()

        mod = 1

        # The slider value tells us when mod we're going to use, depending on its sign
        if self.SliderValue < 0:
            mod = self.UserMinValue
        elif self.SliderValue > 0:
            mod = self.UserMaxValue

        # Get the slider value percentage as an absolute value
        slider_mod = abs(self.SliderValue/1_000) / 100

        # Gets our new mod by use the slider's percentage to determine where in the spectrum it is
        new_mod = mod + ((1 - mod) - ((1 - mod) * slider_mod))

        # Modifies our base value, to get out modified value
        newValue = new_mod * self.base_value

        # if mod == 1:
        #     self.statxt2.SetLabel("{0:.3f}".format(newValue))
        # else:
        #     self.statxt2.SetLabel("{0:.3f} ({1:+.3f})".format(newValue, newValue - self.base_value, ))
        #     self.statxt2.SetToolTip("{0:+f}%".format(new_mod*100))


class TestAttributeSlider(wx.Frame):

    def __init__(self, parent, id):
        title = 'Slider...'
        pos = wx.DefaultPosition
        size = wx.DefaultSize
        sty = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, parent, id, title, pos, size, sty)

        self.panel = AttributeSlider(self, 10, .80, 1.5)
        self.panel.SetValue(9.0)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self.Destroy()


if __name__ == "__main__":
    app = wx.App()
    frame = TestAttributeSlider(None, wx.ID_ANY)
    frame.Show()
    app.MainLoop()


# class AttributeSliderDEV(wx.Panel):
#     # Slider which abstracts users values from internal values (because the built in slider does not deal with floats
#     # and the like), based on http://wxpython-users.wxwidgets.narkive.com/ekgBzA7u/anyone-ever-thought-of-a-floating-point-slider
#
#     def __init__(self, parent, baseValue, minMod, maxMod):
#         wx.Panel.__init__(self, parent)
#
#         self.parent = parent
#
#         self.base_value = baseValue
#
#         self.UserMinValue = minMod
#         self.UserMaxValue = maxMod
#
#         # The internal slider basically represents the percentage towards the end of the range. It has to be normalized
#         # in this way, otherwise when we start off with a base, if the range is skewed to one side, the base value won't
#         # be centered. We use a range of -100,100 so that we can depend on the SliderValue to contain the percentage
#         # toward one end
#
#         # Additionally, since we want the slider to be accurate to 3 decimal places, we need to blow out the two ends here
#         # (if we have a slider that needs to land on 66.66% towards the right, it will actually be converted to 66%. Se we need it to support 6,666)
#
#         self.SliderMinValue = -100_000
#         self.SliderMaxValue = 100_000
#         self.SliderValue = 0
#
#         self.statxt1 = wx.StaticText(self, wx.ID_ANY, 'left',
#         style=wx.ST_NO_AUTORESIZE | wx.ALIGN_LEFT)
#         self.statxt2 = wx.StaticText(self, wx.ID_ANY, 'middle',
#         style=wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE)
#         self.statxt3 = wx.StaticText(self, wx.ID_ANY, 'right',
#         style=wx.ST_NO_AUTORESIZE | wx.ALIGN_RIGHT)
#
#         self.statxt1.SetLabel("{0:.3f}".format(self.UserMinValue * self.base_value))
#         self.statxt1.SetToolTip("{0:+f}%".format((1-self.UserMinValue)*-100))
#         self.statxt2.SetLabel("{0:.3f}".format(self.base_value))
#         self.statxt3.SetLabel("{0:.3f}".format(self.UserMaxValue * self.base_value))
#         self.statxt3.SetToolTip("{0:+f}%".format((1-self.UserMaxValue)*-100))
#
#         self.slider = wx.Slider(
#             self, wx.ID_ANY,
#             self.SliderValue,
#             self.SliderMinValue,
#             self.SliderMaxValue,
#             style=wx.SL_HORIZONTAL)
#
#         self.slider.SetTickFreq((self.SliderMaxValue - self.SliderMinValue) / 15)
#
#         self.slider.Bind(wx.EVT_SCROLL, self.OnScroll)
#
#         b = 20
#         hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
#         hsizer1.Add(self.statxt1, 1, wx.RIGHT, b)
#         hsizer1.Add(self.statxt2, 1, wx.LEFT | wx.RIGHT, b)
#         hsizer1.Add(self.statxt3, 1, wx.LEFT, b)
#
#         b = 4
#         vsizer1 = wx.BoxSizer(wx.VERTICAL)
#         vsizer1.Add(hsizer1, 0, wx.EXPAND | wx.ALL, b)
#         vsizer1.Add(self.slider, 0, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, b)
#
#         self.SetSizerAndFit(vsizer1)
#         self.parent.SetClientSize((500, vsizer1.GetSize()[1]))
#
#     def OnScroll(self, event):
#         self.CalculateUserValue()
#
#     def SetValue(self, value):
#         # todo: check this against values that might be 2.5x and whatnot
#         mod = value / self.base_value
#         slider_percentage = 0
#         if mod < 1:
#             modEnd = -1 * self.UserMinValue
#             slider_percentage = (modEnd / mod) * 10_000
#         elif mod > 1:
#             modEnd = self.UserMaxValue
#             slider_percentage = ((mod-1)/(modEnd-1)) * 100_000
#
#         self.slider.SetValue(slider_percentage)
#         self.CalculateUserValue()
#
#     def CalculateUserValue(self):
#         self.SliderValue = self.slider.GetValue()
#
#         mod = 1
#
#         # The slider value tells us when mod we're going to use, depending on its sign
#         if self.SliderValue < 0:
#             mod = self.UserMinValue
#         elif self.SliderValue > 0:
#             mod = self.UserMaxValue
#
#         # Get the slider value percentage as an absolute value
#         slider_mod = abs(self.SliderValue/1_000) / 100
#
#         # Gets our new mod by use the slider's percentage to determine where in the spectrum it is
#         new_mod = mod + ((1 - mod) - ((1 - mod) * slider_mod))
#
#         # Modifies our base value, to get out modified value
#         newValue = new_mod * self.base_value
#
#         if mod == 1:
#             self.statxt2.SetLabel("{0:.3f}".format(newValue))
#         else:
#             self.statxt2.SetLabel("{0:.3f} ({1:+.3f})".format(newValue, newValue - self.base_value, ))
#             self.statxt2.SetToolTip("{0:+f}%".format(new_mod*100))

