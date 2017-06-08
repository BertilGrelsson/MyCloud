# The cloud monitor
# Its purpose is to bring up and tear down the entire cloud service,
# to create/remove instances when necessary (scaling, robustness)
# and to monitor the health and usage of the VM's that are part of
# the cloud service.


import datetime
import openStackHandler as OpenStackHandler
import vmhandler as VMHandler

class Monitor:
  def __init__(self):
    self.open_stack_handler = OpenStackHandler()

    self.worker_counter = 0
    self.workers = []

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

    while True:
      # Manage workers
      for worker in self.workers:
        worker.update()
        # TODO Log status
        if worker.state == VM_STATE.UNRESPONSIVE:
          worker.shut_down()
          # TODO Remove worker from workers
        elif worker.state == VM_STATE.WORKING:
          # TODO Collect measurements if suitable
          pass

      # Control number of workers
      # TODO
      
      # Communicate with outside.
      #  * Report status and measurements.
      #  * Take commands.
      # TODO

  def create_worker(self):
    vm_name = "worker"+str(self.backend_counter)
    self.worker_counter += 1
    vm = self.open_stack_handler.createVM(vm_name,
                                         self.config.worker_image,
                                         self.config.worker_flavor,
                                         self.config.worker_script)
    ip = self.open_stack_handler.getInternalIP(vm_name)
    vm_handler = VMHandler(vm, ip)
    self.workers.append(vm_handler)

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
