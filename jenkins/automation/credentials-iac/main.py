from jenkinsapi.jenkins import Jenkins

def create_credentials_in_jenkins(jenkins_url, username, password, cred_id, cred_desc, cred_user, cred_pass):
    jenkins = Jenkins(jenkins_url, username=username, password=password)
    cred_dict = {
        'description': cred_desc,
        'userName': cred_user,
        'password': cred_pass,
        'stapler-class': 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
        '$class': 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
        'scope': 'GLOBAL'
    }
    jenkins.requester.post_and_confirm_status(
        f"{jenkins.baseurl}/credentials/store/system/domain/_/createCredentials",
        json=cred_dict,
        params={
            'json': {
                '': '0',
                'credentials': cred_dict
            }
        }
    )

if __name__ == '__main__':
    JENKINS_URL = "http://your_jenkins_server.com"
    JENKINS_USER = "admin_user"
    JENKINS_PASS = "admin_pass"
    CREDENTIAL_ID = "git-credentials-id"
    CREDENTIAL_DESCRIPTION = "GitLab Username and Password"
    CREDENTIAL_USERNAME = "git_user"
    CREDENTIAL_PASSWORD = "git_pass"

    create_credentials_in_jenkins(
        JENKINS_URL,
        JENKINS_USER,
        JENKINS_PASS,
        CREDENTIAL_ID,
        CREDENTIAL_DESCRIPTION,
        CREDENTIAL_USERNAME,
        CREDENTIAL_PASSWORD
    )
