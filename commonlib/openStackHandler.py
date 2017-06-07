from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient.client import Client as NovaClient
import ConfigParser

class OpenStackHandler:
  def __init__(self):
    self.readConf()
    self.auth = v3.Password(
      username=self.openStackUsername,
      password=self.openStackPassword,
      project_name=self.projectName,
      auth_url= self.openStackAuthUrl,
      user_domain_name = self.openStackUserDomainName,
      # domain_name = 'xerces',
      project_domain_name = self.openStackProjectDomainName,
      project_id =self.openStackProjectDomainId
    )
    self.sess = session.Session(auth=self.auth)
    self.nova = NovaClient("2", session=self.sess)

  def readConf(self):
    config = ConfigParser.RawConfigParser()
    config.read('config.properties')
    self.openStackUsername=config.get('user', 'username')
    self.openStackPassword=config.get('user', 'password')
    self.projectName=config.get('openstack', 'projectName')
    self.openStackAuthUrl=config.get('openstack','authUrl')
    self.openStackKeyName=config.get('openstack','keyName')
    self.openStackNetId=config.get('openstack','netId')
    self.openStackProjectDomainName=config.get('openstack','project_domain_name')
    self.openStackProjectDomainId=config.get('openstack','project_domain_id')
    self.openStackUserDomainName=config.get('openstack','user_domain_name')

  def createVM(self, VMName, image="ubuntu 16.04", flavor="c2m2", script="vm-init.sh"):
    # nova.servers.list()
    image = self.nova.images.find(name=image)  # nova.images.find(name="Test") #
    flavor = self.nova.flavors.find(name=flavor)
    net = self.nova.networks.find(label=self.openStackNetId)
    nics = [{'net-id': net.id}]
    vm = self.nova.servers.create(name=VMName, image=image, flavor=flavor, key_name=self.openStackKeyName, nics=nics, userdata=open(script))
    return vm

  def terminateVM(self,VMName):
    instance = self.nova.servers.find(name=VMName)
    if instance == None :
      print("server %s does not exist" % VMName)
      return False
    else:
      print("deleting server..........")
      self.nova.servers.delete(instance)
      print("server %s deleted" % VMName)
      return True

  def getVMs(self):
    """Every element has the following properties:
         id,name,image,flavor,key_name,user_id,networks
    """
    return self.nova.servers.list()

  def getVM(self, VMName):
    return self.nova.servers.find(name=VMName)

  def getInternalIP(self, VMName):
    instance = self.nova.servers.find(name=VMName)
    return instance.networks['Test'][0]

  def getExternalIP(self, VMName):
    instance = self.nova.servers.find(name=VMName)
    return instance.networks['Test'][1]


