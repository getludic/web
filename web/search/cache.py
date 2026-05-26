import logging
import pickle

from .index import Index

logger = logging.getLogger(__name__)

_CACHE_KEY = "search_index.pkl"


def save_to_s3(index: Index, bucket: str) -> None:
    import boto3  # type: ignore[import-untyped]

    boto3.client("s3").put_object(
        Bucket=bucket, Key=_CACHE_KEY, Body=pickle.dumps(index)
    )
    logger.info("Search index uploaded to s3://%s/%s", bucket, _CACHE_KEY)


def load_from_s3(bucket: str) -> Index | None:
    """Fetch a prebuilt index from S3.

    Unpickling is safe here because the bucket is private and writable only
    by the CI deploy role (see terraform/iam.tf).
    """
    import boto3  # type: ignore[import-untyped]
    from botocore.exceptions import ClientError  # type: ignore[import-untyped]

    try:
        obj = boto3.client("s3").get_object(Bucket=bucket, Key=_CACHE_KEY)
        index: Index = pickle.loads(obj["Body"].read())  # noqa: S301
        logger.info("Search index loaded from s3://%s/%s", bucket, _CACHE_KEY)
        return index
    except ClientError:
        logger.warning("Search index not found in s3://%s, rebuilding", bucket)
        return None
