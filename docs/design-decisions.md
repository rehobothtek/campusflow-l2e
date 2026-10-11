# CampusFlow design decisions

## Current status

This is the initial team design plan prepared by Engineer A. Engineer B will review and confirm the shared decisions before beginning their feature work.

## Ticket storage

Tickets will be stored in a Python list of dictionaries. Each dictionary will contain:

- id
- title
- category
- urgency
- affected_users
- priority
- status
- assigned_to

The list will be passed into business-logic functions so that the logic can be tested without terminal input.

## Validation and errors

Business-logic functions will reject invalid input by raising `ValueError` with clear messages. The command-line interface will catch these errors and display helpful feedback without crashing or changing valid ticket data.

## Function return values

- Ticket creation will return the newly created ticket dictionary.
- Ticket lookup will return the matching ticket dictionary or raise an error if it does not exist.
- Assignment and status-update functions will return the updated ticket dictionary.

## JSON persistence

A separate storage module will load tickets from JSON at startup and save tickets to JSON when requested or when the user exits.

A missing JSON file means a fresh start. Malformed JSON must show a clear error and must not be overwritten automatically.

## Testability

Interactive input and printing will remain in `main.py`. Ticket creation, validation, priority calculation, workflow, reports, and storage will be ordinary functions so they can be tested using `unittest`.

## Initial ownership plan

- Engineer A: ticket creation, input validation, ticket IDs, priority calculation, and matching tests.
- Engineer B: assignment, ticket status workflow, work queue, reports, and matching tests.
- Both engineers: JSON integration, PR review, final testing, documentation, and demonstration.