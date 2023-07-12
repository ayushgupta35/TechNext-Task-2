import json
import matplotlib.pyplot as plt
import numpy as np
import requests
from flask import Flask, render_template

flask_app = Flask(__name__)

@flask_app.route('/')
def plot():
    # Retrieve the JSON data from REST endpoint
    url = "https://testtechnext1-pearl118.b4a.run/search/api/phases/"
    data = json.loads(requests.get(url).text)

    # Extract phase labels and entries, skipping any null entries
    labels = []
    heights = []
    for item in data:
        if item['phase'] is not None:
            labels.append(item['phase'])
            heights.append(item['entries'])

    # Create bar chart
    x = range(len(labels))
    plt.bar(x, heights)
    plt.xticks(x, labels)
    plt.xlabel('Phase')
    plt.ylabel('Entries')
    plt.title('Phase Entries')

    # Create line chart superimposed on bar chart 
    indices = [i for i, entry in enumerate(heights) if entry > 0]
    values = np.array(heights)[indices]
    plt.plot(np.array(indices), values, color='red', marker='o')

    # Save plot to .png file
    plt.savefig("static/temp_plot.png")
    plt.close()

    # Render the template with the plot png
    return render_template('plot.html', plot_filename="static/temp_plot.png")

if __name__ == '__main__':
    flask_app.run()
