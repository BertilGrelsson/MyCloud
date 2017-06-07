# Blah

import datetime
import openStackHandler as OpenStackHandler

import socket

class VMHandler:
  def __init__(self, vm_instance, ip):
    self.vm_instance = vm_instance
    self.socket = socket.socket()
    self.socket.setblocking(0)
    self.port = 12345
    self.host = ip
    self.socket.bind(self.host, self.port)
    self.buffer_size = 4096

  def try_connect(self):
    try:
      self.socket.connect()
      return True
    except Exception as e:
      return False

  def send_config(self, conf):
    try:
      self.socket.send(conf)
      return True
    except Exception as e:
      return False

  def try_recieve(self):
    try:
      data = self.socket.recv(4096)
      return data
    except Exception as e:
      return []

class Monitor:
  def __init__(self):
    self.open_stack_handler = OpenStackHandler()

    self.worker_counter = 0
    self.workers_started = []
    self.workers_configurating = []
    self.workers_running = []

    self.start_time = -1

    self.config = dict(
      "n_workers": 1,
      "worker_image": "ubuntu 16.04",
      "worker_flavor": "c2m2",
      "worker_script": "vm-worker-init.sh"
    )

  def configurate(self, args):
    pass

  def start(self):
    self.start_time = datetime.datetime.now()
    for k in range(0, self.config.n_workers):
       self.create_worker()

   def create_worker(self):
    vm_name = "worker"+str(self.backend_counter)
    self.worker_counter += 1
    vm = self.open_stack_handler.createVM(vm_name,
                                         self.config.worker_image,
                                         self.config.worker_flavor,
                                         self.config.worker_script)
    ip = self.open_stack_handler.getInternalIP(vm_name)
    vm_handler = VMHandler(vm, ip)
    self.workers_started.append(vm_handler)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-o", "--operation",
    metavar = "VM_OPERATION",
    help = "The operation that you want to perform",
    required = True,
    choices=["create","listVM","VMIP","terminate","listIP","assignFIP","monitor"],
    dest="operation")

  parser.add_argument("-n", "--name",
    metavar = "VM_NAME",
    help = "The name  for the VM that you want to perform the operation",
    dest="name")
  args = parser.parse_args()

  monitor = Monitor()
  monitor.configurate(args)
  monitor.start()
  exit(0)
