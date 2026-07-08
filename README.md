# AWS Cloud Lab

A hands-on AWS DevOps lab built with Terraform, GitHub Actions, and serverless AWS services.

## Current Architecture

```text
GitHub
  |
  | push to main
  v
GitHub Actions
  |
  | OIDC assume role
  v
AWS IAM Role
  |
  | terraform apply
  v
API Gateway -> Lambda -> DynamoDB
