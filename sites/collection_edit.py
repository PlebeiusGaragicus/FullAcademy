import streamlit as st

from src.database import get_db
from src.login import login
from src.schema import ProblemSet, ProblemType

def page():
    if not login():
        return

    st.header("📝 :rainbow[Edit a Collection]", divider="rainbow")


    db = get_db()

    user_id = db["users"].find_one({"name": st.session_state.username})
    user_id = str(user_id["_id"])
    st.sidebar.write(f"User ID: '{user_id}'")


    # find all ProblemSets inside "problemset" collection that belong to the current user
    problemsets = list(db["problemset"].find({"user_id": user_id}))

    if problemsets == []:
        st.warning("You have no study collections yet!")
        return

    set_titles = [problemset['title'] for problemset in problemsets]

    selected_problemset = st.selectbox("Select a problemset", set_titles)
    selected_problemset = db["problemset"].find_one({"title": selected_problemset})

    if selected_problemset['type'] is None:
        new_problem_type = st.selectbox("Problem Type", [problem_type.value for problem_type in ProblemType])
    else:
        new_problem_type = selected_problemset['type']
        st.markdown(f"Collection Problem Type: `{new_problem_type}`")

    with st.form(key="add_problem", clear_on_submit=True):

        if new_problem_type == ProblemType.SHORT_ANSWER.value:
            question = st.text_input("Question")
            answer = st.text_input("Answer")
            prompt = st.text_input("Prompt")
            if st.form_submit_button("Add Problem"):
                if question == "" or answer == "" or prompt == "":
                    st.error("All fields must be filled")
                else:
                    existing_problem = db["problemset"].find_one({"title": selected_problemset['title'], "problems.question": question})
                    if existing_problem is None:
                        db["problemset"].update_one({"title": selected_problemset['title']}, {"$push": {"problems": {"type": new_problem_type, "question": question, "answer": answer, "prompt": prompt}}})
                        st.rerun()
                    else:
                        st.error("Problem already exists in the selected problemset")

        elif new_problem_type == ProblemType.SPELLING.value:
            st.header("New spelling word", divider=True)
            word = st.text_input("Word")
            example_usage = st.text_input("Example Usage")
            if st.form_submit_button("Add word"):
                if word == "" or example_usage == "":
                    st.error("All fields must be filled")
                else:
                    existing_problem = db["problemset"].find_one({"title": selected_problemset['title'], "problems.word": word})
                    if existing_problem is None:
                        db["problemset"].update_one({"title": selected_problemset['title']}, {"$push": {"problems": {"type": new_problem_type, "word": word, "example_usage": example_usage}}})
                        st.rerun()
                    else:
                        st.error("Problem already exists in the selected problemset")


        elif new_problem_type == ProblemType.MATH.value:
            equation = st.text_input("Equation")
            answer = st.text_input("Answer")
            if st.form_submit_button("Add Problem"):
                if equation == "" or answer == "":
                    st.error("All fields must be filled")
                else:
                    existing_problem = db["problemset"].find_one({"title": selected_problemset['title'], "problems.equation": equation})
                    if existing_problem is None:
                        db["problemset"].update_one({"title": selected_problemset['title']}, {"$push": {"problems": {"type": new_problem_type, "equation": equation, "answer": answer}}})
                        st.rerun()
                    else:
                        st.error("Problem already exists in the selected problemset")

        elif new_problem_type == ProblemType.DEFINITION.value:
            word = st.text_input("Word")
            definition = st.text_input("Definition")
            if st.form_submit_button("Add Problem"):
                if word == "" or definition == "":
                    st.error("All fields must be filled")
                else:
                    existing_problem = db["problemset"].find_one({"title": selected_problemset['title'], "problems.word": word})
                    if existing_problem is None:
                        db["problemset"].update_one({"title": selected_problemset['title']}, {"$push": {"problems": {"type": new_problem_type, "word": word, "definition": definition}}})
                        st.rerun()
                    else:
                        st.error("Problem already exists in the selected problemset")

    if new_problem_type == ProblemType.SPELLING.value:
        st.header("List of words in collection", divider=True)
    else:
        st.header("List of problems in collection", divider=True)

    # list all problems in the selected problemset
    # with st.expander("Problems"):
    for problem in selected_problemset['problems']:
        with st.container(border=True):
            cols2 = st.columns((3, 1))
            with cols2[0]:
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
                    # st.write("`Definition`")
                    st.write(f"Word: {problem['word']}")
                    st.write(f"Definition: {problem['definition']}")

            with cols2[1]:
                with st.popover(":red[Delete]"):
                    st.error("Are you sure you want to delete this problem?")
                    if st.button(f":red[Delete]", key=problem):
                        db["problemset"].update_one({"title": selected_problemset['title']}, {"$pull": {"problems": problem}})
                        st.rerun()


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
