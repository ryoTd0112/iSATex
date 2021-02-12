from math import isclose

from numpy import (array, count_nonzero, inf, linspace, ndarray, newaxis, ones,
                   reshape, squeeze, tile, zeros)
from numpy.linalg import pinv
from scipy.interpolate import (Akima1DInterpolator, BarycentricInterpolator,
                               KroghInterpolator, PchipInterpolator, interp1d,
                               lagrange)
from scipy.optimize import curve_fit
from scipy.signal import find_peaks, savgol_filter

from .objects import (ChoiceContainer, FloatContainer, IntContainer,
                     ListArgumentContainer, OptionalFloatContainer,
                     PeakFunctionContainerList, SpectrumFunctionContainerBase)


class Clipping(SpectrumFunctionContainerBase):
    def __init__(self):
        super().__init__({'Left': FloatContainer(), 'Right': FloatContainer()})

    def Function(self, args):
        x, y, bg, left, right = args

        if left >= right:
            raise AttributeError('"left" should be less than "right".')

        if left >= max(x):
            raise AttributeError('"left" should be less than the maximum value of "x".')

        if right <= min(x):
            raise AttributeError('"right" should be greater than the minimum value of "x".')

        min_index = 0
        max_index = len(x) - 1

        while(min_index + 1 < len(x) - 1 and x[min_index + 1] <= left):
            min_index += 1

        while(max_index - 1 > 0 and x[max_index - 1] >= right):
            max_index -= 1

        if max_index <= min_index:
            raise AttributeError('Probably, "x" is not a monotonic increase.')

        clipped_x = x[min_index: max_index + 1]
        clipped_y = y[min_index: max_index + 1]
        clipped_bg = bg[min_index: max_index + 1]

        return clipped_x, clipped_y, clipped_bg

    def SendRequireParams(self):
        return 'xyb'

    def SendReturnParams(self):
        return 'xyb'

    def IsGoodCondition(self, *args) -> bool:
        left, right = args
        return left < right


class Smooth(SpectrumFunctionContainerBase):
    def __init__(self):
        methods = ('quadratic', 'linear', 'lagrange', 'barycentric', 'krogh', 'cubic', 'Akima', 'Pchip',)
        super().__init__({'Resolution': IntContainer(20, 1, None), 'Method': ChoiceContainer(methods[0], methods)})

    def Function(self, args):
        x, y, bg, resolution, method = args

        smoothed_x = linspace(min(x), max(x), resolution)
        method_dict = {
            'nearest': lambda x, y: interp1d(x, y, kind='nearest'),
            'linear': interp1d,
            'lagrange': lagrange,
            'barycentric': BarycentricInterpolator,
            'krogh': KroghInterpolator,
            'quadratic': lambda x, y: interp1d(x, y, kind='quadratic'),
            'cubic': lambda x, y: interp1d(x, y, kind='cubic'),
            'Akima': Akima1DInterpolator,
            'Pchip': PchipInterpolator,
        }

        method = method_dict[method]
        smoothed_y = method(x, y)(smoothed_x)
        smoothed_bg = method(x, bg)(smoothed_x)

        return (smoothed_x, smoothed_y, smoothed_bg,)

    def SendRequireParams(self):
        return 'xyb'

    def SendReturnParams(self):
        return 'xyb'


class Normalize(SpectrumFunctionContainerBase):
    def Function(self, args):
        y, bg, peaks = args
        ymin, ymax = min(y), max(y)
        if isclose(ymin, ymax):
            return y, bg, peaks

        height = ymax - ymin

        def normalizer(x):
            # return (x - ymin) / (ymax - ymin)
            return (x - min(x)) / height

        normalized_y = normalizer(y)
        # normalized_bg = normalizer(bg) if not (min(bg) == max(bg) == 0.0) else bg
        normalized_bg = normalizer(bg)
        normalized_peaks = PeakFunctionContainerList()
        for peak in peaks:
            normalized_peak = peak
            normalized_peak.Amp = peak.Amp / height

            normalized_peaks.append(normalized_peak)

        return normalized_y, normalized_bg, normalized_peaks

    def SendRequireParams(self):
        return 'ybp'

    def SendReturnParams(self):
        return 'ybp'


class SavgolFilter(SpectrumFunctionContainerBase):
    def __init__(self):
        super().__init__({'Window length': IntContainer(5, 1, None), 'Poly order': IntContainer(2)})

    def Function(self, args):
        y, bg, window_length, poly_order = args
        filtered_y = savgol_filter(y, window_length, poly_order)
        filtered_bg = savgol_filter(bg, window_length, poly_order)

        return filtered_y, filtered_bg

    def SendRequireParams(self):
        return 'yb'

    def SendReturnParams(self):
        return 'yb'

    def IsGoodCondition(self, *args) -> bool:
        window_length, poly_order = args
        if window_length % 2 == 0:
            return False

        if poly_order >= window_length:
            return False

        return True


