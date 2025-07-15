slli x28, x28, 2
add x5, x28, x18
lw x21, 0(x5)
addi x23, x21, 10
sw x23, 8(x20)

#Incorrect lines
slli x28,x28, 4
sw x23, 2(x20)