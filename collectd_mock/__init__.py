__all__ = ("Values",)


class Data(object):
    def __init__(
            self,
            plugin_instance=None,
            meta=None,
            plugin=None,
            host=None,
            type=None,
            type_instance=None,
            interval=None,
            time=None,
            values=None,
    ):
        self.plugin = plugin
        self.plugin_instance = plugin_instance,
        self.meta = meta
        self.host = host
        self.type = type
        self.type_instance = type_instance
        self.values = values
        self.interval = interval
        self.time = time

    def dispatch(self):
        pass


def mk_values(
        plugin_instance=None,
        meta=None,
        plugin=None,
        host=None,
        type=None,
        type_instance=None,
        interval=None,
        time=None,
        values=None,
):
    return Data(
        plugin_instance=plugin_instance,
        meta=meta,
        plugin=plugin,
        host=host,
        type=type,
        type_instance=type_instance,
        interval=interval,
        time=time,
        values=values,
    )


Values = mk_values


def register_init(func):
    pass


def register_shutdown(func):
    pass


def register_config(func):
    pass


def register_read(func):
    pass


def register_write(func):
    pass


def info(msg):
    print(msg)


def warning(msg):
    print(msg)