class Goldindec(SpectrumFunctionContainerBase):
    def __init__(self):
        super().__init__({'Poly order': IntContainer(4, 1, None), 'Peak ratio': FloatContainer(0.5, 0.1, 0.9)})

    def Function(self, args):
        x, y, peaks, poly_order, ratio = args
        bg = self.goldindec(x, y, poly_order, ratio)
        subtracted_y = y - bg
        ymin = min(subtracted_y)

        n = 0
        for peak in peaks:
            amp = peak.Amp
            ctr = peak.Ctr

            while n < len(bg) and x[n] < ctr:
                n += 1

            a = (bg[n + 1] - bg[n]) / (x[n + 1] - x[n])
            b = bg[n] - a * x[n]

            peak.Amp = amp - (a * ctr + b) - ymin

        return subtracted_y - ymin, bg - ymin, peaks

    def goldindec(self, x, y, p, peak_ratio, eps=0.0001):
        """Estimate baseline with polynomial fitting

        Args:
            x (array_like): Raman wave number. This array should be monotonically increasing and column vector.
            y (array_like): Raman intensity. This array should be column vector.
            p (int): the polynomial order.
            peak_ratio (float): the ratio of peaks. you can choose this value from 0.1 to 0.9 with step length 0.1.
            eps (float): the parameter XX to terminate the iteration and users can specify this value.

        Returns:
            1-dimension ndarray: baseline
        """
        if not isinstance(x, ndarray):
            try:
                x = array(x, dtype=float, ndmin=2)
            except TypeError:
                raise TypeError()

        if not isinstance(y, ndarray):
            try:
                y = array(y, dtype=float, ndmin=2)
            except TypeError:
                raise TypeError()

        if x.ndim > 2:
            raise AttributeError('x should be 2-dimensions array')

        if y.ndim > 2:
            raise AttributeError('y should be 2-dimensions array')

        if x.ndim == 1:
            x = x[:, newaxis]

        if y.ndim == 1:
            y = y[:, newaxis]

        row_x, col_x = x.shape
        row_y, col_y = y.shape

        if row_x < col_x:
            x = reshape(x, (col_x, row_x))

        if row_y < col_y:
            y = reshape(y, (col_y, row_y))

        a, b = 0, 1
        r_ud = self.t_rate(peak_ratio)

        s = a + 0.618 * (b - a)
        z = self.legend_c(x, y, p, s)

        up_down_rate = count_nonzero(y >= z) / count_nonzero(y < z)
        t = 0

        while abs(up_down_rate - r_ud) > eps:
            old_s = s
            if up_down_rate - r_ud > eps:
                a = s
            else:
                b = s

            s = a + 0.618 * (b - a)
            z = self.legend_c(x, y, p, s)
            up_down_rate = count_nonzero(y >= z) / count_nonzero(y < z)
            if abs(old_s - s) < 0.00001:
                break

            t += 1

        return squeeze(self.legend_c(x, y, p, s))

    def t_rate(self, x):
        """Compute by cubic polynomial function. This function correlates the Up_Down_Ratio shows with the peak ratio, and this correlation is hardly influenced by the noise.

        Args:
            x (float): value

        Returns:
            float: 0.7679 + 11.2358 x - 39.7064 x ^ 2 + 92.3583 x ^ 3
        """

        return 0.7679 + 11.2358 * x - 39.7064 * x ** 2 + 92.3583 * x ** 3

    def legend_c(self, x, y, order, s):
        """Compute p-order coefficients and return fitted line.

        Args:
            x (ndarray): Raman wave number. This array should be monotonically increasing and column vector.
            y (ndarray): Raman intensity. This array should be column vector.
            order (int): the polynomial order.
            s (float): positively correlated with the noise standard deviation.

        Returns:
            [type]: [description]
        """
        n = len(x)

        xmax = x.max(0)
        xmin = x.min(0)
        ymax = y.max(0)
        ymin = y.min(0)

        x = 2 * (x - xmax) / (xmax - xmin) + 1  # rescale to [-1, 1]
        y = 2 * (y - ymax) / (ymax - ymin) + 1  # rescale to [-1, 1]

        p = array(range(0, order + 1))
        # The Vandermonde matrix of wave number x.
        t = tile(x, (1, order + 1)) ** tile(p, (n, 1))

        Tinv = pinv(t.T @ t) @ t.T
        a = Tinv @ y  # The polynomial coefficients
        z = t @ a
        alpha = 0.99 * 1 / 2

        zp = ones((n, 1))
        d = zeros((n, 1))  # an auxiliary vector to solve for "a".

        while sum((z - zp) ** 2) / sum(zp ** 2) > 1e-9:
            zp = z
            residual = y - z

            for num in range(n):
                if residual[num] < s:
                    d[num] = residual[num] * (2 * alpha - 1)

                elif residual[num] >= s:
                    d[num] = -residual[num] - alpha * \
                        (s ** 3) / (2 * residual[num] ** 2)
            a = Tinv @ (y + d)
            z = t @ a

        return reshape((z - 1) @ (ymax - ymin) / 2 + ymax, (n, 1))

    def SendRequireParams(self):
        return 'xyp'

    def SendReturnParams(self):
        return 'ybp'


