# CloudShop Architecture

## Overview

CloudShop is a production-style AWS cloud platform built with Terraform, Docker, GitHub Actions, and modern AWS services.

The goal is to demonstrate real-world cloud architecture rather than isolated AWS examples.

---

# Current Architecture

                 Internet
                     │
               API Gateway
                     │
                 AWS Lambda
                     │
                 DynamoDB

Terraform Backend

S3
│
└── terraform.tfstate

DynamoDB
│
└── State Lock

GitHub

↓

GitHub Actions

↓

OIDC

↓

Terraform

↓

AWS

---

# Networking

VPC

10.0.0.0/16

Public Subnets

10.0.1.0/24

10.0.2.0/24

Private Subnets

10.0.101.0/24

10.0.102.0/24

Internet Gateway

Public Route Table

Private Route Table

---

# Container Platform

FastAPI

↓

Docker

↓

Amazon ECR

The Docker image is stored in Amazon ECR and will be deployed to ECS Fargate.

---

# Current AWS Services

Terraform

GitHub Actions

IAM

OIDC

Lambda

API Gateway

DynamoDB

CloudWatch

S3

VPC

Internet Gateway

Subnets

ECR

---

# Planned Architecture

Users

↓

Route53

↓

CloudFront

↓

AWS WAF

↓

Application Load Balancer

↓

ECS Fargate

↓

PostgreSQL (RDS)

↓

SNS

↓

SQS

↓

Lambda Workers

↓

CloudWatch

↓

X-Ray

↓

Secrets Manager

↓

KMS

---

# Learning Objectives

Learn Infrastructure as Code with Terraform

Learn AWS networking

Learn serverless architecture

Learn containers with Docker

Deploy applications to ECS

Design secure AWS architectures

Implement production CI/CD

Monitor applications

Optimize for scalability and cost

