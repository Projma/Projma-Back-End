

class Chart:
    def __init__(self, label, xlabel, ylabel) -> None:
        self.label = label
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xdata = []
        self.ydata = []

    def add_x(self, xdata):
        self.xdata.append(xdata)

    def add_y(self, ydata):
        self.ydata.append(ydata)

    @property
    def data(self):
        return {
            'chartlabel': self.label,
            'xlabel': self.xlabel,
            'ylabel': self.ylabel,
            'xdata': self.xdata,
            'ydata': self.ydata
        }
