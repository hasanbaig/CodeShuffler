class userProfile:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone    
    def get_email(self):                   
        return self.email        
    def get_email_phone(self):             
        return self.email, self.phone
sumaiya = userProfile("Sumaiya", "sumaiya@mail.com", 1234567)
