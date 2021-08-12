pipeline {
  agent {
        docker { image 'node:14-alpine' }
    }ny
  stages {

    stage('initial test'){
      steps {
                sh 'node --version'
            }
    }
    stage('Build') {
      parallel {
        stage('Build') {
          steps {
            echo 'stage build'
          }
        }

        stage('send telegram') {
          steps {
            telegramSend(chatId: 1230975396, message: 'jenkins build')
          }
        }

      }
    }

    stage('print time') {
      steps {
        timestamps() {
          echo 'timestamp test'
        }

      }
    }

  }
}