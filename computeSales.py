import json
import sys
import time
from datetime import datetime


def read_json_file(file_path):
    """Read and parse a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file - {file_path}")
        return None


def compute_total_sales(prices, sales):
    """Compute total sales from price catalogue and sales records."""
    total_cost = 0
    invalid_sales = []

    # Convert price catalogue to a dictionary: {title: price}
    price_dict = {item["title"]: item["price"] for item in prices}

    for sale in sales:
        product = sale.get("Product")
        quantity = sale.get("Quantity")

        if product in price_dict:
            total_cost += price_dict[product] * quantity
        else:
            invalid_sales.append(sale)

    return total_cost, invalid_sales


def main():
    # Start timer
    start_time = time.time()

    # Check if the correct number of arguments are passed
    if len(sys.argv) != 3:
        print(
            "Use: python computeSales.py priceCatalogue.json salesRecord.json"
        )
        return

    # Get file paths from command-line arguments
    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    # Read JSON files
    price_catalogue = read_json_file(price_catalogue_file)
    sales_records = read_json_file(sales_record_file)

    # Exit if either file is invalid
    if price_catalogue is None or sales_records is None:
        return

    # Compute total sales
    total_sales, invalid_sales = compute_total_sales(
        price_catalogue, sales_records
    )

    # Prepare results
    elapsed_time = round(time.time() - start_time, 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result_lines = [
        f"Sales Results (computed on {timestamp}):",
        f"Total Sales Amount: ${total_sales:.2f}",
        f"Execution Time: {elapsed_time} seconds",
        "Invalid Sales Records:",
    ]
    result_lines.extend([f"  {sale}" for sale in invalid_sales])

    # Print results to console
    for line in result_lines:
        print(line)

    # Write results to SalesResults.txt
    with open("SalesResults.txt", "w") as result_file:
        result_file.write("\n".join(result_lines))


if __name__ == "__main__":
    main()
