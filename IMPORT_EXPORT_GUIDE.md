# Import/Export Guide for Talinda POS System

This guide explains how to use the import and export functionality for products and categories in the Talinda POS system.

## Overview

The Import/Export feature allows you to:
- Export existing products and categories to Excel files
- Import products and categories from Excel files
- Download template files to understand the required format
- Update existing items during import

## Accessing Import/Export

1. Open the Talinda POS system
2. Navigate to **Product Management**
3. Click on the **Import/Export** tab

## Exporting Data

### Export Products
1. Click the **Export Products** button
2. Choose a location and filename for the Excel file
3. The system will export all products with the following columns:
   - Name
   - Description
   - Price
   - Category
   - Barcode
   - Image Path

### Export Categories
1. Click the **Export Categories** button
2. Choose a location and filename for the Excel file
3. The system will export all categories with the following columns:
   - Name
   - Description
   - Tax Rate (%)
   - Product Count

## Importing Data

### Before Importing
1. **Download Templates**: Use the template download buttons to get sample files
2. **Prepare Your Data**: Fill in the template with your product/category data
3. **Check Format**: Ensure your Excel file follows the template structure

### Import Options
- **Update Existing Items**: Check this box if you want to update existing products/categories with the same name or barcode
- **Skip Existing Items**: Leave unchecked to skip items that already exist

### Import Products
1. Click the **Import Products** button
2. Select your Excel file
3. Choose whether to update existing items
4. Confirm the import operation
5. Review the results in the status section

### Import Categories
1. Click the **Import Categories** button
2. Select your Excel file
3. Choose whether to update existing items
4. Confirm the import operation
5. Review the results in the status section

## Excel File Format

### Products Sheet
| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| Name | Yes | Product name | "Coffee" |
| Description | No | Product description | "Hot coffee drink" |
| Price | Yes | Product price (must be > 0) | 5.99 |
| Category | No | Category name | "Beverage" |
| Barcode | No | Product barcode | "1234567890" |
| Image Path | No | Path to product image | "images/coffee.jpg" |

### Categories Sheet
| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| Name | Yes | Category name | "Food" |
| Description | No | Category description | "Food items and meals" |
| Tax Rate (%) | No | Tax rate percentage | 14.0 |

## Import Rules

### Products
- **Name and Price** are required fields
- **Category** will be created automatically if it doesn't exist
- **Barcode** must be unique (if provided)
- **Price** must be greater than 0
- Existing products are identified by name or barcode

### Categories
- **Name** is the only required field
- **Tax Rate** defaults to 14.0% if not specified
- Existing categories are identified by name

## Error Handling

The import process provides detailed feedback:
- **Total Rows**: Number of rows processed
- **Imported**: Successfully imported items
- **Updated**: Existing items that were updated
- **Skipped**: Items that were skipped (duplicates, invalid data)
- **Errors**: List of specific errors encountered

### Common Errors
- **Invalid name or price**: Missing or invalid required fields
- **Product already exists**: Duplicate product found
- **Category already exists**: Duplicate category found
- **Invalid barcode**: Barcode format issues

## Best Practices

1. **Backup First**: Always backup your data before importing
2. **Test with Small Files**: Test the import process with a few items first
3. **Use Templates**: Download and use the provided templates
4. **Validate Data**: Check your Excel file for errors before importing
5. **Review Results**: Always review the import results and error messages

## Troubleshooting

### Import Fails
- Check that your Excel file has the correct column headers
- Ensure required fields are filled
- Verify that prices are numeric and greater than 0
- Check for duplicate barcodes

### Export Fails
- Ensure you have write permissions to the selected location
- Check that the file is not open in another application
- Verify that you have sufficient disk space

### Template Download Fails
- Ensure Excel functionality is available (openpyxl installed)
- Check that you have write permissions to the selected location

## Technical Notes

- The system uses pandas and openpyxl for Excel operations
- Import/export operations run in background threads to prevent UI freezing
- Progress is shown in real-time during operations
- All operations are logged for debugging purposes

## Support

If you encounter issues with import/export functionality:
1. Check the status messages in the Import/Export tab
2. Review the error messages for specific issues
3. Ensure your Excel file follows the template format
4. Contact system administrator for technical support 