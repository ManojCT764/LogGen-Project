import pandas as pd
import numpy as np
import random
import logging
import string
import matplotlib.pyplot as plt

def generate_log_entry():
    """
    Generate a random log entry with a timestamp, log level, action and user
    """
    timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    log_level = random.choice(["INFO", "DEBUG", "ERROR", "WARNING"])
    action = random.choice(['login', 'logout', 'Data Request', 'File Upload', 'Download', 'Error'])
    user = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) # Generate random user ID
    return f"{timestamp} - {log_level} - {action} - User: {user}"

#function to write logs to a file
def write_logs_to_file(log_filename, num_entries=100):
    """
    Write the specified number of random logs to the given file.
    """
    try:
        with open(log_filename, 'w') as file:
            for _ in range(num_entries):
                log = generate_log_entry()
                file.write(log + '\n')
        print(f'Logs have been written to {log_filename}')
    except Exception as e:
        logging.error(f"Error in write_logs_to_file: {e}")
        print("An error occurred while writing logs to the file")

# Function to read logs from a file and process it
def load_and_process_logs(log_filename="generated_logs.txt"):
    """
    Loads and process the logs from the given file, cleaning and parsing the timestamps.
    """
    try:
        #Read teh log file into Pandas DataFrame, splitting by the ' - ' seperator
        df = pd.read_csv(log_filename, sep=' - ', header=None, names=['Timestamp', 'Log Level', 'Action', 'User'], engine='python')

        # Clean and trim spaces around the timestamp column
        df['Timestamp'] = df['Timestamp'].str.strip()
        # Convert the 'Timestamp' column to datetime objects
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        # Drop rows with invalid timestamps
        df = df.dropna(subset=['Timestamp'])

        if df.empty:
            print("No valid log entries found after timestamp parsing. ")
        else:
            print("Data after timestamp conversion:")
            print(df.head())
        
        # Set the 'Timestamp' column as the index for time-based operations
        df.set_index('Timestamp', inplace=True)

        return df
    except Exception as e:
        logging.error(f"Error in load_and_process_logs: {e}")
        return None
    
# FUnction to visualize log data
def analyze_data(df):
    """
    Analyze and visualize the log data.
    """
    try:
        if df is None or df.empty:
            print("No data available for analysis.")
            return None, None

        # Count teh occurance of each log level
        log_level_counts = df['Log Level'].value_counts()

        # Count the occurance of each action
        action_counts = df['Action'].value_counts()

        log_count = len(df) # Total number of logs
        unique_users = df['User'].nunique() # Number of unique users
        logs_per_day = df.resample('D').size() # Logs per day

        # Averages of actions per user
        average_logs_per_day = logs_per_day.mean()

        # Maximum logs in a single day
        max_logs_in_a_day = logs_per_day.max()

        # Print summary statistics
        print("\nLog Level Counts:\n", log_level_counts)
        print("\nAction Counts:\n", action_counts)
        print(f"Total number of logs: {log_count}")
        print(f"Number of unique users: {unique_users}")
        print(f"Average logs per day: {average_logs_per_day:.2f}")
        print(f"Maximum logs in a single day: {max_logs_in_a_day}") 

        # Create a dictionary to hold analysis results
        stats = {
            "log_level_counts": log_level_counts,
            "action_counts": action_counts,
            "total_logs": log_count,
            "unique_users": unique_users,
            "average_logs_per_day": average_logs_per_day,
            "max_logs_in_a_day": max_logs_in_a_day
        }

        return stats
    except Exception as e:
        logging.error(f"Error in analyze_data: {e}")
        return None
    
# Function to visualize trends over time using Matplotlib
def vizualize_trends(df):
    """
    Visualize trends in log data over time using Matplotlib.
    """
    try:
        # if df is None or df.empty:
        #     print("No data available for visualization.")
        #     return

        # Resample to daily frequency and count logs per day
        logs_per_day = df.resample('D').size()

        plt.figure(figsize=(10, 5))
        plt.plot(logs_per_day.index, logs_per_day.values, marker='o', linestyle='-', color='b')
        plt.title('Logs Frequency Over Time')
        plt.xticks(rotation=45)
        plt.xlabel('Date')
        plt.ylabel('Number of Logs')
        plt.grid(True)
        # show the plot
        plt.tight_layout()
        plt.savefig("output.png")  # Save the plot as a PNG file
        plt.show()
    except Exception as e:
        logging.error(f"Error in visualize_trends: {e}")


log_filename = "generated_logs.txt" # Assumed that this file exists


# Step 1: Write random logs to a file
write_logs_to_file(log_filename, num_entries=1000)

# step 2: Load and process the logs
df_logs = load_and_process_logs(log_filename)


if df_logs is not None and not df_logs.empty:
    print("Loaded and processed logs successfully.")

    # Step 3: Analyze the data
    stats = analyze_data(df_logs)

    # Step 4: Visualize trends in the data
    vizualize_trends(df_logs)

