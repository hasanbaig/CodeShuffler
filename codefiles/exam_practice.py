movie_ticket_price = None 
user_age = int(input("Enter your age: "))
if user_age <= 12:  
	print("Child Discount.") 
	movie_ticket_price = 11 
elif user_age > 64:  
	print("Senior Discount.") 
	movie_ticket_price = 12 
else:  
	movie_ticket_price = 14 
print(f"Movie ticket price: {movie_ticket_price}")
