
.globl variables

.text
variables:
    li $t0, 1
    li $t1, 2
L1:
    beq $t0, 0, L2
    beq $t0, 1, L3
    mul $a0, $t0, $t1
    li $v0, 1
    syscall
L2:
    add $a0, $t0, $t1
    li $v0, 1
    syscall
L3:
    sub $a0, $t0, $t1
    li $v0, 1
    syscall


end:
li $v0, 10
syscall
