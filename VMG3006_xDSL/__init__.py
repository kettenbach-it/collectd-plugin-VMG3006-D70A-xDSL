try:
    # This is only availabe "inside" collectd
    import collectd
except ImportError:
    # Outside collectd we need to mock this class, since the linter will complain etc.
    import collectd_mock as collectd

import requests
import sys, time, os
from bs4 import BeautifulSoup

PLUGIN_NAME = 'VMG3006_xDSL'
loginpath = "/webng.cgi"
dslpath = "/webng.cgi?ajaxrequest=2&controller=Ajax&action=index&id=0&subcontroller=Internet&subaction=renderDslState&evalJS=force"
params = {}


class XdslInfo:
    upstream_datarate: str = None
    downstream_datarate: str = None
    upstream_linecapacity: str = None
    downstream_linecapacity: str = None

    upstream_band0_snr: str = None
    downstream_band0_snr: str = None
    upstream_band0_lineattenuation: str = None
    downstream_band0_lineattenuation: str = None
    upstream_band0_signalattenuation: str = None
    downstream_band0_signalattenuation: str = None

    upstream_band1_snr: str = None
    downstream_band1_snr: str = None
    upstream_band1_lineattenuation: str = None
    downstream_band1_lineattenuation: str = None
    upstream_band1_signalattenuation: str = None
    downstream_band1_signalattenuation: str = None

    upstream_band2_snr: str = None
    downstream_band2_snr: str = None
    upstream_band2_lineattenuation: str = None
    downstream_band2_lineattenuation: str = None
    upstream_band2_signalattenuation: str = None
    downstream_band2_signalattenuation: str = None

    def xstr(self, s):
        if s is None:
            return 'N/A '
        else:
            return str(s)

    def __str__(self):
        out = "Upstream Datenrate: " + self.upstream_datarate + " KBit/s"
        out += "\nDownstream Datenrate: " + self.downstream_datarate + " KBit/s"
        out += "\nUpstream Leitungskapazität: " + self.upstream_linecapacity + " KBit/s"
        out += "\nDownstream Leitungskapazität: " + self.downstream_linecapacity + " KBit/s"
        out += "\nupstream_band0_snr: " + self.upstream_band0_snr + " db"
        out += "\ndownstream_band0_snr: " + self.downstream_band0_snr + " db"
        out += "\nupstream_band0_lineattenuation: " + self.upstream_band0_lineattenuation + " db"
        out += "\ndownstream_band0_lineattenuation: " + self.downstream_band0_lineattenuation + " db"
        out += "\nupstream_band0_signalattenuation: " + self.upstream_band0_signalattenuation + " db"
        out += "\ndownstream_band0_signalattenuation: " + self.downstream_band0_signalattenuation + " db"
        out += "\nupstream_band1_snr: " + self.upstream_band1_snr + " db"
        out += "\ndownstream_band1_snr: " + self.downstream_band1_snr + " db"
        out += "\nupstream_band1_lineattenuation: " + self.upstream_band1_lineattenuation + " db"
        out += "\ndownstream_band1_lineattenuation: " + self.downstream_band1_lineattenuation + " db"
        out += "\nupstream_band1_signalattenuation: " + self.upstream_band1_signalattenuation + " db"
        out += "\ndownstream_band1_signalattenuation: " + self.downstream_band1_signalattenuation + " db"
        out += "\nupstream_band2_snr: " + self.upstream_band2_snr + " db"
        out += "\ndownstream_band2_snr: " + self.downstream_band2_snr + " db"
        out += "\nupstream_band2_lineattenuation: " + self.upstream_band2_lineattenuation + " db"
        out += "\ndownstream_band2_lineattenuation: " + self.downstream_band2_lineattenuation + " db"
        out += "\nupstream_band2_signalattenuation: " + self.upstream_band2_signalattenuation + " db"
        out += "\ndownstream_band2_signalattenuation: " + self.downstream_band2_signalattenuation + " db"
        out += "\nfec_errors_nearend: " + self.fec_errors_nearend
        out += "\nfec_errors_farend: " + self.fec_errors_farend
        out += "\ncrc_errors_nearend: " + self.crc_errors_nearend
        out += "\ncrc_errors_farend: " + self.crc_errors_farend
        out += "\ncrcp_errors_nearend: " + self.crcp_errors_nearend
        out += "\ncrcp_errors_farend: " + self.crcp_errors_farend
        out += "\ncrcpp_errors_nearend: " + self.crcpp_errors_nearend
        out += "\ncrcpp_errors_farend: " + self.crcpp_errors_farend
        out += "\ncvp_errors_nearend: " + self.cvp_errors_nearend
        out += "\ncvp_errors_farend: " + self.cvp_errors_farend
        out += "\ncvpp_errors_nearend: " + self.cvpp_errors_nearend
        out += "\ncvpp_errors_farend: " + self.cvpp_errors_farend
        return out

    def parse(self, tables):
        cells = tables[1].findAll("td")

        self.upstream_datarate = str(cells[0].text).split("\xa0")[0]
        self.downstream_datarate = str(cells[1].text).split("\xa0")[0]
        self.upstream_linecapacity = str(cells[2].text).split("\xa0")[0]
        self.downstream_linecapacity = str(cells[3].text).split("\xa0")[0]

        cells = tables[2].findAll("td")
        self.upstream_band0_snr = str(cells[0].text).split("\xa0")[0]
        self.downstream_band0_snr = str(cells[1].text).split("\xa0")[0]
        self.upstream_band0_lineattenuation = str(cells[2].text).split("\xa0")[0]
        self.downstream_band0_lineattenuation = str(cells[3].text).split("\xa0")[0]
        self.upstream_band0_signalattenuation = str(cells[4].text).split("\xa0")[0]
        self.downstream_band0_signalattenuation = str(cells[5].text).split("\xa0")[0]
        self.upstream_band1_snr = str(cells[6].text).split("\xa0")[0]
        self.downstream_band1_snr = str(cells[7].text).split("\xa0")[0]
        self.upstream_band1_lineattenuation = str(cells[8].text).split("\xa0")[0]
        self.downstream_band1_lineattenuation = str(cells[9].text).split("\xa0")[0]
        self.upstream_band1_signalattenuation = str(cells[10].text).split("\xa0")[0]
        self.downstream_band1_signalattenuation = str(cells[11].text).split("\xa0")[0]
        self.upstream_band2_snr = str(cells[12].text).split("\xa0")[0]
        self.downstream_band2_snr = str(cells[13].text).split("\xa0")[0]
        self.upstream_band2_lineattenuation = str(cells[14].text).split("\xa0")[0]
        self.downstream_band2_lineattenuation = str(cells[15].text).split("\xa0")[0]
        self.upstream_band2_signalattenuation = str(cells[16].text).split("\xa0")[0]
        self.downstream_band2_signalattenuation = str(cells[17].text).split("\xa0")[0]

        cells = tables[3].findAll("td")
        self.fec_errors_nearend = cells[0].text
        self.fec_errors_farend = cells[1].text
        self.crc_errors_nearend = cells[2].text
        self.crc_errors_farend = cells[3].text
        self.crcp_errors_nearend = cells[4].text
        self.crcp_errors_farend = cells[5].text
        self.crcpp_errors_nearend = cells[6].text
        self.crcpp_errors_farend = cells[7].text
        self.cvp_errors_nearend = cells[8].text
        self.cvp_errors_farend = cells[9].text
        self.cvpp_errors_nearend = cells[10].text
        self.cvpp_errors_farend = cells[11].text


