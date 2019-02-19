pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'build instagram'
      }
    }
    stage('Test') {
      parallel {
        stage('Test') {
          steps {
            echo 'test page'
          }
        }
        stage('test_down') {
          steps {
            echo 'test download function'
          }
        }
        stage('test_request') {
          steps {
            echo 'test request function'
          }
        }
        stage('test_paralle') {
          steps {
            echo 'test paraller'
          }
        }
      }
    }
    stage('deploy') {
      parallel {
        stage('deploy') {
          steps {
            echo 'deploy stage'
          }
        }
        stage('deploy_log') {
          steps {
            echo 'deploy log'
          }
        }
      }
    }
    stage('post') {
      steps {
        sleep 20
      }
    }
  }
}