import os
import errno
import requests
import datetime
import subprocess
import urllib3
from requests.auth import HTTPBasicAuth
from influxdb import InfluxDBClient


def check_dir_exists(path):
    try:
        return os.path.isdir(path)
    except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise


def check_file_exists(full_name):
    try:
        handler = open(full_name, 'r')
        handler.close()
        return True
    except (FileNotFoundError, Exception) as e:
        print('File ' + full_name + ' not found', e)
        return False


def mkdir_p(path):
    try:
        os.makedirs(path, exist_ok=True)
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise


def get_last_commit(branch, logger):
    logger.info('Trying to get last commit for branch')
    try:
        if branch['auth']['type'] == 'basic':
            r = requests.get(branch['url'], branch['params'], auth=HTTPBasicAuth(branch['auth']['login'], branch['auth']['password']))
        elif branch['auth']['type'] == 'token':
          #  params = branch['params']
           # params['since'] = str((datetime.datetime.now() - datetime.timedelta(hours=24)).isoformat())
            r = requests.get(branch['url'], branch['params'], headers=branch['headers'])

        data = r.json()

        if len(data) == 0:
            commit_id = 'No commits'
        else:
            if branch['vcs'] == 'bitbucket':
                commit_id = data['values'][0]['id']
            elif branch['vcs'] == 'gitlab':
                commit_id = data[0]['id']


    except (IndexError, KeyError) as e:
        logger.error('Results Error')
        logger.exception('message')
        return False
        quit(3)

    except (ConnectionRefusedError, requests.exceptions.ConnectionError) as e:
        logger.error('Connection Error ')
        logger.exception('message')
        return False
        quit(4)

    return commit_id


def gitPull(repoDir, repoUrl, logger):
    logger.info('Trying to pull from master repo')
    try:
        cmd = ['git', 'pull']
        p = subprocess.Popen(cmd, cwd=repoDir)
        p.wait()
    except Exception as e:
        logger.error('Exception')
        logger.error(repoDir)
        logger.exception('message')
        return False
        quit(3)
    logger.info('Pull successfull')
    return True


def gitCheckout(branch_name, repoDir, logger):
    logger.info('Trying to checkout branch')
    logger.info(branch_name)
    try:
        cmd = ['git', 'checkout', branch_name]
        p = subprocess.Popen(cmd, cwd=repoDir)
        p.wait()
    except FileNotFoundError as e:
        logger.error('Exception')
        logger.error(repoDir)
        logger.exception('message')
        quit(3)
    logger.info('Checkout successfull')
    return True


def gitPush(repoDir, logger):
    logger.info('Trying to push branch to slave repo')
    try:
        cmd = ['git', 'push', '--all']
        p = subprocess.Popen(cmd, cwd=repoDir)
        p.wait()
    except FileNotFoundError as e:
        logger.error('Exception')
        logger.error(repoDir)
        logger.exception('message')
        quit(3)
    logger.info('Push successfull')
    return True


def sync_branches(master, logger):
    logger.info('Trying to sync branches')
    try:
        gitPull(master['path'], master['repo'], logger)
        gitCheckout(master['branch'], master['path'], logger)
        gitPush(master['path'], logger)
    except FileNotFoundError as e:
        logger.error('Exception')
        logger.error(master['path'])
        logger.exception('message')
        quit(3)
    logger.info('Sync successfull')
    return True


def get_event(measurement, repo, sync_state):
    log_event = [{"measurement": measurement,
                    "tags": {
                        "repo": repo
                        },
                    "fields": {
                        "syncstate": sync_state
                    }
                    }]
    return log_event


def write_to_Influx(monitoring, state, logger):
    event = get_event(monitoring['measurement'], monitoring['repo_name'], state)
    try:
        client = InfluxDBClient(monitoring['dbhost'], monitoring['dbport'], monitoring['dbuser'], monitoring['dbpass'], monitoring['dbname'])
        try:
            client.write_points(event)
        except (requests.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as e:
            logger.error('Could net connect to InfluxDB server')
            return 'No Connect'
    except Exception as e:
        logger.error('something went wrong ', str(e))
