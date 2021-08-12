pipeline {
  agent any
  stages {
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