import networkx as nx
import plotly.graph_objects as go
import numpy as np


def create_course_graph(data):
    G = nx.DiGraph()

    # Add nodes and edges
    for course in data:
        G.add_node(course["shorthand"], **course)
        for pre in course["preliminary"]:
            G.add_edge(pre, course["shorthand"])

    return G


def semester_pos(G):
    pos = {}
    # Group nodes by semester
    semester_groups = {}
    for node in G.nodes(data=True):
        semester = node[1]["semester"]
        if semester not in semester_groups:
            semester_groups[semester] = []
        semester_groups[semester].append(node[0])

    # Assign positions based on semester
    for semester, nodes in semester_groups.items():
        y = -semester  # Each semester gets a different y-value
        x_step = 1 / (
            len(nodes) + 1
        )  # Equal spacing for nodes within the same semester
        for i, node in enumerate(nodes):
            x = x_step * (i + 1)
            pos[node] = (x, y)

    return pos


def generate_label(node_data, label_columns):
    label_parts = []
    for key in label_columns:
        lower_key = key.lower().replace(" ", "_")
        label_value = node_data.get(lower_key, "")
        label_parts.append(f"{key.capitalize()}: {label_value}")
    return "<br>".join(label_parts)


def calculate_color_range(semesters):
    min_semester = min(semesters)
    max_semester = max(semesters)
    range_len = max_semester - min_semester

    if range_len == 0:
        # All nodes are in the same semester, return a single color
        return [0.5] * len(semesters)

    return [(semester - min_semester) / range_len for semester in semesters]


def draw_course_graph(G, label_columns):
    pos = semester_pos(G)

    # Prepare colors based on semesters
    semesters = [G.nodes[node]["semester"] for node in G.nodes()]
    color_range = calculate_color_range(semesters)

    # Create edges and nodes for the Plotly graph
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=2, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    node_x = []
    node_y = []
    node_text = []  # Shorthand names for nodes
    node_labels = []  # Metadata labels for hover
    node_colors = []  # Colors based on semesters
    for i, node in enumerate(G.nodes()):
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)  # Display shorthand on node
        node_labels.append(
            generate_label(G.nodes[node], label_columns)
        )  # Metadata dynamically generated
        node_colors.append(color_range[i])  # Assign color based on semester

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,  # Shorthand names displayed on nodes
        hoverinfo="text",
        hovertext=node_labels,  # Metadata displayed on hover
        textposition="middle center",
        marker=dict(
            colorscale="Bluered",  # Use the "Viridis" colorscale
            cmin=0,
            cmax=1,
            color=node_colors,
            size=50,  # Node size
            line_width=2,
        ),
    )

    # Create the figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="Strict Hierarchical Tree Layout of Courses",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=0, l=0, r=0, t=50),
            annotations=[
                dict(
                    text="Course Dependencies",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    return fig
