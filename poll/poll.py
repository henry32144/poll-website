import os
import uuid
import hashlib
from poll.models import db
from poll.models import Poll, Answer, Vote
from flask import Flask, render_template, request, Blueprint, escape, abort, redirect, url_for

bp = Blueprint("poll", __name__)

def generate_access_key():
    random_value = os.urandom(16)
    md5 = hashlib.md5()
    md5.update(random_value)
    return md5.hexdigest()

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/result/<uuid>")
def result(uuid):
    # Do basic analytics
    return render_template("result.html")

@bp.route("/share/<uuid>")
def share(uuid):
    obj = Poll.query.filter_by(uuid=uuid).first()

    if obj is None:
        abort(404)
    
    variables = {
        "share_link": "http://127.0.0.1:5000/poll/{}".format(obj.uuid),
    }

    return render_template("share.html", **variables)

@bp.route("/vote", methods=["POST"])
def vote():
    print(request.form)
    user_id = request.form["uuid"]
    poll_id = request.form["pollId"]
    voted_answers_id = request.form.getlist("answer")
    print(voted_answers_id)
    # Sanity check
    if user_id is None or voted_answers_id is None or poll_id is None:
        abort(422)     
    if len(user_id) < 1 or len(voted_answers_id) < 1:
        abort(422)

    # Answer should exist
    Vote.query.filter_by(poll_id=poll_id).delete()
    
    # Get Poll UUID
    poll = Poll.query.filter_by(id=poll_id).first()

    voted_answers = []
    for ans_id in voted_answers_id:
        voted_answers.append(Vote(voter=user_id,
                                 answer_id=ans_id,
                                 poll_id=poll_id
        ))

    db.session.add_all(voted_answers)
    db.session.commit()

    return render_template("after_vote.html", result_link="http://127.0.0.1:5000/result/{}".format(poll.uuid))


# TODO: 1. Add a "/poll" route to handle POST request from the web page.
# 
# Hint: Variables you should return in render_template:
#       template_name_or_list (str): "index.html"
#       number (int): the user previous input, just for fill in the input box.
#       luckyPerson (int): the picked number produced by random_pick function.

@bp.route("/poll", methods=["GET", "POST"])  
@bp.route("/poll/<uuid>", methods=["GET", "POST"])
def poll(uuid=None):
    if request.method == "POST":
        question = escape(request.form["questionTitle"])
        answers = request.form.getlist("answer")
        max_selection_limit = request.form.get("maxSelectionLimit", 1)
        access_key = generate_access_key()

        # Sanity check
        if question is None or answers is None:
            abort(422)
        try:
            max_selection_limit = int(max_selection_limit)
        except Exception as e:
            print(str(e))
            abort(422)
        if len(question) < 1 or len(answers) < 1 or max_selection_limit < 1 or max_selection_limit > len(answers):
            abort(422)
        
        answer_objects = [Answer(text=escape(ans)) for ans in answers]

        new_poll = Poll(question=question,
                        access_key=access_key,
                        max_selection_limit=max_selection_limit,
                        answers=answer_objects
        )

        db.session.add(new_poll)
        db.session.commit()

        new_uuid = new_poll.uuid

        return redirect(url_for("poll.share", uuid=new_uuid))
    
    elif request.method == "GET":
        # User has voted before, help him/her check the answers.
        user_uuid = request.cookies.get('uuid')
        voted_answers = None

        poll = Poll.query.filter_by(uuid=uuid).first()

        if poll is None:
            abort(404)

        answers = [ans.to_json() for ans in poll.answers]

        if user_uuid is not None:
            voted_answers_obj_list = Vote.query.filter_by(voter=user_uuid, poll_id=poll.id).all()
            voted_answers = {}
            for obj in voted_answers_obj_list:
                voted_answers[obj.answer_id] = True

        # Add checked in answers
        for ans in answers:
            if user_uuid is not None and ans["id"] in voted_answers:
                ans["checked"] = True
            else:
                ans["checked"] = False

        
        variables = {
            "question": poll.question,
            "max_limit": poll.max_selection_limit,
            "answers": answers,
            "voted_answers": voted_answers,
            "poll_id": poll.id,
            "result_link": "http://127.0.0.1:5000/result/{}".format(poll.uuid)
        }
        print(variables)
        return render_template("poll.html", **variables)