xdslinfo = XdslInfo()


def getXDSLStats(host, user, password):
    session = requests.session()
    postreply = session.post(host + loginpath, {
        'LoginName': user,
        'LoginPass': password
    })
    sid = postreply.cookies.get("SESSION_ID")
    # Get page with xDSL Stats
    xdslrequest = session.get(host + dslpath + "&sid=" + sid)
    # Parse page with BS
    soup = BeautifulSoup(xdslrequest.content, 'html.parser')
    # Extract text-object and parse with XdslInf
    xdslinfo.parse(soup.findAll("table"))


def printDSLStats():
    log(xdslinfo)


def init():
    log("Plugin %s initializing..." % PLUGIN_NAME)


def shutdown():
    log("Plugin %s shutting down..." % PLUGIN_NAME)


def callback_configure(config):
    """ Configure callback """
    for node in config.children:
        if node.key == 'URL':
            if str(node.values[0]).endswith("/"):
                params['url'] = str(node.values[0]).rstrip("/")
            else:
                params['url'] = node.values[0]
            log("Plugin %s configured to get %s." % (PLUGIN_NAME, params['url']))
        elif node.key == 'User':
            params['user'] = node.values[0]
        elif node.key == 'Password':
            params['password'] = node.values[0]
        else:
            collectd.warning('Unknown config %s' % node.key)


def log(param):
    if __name__ != '__main__':
        collectd.info("%s: %s" % (PLUGIN_NAME, param))
    else:
        sys.stderr.write("%s\n" % param)


