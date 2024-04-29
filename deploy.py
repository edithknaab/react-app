#import argparse and fabric to execute commands using python
import argparse
from fabric import Connection
#define function
def deploy_to_ec2(repo_url):
    # ec2 instance ip, username, and key path
    ec2_host = '3.19.202.148'
    ec2_username = 'ec2-user'
    #stored in desktop
    ec2_key_path = 'deploy.pem' 

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
	    #when succeffsul print this message, you shall not fail me!
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


#https://docs.fabfile.org/en/latest/api/connection.html
#https://stackoverflow.com/questions/27957373/python-import-and-initialize-argparse-after-if-name-main
#https://docs.python.org/3/library/argparse.html
#https://www.phusionpassenger.com/library/deploy/nginx/automating_app_updates/python/
    