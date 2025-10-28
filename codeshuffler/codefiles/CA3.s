      bne x22, x23, Else
      add x19, x20, x21
      beq x0,x0,Exit 
Else: sub x19, x20, x21
Exit: …

#Incorrect lines
incorrect_lines = {
    "bne x22, x23, Else": "beq x22, x23, Else",
    "Else: sub x19, x20, x21": "Else: sub x19, x21, x20",
}