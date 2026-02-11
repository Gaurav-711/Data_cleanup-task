# Member Cleanup Script

## Overview

The marketing team exported a list of new members from three different landing pages.  
The dataset was messy and required cleaning before being used in the CRM system.

This project implements a Python script that processes the raw `signups.xls` file and generates:

- `members_final.csv` → Cleaned Golden Record
- `quarantine.csv` → Low-quality or invalid leads

---

## Problem Statement

The script handles the following business requirements:

1. **Standardize Dates**  
   All signup dates are converted to `YYYY-MM-DD` format.

2. **Deduplication**  
   Ensure only one record per member exists in the final output.

3. **Low-Quality Lead Detection**  
   Rows that appear to be test data, invalid, or structurally corrupted are moved to `quarantine.csv`.

4. **Multi-Plan Context Rule**  
   If a member signed up for multiple plans (e.g., Plan A and Plan B):
   - Keep the most recent signup
   - Add `is_multi_plan = True`

---

## Key Challenges Solved

- The `.xls` file contained improperly formatted CSV data.
- Some names included commas (e.g., "Doe, John"), which broke standard parsing.
- Gmail addresses had variations (dots and aliases) that represented the same mailbox.
- Duplicate users needed to be merged correctly while preserving business context.

---

## Cleaning Logic Applied

- Reconstructed malformed CSV rows.
- Normalized names (handled "Last, First" format).
- Standardized email formatting (Gmail alias normalization).
- Converted all dates to consistent format.
- Identified and quarantined:
  - Test users
  - Invalid domains
  - Garbage notes
- Deduplicated users at the person level.
- Computed `is_multi_plan` flag before removing duplicates.

---

## Output Files

### 1. members_final.csv
Contains the cleaned Golden Record:
- name
- email
- signup_date
- plan
- notes
- is_multi_plan

### 2. quarantine.csv
Contains removed records:
- Test entries
- Invalid emails
- Corrupted or low-quality data

---

## Installation & Setup

### Requirements

