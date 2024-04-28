import argparse
from fabric import Connection

def deploy_to_ec2(repo_url):
    ec2_host = '3.141.240.128'
    ec2_username = 'ec2-user'
    ec2_key_path = 'csc497.pem'  # Update with the correct path

    try:
        conn = Connection(host=ec2_host, user=ec2_username, connect_kwargs={'key_filename': ec2_key_path})

        with conn.cd('/home/ec2-user/react-app'):
            conn.run('git pull {}'.format(repo_url)) 
            conn.run('npm install')            
            conn.run('npm run build')          
            conn.sudo('pm2 restart react-app')

        print("Deployment completed successfully!")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy a React application to EC2.')
    parser.add_argument('repo_url', type=str, help='GitHub repository URL')

    args = parser.parse_args()

    deploy_to_ec2(args.repo_url)
