# AI-Assisted TRIZ Engineering Problem Solver - Technical Requirement Document

**Version**: 1.0  
**Date**: 2025-12-28  
**Architecture**: Python Backend with strict typing

---

## 1. System Overview
The "Blue Box" TRIZ Engine is a software component designed to guide engineers through resolving technical contradictions using the classical TRIZ framework (ARIZ logic). It abstracts the complexity of the Altshuller Matrix and Inventive Principles into a streamlined workflow.

## 2. Data Model & Knowledge Base

### 2.1 Engineering Parameters (39 Attributes)
Standard parameters describing physical systems.
*   **Format**: JSON
*   **Fields**: `id` (int), `name` (str), `description` (str), `keywords` (list[str])

### 2.2 Inventive Principles (40 Principles)
The solutions provided by TRIZ.
*   **Format**: JSON
*   **Fields**: `id` (int), `name` (str), `description` (str), `examples` (list[str])

### 2.3 Contradiction Matrix
Mapping between Improving vs. Worsening parameters.
*   **Structure**: Sparse Matrix or Hash Map.
*   **Key**: `(improving_id, worsening_id)`
*   **Value**: `list[principle_ids]`

## 3. Core Algorithms

### 3.1 Problem Normalization (Text-to-Parameter)
*   **Input**: Natural language string (e.g., "The object is too heavy").
*   **Logic**: 
    1.  Keyword matching / Semantic similarity.
    2.  Map to one of the 39 Parameters.
*   **Output**: `ParameterID` or `AmbiguousError`.

### 3.2 Matrix Lookup Engine
*   **Input**: `improving_id` (int), `worsening_id` (int).
*   **Logic**:
    1.  Check for Physical Contradiction (improving == worsening). If true, return Separation Principles.
    2.  Lookup standard matrix.
    3.  If empty cell, return Heuristic Top 4 principles (#35, #10, #1, #28).
*   **Output**: List of `InventivePrinciple` objects.

### 3.3 Ideality Calculator
*   **Formula**: `Ideality = Benefits / (Costs + Harms)`
*   **Inputs**: User-rated effectiveness of benefits vs cost/harm impact.

## 4. Workflow State Machine

1.  **Stage 1: System Definition**
    *   Goal: Define System Name, Primary Function.
    *   Data: 9-Windows Context (Past/Present/Future x Sub/System/Super).

2.  **Stage 2: Contradiction Definition**
    *   Goal: Identify "What gets better?" vs "What gets worse?".
    *   Action: Normalize inputs to Parameters (1-39).

3.  **Stage 3: Solver Execution**
    *   Action: Matrix Lookup.
    *   Result: List of Principles.

4.  **Stage 4: Solution Instantiation**
    *   Action: User maps Principles to concrete ideas.
    *   Action: Calculate Ideality of new solution.

## 5. API / Interface Specification

### Class: `TRIZSolverEngine`
*   `load_knowledge_base(path: str)`: Load JSON data.
*   `normalize_input(text: str) -> Parameter`: Guess parameter from text.
*   `solve_contradiction(imp: int, wor: int) -> SolutionReport`: Get principles.
*   `calculate_ideality(benefits: list, costs: list) -> float`: Score solution.

---
**Implementation Note**:
This document serves as the basis for the `src` directory implementation.
