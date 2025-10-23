
# Lost and Found Management System for University
import datetime

class Item:
	def __init__(self, name, description, location, date, reporter):
		self.name = name
		self.description = description
		self.location = location
		self.date = date
		self.reporter = reporter

	def __str__(self):
		return f"Name: {self.name}\nDescription: {self.description}\nLocation: {self.location}\nDate: {self.date}\nReporter: {self.reporter}"

class LostAndFound:
	def __init__(self):
		self.lost_items = []
		self.found_items = []

	def report_lost(self, item):
		self.lost_items.append(item)

	def report_found(self, item):
		self.found_items.append(item)

	def search_items(self, keyword, item_type='all'):
		results = []
		items = []
		if item_type == 'lost' or item_type == 'all':
			items += self.lost_items
		if item_type == 'found' or item_type == 'all':
			items += self.found_items
		for item in items:
			if keyword.lower() in item.name.lower() or keyword.lower() in item.description.lower():
				results.append(item)
		return results

	def list_items(self, item_type='all'):
		if item_type == 'lost':
			return self.lost_items
		elif item_type == 'found':
			return self.found_items
		else:
			return self.lost_items + self.found_items

def main():
	system = LostAndFound()
	while True:
		print("\n--- University Lost and Found ---")
		print("1. Report Lost Item")
		print("2. Report Found Item")
		print("3. Search Items")
		print("4. List All Lost Items")
		print("5. List All Found Items")
		print("6. Exit")
		choice = input("Select an option: ")
		if choice == '1':
			name = input("Item name: ")
			desc = input("Description: ")
			loc = input("Where was it lost?: ")
			date = input("Date lost (YYYY-MM-DD): ")
			reporter = input("Your name: ")
			item = Item(name, desc, loc, date, reporter)
			system.report_lost(item)
			print("Lost item reported.")
		elif choice == '2':
			name = input("Item name: ")
			desc = input("Description: ")
			loc = input("Where was it found?: ")
			date = input("Date found (YYYY-MM-DD): ")
			reporter = input("Your name: ")
			item = Item(name, desc, loc, date, reporter)
			system.report_found(item)
			print("Found item reported.")
		elif choice == '3':
			keyword = input("Enter keyword to search: ")
			results = system.search_items(keyword)
			if results:
				print(f"Found {len(results)} item(s):")
				for item in results:
					print("-"*20)
					print(item)
			else:
				print("No items found.")
		elif choice == '4':
			items = system.list_items('lost')
			if items:
				for item in items:
					print("-"*20)
					print(item)
			else:
				print("No lost items reported.")
		elif choice == '5':
			items = system.list_items('found')
			if items:
				for item in items:
					print("-"*20)
					print(item)
			else:
				print("No found items reported.")
		elif choice == '6':
			print("Goodbye!")
			break
		else:
			print("Invalid option. Try again.")

if __name__ == "__main__":
	main()
