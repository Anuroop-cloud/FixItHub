import os
import praw
import google.generativeai as genai
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Reddit Service ---
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

reddit = None
if REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET and REDDIT_USER_AGENT:
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )
        print("PRAW Reddit instance created successfully.")
    except Exception as e:
        print(f"Error creating PRAW Reddit instance: {e}")

def get_reddit_posts(subreddit_name: str, limit: int = 10):
    if not reddit:
        raise Exception("Reddit API credentials are not configured. Cannot fetch posts.")

    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.hot(limit=limit):
        # We only want text posts for now
        if not post.is_self:
            continue

        posts.append({
            "id": post.id,
            "title": post.title,
            "selftext": post.selftext,
            "created_utc": post.created_utc,
            "score": post.score,
            "subreddit": post.subreddit.display_name,
            "author_username": post.author.name if post.author else "N/A",
            "author_karma": post.author.link_karma + post.author.comment_karma if post.author else 0,
        })
    return posts

# --- Gemini Service ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

gemini_model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-pro')
        print("Gemini model configured successfully.")
    except Exception as e:
        print(f"Error configuring Gemini model: {e}")

def process_text_with_gemini(text: str, source: str):
    if not gemini_model:
        # If Gemini is not configured, return a placeholder response
        return {
            "summary": "This is a placeholder summary. Configure Gemini API key to enable AI processing.",
            "keywords": ["placeholder", "ai"],
            "category": "Other",
        }

    prompt_template = f"""
    Summarize this problem in 3 sentences or less.
    Extract 3-5 keywords as a comma-separated list.
    Categorize it into one of the following: Traffic, Environment, Education, Healthcare, Governance, Technology, Other.
    Return a single, minified JSON object with three keys: "summary", "keywords", "category".

    Problem: "{text}"
    Source: {source}
    """

    try:
        response = gemini_model.generate_content(prompt_template)
        # Clean up the response to make it valid JSON
        json_response_str = response.text.strip().replace('`', '').replace('json', '').strip()
        result = json.loads(json_response_str)

        # Ensure keywords are a list of strings
        if isinstance(result.get("keywords"), str):
            result["keywords"] = [k.strip() for k in result["keywords"].split(',')]

        return result
    except Exception as e:
        print(f"Error processing text with Gemini: {e}")
        # Fallback to placeholder if API call fails
        return {
            "summary": f"AI processing failed: {e}",
            "keywords": ["error"],
            "category": "Other",
        }
