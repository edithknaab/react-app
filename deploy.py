#import argparse and fabric to execute commands using python
import argparse
from fabric import Connection, Config
#define function
def deploy_to_ec2(repo_url):
    # ec2 instance ip, username, and key path
    ec2_host = '3.141.240.128'
    ec2_username = 'ec2-user'
    #stored in desktop
    ec2_key_path = 'csc497.pem' 

    try:
        # connect to the ec2 instance
        conn = Connection(host=ec2_host, user=ec2_username, connect_kwargs={'key_filename': ec2_key_path})

        # commands used to execute ec2 instance connections
        with conn.cd('/home/ec2-user/react-app'):
	    #pull recent commits from github
            conn.run('git pull {}'.format(repo_url)) 
	    # npm install
            conn.run('npm install')            
            # build an optimized version of the app
            conn.run('npm run build')          
            # run the applicatino using pm2
            conn.sudo('pm2 restart react-app')
	#if succeffsul print this message
        print("Deployment completed successfully!")

    except Exception as e:
        print("Error:", e)
#initilize argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy a React application to EC2.')
    parser.add_argument('repo_url', type=str, help='GitHub repository URL')

    args = parser.parse_args()

    # Trigger deployment funciotn
    deploy_to_ec2(args.repo_url)

