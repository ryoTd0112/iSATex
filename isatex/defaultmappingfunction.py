from numpy import array, inf

from .objects import MappingFunctionContainerBase


class FTIR_WaterContentMapping(MappingFunctionContainerBase):
    def __init__(self):
        super().__init__()

    def Function(self, data_list, args):
        K = 36.37

        warter_contents_list = []
        for data in data_list:
            x, y = data.X, data.Y
            t = self.EstimateThickness(x, y, (1624.9, 2150.1), 1 / 0.6366)
            G1 = self.EstimateThickness(x, y, (3414.9, 3653.1))
            G2 = self.EstimateThickness(x, y, (3264.9, 3415.1))
            G3 = self.EstimateThickness(x, y, (3264.9, 3415.1))

            warter_contents = self.EstimateWarterContents(K, t, G1, G2, G3)
            warter_contents_list.append(warter_contents)

        return array(warter_contents_list)

    def EstimateThickness(self, xdata, ydata, bounds=(-inf, inf,), rate=1):
        if len(xdata) != len(ydata):
            raise TypeError('"x" and "y" should be the same length.')

        lower_bound, upper_bound = bounds
        matched_index = [index for index, x in enumerate(xdata) if lower_bound < x < upper_bound]

        clipped_xdata = array([xdata[i] for i in matched_index])
        clipped_ydata = array([ydata[i] for i in matched_index])

        if len(clipped_xdata) == 0:
            return 0

        total_area = sum([abs(y) for y in clipped_ydata])

        upper_base = clipped_ydata[-1]
        lower_base = clipped_ydata[0]
        height = abs(clipped_xdata[-1] - clipped_xdata[0])
        base_area = (upper_base + lower_base) * height / 2

        return (total_area - base_area) * rate

    def EstimateWarterContents(self, K, t, G1, G2, G3):
        return 1e5 / t * 3.5 * K * ((G1 / (3780 - 3572)) + (G2 / (3780 - 3328)) + (G3 / (3780 - 3228)))
