from mesos_collectd import MesosCollectd
import collectd


class MesosMaster(MesosCollectd):

    def __init__(self, config):
        super(MesosMaster, self).__init__(config)
        self.name = self.__class__.__name__
        self.log_info('Configured {} plugin.'.format(self.name))

#
# mesos master metrics collector python plugin for collectd
#
client = None


def configurator(collectd_conf):
    """
    configure the mesos metrics collector
    options:
        host: ip of target mesos host
        port: port of target mesos host
        trackingname: vanity host name to use for master tracking
        separator: separator character for mesos metric names
        configfile: metric configuration file
    """
    global client

    config = {'port': 5050}
    for item in collectd_conf.children:
        key = item.key.lower()
        val = item.values[0]
        if key == 'host':
            config['host'] = val
        elif key == 'port':
            config['port'] = int(val)
        elif key == 'separator':
            config[key] = val
        elif key == 'trackingname':
            config['tracking_name'] = val
        elif key == 'configfile':
            config['config_file'] = val
        else:
            collectd.warning('mesos-master plugin: unknown config key {} = {}'.format(item.key, val))

    #
    # this cannot be overridden
    #
    config['master'] = True

    client = MesosMaster(config)


def reader():
    global client
    client.emit_metrics(client.fetch_metrics())


collectd.register_config(configurator)
collectd.register_read(reader)
