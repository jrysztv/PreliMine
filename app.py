import streamlit as st
from prelimine.course_graph import create_course_graph, draw_course_graph

# Constants
LABEL_COLUMNS = ["Course Name", "Semester", "Professor"]

# Sample data
data = [
    {
        "course_name": "Introduction to Programming",
        "shorthand": "ITP",
        "preliminary": [],
        "semester": 1,
        "professor": "Dr. Smith",
    },
    {
        "course_name": "Data Structures",
        "shorthand": "DST",
        "preliminary": ["ITP"],
        "semester": 2,
        "professor": "Dr. Johnson",
    },
    {
        "course_name": "Algorithms",
        "shorthand": "ALG",
        "preliminary": ["DST", "ITP"],
        "semester": 3,
        "professor": "Dr. Williams",
    },
    {
        "course_name": "Operating Systems",
        "shorthand": "OPS",
        "preliminary": ["DST"],
        "semester": 3,
        "professor": "Dr. Brown",
    },
    {
        "course_name": "Database Systems",
        "shorthand": "DBS",
        "preliminary": ["DST"],
        "semester": 3,
        "professor": "Dr. Davis",
    },
    {
        "course_name": "Software Engineering",
        "shorthand": "SWE",
        "preliminary": ["ALG", "OPS", "DBS"],
        "semester": 4,
        "professor": "Dr. Miller",
    },
]

st.title("Course Dependency Graph")

# Create the graph
G = create_course_graph(data)

# Draw the graph and get the figure
fig = draw_course_graph(G, label_columns=LABEL_COLUMNS)

# Display the graph in the Streamlit app using Plotly
st.plotly_chart(fig)
