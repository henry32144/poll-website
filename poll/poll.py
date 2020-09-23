import os
import uuid
import hashlib
from poll.models import db
from poll.models import Poll, Answer, Vote
from sqlalchemy import func
from flask import Flask, render_template, request, Blueprint, escape, abort, redirect, url_for, jsonify

bp = Blueprint("poll", __name__)

def generate_access_key():
    """
        Generate access key for modifications, this feature is not inplemented yet
    """
    random_value = os.urandom(16)
    md5 = hashlib.md5()
    md5.update(random_value)
    return md5.hexdigest()

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/result", methods=["POST"])  
@bp.route("/result/<uuid>", methods=["GET"])
def result(uuid=None):
    if request.method == "GET":
        """
            return basic data for page rendering
        """
        poll = Poll.query.filter_by(uuid=uuid).first()

        if poll is None:
            abort(404)
        
        # Select answers and vote count in descending order 
        answer_tuples = Answer.query.with_entities(Answer.text, func.count(Answer.votes)) \
                    .filter_by(poll_id=poll.id).outerjoin(Vote) \
                    .group_by(Answer.id).order_by(func.count(Vote.id).desc()).all()

        result = "No vote yet"

        total_votes = len(poll.votes)

        if len(answer_tuples) > 0 and total_votes > 0:
            # Find the most voted answer
            result = answer_tuples[0][0]
            current_highest = answer_tuples[0][1]
            for i in range(len(answer_tuples)):
                if i == 0:
                    continue
                if answer_tuples[i][1] > current_highest:
                    # Tie, this answer has the same votes as the current highest votes
                    result = "Tie"

        

        variables = {
            "question": poll.question,
            "answers": answer_tuples,
            "total_votes": total_votes,
            "result": result,
            "uuid": poll.uuid
        }

        return render_template("result.html", **variables)

    elif request.method == "POST":
        """
            Receive uuid and return data for drawing charts
        """
        req = request.get_json()
        uuid = req.get("uuid", None)

        poll = Poll.query.filter_by(uuid=uuid).first()

        if poll is None:
            abort(404)

        # Select answers and vote count in descending order 
        answer_tuples = Answer.query.with_entities(Answer.text, func.count(Answer.votes)) \
                    .filter_by(poll_id=poll.id).outerjoin(Vote) \
                    .group_by(Answer.id).order_by(func.count(Vote.id).desc()).all()

        print(answer_tuples)
        answer_texts, votes = zip(*answer_tuples)

        variables = {
            "answer_texts": answer_texts,
            "votes": votes,
        }

        return jsonify(variables)

@bp.route("/share/<uuid>")
def share(uuid):
    poll = Poll.query.filter_by(uuid=uuid).first()

    if poll is None:
        abort(404)
    
    variables = {
        "share_link": "http://127.0.0.1:5000/poll/{}".format(poll.uuid),
    }

    return render_template("share.html", **variables)

@bp.route("/vote", methods=["POST"])
def vote():
    user_id = request.form["uuid"]
    poll_id = request.form["pollId"]
    voted_answers_id = request.form.getlist("answer")

    # Sanity check
    if user_id is None or voted_answers_id is None or poll_id is None:
        abort(422)     
    if len(user_id) < 1 or len(voted_answers_id) < 1:
        abort(422)
    
    # Get Poll UUID
    poll = Poll.query.filter_by(id=poll_id).first()

    if poll is None:
        abort(422)
    elif len(voted_answers_id) > poll.max_selection_limit:
        abort(422)

    # Delete old votes
    Vote.query.filter_by(poll_id=poll_id, voter=user_id).delete()

    voted_answers = []
    for ans_id in voted_answers_id:
        voted_answers.append(Vote(voter=user_id,
                                 answer_id=ans_id,
                                 poll_id=poll_id
        ))

    db.session.add_all(voted_answers)
    db.session.commit()

    return render_template("after_vote.html", result_link="/result/{}".format(poll.uuid))


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
        question = request.form.get("questionTitle", None)
        answers = request.form.getlist("answer")
        max_selection_limit = request.form.get("maxSelectionLimit", 1)
        access_key = generate_access_key()

        # Sanity check
        if question is None or answers is None:
            abort(422)
        try:
            max_selection_limit = int(max_selection_limit)
        except Exception as e:
            abort(422)
        if len(question) < 1 or len(answers) < 1 or max_selection_limit < 1 or max_selection_limit > len(answers):
            abort(422)
        
        try:
            question = escape(question)
            answer_objects = [Answer(text=escape(ans)) for ans in answers]
        except Exception as e:
            abort(422)

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
        user_uuid = request.cookies.get("uuid")
        voted_answers = None

        try:
            poll = Poll.query.filter_by(uuid=uuid).first()
        except Exception as e:
            abort(422)
        
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
            "result_link": "/result/{}".format(poll.uuid)
        }

        print(variables)
        return render_template("poll.html", **variables)