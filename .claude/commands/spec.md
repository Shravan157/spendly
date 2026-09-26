---
description: Generate a comprehensive Technical & Product Specification document
argument-hint: "[Project Name]"
allowed-tools: Read, Bash, Artifact
---
# Task: Generate Technical & Product Specification

The user wants to create a professional technical specification for a project.

## Step 1 — Parse Input
Extract the project name from $ARGUMENTS. If $ARGUMENTS is empty, use "Untitled Project".

## Step 2 — Research (if applicable)
If the project name corresponds to a feature or codebase already present in the repository:
1. Use `Grep` and `Read` to understand the current implementation, requirements, or existing notes.
2. Identify key components, API endpoints, and data models.

## Step 3 — Draft Specification
Create a detailed document following this exact structure:

### 1. Document Metadata
- Author: Claude Code
- Status: Draft
- Last Updated: [Current Date]
- Target Release: [Suggested based on context or "TBD"]
- Tracking Link: [TBD]

### 2. Executive Summary & Objectives
- **Problem Statement**: Define the pain point being solved.
- **Core Goals**: List 2-3 high-level technical and product targets.
- **Non-Goals**: Explicitly list what is out-of-scope to prevent scope creep.

### 3. Requirements
- **Functional Requirements**: User-facing features (FR-1, FR-2, etc.).
- **Non-Functional Requirements**: Scalability, Security, Availability constraints.

### 4. Proposed Architecture & System Design
- **High-Level Architecture**: Provide an ASCII or Mermaid diagram of component interaction.
- **Data Model**: Provide SQL schema or entity-relationship descriptions.
- **API Contracts**: Define endpoints, request payloads, and response examples.

### 5. Alternatives Considered & Trade-offs
- Compare the chosen approach with at least one alternative.
- Explain why the current approach was selected.

### 6. Operational Plan
- **Testing Strategy**: Define unit and integration test goals.
- **Deployment Phases**: Outline a phased rollout (e.g., Staging -> Canary -> Production).
- **Rollback Plan**: Define the trigger and action for reverting changes.

## Step 4 — Output
1. Generate the specification as a Markdown document.
2. If the project is significant, offer to publish it as an Artifact for better sharing and review.
