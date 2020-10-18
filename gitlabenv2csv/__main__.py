#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
gitlabenv2csv GitLab ENV downloader/uploader.
"""

import sys
from datetime import datetime
import re
import os
import logging
import gitlab
import configargparse
import pandas as pd
from pandas_schema.validation import CustomElementValidation
import pandas_schema
from pandas_schema import Column
import numpy as np

logging.getLogger().setLevel(logging.INFO)
pd.set_option('display.max_colwidth', 120)


def check_boolean(boolean):
    """return True if boolean"""

    if isinstance(boolean, bool):
        return True
    return False


def check_key(key):
    """return True if ENV key is valid"""

    if re.match("^[A-Za-z0-9_-]*$", key):
        return True
    return False


def check_variable_type(variable_type):
    """return True if GitLab variable_type is valid"""

    if variable_type in {'env_var', 'file'}:
        return True
    return False


def check_environment_scope(environment_scope, environment_scopes):
    """check if evironment_scope exists"""

    if environment_scope in environment_scopes or environment_scope == '*':
        return True
    return False


def data_validation(data, element):
    """return True if csv data to upload id valid"""

    environment_scopes = []
    for e_scope in element.environments.list():
        environment_scopes.append(e_scope.slug)

    # define validation elements
    key_validation = [CustomElementValidation(
        lambda k: check_key(k), 'is not valid key - only letters, digits and _'
        )]
    bool_validation = [CustomElementValidation(
        lambda b: check_boolean(b), 'is not boolean'
        )]
    null_validation = [CustomElementValidation(
        lambda d: d is not np.nan, 'this field cannot be null'
        )]
    variable_type_validation = [CustomElementValidation(
        lambda t: check_variable_type(t), 'is not valid variable_type'
        )]
    environment_scope_validation = [CustomElementValidation(
        lambda e: check_environment_scope(e, environment_scopes), 'is not valid environment_scope'
        )]


    # variable_type,key,value,protected,masked
    # define validation schema
    schema = pandas_schema.Schema([
        Column('variable_type', variable_type_validation + null_validation),
        Column('key', key_validation + null_validation),
        Column('value', null_validation),
        Column('protected', bool_validation + null_validation),
        Column('masked', bool_validation + null_validation),
        Column('environment_scope', null_validation + environment_scope_validation)])

    # apply validation
    errors = schema.validate(data)
    errors_index_rows = [e.row for e in errors]

    if errors_index_rows:
        logging.error(pd.DataFrame({'errors':errors}))
        return False

    logging.info("CSV validation passed.")
    return True


def gitlab_env_to_csv(element, file_path):
    """download all env from projekt gitlab to csv file"""

    # ENV variables to list
    test = []
    for env in element.variables.list(as_list=False):
        test.append([env.variable_type, env.key, env.value, env.protected,
                     env.masked, env.environment_scope])

    # ENV variables to csv file
    df = pd.DataFrame(test, columns=['variable_type', 'key', 'value', 'protected',
                                     'masked', 'environment_scope'])
    logging.info(df)
    df.to_csv(file_path, index=False)


def csv_to_gitlab_env(element, file_path, backup_path='backups'):
    """upload csv file with env data to Gitlab project/group"""

    # Parse csv file
    df = pd.read_csv(file_path, index_col=False)

    # validate csv file
    if data_validation(df, element):
        logging.info("Data validation passed.")
    else:
        logging.error("Data validation failed. Please check csv file.")
        sys.exit(123)

    # Backup current ENV variables
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    repo_name = element.name
    repo_id = element.id
    timestamp = datetime.today().strftime('%Y%m%d%H%M%S')
    backup_file = "%s/backup-%s-%s-%s.csv" % (backup_path, repo_name, repo_id, timestamp)
    gitlab_env_to_csv(element, backup_file)


    # Delete all ENV variables in group/project
    variables = element.variables.list(all=True)
    for env in variables:
        logging.info("Deleting variable: %s", env.key)
        element.variables.delete(env.key)

    # Create ENV variables
    for row in df.itertuples(index=True):
        variable = {'variable_type': row.variable_type, 'key': row.key, 'value': row.value,
                    'protected': row.protected, 'masked': row.masked,
                    'environment_scope': row.environment_scope}
        logging.info("Creating variable: %s", variable.values())
        element.variables.create(variable)


def main():
    """gitlabenv2csv parse config"""
    p = configargparse.ArgParser(default_config_files=['config.ini'])
    p.add('-c', '--my-config', required=False, is_config_file=True,
          help='config file path')
    p.add('-l', '--gitlab_url', required=True,
          help='Gitlab url')
    p.add('-t', '--gitlab_token', required=True,
          help='Gitlab token')
    element = p.add_mutually_exclusive_group(required=True)
    element.add_argument('-g', '--group', action='store_true',
                         help='Edit group ENV')
    element.add_argument('-p', '--project', action='store_true',
                         help='Edit project ENV')
    p.add('-i', '--element_id', type=int, required=True,
          help='Gitab project/group id')
    p.add('-f', '--file_path', required=False, default='data_env.csv',
          help='path to csv file')
    method = p.add_mutually_exclusive_group(required=True)
    method.add_argument('-d', '--download', action='store_true',
                        help='Download gitlab ENV to csv')
    method.add_argument('-u', '--upload', action='store_true',
                        help='Upload csv to gitlab ENV')

    options = p.parse_args()

    gl = gitlab.Gitlab(options.gitlab_url, private_token=options.gitlab_token, api_version=4)
    gl.auth()

    if options.group:
        element = gl.groups.get(options.element_id)
    if options.project:
        element = gl.projects.get(options.element_id)

    if options.download:
        gitlab_env_to_csv(element, options.file_path)
    if options.upload:
        csv_to_gitlab_env(element, options.file_path)


if __name__ == "__main__":
    sys.exit(main())
