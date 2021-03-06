import os
import bumblebee.util
import bumblebee.module

def description():
    return "Shows free diskspace, total diskspace and the percentage of free disk space."

def parameters():
    return [
        "disk.warning: Warning threshold in % (defaults to 80%)",
        "disk.critical: Critical threshold in % (defaults to 90%)"
    ]

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)
        self._path = self._config.parameter("path", "/")

        output.add_callback(module=self.instance(), button=1, cmd="nautilus {}".format(self._path))

    def widgets(self):
        st = os.statvfs(self._path)

        self._size = st.f_frsize*st.f_blocks
        self._used = self._size - st.f_frsize*st.f_bavail
        self._perc = 100.0*self._used/self._size

        return bumblebee.output.Widget(self,
            "{} {}/{} ({:05.02f}%)".format(self._path,
            bumblebee.util.bytefmt(self._used),
            bumblebee.util.bytefmt(self._size), self._perc)
        )

    def warning(self, widget):
        return self._perc > self._config.parameter("warning", 80)

    def critical(self, widget):
        return self._perc > self._config.parameter("critical", 90)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
