#!/usr/bin/env python3

import sys
from datetime import datetime
import re
import logging
import gitlab
import configargparse
import pandas as pd
from pandas_schema.validation import CustomElementValidation
import pandas_schema
from pandas_schema import Column
import numpy as np



pd.set_option('display.max_colwidth', 120)


def check_boolean(boolean):

    if isinstance(boolean, bool):
        return True
    return False


def check_key(key):

    if re.match("^[A-Za-z0-9_-]*$", key):
        return True
    return False


def check_variable_type(variable_type):

    if variable_type in {'env_var', 'file'}:
        return True
    return False


def data_validation(data):

    # define validation elements
    key_validation = [CustomElementValidation(lambda k: check_key(k), 'is not valid key - only letters, digits and _')]
    bool_validation = [CustomElementValidation(lambda b: check_boolean(b), 'is not boolean')]
    null_validation = [CustomElementValidation(lambda d: d is not np.nan, 'this field cannot be null')]
    variable_type_validation = [CustomElementValidation(lambda t: check_variable_type(t), 'is not valid variable_type')]


    # variable_type,key,value,protected,masked
    # define validation schema
    schema = pandas_schema.Schema([
        Column('variable_type', variable_type_validation + null_validation),
        Column('key', key_validation + null_validation),
        Column('value', null_validation),
        Column('protected', bool_validation + null_validation),
        Column('masked', bool_validation + null_validation)])

    # apply validation
    errors = schema.validate(data)
    errors_index_rows = [e.row for e in errors]

    if not errors_index_rows:
        return True
    else:
        logging.error(pd.DataFrame({'errors':errors}))
        return False


def gitlab_env_to_csv(element, file_path):

    # ENV variables to list
    test = []
    for env in element.variables.list(as_list=False):
        test.append([env.variable_type, env.key, env.value, env.protected, env.masked])

    # ENV variables to csv file
    df = pd.DataFrame(test, columns=['variable_type', 'key', 'value', 'protected', 'masked'])
    logging.info(df)
    df.to_csv(file_path, index=False)


def csv_to_gitlab_env(element, file_path='dict.csv'):

    # Parse csv file
    df = pd.read_csv(file_path, index_col=False)

    # validate csv file
    if data_validation(df):
        logging.info("Data validation passed.")
    else:
        logging.error("Data validation failed. Please check csv file.")
        sys.exit(123)


    # Backup current ENV variables
    repo_name = element.name
    repo_id = element.id
    timestamp = datetime.today().strftime('%Y%m%d%H%M%S')
    backup_file = "backup-%s-%s-%s" % (repo_name, repo_id, timestamp)
    gitlab_env_to_csv(element, backup_file)

    # Delete all ENV variables in group/project
    for env in element.variables.list(as_list=False):
        element.variables.delete(env.key)

    # Create ENV variables
    for row in df.itertuples(index=True):
        variable = {'variable_type': row.variable_type, 'key': row.key, 'value': row.value,
                    'protected': row.protected, 'masked': row.masked}

        element.variables.create(variable)


def main():
    p = configargparse.ArgParser(default_config_files=['config.ini'])
    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    p.add('-l', '--gitlab_url', required=True,
          help='Gitlab url')
    p.add('-t', '--gitlab_token', required=True,
          help='Gitlab token')
    element = p.add_mutually_exclusive_group(required=True)
    element.add_argument('-g', '--group', action='store_true', help='Edit group ENV')
    element.add_argument('-p', '--project', action='store_true', help='Edit project ENV')
    p.add('-i', '--element_id', type=int, required=True,
          help='Gitab project/group id')
    p.add('-f', '--file_path', required=False, default='data_env.csv')
    method = p.add_mutually_exclusive_group(required=True)
    method.add_argument('-d', '--download', action='store_true', help='Download gitlab ENV to csv')
    method.add_argument('-u', '--upload', action='store_true', help='Upload csv to gitlab ENV')

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
