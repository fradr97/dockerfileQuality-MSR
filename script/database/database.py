import mysql.connector
from script.config.constants import *


database = mysql.connector.connect(
  host=HOST,
  user=USER_DB,
  password=PASSWORD_DB,
  database=DATABASE
)


def insert_repositories_data(name, github_url, n_stars, dockerfile_instructions, n_contributors):
  cursor = database.cursor()

  sql = 'INSERT INTO repositories (name, github_url, n_stars, dockerfile_instructions, n_contributors) VALUES (%s, %s, %s, %s, %s)'
  values = (name, github_url, n_stars, dockerfile_instructions, n_contributors)
  cursor.execute(sql, values)
  database.commit()
  return cursor.getlastrowid()


def insert_languages(language_name, id_repository, percentage):
  cursor = database.cursor()
  
  sql = 'INSERT INTO languages (name, id_repository, percentage) VALUES (%s, %s, %s)'
  values = (language_name, id_repository, percentage)
  cursor.execute(sql, values)
  database.commit()


def insert_smells(category, description, type, repository_id):
  cursor = database.cursor()

  sql = 'INSERT INTO smells (category, description, type, repository_id) VALUES (%s, %s, %s, %s)'
  values = (category, description, type, repository_id)
  cursor.execute(sql, values)
  database.commit()
