resource "aws_s3_bucket" "search_index" {
  bucket = "${var.app_name}-search-index"
}

resource "aws_s3_bucket_public_access_block" "search_index" {
  bucket = aws_s3_bucket.search_index.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
