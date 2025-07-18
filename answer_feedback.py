from difflib import SequenceMatcher
from supabase import create_client
from typing import Optional

import os

def create_feedback_client():
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def save_feedback_to_supabase(client, question, answer, issue_type, feedback):
    print("🚀 저장 시도 중...")

    data = {
        "question": question,
        "answer": answer,
        "issue_type": issue_type,
        "feedback": feedback
    }

    try:
        response = client.table("feedback").insert(data).execute()
        print("✅ Supabase 저장 성공:", response)
    except Exception as e:
        print("❌ Supabase 저장 실패:", e)

def get_similar_negative_feedback(client, new_question: str, threshold: float = 0.6) -> Optional[dict]:
    """
    Supabase에서 👎 받은 피드백 중 유사한 질문을 찾아 반환.
    """
    try:
        response = client.table("feedback").select("*").eq("feedback", "👎").execute()
        feedbacks = response.data
        best_match = None
        best_score = threshold

        for fb in feedbacks:
            score = SequenceMatcher(None, new_question, fb["question"]).ratio()
            if score > best_score:
                best_score = score
                best_match = fb

        return best_match
    except Exception as e:
        print(f"[❌ Supabase 조회 실패]: {e}")
        return None