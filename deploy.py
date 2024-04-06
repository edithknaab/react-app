import argparse
from fabric import Connection, Config

def deploy_to_ec2(repo_url):
    # EC2 instance details
    ec2_host = '3.141.240.128'
    ec2_username = 'ec2-user'
    ec2_key_path = 'csc497.pem'  # Update the path to the PEM file

    try:
        # Connect to EC2 instance
        conn = Connection(host=ec2_host, user=ec2_username, connect_kwargs={'key_filename': ec2_key_path})

        # Commands to execute on EC2 instance
        with conn.cd('/home/ec2-user/react-app'):
            conn.run('git pull {}'.format(repo_url))  # Pull latest changes from your Git repository
            conn.run('npm install')             # Install any new dependencies
            conn.run('npm run build')           # Build your React application
            conn.sudo('pm2 restart react-app')

        print("Deployment completed successfully!")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy a React application to EC2.')
    parser.add_argument('repo_url', type=str, help='GitHub repository URL')

    args = parser.parse_args()

    # Trigger deployment
    deploy_to_ec2(args.repo_url)

