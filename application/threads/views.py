from flask import redirect, render_template, request, url_for

from application import app, db
from application.threads.models import Thread
from application.threads.forms import ThreadForm


# List All Threads
@app.route("/threads", methods=["GET"])
def threads_index():
   threadList = Thread.query.all()

   return render_template("threads/list.html", form=ThreadForm(), threadList=threadList)



# Create New Thread
@app.route("/threads/new", methods=["GET", "POST"])
def threads_create():
   if request.method == "GET":
      return render_template("threads/new.html", form=ThreadForm())

   form = ThreadForm(request.form)
   if not form.validate():
      return render_template("threads/new.html", form=form)

   dbThread = Thread(form.topic.data)
   db.session().add(dbThread)
   db.session().commit()

   return redirect(url_for("threads_index"))



# Update Thread Topic
@app.route("/threads/update/<threadId>", methods=["GET", "POST"])
def threads_update(threadId):
   oldTopic = Thread.query.get(threadId).topic

   if request.method == "GET":
      return render_template("threads/update.html", form=ThreadForm(), threadId=threadId, oldTopic=oldTopic)

   form = ThreadForm(request.form)
   if not form.validate():
      return render_template("threads/update.html", form=form, threadId=threadId, oldTopic=oldTopic)

   dbThread = Thread.query.get(threadId)
   dbThread.topic = form.topic.data
   db.session().commit()

   return redirect(url_for("threads_index"))


 
# Remove Thread
@app.route("/threads/remove/<threadId>", methods=["POST"])
def threads_remove(threadId):

   dbThread = Thread.query.get(threadId)
   db.session().delete(dbThread)
   db.session().commit()

   return redirect(url_for("threads_index"))





