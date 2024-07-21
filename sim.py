import plotly.graph_objects as go
import numpy as np

# Define the 20 standard amino acids
amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 
               'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

# Map amino acids to their indices
amino_acid_indices = {aa: i for i, aa in enumerate(amino_acids)}

# Create a grid of amino acid indices
x_indices = np.arange(len(amino_acids))
y_indices = np.arange(len(amino_acids))
X, Y = np.meshgrid(x_indices, y_indices)

# Generate a smoother fitness landscape using a combination of Gaussian and sine functions
Z = (0.5 * np.sin(0.5 * X) * np.cos(0.5 * Y) +
     0.5 * np.exp(-0.1 * ((X - len(amino_acids) / 2) ** 2 + (Y - len(amino_acids) / 2) ** 2)) +
     0.25 * np.sin(0.5 * X) * np.cos(0.5 * Y))

# Define some specific points to plot
specific_points = [
    ('A', 'C'),
    ('D', 'E'),
    ('F', 'G'),
    ('H', 'I'),
    ('K', 'L'),
    ('M', 'N'),
    ('P', 'Q'),
    ('R', 'S'),
    ('T', 'V'),
    ('W', 'Y')
]

# Convert specific points to indices and calculate Z values
x_points = [amino_acid_indices[p[0]] for p in specific_points]
y_points = [amino_acid_indices[p[1]] for p in specific_points]
z_points = [Z[x][y] for x, y in zip(x_points, y_points)]

# Create the surface plot
surface = go.Surface(
    x=X,
    y=Y,
    z=Z,
    colorscale='Viridis',
    colorbar=dict(
        title='Fitness',
        tickvals=[i for i in np.linspace(np.min(Z), np.max(Z), num=5)],  # Adjust tick values
        ticktext=[f'{i:.2f}' for i in np.linspace(np.min(Z), np.max(Z), num=5)],  # Adjust tick text
        tickfont=dict(size=10),  # Font size of ticks
        titlefont=dict(size=12)  # Font size of title
    ),
    showscale=True
)

# Create scatter plot for specific points
scatter = go.Scatter3d(
    x=x_points,
    y=y_points,
    z=z_points,
    mode='markers+text',
    text=[f'{p[0]},{p[1]}: {z:.2f}' for p, z in zip(specific_points, z_points)],
    textposition='top center',
    marker=dict(
        size=10,
        color=z_points,
        colorscale='RdYlBu',
        colorbar=dict(
            title='Fitness',
            tickvals=[i for i in np.linspace(np.min(Z), np.max(Z), num=5)],  # Adjust tick values
            ticktext=[f'{i:.2f}' for i in np.linspace(np.min(Z), np.max(Z), num=5)],  # Adjust tick text
            tickfont=dict(size=10),  # Font size of ticks
            titlefont=dict(size=12)  # Font size of title
        ),
        showscale=True
    )
)

# Add arrows to show a process
arrows = []
for i in range(len(x_points) - 1):
    arrows.append(
        go.Scatter3d(
            x=[x_points[i], x_points[i+1]],
            y=[y_points[i], y_points[i+1]],
            z=[z_points[i], z_points[i+1]],
            mode='lines+markers',
            line=dict(
                color='blue',
                width=2,
                dash='dash'
            ),
            marker=dict(
                size=5,
                color='blue'
            )
        )
    )

# Create the figure and add both the surface, scatter plot, and arrows
fig = go.Figure(data=[surface, scatter] + arrows)

# Update layout to hide background planes and grid
fig.update_layout(
    title='3D Fitness Landscape of Proteins with Annotations and Process Arrows',
    scene=dict(
        xaxis=dict(
            title='Amino Acid 1', 
            tickmode='array', 
            tickvals=list(range(len(amino_acids))), 
            ticktext=amino_acids,
            showgrid=False,  # Hide grid
            zeroline=False,  # Hide zero line
            showbackground=False,  # Hide background plane
            backgroundcolor='rgba(0,0,0,0)'  # Transparent background
        ),
        yaxis=dict(
            title='Amino Acid 2', 
            tickmode='array', 
            tickvals=list(range(len(amino_acids))), 
            ticktext=amino_acids,
            showgrid=False,  # Hide grid
            zeroline=False,  # Hide zero line
            showbackground=False,  # Hide background plane
            backgroundcolor='rgba(0,0,0,0)'  # Transparent background
        ),
        zaxis=dict(
            title='Fitness',
            showgrid=False,  # Hide grid
            zeroline=False,  # Hide zero line
            showbackground=False,  # Hide background plane
            backgroundcolor='rgba(0,0,0,0)'  # Transparent background
        ),
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.5)  # Adjust camera angle
        )
    )
)

# Show the plot
fig.show()
