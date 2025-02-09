from application import db
from application.models import Base

from sqlalchemy.sql import text

class User(Base):
   __tablename__ = "account"

   name = db.Column(db.String(255), nullable=False)
   username = db.Column(db.String(255), nullable=False)
   password = db.Column(db.String(255), nullable=False)
   userrole = db.Column(db.String(80), nullable=False)

   posts = db.relationship("Post", backref='account', lazy=True)

   def __init__(self, name, username, password, userrole):
      self.name = name
      self.username = username
      self.password = password
      self.userrole = userrole
  
   def get_id(self):
      return self.id

   def is_active(self):
      return True

   def is_anonymous(self):
      return False

   def is_authenticated(self):
      return True

   def get_userrole(self):
      return self.userrole


   # Number of threads started by User(userId)
   @staticmethod
   def count_user_threads(userId):
      statement = text("SELECT COUNT(Post.id) FROM Account"
                  " LEFT JOIN Post ON Account.id = Post.account_id"
                  " WHERE Post.priority = 1 AND Account.id = :userId").params(userId=userId)
      res = db.engine.execute(statement)

      for row in res:
         response = row[0]
      return response


   # Number of posts send by User(userId)
   @staticmethod
   def count_user_posts(userId):
      statement = text("SELECT COUNT(Post.id) FROM Account"
                  " LEFT JOIN Post ON Account.id = Post.account_id"
                  " WHERE Account.id = :userId").params(userId=userId)
      res = db.engine.execute(statement)

      for row in res:
         response = row[0]
      return response


   # List of Post.id posted by User(userId)
   @staticmethod
   def user_post_ids(userId):
      statement = text("SELECT Post.id FROM Account"
                  " LEFT JOIN Post ON Account.id = Post.account_id"
                  " WHERE Account.id = :userId").params(userId=userId)
      res = db.engine.execute(statement)

      response = []
      for row in res:
         response.append(row[0])
      return response


   @staticmethod
   # Total number of accounts in database
   def total_users():
      statement = text("SELECT COUNT(*) FROM Account")
      res = db.engine.execute(statement)

      for row in res:
         response = row[0]
      return response


   # List account data where account.status USER or ADMIN
   @staticmethod
   def list_users_and_admins():
      statement = text("SELECT Account.id, Account.username, Account.userrole FROM Account"
                  " WHERE NOT Account.userrole='MASTER'"
                  " ORDER BY Account.userrole, Account.username")
      res = db.engine.execute(statement)

      response = []
      for row in res:
         response.append([row[0], row[1], row[2]])
      return response


   # List account data where account.status is USER
   @staticmethod
   def list_users():
      statement = text("SELECT Account.id, Account.username, Account.userrole FROM Account"
                  " WHERE NOT Account.userrole='MASTER' AND NOT Account.userrole='ADMIN'"
                  " ORDER BY Account.userrole, Account.username")
      res = db.engine.execute(statement)

      response = []
      for row in res:
         response.append([row[0], row[1], row[2]])
      return response





