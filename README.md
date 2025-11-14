# ecom-synth

A simple synthetic E-Commerce data pipeline built using Python and SQLite.
The project was developed in Cursor IDE as part of an A-SDLC exercise.

## Features
- Generates ~5 synthetic CSV datasets (customers, products, orders, etc.)
- Ingests all generated data into a SQLite database (`ecom.db`)
- Performs a multi-table JOIN using SQL
- Exports the final joined result to `output/order_lines.csv`

## Project Structure