class PeakFind(SpectrumFunctionContainerBase):
    def __init__(self):
        super().__init__({
            'Height': FloatContainer(0, 0),
            'Threshold': FloatContainer(0, 0),
            'Distance': FloatContainer(0, 0),
            'Prominence': FloatContainer(0, 0),
            'Width': FloatContainer(0, 0),
        })

    def Function(self, args):
        x, y, height, threshold, distance, prominence, width = args
        dx = (max(x) - min(x)) / len(x)
        if distance is not None:
            distance = max(int(distance / dx), 1)

        if width is not None:
            width = max(int(width / dx), 0)
        else:
            width = 1

        peak_index_list, properties = find_peaks(y, height, threshold, distance, prominence, width, plateau_size=1)

        peaks = PeakFunctionContainerList()
        peak_type = self.data_accessor.GetPeakType()
        widths = dx * properties['widths']
        for amp, ctr, wid in zip(y[peak_index_list], x[peak_index_list], widths):

            peak = peak_type.GetPeakInstance()
            peak.Amp = amp
            peak.Ctr = ctr
            peak.Wid = wid

            peaks.append(peak)

        return (peaks,)

    def SendRequireParams(self):
        return 'xy'

    def SendReturnParams(self):
        return 'p'


class PeakSetting(SpectrumFunctionContainerBase):
    def __init__(self):
        super().__init__({
            'Amplitude': FloatContainer(100, 0),
            'Center': FloatContainer(0),
            'Width': FloatContainer(0, 0),
        })
        self.__arg_buffer = {}

    def Function(self, args):
        peaks = args[0]

        if (peak_type := self.data_accessor.GetPeakType()) is None:
            raise AttributeError()

        peak = peak_type.GetPeakInstance()
        peak.SetArgs(args[1:])

        peaks.append(peak)

        return (peaks,)

    def SendRequireParams(self):
        return 'p'

    def SendReturnParams(self):
        return 'p'

    def OnPeakTypeChanged(self, event):
        peak_type = self.data_accessor.GetPeakType()

        container_name = peak_type.GetArgumentNames()
        container_list = peak_type.GetArgumentContainerList()
        self.arg_container_dict = {key: value for key, value in zip(container_name, container_list)}


class CurveFit(SpectrumFunctionContainerBase):
    def __init__(self):
        super().__init__()
        self.__arg_buffer = {}

    def Function(self, args):
        if (peak_type := self.data_accessor.GetPeakType()) is None:
            raise AttributeError()

        x, y, peaks, *thresholds = args

        if (peak_length := len(peaks)) == 0:
            return PeakFunctionContainerList()

        peak_arg_length = peak_type.GetArgumentLength()

        culc_y_func = peak_type.GetFunction()

        def culc_spectrum_value(xdata, *param):
            values = []
            for n in range(peak_length):
                values.append(culc_y_func(xdata, param[peak_arg_length * n: peak_arg_length * (n + 1)]))

            return sum(values)

        lower_threshold = [inf if t[0] is None else t[0] for t in thresholds]
        upper_threshold = [inf if t[1] is None else t[1] for t in thresholds]

        lower_bounds = []
        upper_bounds = []
        for peak in peaks:
            for c, lt, ut in zip(peak.GetArgumentContainerList(), lower_threshold, upper_threshold):
                v = c.GetValue()
                lb, ub = c.GetBounds()
                lower_bounds.append(max(v - lt, lb))
                upper_bounds.append(min(v + ut, ub))

        bounds = [lower_bounds, upper_bounds]
        p0 = sum([list(peak.GetArgs()) for peak in peaks], [])

        popt, _ = curve_fit(culc_spectrum_value, x, y, p0=p0, bounds=bounds, check_finite=True)

        for n, peak in enumerate(peaks):
            peak.SetArgs(popt[peak_arg_length * n: peak_arg_length * (n + 1)])

        return (peaks,)

    def SendRequireParams(self):
        return 'xyp'

    def SendReturnParams(self):
        return 'p'

    def OnPeakTypeChanged(self, event):
        peak_type = self.data_accessor.GetPeakType()

        arg_names = peak_type.GetArgumentNames()
        self.arg_container_dict = {}

        for name in arg_names:
            key = name + ' threshold'

            if key in self.__arg_buffer:
                self.arg_container_dict[key] = self.__arg_buffer[key]
                continue

            self.arg_container_dict[key] = ListArgumentContainer([OptionalFloatContainer(None, 0, None), OptionalFloatContainer(None, 0, None)])


__all__ = [
    'Clipping',
    'Smooth',
    'Normalize',
    'SavgolFilter',
    'Goldindec',
    'PeakFind',
    'PeakSetting',
    'CurveFit',
]
