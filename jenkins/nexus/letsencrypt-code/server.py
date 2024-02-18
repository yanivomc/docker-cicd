import subprocess
# import schedule
import time

# Configuration variables
domain = "satixfy-repo.devopshift.com"
email = "yanivomc@gmail.com.com"
certbot_path = "/usr/bin/certbot"  # Adjust if Certbot is located elsewhere
nginx_path = "/usr/sbin/nginx"  # Adjust if NGINX is located elsewhere

def run_certbot():
    # Check if the certificate already exists
    cert_path = f"/etc/letsencrypt/live/{domain}/fullchain.pem"
    try:
        # If the certificate file exists, renew instead of creating a new one
        open(cert_path)
        certbot_command = [certbot_path, "renew"]
    except FileNotFoundError:
        # If the certificate file does not exist, create a new one
        certbot_command = [
            "sudo", certbot_path, "certonly", "--nginx",
            "--non-interactive", "--agree-tos",
            "--email", email, "-d", domain
        ]

    # Run the Certbot command
    subprocess.run(certbot_command, check=True)

def restart_nginx():
    # Restart NGINX to apply the new certificates
    subprocess.run([nginx_path, "-s", "reload"], check=True)

def schedule_renewal():
    # Schedule the certificate renewal every 60 days
    schedule.every(60).days.do(run_certbot)
    schedule.every(60).days.do(restart_nginx)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Run Certbot immediately to either obtain or renew the certificate
    run_certbot()
    
    # Then restart NGINX to apply the certificate
    # restart_nginx()
    
    # # Start the scheduled job
    # schedule_renewal()
