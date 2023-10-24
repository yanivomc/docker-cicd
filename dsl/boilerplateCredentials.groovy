import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.domains.*
import com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl
// Echo the parameters passed from the parameterized seed job
def username = 'test'
def password = 'test'
def credsId = 'git-credentials-id'
def description = 'GitLab Username and Password'


// Check if credentials already exist
def existingCreds = null
CredentialsStore store = Jenkins.instance.getExtensionList('com.cloudbees.plugins.credentials.SystemCredentialsProvider')[0].getStore()
existingCreds = store?.getCredentials(Domain.global())?.find { it.id == credsId }

if (existingCreds) {
    println("Credentials with ID ${credsId} already exist.")
    if(params.FORCE_UPDATE) {  // FORCE_UPDATE is another parameter you could set in the seed job
        println("Force updating the existing credentials.")
        existingCreds.username = username
        existingCreds.password = hudson.util.Secret.fromString(password)
        store.updateCredentials(Domain.global(), existingCreds, existingCreds)
    }
} else {
    println("Creating new credentials with ID ${credsId}.")
    def newCreds = new UsernamePasswordCredentialsImpl(
        CredentialsScope.GLOBAL,
        credsId,
        description,
        username,
        password
    )
    store.addCredentials(Domain.global(), newCreds)
}

