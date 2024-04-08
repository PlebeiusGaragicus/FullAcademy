import streamlit as st

from src.database import get_db
from src.login import login
from src.schema import ProblemSet, ProblemType

def page():
    if not login():
        return

    st.header("Study Collections")

    db = get_db()

    user_id = db["users"].find_one({"name": st.session_state.username})
    user_id = str(user_id["_id"])
    st.write(f"User ID: '{user_id}'")


    # find all ProblemSets inside "problemset" collection that belong to the current user
    problemsets = list(db["problemset"].find({"user_id": user_id}))

    set_titles = [problemset['title'] for problemset in problemsets]

    selected_problemset = st.selectbox("Select a problemset", set_titles)

    selected_problemset = db["problemset"].find_one({"title": selected_problemset})

    st.write(f"Selected Problemset: {selected_problemset['title']}")

    with st.form(key="add_problem"):
        st.write("Add a new problem to the selected problemset")
        problem_type = st.selectbox("Problem Type", [problem_type.value for problem_type in ProblemType])
        if problem_type == ProblemType.SHORT_ANSWER.value:
            question = st.text_input("Question")
            answer = st.text_input("Answer")
            prompt = st.text_input("Prompt")
            if st.form_submit_button("Add Problem"):
                db["problemset"].update_one({"title": selected_problemset['title']}, {"$push": {"problems": {"type": problem_type, "question": question, "answer": answer, "prompt": prompt}}})
        elif problem_type == ProblemType.SPELLING.value:
            word = st.text_input("Word")
            example_usage = st.text_input("Example Usage")
            if st.form_submit_button("Add Problem"):
                db["problemset"].update_one({"title": selected_problemset['title']}, {"$push": {"problems": {"type": problem_type, "word": word, "example_usage": example_usage}}})
        elif problem_type == ProblemType.MATH.value:
            equation = st.text_input("Equation")
            answer = st.text_input("Answer")
            if st.form_submit_button("Add Problem"):
                db["problemset"].update_one({"title": selected_problemset['title']}, {"$push": {"problems": {"type": problem_type, "equation": equation, "answer": answer}}})
        elif problem_type == ProblemType.DEFINITION.value:
            word = st.text_input("Word")
            definition = st.text_input("Definition")
            if st.form_submit_button("Add Problem"):
                db["problemset"].update_one({"title": selected_problemset['title']}, {"$push": {"problems": {"type": problem_type, "word": word, "definition": definition}}})

    # list all problems in the selected problemset
    with st.expander("Problems"):
        for problem in selected_problemset['problems']:
            if problem['type'] == "short_answer":
                st.write(f"Question: {problem['question']}")
                st.write(f"Answer: {problem['answer']}")
                st.write(f"Prompt: {problem['prompt']}")
            elif problem['type'] == "spelling":
                st.write(f"Word: {problem['word']}")
                st.write(f"Example Usage: {problem['example_usage']}")
            elif problem['type'] == "math":
                st.write(f"Equation: {problem['equation']}")
                st.write(f"Answer: {problem['answer']}")
            elif problem['type'] == "definition":
                st.write(f"Word: {problem['word']}")
                st.write(f"Definition: {problem['definition']}")


    # # for each problemset, display its title, description, and problems
    # for problemset in problemsets:
    #     with st.container(border=True):
    #         st.markdown(f"## {problemset['title']}")
    #         st.write(problemset['description'])

    #         with st.expander("Problems"):
    #             for problem in problemset['problems']:
    #                 if problem['type'] == "short_answer":
    #                     st.write(f"Question: {problem['question']}")
    #                     st.write(f"Answer: {problem['answer']}")
    #                     st.write(f"Prompt: {problem['prompt']}")
    #                 elif problem['type'] == "spelling":
    #                     st.write(f"Word: {problem['word']}")
    #                     st.write(f"Example Usage: {problem['example_usage']}")
    #                 elif problem['type'] == "math":
    #                     st.write(f"Equation: {problem['equation']}")
    #                     st.write(f"Answer: {problem['answer']}")
    #                 elif problem['type'] == "definition":
    #                     st.write(f"Word: {problem['word']}")
    #                     st.write(f"Definition: {problem['definition']}")

    #         if st.button(f":red[Delete] {problemset['title']}"):
    #             db["problemset"].delete_one({"_id": problemset["_id"]})
    #             st.rerun()
