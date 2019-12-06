# Cloud Nonce Discovery (CND) deployment in AWS
 
 ## Deployment Process
1. Download user credentials from Educate and configure in .aws/ folder via CLI (~/.aws/credentials for keys and ~/.aws/config for region)
2. Create Key Pair (In code it's named "cloud")
3. Create Custom AMI Image:
	* Launch new EC2 instance (Linux2 AMI x86)
	* SSH into machine ssh -i "cloud.pem" ec2user@ec2-3-81-141-139.compute-1.amazonaws.com
	* Run sudo yum install python3.x86_64 (see sudo yum list | grep python3 for all py3 versions)
	* Run pip3 install boto3 awscli --user
	* in case pip is not installed, run curl -O https://bootstrap.pypa.io/get-pip.py and then python3 get-pip.py --user
	* validate install (python3 --version; pip3 --version)
	* exit VM
	* scp nonce.py and .aws folder on machine (scp -r -i "cloud.pem" ./.aws ec2-user@ec2-3-81-141-139.compute-1.amazonaws.com:~)
	* In AWS web, click on instance -> Image -> Create New Image
	* Use new custom AMI in script.py file when launching new instances
4. Run script.py:
	* gnuOptions = ["runtime=", "block=", "confidence=", "numberofmachines=", "difficulty=", "price="]
	* e.g python3 script.py -n 4 -d 25
5. Run stop.py in order to stop all instances in a clean fashion (if needed as an extension)
