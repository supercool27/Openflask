from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps import db
from apps.quiz.models import Question, UserProgress
from apps.authentication.models import Users

quiz_bp = Blueprint("quiz", __name__, url_prefix="/api/quiz")

# 1. Get a random question for the logged-in user
@quiz_bp.route("/question", methods=["GET"])
@jwt_required()
def get_question():
    user_id = get_jwt_identity()

    # Example: fetch first unanswered question for this user
    answered_qs = db.session.query(UserProgress.question_id).filter_by(user_id=user_id).all()
    answered_ids = [q[0] for q in answered_qs]

    question = Question.query.filter(~Question.id.in_(answered_ids)).first()

    if not question:
        return jsonify({"msg": "No more questions available!"}), 404

    return jsonify({
        "id": question.id,
        "flag_url": question.flag_url,
        "options": [
            question.correct_answer,  # correct answer
            "Fake Option 1",
            "Fake Option 2",
            "Fake Option 3"
        ]
    }), 200


# 2. Submit answer
@quiz_bp.route("/answer", methods=["POST"])
@jwt_required()
def submit_answer():
    user_id = get_jwt_identity()
    data = request.get_json()

    question_id = data.get("question_id")
    selected_answer = data.get("answer")

    question = Question.query.get(question_id)
    if not question:
        return jsonify({"msg": "Question not found"}), 404

    is_correct = (selected_answer == question.correct_answer)

    # Save user progress
    progress = UserProgress(
        user_id=user_id,
        question_id=question_id,
        is_correct=is_correct
    )
    db.session.add(progress)
    db.session.commit()

    return jsonify({
        "msg": "Answer submitted",
        "is_correct": is_correct
    }), 200


# 3. Get user progress
@quiz_bp.route("/progress", methods=["GET"])
@jwt_required()
def get_progress():
    user_id = get_jwt_identity()
    total_questions = Question.query.count()
    correct_answers = UserProgress.query.filter_by(user_id=user_id, is_correct=True).count()

    return jsonify({
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "score": f"{correct_answers}/{total_questions}"
    }), 200
