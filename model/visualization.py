import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_heatmap(data):
    """
    Generate a heatmap for genre metrics based on hardcoded data.
    """
    # Convert the dictionary to a DataFrame
    performance_df = pd.DataFrame.from_dict(data, orient="index")
    performance_df.reset_index(inplace=True)
    performance_df.columns = ["Genre", "Accuracy", "Precision", "Recall", "F1_Score"]

    # Set Genre as the index for the heatmap
    performance_df.set_index("Genre", inplace=True)

    # Plot the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(performance_df, annot=True, cmap="Blues", fmt=".2f", linewidths=0.5)
    plt.title("Metrics by Genre")
    plt.ylabel("Genre")
    plt.xlabel("Metrics")
    plt.show()


def plot_bar_graph(data):
    """
    Generate a bar graph for a specific metric based on hardcoded data.
    """
    # Convert the dictionary to a DataFrame
    performance_df = pd.DataFrame.from_dict(data, orient="index")
    performance_df.reset_index(inplace=True)
    performance_df.columns = ["Genre", "Accuracy", "Precision", "Recall", "F1_Score"]

    # Select a specific metric for the bar graph (e.g., Accuracy)
    bar_data = performance_df[["Genre", "Accuracy"]]

    # Plot the bar graph
    plt.figure(figsize=(12, 8))
    sns.barplot(data=bar_data, x="Genre", y="Accuracy", palette="viridis")
    plt.title("Accuracy by Genre")
    plt.ylabel("Accuracy Value")
    plt.xlabel("Genre")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def plot_histogram(data):
    """
    Generate a histogram for a specific metric based on hardcoded data.
    """
    # Convert the dictionary to a DataFrame
    performance_df = pd.DataFrame.from_dict(data, orient="index")
    performance_df.reset_index(inplace=True)
    performance_df.columns = ["Genre", "Accuracy", "Precision", "Recall", "F1_Score"]

    # Select a specific metric for the histogram (e.g., Recall)
    metric_values = performance_df["Recall"]

    # Plot the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(metric_values, bins=10, color="skyblue", edgecolor="black", alpha=0.7)
    plt.title("Distribution of Recall Across Genres")
    plt.xlabel("Recall Value")
    plt.ylabel("Frequency")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


def plot_boxplot(data):
    """
    Generate a box plot to show the distribution of metrics across genres based on hardcoded data.
    """
    # Convert the dictionary to a DataFrame
    performance_df = pd.DataFrame.from_dict(data, orient="index")
    performance_df.reset_index(inplace=True)
    performance_df.columns = ["Genre", "Accuracy", "Precision", "Recall", "F1_Score"]

    # Melt the DataFrame for boxplot compatibility
    melted_df = performance_df.melt(id_vars=["Genre"], var_name="Metric", value_name="Value")

    # Plot the box plot
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=melted_df, x="Metric", y="Value", palette="Set3")
    plt.title("Distribution of Metrics Across Genres")
    plt.ylabel("Metric Value")
    plt.xlabel("Metric")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Hardcoded data
    sample_data = {
        "Funk": {"accuracy": 0.1, "precision": 0.1, "recall": 0.1, "f1_score": 0.1},
        "K-Pop": {"accuracy": 0.52, "precision": 0.52, "recall": 0.52, "f1_score": 0.52},
        "Folk/Americana": {"accuracy": 0.25, "precision": 0.25, "recall": 0.25, "f1_score": 0.25},
        "Reggaeton": {"accuracy": 0.03, "precision": 0.03, "recall": 0.03, "f1_score": 0.03},
        "Indie": {"accuracy": 0.17, "precision": 0.16, "recall": 0.17, "f1_score": 0.17},
        "Pop": {"accuracy": 0.19, "precision": 0.19, "recall": 0.19, "f1_score": 0.19},
        "Latin": {"accuracy": 0.14, "precision": 0.16, "recall": 0.14, "f1_score": 0.14},
        "Kids": {"accuracy": 0.08, "precision": 0.07, "recall": 0.08, "f1_score": 0.08},
        "Hip-Hop": {"accuracy": 0.24, "precision": 0.24, "recall": 0.24, "f1_score": 0.24},
        "R&B": {"accuracy": 0.45, "precision": 0.48, "recall": 0.45, "f1_score": 0.45},
        "Jazz": {"accuracy": 0.34, "precision": 0.33, "recall": 0.34, "f1_score": 0.34},
        "Blues": {"accuracy": 0.06, "precision": 0.06, "recall": 0.06, "f1_score": 0.06},
        "Country": {"accuracy": 0.33, "precision": 0.33, "recall": 0.33, "f1_score": 0.33},
        "Metal": {"accuracy": 0.27, "precision": 0.27, "recall": 0.27, "f1_score": 0.27},
        "Musica Mexicana": {"accuracy": 0.57, "precision": 0.57, "recall": 0.57, "f1_score": 0.57},
        "Christian/Gospel": {"accuracy": 0.55, "precision": 0.55, "recall": 0.55, "f1_score": 0.55},
        "Rock": {"accuracy": 0.58, "precision": 0.58, "recall": 0.58, "f1_score": 0.58},
        "Dance/Electronic": {"accuracy": 0.52, "precision": 0.52, "recall": 0.48, "f1_score": 0.52},
    }

    print("Generating visualizations using hardcoded data...")
    plot_heatmap(sample_data)
    print("Now generating the bar graph...")
    plot_bar_graph(sample_data)
    print("Now generating the histogram...")
    plot_histogram(sample_data)
    print("Now generating the box plot...")
    plot_boxplot(sample_data)




