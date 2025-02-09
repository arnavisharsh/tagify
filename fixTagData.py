import pandas as pd
import ast

# Load data from CSV
df = pd.read_csv('add_tags_data_with_tags.csv')

# Ensure tags are properly formatted and parsed
def correct_and_parse_tags(tag_str):
    try:
        corrected_tags = tag_str.replace("[", '["').replace("]", '"]').replace(", ", '", "')
        return ast.literal_eval(corrected_tags) if isinstance(tag_str, str) else []
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing tags: {e} - {tag_str}")
        return []

# Apply the correction and parsing function to the 'tags' column
df['parsed_tags'] = df['tags'].apply(correct_and_parse_tags)

# Split parsed tags into separate columns
max_tags = df['parsed_tags'].apply(len).max()

for i in range(max_tags):
    if i == 3:  # Skip creating the 4th tag column (i starts from 0, so index 3 is the 4th)
        continue
    df[f'tag_{i+1}'] = df['parsed_tags'].apply(lambda x: x[i] if len(x) > i else None)

# Drop the original tags and parsed_tags columns
df = df.drop(columns=['tags', 'parsed_tags'])

# Save the updated DataFrame to a new CSV file
df.to_csv('add_tags_data_with_individual_tags.csv', index=False)

# Display the dataframe to ensure it's working
print(df)