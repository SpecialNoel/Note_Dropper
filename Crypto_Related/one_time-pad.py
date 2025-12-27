# one_time_pad.py
# This file is used to try out some techniques mentioned in Crypto101.pdf.

# Bit-wise XOR Rules: 
# 1. a^(b^c) = (a^b)^c
# 2. a^b = b^a
# 3. a^a = 0
# 4. a^0 = a
# 5. a^b^a = b

# **One-Time Pad**: utilizes the XOR operation only
# If we translate our plaintext P into a sequence of bits, and we have a pad of
#   random bits K, then the ciphertext C, which is the result of P XOR K, 
#   guarantees the strongest possible secuirty so long as K is truly random and
#   only used once. The existence and length of P can be learned by the 
#   attacker, though.
# This approach is impractical since it requires the pad K to be the same size
#   as the plaintext P, making the pad generation and exchange difficult and 
#   time-consuming.
# If K is reused, and the attacker is able to compromise c_i and c_j, then
#   the attacker can obtain p_i XOR p_j, which can give the attacker quite 
#   a bit of information.
# Suppose c_i=1 was compromised by the attacker. The attacker will obtain
#   no information from this, since the only two available cases share 
#   the same probability: 
#     Pr(p_i = 1 | k_i = 0) = 0.5, and
#     Pr(p_i = 0 | k_i = 1) = 0.5.
# Crib-dragging: Suppose the attacker has both C and a confirmed message P_j, 
#   then they can compromise K with C_j XOR P_j, which can then be used to 
#   compromise all other messages (P_i for all i) that are encrypted with K.
P = 0b1001001
K = 0b1010111
print(f'C = {P} XOR {K} = {P^K}') # should be 30
