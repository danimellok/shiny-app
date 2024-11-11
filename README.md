# Setup and Deployment Instructions for Shiny App on EC2

### 1. Connect to Your EC2 Instance

1. **SSH into EC2**: Connect to your EC2 instance.
   ```
   ssh -i "shiny-key.pem" ubuntu@18.191.114.220
   ```

2. **Navigate to Project Directory**:
   ```
   cd /srv/shiny-app
   ```

### 2. Activate the Virtual Environment

1. **Activate Virtual Environment**:
   ```
   source ~/myenv/bin/activate
   ```

### 3. Run the Shiny App

1. **Run the App in Foreground** (will stop when you close the terminal):
   ```
   shiny run --host 0.0.0.0 --port 3838 test2.py
   ```

2. **Run the App in Background with `nohup`** (keeps running after you disconnect):
   ```
   nohup shiny run --host 0.0.0.0 --port 3838 test2.py &
   ```

3. **Access the App**: Open your browser and go to:
   ```
   http://18.191.114.220:3838
   ```

4. Stopping the App
   - Find the Process ID (PID):
     ps aux | grep shiny

   - Stop the App:
     kill PID  # Replace PID with the actual process ID found in the previous step

### Important Notes:
- **Security Group**: Ensure your EC2 security group allows inbound traffic on port `3838`.
- **Updating Code**: To pull updates from GitHub, repeat Steps 1-3 with `git pull origin main`.
- **Stopping the App**: Use `ps aux | grep shiny` to find the process ID and `kill PID` to stop the app.### Important Notes:
- **Security Group**: Ensure your EC2 security group allows inbound traffic on port `3838`.
- **Updating Code**: To pull updates from GitHub, repeat Steps 1-3 with `git pull origin main`.
- **Stopping the App**: Use `ps aux | grep shiny` to find the process ID and `kill PID` to stop the app.
