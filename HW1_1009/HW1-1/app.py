from flask import Flask, request, render_template
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Function to generate synthetic data
def generate_data(a, b, noise_level, n_points):
    np.random.seed(42)  # For reproducibility
    X = 2 * np.random.rand(n_points, 1)
    y = a * X + b + noise_level * np.random.randn(n_points, 1)
    return X, y

@app.route("/", methods=["GET", "POST"])
def index():
    # Default slider values
    a_val = 3
    b_val = 1  # Fixed intercept
    noise_val = 1
    n_points_val = 100

    plot_url = None

    if request.method == "POST":
        # Get values from the form submission
        a_val = float(request.form["a"])
        noise_val = float(request.form["noise"])
        n_points_val = int(request.form["n_points"])

        # Generate data and perform linear regression
        X, y = generate_data(a_val, b_val, noise_val, n_points_val)
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        # Create the plot
        plt.figure(figsize=(8, 6))
        plt.scatter(X, y, color='blue', label="Data Points")
        plt.plot(X, y_pred, color='red', label="Regression Line")
        plt.xlabel('X')
        plt.ylabel('y')
        plt.title('Linear Regression Fit')
        plt.legend()

        # Convert the plot to a PNG image
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        plt.close()

    # Render the HTML template and pass values to it
    return render_template(
        "index.html",
        a=a_val,
        noise=noise_val,
        n_points=n_points_val,
        plot_url=plot_url
    )

if __name__ == "__main__":
    app.run(debug=True)
