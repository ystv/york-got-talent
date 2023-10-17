@Library('ystv-jenkins')

def imageTag = ''
pipeline {
  agent {
    label 'docker'
  }

  environment {
    DOCKER_BUILDKIT = "1"
  }

  stages {
    stage('Prepare') {
      steps {
        ciSkip action: 'check'
        script {
          def imageNamePrefix = ''
          if (env.BRANCH_NAME != 'main') {
            imageNamePrefix = "${env.BRANCH_NAME}-"
          }
          imageTag = "${imageNamePrefix}${env.BUILD_NUMBER}"
        }
      }
    }
    stage('Build Images') {
      steps {
        sh """docker build \\
          -t registry.comp.ystv.co.uk/ystv/york-got-talent:${imageTag}\\
          .
        """
      }
    }

    stage('Push') {
      when {
        anyOf {
          branch 'main'
          tag 'v*'
        }
      }
      steps {
        withDockerRegistry(credentialsId: 'docker-registry', url: 'https://registry.comp.ystv.co.uk') {
          sh "docker push registry.comp.ystv.co.uk/ystv/york-got-talent:${imageTag}"
          script {
            if (env.BRANCH_NAME == 'main') {
              sh "docker tag registry.comp.ystv.co.uk/ystv/york-got-talent:${imageTag} registry.comp.ystv.co.uk/ystv/york-got-talent:latest"
              sh 'docker push registry.comp.ystv.co.uk/ystv/york-got-talent:latest'
            }
          }
        }
      }
    }

    stage('Deploy to development') {
      when {
        branch 'main'
      }
      steps {
        build job: 'Deploy Nomad Job', parameters: [
          string(name: 'JOB_FILE', value: 'york-got-talent-dev.nomad'),
          text(name: 'TAG_REPLACEMENTS', value: "registry.comp.ystv.co.uk/ystv/york-got-talent:${imageTag}")
        ]
      }
    }
  }

  post {
    always {
      ciSkip action: 'postProcess'
      cleanWs()
    }
  }
}
