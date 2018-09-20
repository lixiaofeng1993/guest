BS = 16

pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

print(pad('sadsda'))