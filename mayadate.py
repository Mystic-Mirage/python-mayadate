from datetime import date, datetime, timedelta
from types import IntType, NoneType


__all__ = ['Correlation', 'Haab', 'LongCount', 'MayaDate', 'Tzolkin']


def _check_longcount_fields(piktun, baktun, katun, tun, uinal, kin):
    if not all([
        isinstance(piktun, (IntType, NoneType)),
        isinstance(baktun, IntType),
        isinstance(katun, IntType),
        isinstance(tun, IntType),
        isinstance(uinal, IntType),
        isinstance(kin, IntType),
    ]):
        raise TypeError('int expected')
    if piktun is not None and not 0 <= piktun <= 1:
        raise ValueError('piktun must be in 0..19', piktun)
    if not 0 <= baktun <= 19:
        raise ValueError('baktun must be in 0..19', baktun)
    if not 0 <= katun <= 19:
        raise ValueError('katun must be in 0..19', katun)
    if not 0 <= tun <= 19:
        raise ValueError('tun must be in 0..19', tun)
    if not 0 <= uinal <= 17:
        raise ValueError('uinal must be in 0..17', uinal)
    if not 0 <= kin <= 19:
        raise ValueError('kin must be in 0..19', kin)


def _cmperror(x, y):
    raise TypeError("can't compare '%s' to '%s'" % (
                    x.__class__.__name__, y.__class__.__name__))


class _PicklableMixin:

    def __reduce__(self):
        return self.__class__, self.tuple()


class Correlation(object):

    __slots__ = '_jdn'

    def __new__(cls, jdn):
        self = object.__new__(cls)
        self._jdn = int(jdn)
        return self

    @classmethod
    def gmt(cls):
        return cls(584283)

    @classmethod
    def tl(cls):
        return cls(584285)

    def __int__(self):
        return self._jdn

    def __repr__(self):
        return '%s.%s(%d)' % (__name__, self.__class__.__name__, self._jdn)

    def __eq__(self, other):
        if isinstance(other, Correlation):
            return int(self) == int(other)
        _cmperror(self, other)

    def __reduce__(self):
        return self.__class__, (self._jdn,)


_HAABNAMES = ("Pop", "Wo", "Sip", "Sotz'", "Tzek", "Xul", "Yaxk'", "Mol",
              "Ch'en", "Yax", "Sac", "Keh", "Mak", "K'ank'in", "Muwan", "Pax",
              "K'ayab'", "Kumk'u", "Wayeb'")


class Haab(_PicklableMixin, object):

    def __new__(cls, h1, h2):
        self = object.__new__(cls)
        self._h1, self._h2 = h1, h2
        return self

    @classmethod
    def fromlongcount(cls, l):
        d = l.toordinal()
        h1, h2 = divmod((d + 348) % 365, 20)
        return cls(h1, h2)

    def tuple(self):
        return self._h1, self._h2

    def __repr__(self):
        return '%s.%s(%d, %d)' % (
            __name__, self.__class__.__name__, self._h1, self._h2,
        )

    def __str__(self):
        return '%d %s' % (self._h2, _HAABNAMES[self._h1])

    def __eq__(self, other):
        if isinstance(other, Haab):
            return self.tuple() == other.tuple()
        _cmperror(self, other)


_TZOLKINNAMES = ("Imix'", "Ik'", "Ak'b'al", "K'an", "Chikchan", "Kimi",
                 "Manik'", "Lamat", "Muluk", "Ok", "Chuwen", "Eb'", "B'en",
                 "Ix", "Men", "K'ib'", "Kab'an", "Etz'nab'", "Kawak", "Ajaw")


class Tzolkin(_PicklableMixin, object):

    def __new__(cls, t1, t2):
        self = object.__new__(cls)
        self._t1, self._t2 = t1, t2
        return self

    @classmethod
    def fromlongcount(cls, l):
        d = l.toordinal()
        t1, t2 = (d + 19) % 20, (d + 3) % 13 + 1
        return cls(t1, t2)

    def tuple(self):
        return self._t1, self._t2

    def __repr__(self):
        return '%s.%s(%d, %d)' % (
            __name__, self.__class__.__name__, self._t1, self._t2,
        )

    def __str__(self):
        return '%d %s' % (self._t2, _TZOLKINNAMES[self._t1])

    def __eq__(self, other):
        if isinstance(other, Tzolkin):
            return self.tuple() == other.tuple()
        _cmperror(self, other)


_RATES = (2880000, 144000, 7200, 360, 20, 1)


class LongCount(_PicklableMixin, object):
    correlation = Correlation.gmt()

    __slots__ = '_p', '_b', '_k', '_t', '_u', '_n'

    def __new__(cls, *args):
        self = object.__new__(cls)
        if len(args) == 5:
            p = None
            b, k, t, u, n = args
        elif len(args):
            p, b, k, t, u, n = args
        _check_longcount_fields(p, b, k, t, u, n)
        self._p = p
        self._b = b
        self._k = k
        self._t = t
        self._u = u
        self._n = n
        return self

    @classmethod
    def fromdate(cls, date, correlation=None):
        c = cls.correlation if correlation is None else correlation
        d = date.toordinal() + 1721425 - int(c)
        self = cls.fromordinal(d)
        if correlation is not None:
            self.correlation = correlation
        return self

    @classmethod
    def fromordinal(cls, d):
        r = []
        for i in _RATES:
            t, d = divmod(d, i)
            r.append(t)
        if r[0] == 0:
            r = r[1:]
        self = cls(*r)
        return self

    @classmethod
    def today(cls, correlation=None):
        return cls.fromdate(date.today(), correlation)

    @property
    def piktun(self):
        return 0 if self._p is None else self._p

    @property
    def baktun(self):
        return self._b

    @property
    def katun(self):
        return self._k

    @property
    def tun(self):
        return self._t

    @property
    def uinal(self):
        return self._u

    @property
    def kin(self):
        return self._n

    def todate(self, correlation=None):
        c = self.correlation if correlation is None else correlation
        o = self.toordinal() - 1721425 + int(c)
        return date.fromordinal(o)

    def toordinal(self):
        s = 0
        for i, j in zip(reversed(self.tuple()), reversed(_RATES)):
            s += i * j
        return s

    def tuple(self):
        if self._p is None:
            return self._b, self._k, self._t, self._u, self._n
        else:
            return self._p, self._b, self._k, self._t, self._u, self._n

    def __repr__(self):
        return '%s.%s(%s)' % (
            __name__, self.__class__.__name__,
            ', '.join(map(str, self.tuple())),
        )

    def __str__(self):
        return '.'.join(map(str, self.tuple()))

    def _cmp(self, other):
        if isinstance(other, (date, datetime)):
            other = LongCount.fromdate(other)
        elif not isinstance(other, (LongCount, MayaDate)):
            _cmperror(self, other)
        x, y = self.tuple(), other.tuple()
        return 0 if x == y else 1 if x > y else -1

    def __eq__(self, other):
        return self._cmp(other) == 0

    def __ne__(self, other):
        return self._cmp(other) != 0

    def __le__(self, other):
        return self._cmp(other) <= 0

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __ge__(self, other):
        return self._cmp(other) >= 0

    def __gt__(self, other):
        return self._cmp(other) > 0


class MayaDate(LongCount):

    @property
    def longcount(self):
        return LongCount(*self.tuple())

    @property
    def haab(self):
        return Haab.fromlongcount(self)

    @property
    def tzolkin(self):
        return Tzolkin.fromlongcount(self)

    def __str__(self):
        return '%s %s %s' % (super(MayaDate, self).__str__(),
                             self.tzolkin, self.haab)
