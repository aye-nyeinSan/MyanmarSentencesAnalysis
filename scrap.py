import facebook_scraper as fs
import pandas as pd

print("🔥 Facebook Comment Scraper 🔥")
# ✅ Your actual cookies from Facebook (edit manually or export from browser)
cookies = {
    "c_user": "100007141636057",
    "xs": "21%3AtW04NP0R1-b_Jw%3A2%3A1742789829%3A-1%3A10456%3AnqYAVQEk_lapfA%3AAcVXkTHLHB-xBh3dK8lylA_W5jf8EUhudMVrbNCzCg"
}

# ✅ The full post URL
POST_URL = "https://www.facebook.com/bbcnews/posts/pfbid02wvyNkAxbr66hbWQpKGZLDgsZUVR45fFM3tqpReca4DRM7KsBUz2WaVa2Vo71T3bDl"


# ✅ Max comments to load
MAX_COMMENTS = 100

# ✅ Fetch the post with comments
print("⏳ Fetching post...")
gen = fs.get_posts(
    post_urls=[POST_URL],
    options={
        "comments": MAX_COMMENTS,
        "progress": True,
        "allow_extra_requests": True
    }
)

try:
    post = next(gen)
except Exception as e:
    print(f"❌ Error: {e}")
    exit()

print("\n🔍 Available post keys:")
print(list(post.keys()))

# ✅ Extract comments
comments = post.get("comments_full", [])
print(f"\n✅ Total comments found: {len(comments)}")

# Preview first few comments
if comments:
    print("\n📄 Comments Preview:")
    for i, c in enumerate(comments[:5], 1):
        print(f"{i}. {c.get('comment_text')}")
else:
    print("⚠️ No comments found or unable to scrape them.")

# ✅ Create DataFrame
comment_data = []
for comment in comments:
    comment_id = comment.get('comment_id', '')
    comment_text = comment.get('comment_text', '')
    comment_data.append({'comment_id': comment_id, 'comment_text': comment_text})


comment_df = pd.DataFrame(comment_data)

# ✅ Preview the first few rows
print("\n📄 Scraped Comments Preview:\n")
for i, row in enumerate(comment_data[:10], start=1):
    print(f"Comment #{i}")
    print(f"ID   : {row['comment_id']}")
    print(f"Text : {row['comment_text']}\n")

# # ✅ Save to CSV
# comment_df.to_csv("t1_facebook_comment.csv", index=False)
# print("✅ Comments saved to t1_facebook_comment.csv")
