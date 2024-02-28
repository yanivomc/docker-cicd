# docker-bake.hcl
group "default" {
  targets = ["ImageProcessing", "SecurityBase","ServicesSchedulerLib","SharedTypes","TypeExtensions","SSOlogon"]
}

variable "NEXUS_API_KEY" {
  default = "20a4b826-31aa-3ab7-a0b1-cb3fd9fbfa7e"
}

target "ImageProcessing" {
  context = "./src/ImageProcessing"
  dockerfile = "dockerfile"
  tags = ["eldan/image-processing:latest"]
  args = {
    NEXUS_API_KEY = "${NEXUS_API_KEY}"
  }
  // platforms = ["linux/amd64", "linux/arm64"]
}

target "SecurityBase" {
  context = "./src/SecurityBase"
  dockerfile = "dockerfile"

  // inherits = ["webapp-dev"]
  // platforms = ["linux/amd64", "linux/arm64"]
  tags = ["eldan/security-base:latest"]
  args = {
    NEXUS_API_KEY = "${NEXUS_API_KEY}"
  }
}

target "ServicesSchedulerLib" {
  context = "./src/ServicesSchedulerLib"
  dockerfile = "dockerfile"
  tags = ["eldan/services-scheduler-lib:latest"]
  args = {
    NEXUS_API_KEY = "${NEXUS_API_KEY}"
  }
}

target "SharedTypes" {
  context = "./src/SharedTypes"
  dockerfile = "dockerfile"
  tags = ["eldan/shared-types:latest"]
  args = {
    NEXUS_API_KEY = "${NEXUS_API_KEY}"
  }
  
}

target "TypeExtensions" {
  context = "./src/TypeExtensions"
  dockerfile = "dockerfile"
  tags = ["eldan/type-extensions:latest"]
  args = {
    NEXUS_API_KEY = "${NEXUS_API_KEY}"
  }
}

target "SSOlogon" {
  context = "./src/SSOlogon"
  dockerfile = "dockerfile"
  tags= ["eldan/sso-logon:latest"]
  args = {
    NEXUS_API_KEY = "${NEXUS_API_KEY}"
  }
}