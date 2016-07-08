from abc import ABCMeta


def make_column_type(datatype, name, width):
    if datatype == "TEXT":
        Obj = TextColumn
    elif datatype == "INTEGER":
        Obj = IntegerColumn
    elif datatype == "BOOLEAN":
        Obj = BooleanColumn
    else:
        raise Exception("Unsupported datatype %s" % datatype)
    return Obj(name, width)


class ColumnBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, width):
        self.name = name
        self.width = width

    @property
    def formatted_width(self):
        return max(self.width, len(self.name))

    @property
    def formatted_column_name(self):
        return self.name.ljust(self.formatted_width)

    def get_formatted_value(self, raw_value):
        text = unicode(raw_value)
        return text.ljust(self.formatted_width)

    def get_db_value(self, raw_value):
        return unicode(raw_value)


class TextColumn(ColumnBase):
    pass


class BooleanColumn(ColumnBase):
    @property
    def formatted_width(self):
        # is 'self.width' necessary here?
        return max(5, len(self.name), self.width)

    def get_formatted_value(self, raw_value):
        if raw_value == 1:
            return u"True".ljust(self.formatted_width)
        else:
            return u"False".ljust(self.formatted_width)

    def get_db_value(self, raw_value):
        return int(raw_value)


class IntegerColumn(ColumnBase):
    def get_formatted_value(self, raw_value):
        return unicode(raw_value).rjust(self.formatted_width)

    def get_db_value(self, raw_value):
        return int(raw_value)
