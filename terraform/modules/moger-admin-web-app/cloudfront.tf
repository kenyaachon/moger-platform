locals {
  s3_origin_id = "moger-admin-s3-Origin"
}

resource "aws_cloudfront_origin_access_control" "moger_admin" {
  name                              = aws_s3_bucket.moger_admin.bucket_regional_domain_name
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

data "aws_cloudfront_cache_policy" "moger_admin" {
  name = "Managed-CachingOptimized"
}

resource "aws_cloudfront_distribution" "moger_admin_distribution" {

  origin {
    domain_name              = aws_s3_bucket.moger_admin.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.moger_admin.id
    origin_id                = aws_s3_bucket.moger_admin.bucket_regional_domain_name
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Cloudfront distribution for moger admin web app"
  default_root_object = "index.html"
  price_class         = "PriceClass_All"
  retain_on_delete    = false
  wait_for_deployment = true
  aliases             = ["moger-admin-${var.env}.${var.domain_name}"]

  custom_error_response {
    error_caching_min_ttl = 10
    error_code            = 403
    response_code         = 200
    response_page_path    = "/index.html"
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods    = ["GET", "HEAD"]
    target_origin_id = aws_s3_bucket.moger_admin.bucket_regional_domain_name
    cache_policy_id  = data.aws_cloudfront_cache_policy.moger_admin.id

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.moger_admin_cert.arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
    
  }
}