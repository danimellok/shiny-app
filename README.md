
Setup and Deployment Instructions for Shiny App on EC2

1. Set Up Your EC2 Environment
   - SSH into EC2: Connect to your EC2 instance.
     ssh -i "your-key.pem" ubuntu@your-ec2-public-ip

   - Activate Virtual Environment:
     source ~/myenv/bin/activate

2. Download Latest Code from GitHub
   - Navigate to the Project Directory:
     cd /srv/shiny-app

   - Pull the Latest Code:
     git pull origin main

3. Run the Shiny App
   - Start the App with nohup (to keep it running after you disconnect):
     nohup shiny run --host 0.0.0.0 --port 3838 test2.py &

   - Access the App: Open your browser and go to:
     http://your-ec2-public-ip:3838

4. Stopping the App
   - Find the Process ID (PID):
     ps aux | grep shiny

   - Stop the App:
     kill PID  # Replace PID with the actual process ID found in the previous step

Important Notes:
- Security Group: Make sure your EC2 security group allows inbound traffic on port 3838.
- File Updates: To update code, repeat Step 2 to pull the latest changes from GitHub.
- Start/Stop: Use nohup to start the app and kill with the PID to stop it.
