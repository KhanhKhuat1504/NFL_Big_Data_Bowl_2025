import pandas as pd

# File paths for datasets
tracking_file = "sampled_tracking_data.csv"  # Sampled tracking data
other_files = {
    "games": "games.csv",
    "plays": "plays.csv",
    "players": "players.csv",
    "player_play": "player_play.csv"
}

# Load other datasets
def load_other_data(files):
    datasets = {}
    for name, file in files.items():
        print(f"Loading {file}...")
        try:
            datasets[name] = pd.read_csv(file)
        except Exception as e:
            print(f"Error loading {file}: {e}")
    return datasets

# Merge datasets
def merge_datasets(tracking_data, other_data):
    print("Merging datasets...")
    merged_data = tracking_data.copy()
    
    # Merge games
    if "games" in other_data:
        merged_data = merged_data.merge(other_data["games"], on="gameId", how="left")
    
    # Merge plays
    if "plays" in other_data:
        merged_data = merged_data.merge(other_data["plays"], on=["gameId", "playId"], how="left")
    
    # Merge player play
    if "player_play" in other_data:
        merged_data = merged_data.merge(other_data["player_play"], on=["gameId", "playId", "nflId"], how="left")
    
    # Merge players
    if "players" in other_data:
        merged_data = merged_data.merge(other_data["players"], on="nflId", how="left")
    
    print("Merging complete.")
    return merged_data

# Main execution
if __name__ == "__main__":
    # Load the sampled tracking data
    print("Loading sampled tracking data...")
    sampled_tracking_data = pd.read_csv(tracking_file)
    
    # Load other datasets
    other_datasets = load_other_data(other_files)
    
    # Combine all datasets
    combined_data = merge_datasets(sampled_tracking_data, other_datasets)
    
    # Save the combined dataset to a CSV file
    output_file = "combined_dataset.csv"
    print(f"Saving combined dataset to {output_file}...")
    combined_data.to_csv(output_file, index=False)
    print(f"Combined dataset saved to {output_file}.")