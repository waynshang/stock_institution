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

        stage('send email') {
          steps {
            emailext(to: 'wayne18308@gmail.com', subject: 'jenkins test', body: 'this is the result', attachLog: true, from: 'wayne18308@gmail.com')
          }
        }

      }
    }

    stage('print time') {
      steps {
        timestamps()
      }
    }

  }
}