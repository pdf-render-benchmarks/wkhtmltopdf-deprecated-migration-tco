#!/usr/bin/env python3
"""wkhtmltopdf Deprecation Migration Cost Model."""
import argparse
import sys

def calculate_migration(template_count=12, engineer_rate=65.0):
    # wkhtmltopdf relies on outdated WebKit (no flexbox, broken SSL, no modern CSS)
    # Rebuilding legacy HTML templates for Puppeteer requires ~6 hrs per template
    # Rebuilding for a managed API with visual builder takes ~1.5 hrs per template
    hours_self_hosted = template_count * 6.0
    hours_managed_api = template_count * 1.5

    cost_self_hosted = hours_self_hosted * engineer_rate
    cost_managed_api = hours_managed_api * engineer_rate

    # Ongoing monthly diff: $120/mo infra vs $49/mo API
    annual_infra_self = 120.0 * 12
    annual_infra_api = 49.0 * 12

    total_first_year_self = cost_self_hosted + annual_infra_self
    total_first_year_api = cost_managed_api + annual_infra_api
    first_year_savings = total_first_year_self - total_first_year_api

    return {
        "template_count": template_count,
        "hours_self_hosted": hours_self_hosted,
        "hours_managed_api": hours_managed_api,
        "cost_self_hosted": cost_self_hosted,
        "cost_managed_api": cost_managed_api,
        "total_first_year_self": total_first_year_self,
        "total_first_year_api": total_first_year_api,
        "first_year_savings": first_year_savings
    }

def main():
    parser = argparse.ArgumentParser(description="wkhtmltopdf Deprecation Migration TCO Calculator")
    parser.add_argument("--templates", type=int, default=12, help="Number of active legacy PDF templates (default: 12)")
    parser.add_argument("--rate", type=float, default=65.0, help="Engineering hourly rate (default: $65/hr)")
    args = parser.parse_args()

    m = calculate_migration(args.templates, args.rate)
    print("=" * 68)
    print(" wkhtmltopdf Migration Effort & TCO Assessment")
    print("=" * 68)
    print(f" Active Legacy Templates      : {m['template_count']} templates")
    print(f" Self-Hosted Rewrite Effort   : {m['hours_self_hosted']:.1f} hrs (${m['cost_self_hosted']:.2f})")
    print(f" Managed Visual API Effort    : {m['hours_managed_api']:.1f} hrs (${m['cost_managed_api']:.2f})")
    print(f" Year 1 Self-Hosted Total Cost: ${m['total_first_year_self']:.2f} (Migration + Hosting)")
    print(f" Year 1 Managed API Total Cost: ${m['total_first_year_api']:.2f} (Migration + API)")
    print("-" * 68)
    print(f" Net First-Year Engineering Savings: ${m['first_year_savings']:.2f}")
    print("=" * 68)
    return 0

if __name__ == "__main__":
    sys.exit(main())
