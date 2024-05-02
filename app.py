from shiny.express import input, render, ui
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ui.markdown(
    """
    # Normalization and Choice or the other problem with 3rd party candidates. (Made in Shiny)

    ### This my early interactive Shiny app to help understand devisive normalization and why it can be bad for politics.
    
    The influence of 3rd parties in politics has been debated. Discussing whether they pose a [spoiler effect](https://en.wikipedia.org/wiki/Spoiler_effect) and in particular the effect third party candidates have on elections with plurality votting. What is less discussed is that people are well known to break the Axiom of the independence of irrelevant alternatives (IIA). IIA sounds straight forward, if we like A more than B, how good an irrelevant C is shouldn't matter.
    
    Take a look at the graphs below they represent how well 3 representatives align in different policy domains. While A is highly aligned on fiscal domains, B is highly aligned on social domains, and C is not highly aligned with us on either domain. On the right side we see how much we 'like' each candidate. Assuming we weigh social and fiscal policy equally we should like A and B the same. Now move C up just a bit on one of the two domains. Not only does how much we like C go up but how much we like the politician they're moving towards goes down. This breaks IIA.
    
    While this isn't to say that this effect means 3rd party candidates are bad. Or that these effects will even have a large effect on the outcome of an election. It could have effects at the margin. I encourage you to think about how these dynamics could shape a political race in primaries as politicians drop out along the way, or how a bad actor might try to purposefully take use of this effect.
    
    
    This isn't an aspect of third party candidates that get's discussed even in heavily political circles and I think it's a discussion that should happen a little more.
    
    """
)


ui.page_opts(title="Normalization and Choice", fillable=True)
with ui.sidebar():
	ui.input_slider("x1", "A-Social", min=0, max=1, value=0.2),
	ui.input_slider("y1", "A-Fiscal", min=0, max=1, value=0.8),
	ui.input_slider("x2", "B-Social", min=0, max=1, value=0.8),
	ui.input_slider("y2", "B-Fiscal", min=0, max=1, value=0.2),
	ui.input_slider("x3", "C-Social", min=0, max=1, value=0.1),
	ui.input_slider("y3", "C-Fiscal", min=0, max=1, value=0.1),
	ui.input_slider("weight", "Weight", min=0.1, max=2, value=1),
    



@render.plot
def plot():
	data = pd.DataFrame({
		    "Label": ["A", "B", "C"],
		    "Social Policy Alignment": [input.x1(), input.x2(), input.x3()],
		    "Fiscal Policy Alignment": [input.y1(), input.y2(), input.y3()]
		})
	initial_positions = np.array([[input.x1(), input.y1()],
	 [input.x2(), input.y2()], [input.x3(), input.y3()]])

	labels = ['A', 'B', 'C']  # Labels for each point
	normed = initial_positions / (1+(initial_positions.sum(axis=0)*2))
	sum_values = normed.sum(axis=1)
	# Set up the matplotlib figure and axes
	fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
	# Scatter plot on the first axes
	points = ax1.scatter(initial_positions[:, 0], initial_positions[:, 1], s=100, c='blue')
	texts = [ax1.text(pos[0], pos[1], label, fontsize=12, ha='right') for pos, label in zip(initial_positions, labels)]
	ax1.set_xlabel("Social Policy Alignment")
	ax1.set_ylabel("Fiscal Policy Alignment")
	ax1.set_xlim(0, 1)
	ax1.set_ylim(0, 1)
	ax1.grid(True)

	# Bar plot on the second axes
	bars = ax2.bar(labels, sum_values, color=['red', 'green', 'blue'])
	ax2.set_ylim(0, np.max(sum_values)*1.1)
	ax2.set_title('Normalized Values in X')

