name = "Hunter Russo"
target_companies = ["Tesla", "Samsung", "AMD"]
applications_sent = 0

def apply_to_job(company):
    print("Applying to", company, "...")

for company in target_companies:
    apply_to_job(company)
    applications_sent += 1

print("Total applications sent:", applications_sent)