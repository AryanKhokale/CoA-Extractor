import json
import random

first_names = [
    "Rajesh", "Pooja", "Vikram", "Sunanda", "Ananya", "Jaswant", "Inderjit", "Praveen",
    "Gajanand", "Nilesh", "Rohit", "Meera", "Arun", "Sangeeta", "Deepak", "Sneha",
    "Amit", "Kavita", "Rahul", "Priyanka", "Vivek", "Tanvi", "Siddharth", "Neha",
    "Manoj", "Divya", "Suresh", "Ritu", "Alok", "Swati", "Abhay", "Preeti",
    "Karthik", "Bhavna", "Hemant", "Rachna", "Ashok", "Shalini", "Sunil", "Aparna"
]

last_names = [
    "Sharma", "Verma", "Patel", "Bose", "Singh", "Chawney", "Krishnadas", "Ram",
    "Chavan", "Asthana", "Mohan", "Iyer", "Nair", "Deshmukh", "Kulkarni", "Mehta",
    "Shah", "Gupta", "Agarwal", "Reddy", "Rao", "Menon", "Joshi", "Kapoor",
    "Malhotra", "Saxena", "Bhatia", "Chopra", "Dutta", "Mukherjee", "Banerjee", "Ghosh"
]

city_state_map = [
    ("Mumbai", "Maharashtra"),
    ("Pune", "Maharashtra"),
    ("Nagpur", "Maharashtra"),
    ("Nashik", "Maharashtra"),
    ("New Delhi", "Delhi"),
    ("Bengaluru", "Karnataka"),
    ("Mysore", "Karnataka"),
    ("Chennai", "Tamil Nadu"),
    ("Coimbatore", "Tamil Nadu"),
    ("Hyderabad", "Telangana"),
    ("Kolkata", "West Bengal"),
    ("Ahmedabad", "Gujarat"),
    ("Surat", "Gujarat"),
    ("Vadodara", "Gujarat"),
    ("Jaipur", "Rajasthan"),
    ("Jodhpur", "Rajasthan"),
    ("Lucknow", "Uttar Pradesh"),
    ("Noida", "Uttar Pradesh"),
    ("Ghaziabad", "Uttar Pradesh"),
    ("Chandigarh", "Chandigarh"),
    ("Bhopal", "Madhya Pradesh"),
    ("Indore", "Madhya Pradesh"),
    ("Kochi", "Kerala"),
    ("Thiruvananthapuram", "Kerala"),
    ("Patna", "Bihar"),
    ("Ranchi", "Jharkhand"),
    ("Bhubaneswar", "Odisha"),
    ("Guwahati", "Assam"),
    ("Dehradun", "Uttarakhand"),
    ("Shimla", "Himachal Pradesh"),
    ("Goa", "Goa")
]

qualifications = [
    "B.Arch", "M.Arch (Urban Design)", "M.Arch (Landscape)", "B.Arch (Hons)",
    "G.D. Arch", "M.Arch (Conservation)", "M.Arch (Sustainable)", "All India Diploma in Architecture"
]

statuses = ["Active", "Active", "Active", "Defaulter", "Inactive"]

records = []
random.seed(42)

for i in range(1, 251):
    city, state = random.choice(city_state_map)
    reg_year = random.randint(1975, 2024)
    reg_num = f"CA/{reg_year}/{str(i * 137 % 90000 + 10000).zfill(5)}"
    prefix = random.choice(["Ar.", "Mr.", "Ms.", "Dr."])
    fname = random.choice(first_names)
    lname = random.choice(last_names)
    full_name = f"{prefix} {fname} {lname}"
    
    val_year = reg_year + random.randint(1, 40)
    if val_year > 2026:
        val_year = 2026
        status = "Active"
    else:
        status = random.choice(["Defaulter", "Inactive"])
        
    val_date = f"31/12/{val_year}"
    qual = random.choice(qualifications)
    
    records.append({
        "serial_no": i,
        "registration_number": reg_num,
        "name": full_name,
        "city": city,
        "state": state,
        "valid_up_to": val_date,
        "registration_year": reg_year,
        "qualification": qual,
        "status": status,
        "address": f"{random.randint(10, 999)}, Sector {random.randint(1, 50)}, {city} - {random.randint(100001, 799999)}",
        "raw_data": {
            "sl": str(i),
            "name": full_name,
            "reg_no": reg_num,
            "city": city,
            "valid_up_to": val_date,
            "source": "Council of Architecture Directory"
        }
    })

# Add 5 deliberate duplicates for testing deduplication
for j in range(5):
    dup = dict(records[j * 10])
    dup["serial_no"] = 251 + j
    records.append(dup)

with open('mock_data/architects.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, indent=2)

print(f"Generated {len(records)} realistic architect records in mock_data/architects.json")
