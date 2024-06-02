import re

# Extract the number of upvotes from a comment string.
def extract_upvotes(comment):
    match = re.search(r'\((\d+) upvotes\)', comment)
    return int(match.group(1)) if match else 0

# Parse the input string and organize it into comments and their responses.
def extract_comments(input_string):
    lines = input_string.strip().split('\n')
    comments = []
    current_comment = None

    for line in lines:
        depth = line.count('| ') - 1
        if depth == 0:
            if current_comment:
                comments.append(current_comment)
            current_comment = {'text': line, 'responses': []}
        elif current_comment:
            current_comment['responses'].append(line)
    
    if current_comment:
        comments.append(current_comment)
    
    return comments

# Sort the comments by upvotes and return the top n comments
# and their responses.
def get_top_n_comments(comments, n=3):
    comments.sort(key=lambda x: extract_upvotes(x['text']), reverse=True)
    top_comments = comments[:n]
    result = []

    for comment in top_comments:
        result.append(comment['text'])
        result.extend(comment['responses'])
    
    return '\n'.join(result)

def calculate_haiku_cost(message):
    input_tokens = message.usage.input_tokens
    output_tokens = message.usage.output_tokens
    input_cost = 0.25 * (input_tokens / 1_000_000)
    output_cost = 1.25 * (output_tokens / 1_000_000)
    total_cost = input_cost + output_cost
    print("This cost ${:.2f} + ${:.2f} = ${:.2f}.".format(input_cost, output_cost, total_cost))