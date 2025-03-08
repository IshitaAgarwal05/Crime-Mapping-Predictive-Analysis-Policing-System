import csv

# Define the data
users = [
    ['user_id', 'pwd'],
    ['admin', 'admin123'],
    ['user1', 'password1'],
    ['user2', 'password2']
]

# Specify the filename
filename = 'users.csv'

# Write to CSV
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(users)

print(f"CSV file '{filename}' created successfully!")
