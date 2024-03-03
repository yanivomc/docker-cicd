# docker-bake.hcl
group "default" {
  targets = ["ImageProcessing", "SecurityBase","ServicesSchedulerLib","SharedTypes","TypeExtensions","SSOlogon","QR","FireflyBox"]
}



variable "NEXUS_API_KEY" {
  default = "20a4b826-31aa-3ab7-a0b1-cb3fd9fbfa7e"
}
variable "BUILD_NUMBER" {
  default = "1.0.0"
}

target "ImageProcessing" {
  context = "./src/ImageProcessing"
  dockerfile = "dockerfile"
  tags = ["eldan/image-processing:latest"]
  args = {
    NEXUS_API_KEY = "${NEXUS_API_KEY}",
    BUILD_NUMBER = "${BUILD_NUMBER}"
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
    NEXUS_API_KEY = "${NEXUS_API_KEY}",
    BUILD_NUMBER = "${BUILD_NUMBER}"
  }
}

target "ServicesSchedulerLib" {
  context = "./src/ServicesSchedulerLib"
  dockerfile = "dockerfile"
  tags = ["eldan/services-scheduler-lib:latest"]
  args = {
    NEXUS_API_KEY = "${NEXUS_API_KEY}",
    BUILD_NUMBER = "${BUILD_NUMBER}"
  }

}

target "SharedTypes" {
  context = "./src/SharedTypes"
  dockerfile = "dockerfile"
  tags = ["eldan/shared-types:latest"]
  args = {
    NEXUS_API_KEY = "${NEXUS_API_KEY}",
    BUILD_NUMBER = "${BUILD_NUMBER}"
  }
  
}

target "TypeExtensions" {
  context = "./src/TypeExtensions"
  dockerfile = "dockerfile"
  tags = ["eldan/type-extensions:latest"]
  args = {
    NEXUS_API_KEY = "${NEXUS_API_KEY}",
    BUILD_NUMBER = "${BUILD_NUMBER}"
  }
}

target "SSOlogon" {
  context = "./src/SSOlogon"
  dockerfile = "dockerfile"
  tags= ["eldan/sso-logon:latest"]
  args = {
    NEXUS_API_KEY = "${NEXUS_API_KEY}",
    BUILD_NUMBER = "${BUILD_NUMBER}"
  }
  
}

target "QR" {
  context = "./src/QR"
  dockerfile = "dockerfile"
  tags= ["eldan/qr:latest"]
  args = {
    NEXUS_API_KEY = "${NEXUS_API_KEY}",
    BUILD_NUMBER = "${BUILD_NUMBER}"
  }
  
}

target "FireflyBox" {
  context = "./src/FireflyBox"
  dockerfile = "dockerfile"
  tags= ["eldan/qr:latest"]
  args = {
    NEXUS_API_KEY = "${NEXUS_API_KEY}",
    BUILD_NUMBER = "${BUILD_NUMBER}"
  }
  
}