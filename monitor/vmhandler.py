import socket
from enum import Enum

VM_STATE = Enum('STARTING', 'CONNECTED', 'CONFIGURING', 'READY', 'WORKING', 'UNRESPONSIVE')
COM_STATE = Enum('IDLE', 'SENT', 'RECIEVED', 'ERROR')

class VMHandler:
  def __init__(self, vm_instance, ip):
    self.state = VM_STATE.STARTING
    self.com_state = 
    self.vm_instance = vm_instance
    self.socket = socket.socket()
    self.buffer_size = 4096
    self.port = 12345
    self.host = ip
    self.socket.bind(self.host, self.port)
    self.socket.setblocking(0)
    
    self.vm_config = []
    
  def update(self):
  """ Progress the state machine.
      Perform heart beat check.
      Perform measurement of resource usage (if applicable).
  """
    if self.state == VM_STATE.STARTING:
      if self.try_connect():
        self.state == VM_STATE.CONNECTED
    
    if self.state == VM_STATE.CONNECTED:
      if self.try_send(self.vm_config):
        self.state = VM_STATE.CONFIGURING
        
    if self.state == VM_STATE.CONFIGURING:
      data = self.try_recieve()
      if data and data == 'Config OK':
        self.state = VM_STATE.READY        
    
    if self.state == VM_STATE.READY or
       self.state == VM_STATE.WORKING:
      error = try_send('Status')
      if not error:
        try_
      
          

  def try_connect(self):
    try:
      self.socket.connect()
      return True
    except Exception as e:
      return False

  def try_send(self, data):
    try:
      self.socket.send(data)
      return True
    except Exception as e:
      return False

  def try_recieve(self):
    try:
      data = self.socket.recv(4096)
      return data
    except Exception as e:
      return []

