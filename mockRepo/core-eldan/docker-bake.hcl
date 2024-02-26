# docker-bake.hcl
group "default" {
  targets = ["ImageProcessing", "SecurityBase","ServicesSchedulerLib","SharedTypes","TypeExtensions","SSOlogon"]
}

target "ImageProcessing" {
  context = "./src/ImageProcessing"
  dockerfile = "dockerfile"
  tags = ["eldan/image-processing:latest"]
  // platforms = ["linux/amd64", "linux/arm64"]
}

target "SecurityBase" {
  context = "./src/SecurityBase"
  dockerfile = "dockerfile"

  // inherits = ["webapp-dev"]
  // platforms = ["linux/amd64", "linux/arm64"]
  tags = ["eldan/security-base:latest"]
}

target "ServicesSchedulerLib" {
  context = "./src/ServicesSchedulerLib"
  dockerfile = "dockerfile"
  tags = ["eldan/services-scheduler-lib:latest"]
}

target "SharedTypes" {
  context = "./src/SharedTypes"
  dockerfile = "dockerfile"
  tags = ["eldan/shared-types:latest"]
  
}

target "TypeExtensions" {
  context = "./src/TypeExtensions"
  dockerfile = "dockerfile"
  tags = ["eldan/type-extensions:latest"]
}

target "SSOlogon" {
  context = "./src/SSOlogon"
  dockerfile = "dockerfile"
  tags= ["eldan/sso-logon:latest"]
}