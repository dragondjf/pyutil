# -*- coding: utf-8 -*-


class KeyedTuple(tuple):
    """``tuple`` subclass that adds labeled names.

    E.g.::

        >>> k = KeyedTuple([1, 2, 3], labels=["one", "two", "three"])
        >>> k.one
        1
        >>> k.two
        2

    Result rows returned by :class:`.Query` that contain multiple
    ORM entities and/or column expressions make use of this
    class to return rows.

    The :class:`.KeyedTuple` exhibits similar behavior to the
    ``collections.namedtuple()`` construct provided in the Python
    standard library, however is architected very differently.
    Unlike ``collections.namedtuple()``, :class:`.KeyedTuple` is
    does not rely on creation of custom subtypes in order to represent
    a new series of keys, instead each :class:`.KeyedTuple` instance
    receives its list of keys in place.   The subtype approach
    of ``collections.namedtuple()`` introduces significant complexity
    and performance overhead, which is not necessary for the
    :class:`.Query` object's use case.

    .. versionchanged:: 0.8
        Compatibility methods with ``collections.namedtuple()`` have been
        added including :attr:`.KeyedTuple._fields` and
        :meth:`.KeyedTuple._asdict`.

    .. seealso::

        :ref:`ormtutorial_querying`

    """

    def __new__(cls, vals, labels=None):
        t = tuple.__new__(cls, vals)
        t._labels = []
        if labels:
            t.__dict__.update(zip(labels, vals))
            t._labels = labels
        return t

    def keys(self):
        """Return a list of string key names for this :class:`.KeyedTuple`.

        .. seealso::

            :attr:`.KeyedTuple._fields`

        """

        return [l for l in self._labels if l is not None]

    @property
    def _fields(self):
        """Return a tuple of string key names for this :class:`.KeyedTuple`.

        This method provides compatibility with ``collections.namedtuple()``.

        .. versionadded:: 0.8

        .. seealso::

            :meth:`.KeyedTuple.keys`

        """
        return tuple(self.keys())

    def _asdict(self):
        """Return the contents of this :class:`.KeyedTuple` as a dictionary.

        This method provides compatibility with ``collections.namedtuple()``,
        with the exception that the dictionary returned is **not** ordered.

        .. versionadded:: 0.8

        """
        return dict((key, self.__dict__[key]) for key in self.keys())