def read():
    getXDSLStats(params['url'], params['user'], params['password'])
    if __name__ != "__main__":
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="datarateUpstream",
                        type="gauge",
                        values=[xdslinfo.upstream_datarate]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="datarateDownstream",
                        type="gauge",
                        values=[xdslinfo.downstream_datarate]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="linecapacityUpstream",
                        type="gauge",
                        values=[xdslinfo.upstream_linecapacity]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="linecapacityDownstream",
                        type="gauge",
                        values=[xdslinfo.downstream_linecapacity]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="snrUpstreamBand0",
                        type="gauge",
                        values=[xdslinfo.upstream_band0_snr]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="snrDownstreamBand0",
                        type="gauge",
                        values=[xdslinfo.downstream_band0_snr]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="lineattenuationUpstreamBand0",
                        type="gauge",
                        values=[xdslinfo.upstream_band0_lineattenuation]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="lineattenuationDownstreamBand0",
                        type="gauge",
                        values=[xdslinfo.downstream_band0_lineattenuation]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="signalattenuationUpstreamBand0",
                        type="gauge",
                        values=[xdslinfo.upstream_band0_signalattenuation]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="signalattenuationDownstreamBand0",
                        type="gauge",
                        values=[xdslinfo.downstream_band0_signalattenuation]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="snrUpstreamBand1",
                        type="gauge",
                        values=[xdslinfo.upstream_band1_snr]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="snrDownstreamBand1",
                        type="gauge",
                        values=[xdslinfo.downstream_band1_snr]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="lineattenuationUpstreamBand1",
                        type="gauge",
                        values=[xdslinfo.upstream_band1_lineattenuation]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="lineattenuationDownstreamBand1",
                        type="gauge",
                        values=[xdslinfo.downstream_band1_lineattenuation]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="signalattenuationUpstreamBand1",
                        type="gauge",
                        values=[xdslinfo.upstream_band1_signalattenuation]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="signalattenuationDownstreamBand1",
                        type="gauge",
                        values=[xdslinfo.downstream_band1_signalattenuation]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="snrUpstreamBand2",
                        type="gauge",
                        values=[xdslinfo.upstream_band2_snr]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="snrDownstreamBand2",
                        type="gauge",
                        values=[xdslinfo.downstream_band2_snr]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="lineattenuationUpstreamBand2",
                        type="gauge",
                        values=[xdslinfo.upstream_band2_lineattenuation]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="lineattenuationDownstreamBand2",
                        type="gauge",
                        values=[xdslinfo.downstream_band2_lineattenuation]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="signalattenuationUpstreamBand2",
                        type="gauge",
                        values=[xdslinfo.upstream_band2_signalattenuation]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="signalattenuationDownstreamBand2",
                        type="gauge",
                        values=[xdslinfo.downstream_band2_signalattenuation]
                        ).dispatch()

        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="errorsFecNearend",
                        type="gauge",
                        values=[xdslinfo.fec_errors_nearend]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="errorsFecFarend",
                        type="gauge",
                        values=[xdslinfo.fec_errors_farend]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="errorsCrcNearend",
                        type="gauge",
                        values=[xdslinfo.crc_errors_nearend]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="errorsCrcFarend",
                        type="gauge",
                        values=[xdslinfo.crc_errors_farend]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="errorsCrcpNearend",
                        type="gauge",
                        values=[xdslinfo.crcp_errors_nearend]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="errorsCrcpFarend",
                        type="gauge",
                        values=[xdslinfo.crcp_errors_farend]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="errorsCrcppNearend",
                        type="gauge",
                        values=[xdslinfo.crcpp_errors_nearend]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="errorsCrcppFarend",
                        type="gauge",
                        values=[xdslinfo.crcpp_errors_farend]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="errorsCvpNearend",
                        type="gauge",
                        values=[xdslinfo.cvp_errors_nearend]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="errorsCvpFarend",
                        type="gauge",
                        values=[xdslinfo.cvp_errors_farend]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="errorsCvppNearend",
                        type="gauge",
                        values=[xdslinfo.cvpp_errors_nearend]
                        ).dispatch()
        collectd.Values(plugin=PLUGIN_NAME,
                        type_instance="errorsCvppFarend",
                        type="gauge",
                        values=[xdslinfo.cvpp_errors_farend]
                        ).dispatch()

    else:
        printDSLStats()


if __name__ != "__main__":
    # when running inside plugin register each callback
    collectd.register_config(callback_configure)
    collectd.register_init(init)
    collectd.register_shutdown(shutdown)
    collectd.register_read(read)
else:
    # outside plugin just collect the info
    if os.environ.get('URL').endswith("/"):
        params['url'] = os.environ.get('URL').rstrip("/")
    else:
        params['url'] = os.environ.get('URL')
    params['user'] = os.environ.get('USER')
    params['password'] = os.environ.get('PASSWORD')
    read()
    if len(sys.argv) < 2:
        while True:
            time.sleep(10)
            read()
