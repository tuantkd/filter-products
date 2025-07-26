import pandas as pd

import os
import glob
import pandas as pd

# Specify the folder path where Excel files are located
folder_path = 'commission_calculation'
file_result = 'commission_calculation/TienHoaHongBanHang.xlsx'
if os.path.exists(file_result):
        os.remove(file_result)

# Use glob to get all Excel files in the folder
excel_files = glob.glob(os.path.join(folder_path, '*.xlsx'))


# Load the first Excel file: BangHoaHong_KV26072025-154939-042.xlsx
file_1_path = 'commission_calculation/BangHoaHong_KV26072025-154939-042.xlsx'
file_1_path = excel_files[0]
# Get the sheet names to identify the first sheet
excel_file = pd.ExcelFile(file_1_path)
first_sheet_name = excel_file.sheet_names[0]  # Get the name of the first sheet
df_commission = pd.read_excel(file_1_path, sheet_name=first_sheet_name)

# Clean up the data: Rename columns for clarity and filter necessary columns from commission data
df_commission.columns = ['Mã hàng', 'Tên hàng', 'Đơn vị tính', 'Giá bán chung', 'Hoa Hồng Chi Nhánh Cần Thơ']
df_commission_filtered = df_commission[['Mã hàng', 'Tên hàng', 'Hoa Hồng Chi Nhánh Cần Thơ']]

# Load the second Excel file: DanhSachChiTietHoaDon_KV26072025-161619-625.xlsx
file_2_path = 'commission_calculation/DanhSachChiTietHoaDon_KV26072025-161619-625.xlsx'
file_2_path = excel_files[1]
df_sales = pd.read_excel(file_2_path)

# Filter out the necessary columns from sales data
df_sales_filtered = df_sales[['Mã hàng', 'Số lượng']]

# Merge the two datasets based on 'Mã hàng' (Product Code)
df_merged = pd.merge(df_commission_filtered, df_sales_filtered, on='Mã hàng', how='left')

# Calculate the commission amount per product sold
df_merged['Tiền hoa hồng'] = df_merged['Số lượng'] * df_merged['Hoa Hồng Chi Nhánh Cần Thơ']

# Calculate the total commission for TranThiXiu
total_commission = df_merged['Tiền hoa hồng'].sum()

# Add a row at the end showing the total commission amount
total_row = pd.DataFrame({'Mã hàng': ['Tổng tiền hoa hồng'], 'Tên hàng': [''], 'Hoa Hồng Chi Nhánh Cần Thơ': [''], 'Số lượng': [''], 'Tiền hoa hồng': [total_commission]})
df_merged = pd.concat([df_merged, total_row], ignore_index=True)

# Save the result to an Excel file
output_file = 'commission_calculation/TienHoaHongBanHang.xlsx'
df_merged.to_excel(output_file, index=False)

# Print the final result
print(f"Data has been saved to {output_file}")
print(f"Total Commission: {total_commission}")
