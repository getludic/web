locals {
  domain_aliases = [var.domain_name, "www.${var.domain_name}"]
}

# ── ACM certificate (must be in us-east-1 for CloudFront) ─────────────────────

resource "aws_acm_certificate" "app" {
  provider = aws.us_east_1

  domain_name               = var.domain_name
  subject_alternative_names = ["www.${var.domain_name}"]
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# Waits until the DNS validation CNAMEs are visible. With external DNS (name.com)
# this means terraform apply will pause here until you add the records shown in
# the `acm_dns_validation_records` output.
resource "aws_acm_certificate_validation" "app" {
  provider = aws.us_east_1

  certificate_arn = aws_acm_certificate.app.arn
}

# ── Origin Access Control: lets CloudFront SigV4-sign Function URL requests ──

# Copies the viewer's original Host into X-Forwarded-Host BEFORE CloudFront
# rewrites Host to the origin's hostname for SigV4 signing. The app reads
# this back via TrustForwardedHostMiddleware so request.url_for() produces
# canonical getludic.dev URLs instead of the raw Lambda URL.
resource "aws_cloudfront_function" "forward_host" {
  name    = "${var.app_name}-forward-host"
  runtime = "cloudfront-js-2.0"
  comment = "Copy viewer Host into X-Forwarded-Host"
  publish = true
  code    = <<-EOT
    function handler(event) {
      var req = event.request;
      if (req.headers.host) {
        req.headers['x-forwarded-host'] = { value: req.headers.host.value };
      }
      return req;
    }
  EOT
}

# ── CloudFront distribution ───────────────────────────────────────────────────
#
# Note: Function URL is AuthType=NONE, so CloudFront does NOT SigV4-sign
# origin requests (no OAC). OAC for Lambda Function URLs has a known
# body-signing bug that breaks POST requests with InvalidSignatureException.
# The Function URL is publicly addressable but lives on an obscure random
# hostname; for this app (no sensitive data) that's acceptable.

resource "aws_cloudfront_distribution" "app" {
  enabled         = true
  is_ipv6_enabled = true
  http_version    = "http2and3"
  price_class     = "PriceClass_100" # NA + EU edges; cheapest, covers EU/US users
  aliases         = local.domain_aliases
  comment         = var.app_name

  origin {
    domain_name = replace(replace(aws_lambda_function_url.app.function_url, "https://", ""), "/", "")
    origin_id   = "lambda-url"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id       = "lambda-url"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true

    # Managed policies:
    #   CachingDisabled (4135ea2d-6df8-44a3-9df3-4b5a84be39ad)
    #     Default. The app renders HTML dynamically; caching at edge would
    #     break session-aware demos. Tune later per-path if useful.
    #   AllViewerExceptHostHeader (b689b0a8-53d0-40ab-baf2-68738e2966ac)
    #     Forwards everything to Lambda EXCEPT the Host header (Lambda needs
    #     the function URL's host for TLS; the original host arrives via
    #     X-Forwarded-Host / CloudFront-* headers).
    cache_policy_id          = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad"
    origin_request_policy_id = "b689b0a8-53d0-40ab-baf2-68738e2966ac"

    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.forward_host.arn
    }
  }

  # Cache static assets aggressively — they're versioned by URL via Ludic.
  ordered_cache_behavior {
    path_pattern           = "/static/*"
    target_origin_id       = "lambda-url"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true

    # CachingOptimized
    cache_policy_id          = "658327ea-f89d-4fab-a63d-7e88639e58f6"
    origin_request_policy_id = "b689b0a8-53d0-40ab-baf2-68738e2966ac"

    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.forward_host.arn
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.app.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}
