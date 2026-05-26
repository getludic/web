"""Build the search index and upload it to S3.

Usage:
    INDEX_S3_BUCKET=my-bucket uv run python scripts/build_search_index.py
"""

import asyncio
import os
import sys


async def main() -> None:
    bucket = os.environ.get("INDEX_S3_BUCKET")
    if not bucket:
        print("ERROR: INDEX_S3_BUCKET env var is required", file=sys.stderr)
        sys.exit(1)

    from web.search.cache import save_to_s3
    from web.search.index import build_index
    from web.server import app

    print("Building search index...")
    index = await build_index(app)
    print(f"Indexed {len(index.documents)} documents, {len(index.index)} tokens")

    save_to_s3(index, bucket)
    print(f"Uploaded to s3://{bucket}/search_index.pkl")


asyncio.run(main())
