import sys, time, hashlib, boto3
from timeit import default_timer

tag = "comsm0010_CW"

def main(argv):
   first          = int(argv[1])
   last           = int(argv[2])
   difficulty     = int(argv[3])
   block_header   = "COMSM0010cloud"
   found          = False
   nonce          = first
   sqs            = boto3.client('sqs')
   linkQ          = sqs.get_queue_url(QueueName="cloudQ")["QueueUrl"]
   start_time     = default_timer()

   while (nonce <= last):
       bin_nonce = "{0:b}".format(nonce)
       block = (block_header + bin_nonce).encode('utf-8')
       hashed2 = hashlib.sha256(hashlib.sha256(block).digest()).hexdigest()
       bin_hash = bin(int(hashed2, 16))[2:].zfill(256)
       if (bin_hash + '1').index('1') >= difficulty:
           found = True
           nonce = nonce
           break

       bin_nonce = "{0:b}".format(nonce+1)
       block = (block_header + bin_nonce).encode('utf-8')
       hashed2 = hashlib.sha256(hashlib.sha256(block).digest()).hexdigest()
       bin_hash = bin(int(hashed2, 16))[2:].zfill(256)
       if (bin_hash + '1').index('1') >= difficulty:
           found = True
           nonce = nonce + 1
           break

       bin_nonce = "{0:b}".format(nonce+2)
       block = (block_header + bin_nonce).encode('utf-8')
       hashed2 = hashlib.sha256(hashlib.sha256(block).digest()).hexdigest()
       bin_hash = bin(int(hashed2, 16))[2:].zfill(256)
       if (bin_hash + '1').index('1') >= difficulty:
           found = True
           nonce = nonce + 2
           break

       bin_nonce = "{0:b}".format(nonce+3)
       block = (block_header + bin_nonce).encode('utf-8')
       hashed2 = hashlib.sha256(hashlib.sha256(block).digest()).hexdigest()
       bin_hash = bin(int(hashed2, 16))[2:].zfill(256)
       if (bin_hash + '1').index('1') >= difficulty:
           found = True
           nonce = nonce + 3
           break

       bin_nonce = "{0:b}".format(nonce+4)
       block = (block_header + bin_nonce).encode('utf-8')
       hashed2 = hashlib.sha256(hashlib.sha256(block).digest()).hexdigest()
       bin_hash = bin(int(hashed2, 16))[2:].zfill(256)
       if (bin_hash + '1').index('1') >= difficulty:
           found = True
           nonce = nonce + 4
           break

       bin_nonce = "{0:b}".format(nonce+5)
       block = (block_header + bin_nonce).encode('utf-8')
       hashed2 = hashlib.sha256(hashlib.sha256(block).digest()).hexdigest()
       bin_hash = bin(int(hashed2, 16))[2:].zfill(256)
       if (bin_hash + '1').index('1') >= difficulty:
           found = True
           nonce = nonce + 5
           break

       bin_nonce = "{0:b}".format(nonce+6)
       block = (block_header + bin_nonce).encode('utf-8')
       hashed2 = hashlib.sha256(hashlib.sha256(block).digest()).hexdigest()
       bin_hash = bin(int(hashed2, 16))[2:].zfill(256)
       if (bin_hash + '1').index('1') >= difficulty:
           found = True
           nonce = nonce + 6
           break

       bin_nonce = "{0:b}".format(nonce+7)
       block = (block_header + bin_nonce).encode('utf-8')
       hashed2 = hashlib.sha256(hashlib.sha256(block).digest()).hexdigest()
       bin_hash = bin(int(hashed2, 16))[2:].zfill(256)
       if (bin_hash + '1').index('1') >= difficulty:
           found = True
           nonce = nonce + 7
           break

       nonce += 8

   end_time = default_timer()

   if found == False:
      pass
   else:
      sqs.send_message(QueueUrl=linkQ, MessageBody=("Golden nonce is: " + str(nonce) + " " + "Search time: " + " " + str(end_time-start_time)))

if __name__ == "__main__":
   main(sys.argv)
