
from ConfigParser import SafeConfigParser
import re

class Config (SafeConfigParser):
  OPTCRE = re.compile(
          r'\s?(?P<option>[^:=\s][^:=]*)'       # very permissive!
          r'\s*(?P<vi>[:=])\s*'                 # any number of space/tab,
                                                # followed by separator
                                                # (either : or =), followed
                                                # by any # space/tab
          r'(?P<value>.*)$'                     # everything up to eol
          )
  def save (self):
    secrets = ['serial']

    publicConfig = Config( )
    privateConfig = Config( )

    for section in self.sections():
      publicConfig.add_section(section)
      privateConfig.add_section(section)

      for k,v in self.items(section):
        if k in secrets:
          privateConfig.set(section, k, v)
        else:
          publicConfig.set(section, k, v)
    publicConfig.do_save('openaps.ini')
    privateConfig.do_save('secret.ini')


  def do_save(self, filename):
    with open(filename, 'wb') as configfile:
      self.write(configfile)
  def add_device (self, device):
    section = device.section_name( )
    self.add_section(section)
    for k, v in device.items( ):
      self.set(section, k, v)

  def remove_device (self, device):
    section = device.section_name( )
    self.remove_section(section)
  @classmethod
  def Read (klass, name=None, defaults=['openaps.ini', '~/.openaps.ini', '/etc/openaps/openaps.ini']):
    config = Config( )
    if name is not None:
      config.read([name, 'secret.ini'])
    else:
      config.read(defaults)
    return config


