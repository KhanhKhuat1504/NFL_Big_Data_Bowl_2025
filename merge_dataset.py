import pandas as pd
import os

# Define file paths for tracking weeks
tracking_files = [
    "tracking_week_1.csv",
    "tracking_week_2.csv",
    "tracking_week_3.csv",
    "tracking_week_4.csv",
    "tracking_week_5.csv",
    "tracking_week_6.csv",
    "tracking_week_7.csv",
    "tracking_week_8.csv",
    "tracking_week_9.csv"
]

# Load and combine tracking data with chunking
def load_and_combine_tracking_data(files):
    data_frames = []
    for file in files:
        print(f"Loading {file} in chunks...")
        try:
            chunk_list = []
            for chunk in pd.read_csv(file, chunksize=1_000_000, on_bad_lines='skip'):
                chunk_list.append(chunk)
            data_frames.append(pd.concat(chunk_list, ignore_index=True))
        except Exception as e:
            print(f"Error processing {file}: {e}")
    combined_data = pd.concat(data_frames, ignore_index=True)
    print("All tracking data loaded and combined.")
    return combined_data

# Perform random sampling
def random_sample_data(data, sample_size):
    print(f"Sampling {sample_size} data points from the combined dataset...")
    sampled_data = data.sample(n=sample_size, random_state=42)
    print("Sampling complete.")
    return sampled_data

# Main execution
if __name__ == "__main__":
    # Combine all tracking data
    combined_data = load_and_combine_tracking_data(tracking_files)
    
    # Perform random sampling to create a smaller dataset (~2 million rows)
    sample_size = 2_000_000  # Target sample size
    sampled_data = random_sample_data(combined_data, sample_size)
    
    # Save the sampled data to a new CSV file
    output_file = "sampled_tracking_data.csv"
    print(f"Saving sampled data to {output_file}...")
    sampled_data.to_csv(output_file, index=False)
    print(f"Sampled data saved to {output_file}.")