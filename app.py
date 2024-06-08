from reddit2text import Reddit2Text
from openai import OpenAI
import streamlit as st

# import config
import functions
import system_instructions

# Send to openai.
client = OpenAI(
    **st.secrets.openai
)

# Create Reddit2Text.
r2t = Reddit2Text(
    **st.secrets.reddit2text,
    max_comment_depth=3
)

st.header('Summarize Reddit Threads easily!', divider='red')
st.subheader('Paste a Reddit link and watch as OpenAI summarizes its key points.')

reddit_url = st.text_input("Reddit Link")

if st.button("Summarize"):
    with st.spinner("Summarizing..."):
        output = r2t.textualize_post(reddit_url)

        # Get the reddit title and reddit body text to summarize.
        reddit_title = functions.extract_op_metadata(output, "Title:")
        reddit_body_text = functions.extract_op_metadata(output, "Body text:")

        # Truncate Reddit thread to top n_comments comments by upvotes, and their max_comment_depth replies.
        comments = output.split("--------\n")[1]
        parsed_comments = functions.extract_comments(comments)
        top_comments = functions.get_top_n_comments(parsed_comments)

        title_summary = functions.send_message(client, system_instructions.title_and_body_text_summarization, f"{reddit_title}: {reddit_body_text}")
        comment_summary = functions.send_message(client, system_instructions.comment_summarization, top_comments)
    
    st.success("Done!")
    st.header("OpenAI said...")
    st.write(title_summary.choices[0].message.content)
    st.write(comment_summary.choices[0].message.content)

# TODO Pull request to handle posts with no body text e.g. https://www.reddit.com/r/nba/comments/1d9yjev/highlight_jaylen_brown_throws_crosses_luka_doncic/
# TODO Create blog
# TODO Deploy

# NOTE In the future, I can improve summarization of OP by fine-tuning a model
#      on tldr dataset