import sys, time, os, math, getopt
import boto3, paramiko
from timeit import default_timer

tag = "comsm0010_CW"

def main(argv):

    runtime = 0
    confidence = 0
    numberofmachines = 4
    difficulty = 25
    block = "COMSM0010cloud"
    price = 0
    queue_state = 0 # 0 keep, 1 purge , 2 delete

    fullCmdArguments = sys.argv
    argumentList = fullCmdArguments[1:]

    unixOptions = "t:b:c:n:d:p:"
    gnuOptions = ["runtime=", "block=", "confidence=", "numberofmachines=", "difficulty=", "price="]

    try:
        arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
    except getopt.error as err:
        print (str(err))
        sys.exit(2)

    for currentArgument, currentValue in arguments:
        if currentArgument in ("-t", "--runtime"):
            runtime = int(currentValue)
        elif currentArgument in ("-b", "--block"):
            block = currentValue
        elif currentArgument in ("-c", "--confidence"):
            confidence = int(currentValue)
        elif currentArgument in ("-n", "--numberofmachines"):
            numberofmachines = int(currentValue)
        elif currentArgument in ("-d", "--difficulty"):
            difficulty = int(currentValue)
        elif currentArgument in ("-p", "--price"):
            price = int(currentValue)
        elif currentArgument in ("-q", "--queue"):
            queue_state = int(currentValue)

    print ("Runtime " + str(runtime) + ", confidence " + str(confidence) + ", numberofmachines " + str(numberofmachines) + ", difficulty " + str(difficulty) + ", block " + str(block) + ", price " + str(price))

    threshold_machines = 9
    if (price > 0):
        pricing = 0.0116
        numberofmachines = threshold_machines
        runtime = math.ceil(3600*price/(numberofmachines*pricing))
    elif (confidence >= 100):
        confidence = 100
    elif (confidence <= 0):
        confidence = 0
    elif (runtime > 0 & confidence >= 0):
        hashes = 230000
        seconds = 2 ** difficulty / hashes
        adj_sec = seconds * (confidence/100)
        if (adj_sec / runtime >= threshold_machines):
            numberofmachines = threshold_machines
            print("Due to recent issues with AWS Educate account, we must use a maximum number of machines of " + str(threshold_machines) + ".")
        else:
            base_time = 180 * 1.5
            numberofmachines = math.ceil(adj_sec + base_time ) / runtime
    elif (runtime > 0):
        numberofmachines = threshold_machines
    elif (numberofmachines >= threshold_machines):
        numberofmachines = threshold_machines
    elif (numberofmachines <= 1):
        numberofmachines = 1

    ec2Resource = boto3.resource('ec2')
    ec2Client   = boto3.client('ec2')
    sqs         = boto3.client('sqs')
    sqs.create_queue(QueueName="cloudQ")
    linkQ       = sqs.get_queue_url(QueueName="cloudQ")["QueueUrl"]

    print (linkQ)
    print (runtime, confidence, numberofmachines, difficulty, block, price)
    print("Waiting for instance deployment")

    ec2Resource.create_instances(ImageId='ami-???',
                         InstanceType='t2.micro',
                         KeyName='cloud',
                         MinCount=numberofmachines,
                         MaxCount=numberofmachines)
    filters = [
      {
        'Name': 'instance-state-name',
        'Values': ['pending', 'running']
      }
    ]
    instances = ec2Resource.instances.filter(Filters=filters)


    print("Expected wait time 210s.")
    counter = 0
    index = 0
    printed = False
    for instance in instances:
       instance.wait_until_running()
       done = False
       while True:
        statuss = ec2Client.describe_instance_status(InstanceIds=[instance.id])
        status = statuss['InstanceStatuses'][0]
        if status['InstanceStatus']['Status'] == 'ok' and status['SystemStatus']['Status'] == 'ok':
          if done == True:
            print("")
          break
        done = True
        index = index + 1
        time.sleep(10)
        if (210-index*10 > 0):
            print("Expected wait time " + str(210-index*10) + "s.")
        elif (printed == False):
            print("Oh no... We've exceeded the expected wait time. Sorry :(")
            printed = True
        counter = counter + 1

    print("Running code")
    index = 0
    for instance in instances:
      interval = pow(2, 32) / numberofmachines
      first = interval * (index)
      last  = interval * (index + 1)

      try:
        key = paramiko.RSAKey.from_private_key_file('cloud.pem')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=instance.public_dns_name, username='ec2-user', pkey=key)
        nonce = 'python3 nonce.py ' + str(int(first)) + ' ' + str(int(last)) + ' ' + str(difficulty)
        stdin, stdout, stderr = ssh.exec_command(nonce)
        stdin.flush()
      except Exception as e:
        print(e)

      index += 1

    start_time = default_timer()
    iteration = 0
    one_finish = False
    while (one_finish == False and iteration < 100):
        qResponse = sqs.receive_message(QueueUrl=linkQ, WaitTimeSeconds=10, MaxNumberOfMessages=10)
        if "Messages" in qResponse:
            for text in qResponse["Messages"]:
                print(text["Body"])
                rHandle = text["ReceiptHandle"]
                sqs.delete_message(QueueUrl=linkQ, ReceiptHandle=rHandle)
                one_finish = True
        iteration = iteration + 1
        if (runtime != 0 and confidence == 0):
            check_time = default_timer()
            if ((check_time - start_time) >= runtime):
                someone_finished = True

    if (runtime != 0 and confidence == 0):
        print("Program returned early. Out of time!")

    for instance in instances:
        ssh.close()

    if (1 == queue_state):
        sqs.purge_queue(QueueUrl=queueUrl)
    elif(2 == queue_state):
        sqs.delete_queue(QueueUrl=queueUrl)

    print("Shutting down " + str(numberofmachines) + " instances.")
    for instance in instances:
        print("Shutting down instance " + str(instance.id))
        instance.terminate()

if __name__ == "__main__":
  main(sys.argv)
