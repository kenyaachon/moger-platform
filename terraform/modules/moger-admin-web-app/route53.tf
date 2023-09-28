locals {
  moger_admin_domain_name = "moger-admin-${var.env}.${var.domain_name}"
}

resource "aws_route53_record" "moger_admin_domain_A" {
  name    = local.moger_admin_domain_name
  zone_id = var.route53_public_zone_id
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.moger_admin_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.moger_admin_distribution.hosted_zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "moger_admin_domain_AAAA" {
  name    = local.moger_admin_domain_name
  zone_id = var.route53_public_zone_id
  type    = "AAAA"

  alias {
    name                   = aws_cloudfront_distribution.moger_admin_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.moger_admin_distribution.hosted_zone_id
    evaluate_target_health = true
  }
}

resource "aws_acm_certificate" "moger_admin_cert" {
  domain_name       = local.moger_admin_domain_name
  validation_method = "DNS"

  provider = aws.us-east-1
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate_validation" "moger_admin_cert" {
  certificate_arn         = aws_acm_certificate.moger_admin_cert.arn
  validation_record_fqdns = [for record in aws_route53_record.moger_admin_cert : record.fqdn]
  provider = aws.us-east-1
}

resource "aws_route53_record" "moger_admin_cert" {
  for_each = {
    for dvo in aws_acm_certificate.moger_admin_cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = var.route53_public_zone_id
}