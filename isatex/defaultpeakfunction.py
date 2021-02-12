from numpy import exp, log

from .objects import FloatContainer, PeakFunctionContainerBase


class Lorentz(PeakFunctionContainerBase):
    def __init__(self):
        amp = FloatContainer(1.0, min_=0.0)
        ctr = FloatContainer()
        wid = FloatContainer(1.0, min_=0.0)
        super().__init__({'Amplitude': amp, 'Center': ctr, 'Width': wid})

    def Function(self, x, args):
        return args[0] / ((4 * (x - args[1]) / args[2]) ** 2 + 1) if args[2] != 0 else 1e10

    def GetTex(self):
        return r'$Amp\ \frac{Wid^2}{4\left( x - Ctr \right)^2 + Wid^2}$'


class PseudoVoigt(PeakFunctionContainerBase):
    def __init__(self):
        amp = FloatContainer(1.0, min_=0.0)
        ctr = FloatContainer()
        wid = FloatContainer(1.0, min_=0.0)
        eta = FloatContainer(0.5, min_=0.0, max_=1.0)
        super().__init__({'Amplitude': amp, 'Center': ctr, 'Width': wid, 'Eta': eta})

    def Function(self, x, args):
        return args[3] * (args[0] * exp(- 4 * log(2) * ((x - args[1]) / args[2]) ** 2)) + \
            (1 - args[3]) * args[0] / ((4 * (x - args[1]) / args[2]) ** 2 + 1)

    def GetTex(self):
        return r'$Eta\ Amp\ exp\left(-4\ln{2}\left( \frac{x - Ctr}{Wid}\right)^2 \right)$' + '\n' + \
            r'$ + (1 - Eta)\ Amp\ \frac{Wid^2}{4\left( x - Ctr \right)^2 + Wid^2}$'


__all__ = [
    'Lorentz',
    'PseudoVoigt',
]
