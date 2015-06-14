python-mayadate
===============

Maya Date:
```python
>>> m = mayadate.MayaDate(8, 3, 2, 10, 15)
>>> m
mayadate.MayaDate(8, 3, 2, 10, 15)
```

Human readable:
```python
>>> str(m)
"8.3.2.10.15 2 Men 13 Pax"
```

Long Count:
```python
>>> str(m.longcount)
'8.3.2.10.15'
```

Tzolkin:
```python
>>> str(m.tzolkin)
'2 Men'
```

Haab:
```python
>>> str(m.haab)
'13 Pax'
```

To Gregorian Date Conversion:
```python
>>> g = m.todate()
>>> g
datetime.date(103, 5, 19)
```

TODO:
-----
* add computaion and comparsions
* add year bearer
* add lord of night
* replace() method
* pickle support
* publish on PyPI
