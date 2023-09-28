resource "aws_s3_bucket" "moger_admin" {
  bucket = "moger-admin-${var.env}"
}

resource "aws_s3_bucket_public_access_block" "moger_admin_public_access" {
  bucket = aws_s3_bucket.moger_admin.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "aws_iam_policy_document" "moger_admin_policy" {
  statement {
    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }
    actions = ["s3:GetObject"]

    resources = [aws_s3_bucket.moger_admin.arn, "${aws_s3_bucket.moger_admin.arn}/*"]

    condition {
      test     = "StringLike"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.moger_admin_distribution.arn]
    }
  }
}