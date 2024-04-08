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



    # problemsets = list(db["problemset"].find())
    # st.write(f"ALL Problemsets: {problemsets}")

    # find all ProblemSets inside "problemset" collection that belong to the current user
    problemsets = list(db["problemset"].find({"user_id": user_id}))
    # st.write(f"MY Problemsets: {problemsets}")


    # if st.button("Create New Collection"):
    # show a form to create a new collection
    with st.expander("Create New Collection"):
        with st.form(key="new_collection", clear_on_submit=True):
            title = st.text_input("Title")
            description = st.text_area("Description")
            type = st.selectbox("Type", [problem_type.value for problem_type in ProblemType], index=None, placeholder="Mixed")
            if st.form_submit_button("Create Collection"):
                if title == "":
                    st.error("Title must be filled")
                else:
                    new_problemset = ProblemSet(user_id=user_id, title=title, description=description, type=type, problems=[])
                    new = new_problemset.model_dump()
                    db["problemset"].insert_one( new )

                    st.rerun()


    st.header("Your Study Collections", divider=True)

    if problemsets == []:
        st.warning("You have no study collections yet!")
        return


    # for each problemset, display its title, description, and problems
    for problemset in problemsets:
        with st.container(border=True):
            st.markdown(f"## {problemset['title']}")
            st.write(problemset['description'])
            st.write(f"Type: `{problemset['type']}`")

            with st.expander("Problems"):
                for problem in problemset['problems']:
                    with st.container(border=True):
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

            with st.popover(":red[Delete Collection]"):#, key=problemset["_id"]):
                st.error("Warning: This action is irreversible!")
                if st.button(f":red[Delete] {problemset['title']}", key=problemset["_id"]):
                    db["problemset"].delete_one({"_id": problemset["_id"]})
                    st.rerun()
